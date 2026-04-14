#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import time
import threading
import webbrowser
import os
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.core.config import load_config, save_config
from app.window.window_service import WindowService
from app.vision.template_service import TemplateService
from app.navigation.route_engine import RouteEngine
from app.core.task_registry import TaskRegistry
from app.core.pathing import UI_DIR
from app.tasks.task_blueprints import TASK_BLUEPRINTS

CONFIG = load_config()
WINDOW_SERVICE = WindowService(CONFIG)
TEMPLATE_SERVICE = TemplateService(CONFIG)
ROUTE_ENGINE = RouteEngine(CONFIG)
TASKS = TaskRegistry(CONFIG, WINDOW_SERVICE, TEMPLATE_SERVICE, ROUTE_ENGINE)

TASK_ORDER = ['dig_treasure', 'master_task', 'ghost_hunt_leader']

STATE = {
    'app': 'mhxy-bot-win10',
    'version': '0.4.1-studio-preview',
    'boundWindow': '未绑定',
    'currentTask': '空闲',
    'currentTaskKey': 'dig_treasure',
    'running': False,
    'logs': [
        '[init] studio preview ready',
        '[hint] 当前版本已接入自动打图 / 自动师门 / 自动抓鬼 三条任务骨架',
    ],
    'taskSnapshots': {},
}


def get_task_list_payload():
    items = []
    for key in TASK_ORDER:
        task_cfg = CONFIG['tasks'][key]
        bp = TASK_BLUEPRINTS[key]
        items.append({
            'key': key,
            'label': bp['label'],
            'enabled': task_cfg.get('enabled', True),
            'active': key == STATE['currentTaskKey'],
            'stepCount': len(bp['steps']),
        })
    return items


def get_current_steps():
    key = STATE['currentTaskKey']
    task = TASKS.get(key)
    return task.get_step_blueprint()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def _json(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == '/api/status':
            current_snapshot = STATE['taskSnapshots'].get(STATE['currentTaskKey'], {})
            debug = {
                'window': {'title': STATE['boundWindow'], 'mode': 'mock'},
                'vision': {
                    'profile': TEMPLATE_SERVICE.profile,
                    'detections': [d['name'] for d in TEMPLATE_SERVICE.detect_main_ui()['detections']],
                    'ocr_text': CONFIG['ocr']['mock_text'],
                    'target_map': CONFIG['ocr']['mock_target_map']
                },
                'route': {
                    'profile': CONFIG['navigation']['route_profile'],
                    'maps': ROUTE_ENGINE.get_available_maps(),
                    'steps': ROUTE_ENGINE.plan_dig_route(CONFIG['ocr']['mock_target_map'])['steps']
                },
                'stats': {
                    'completed_rounds': 3,
                    'current_scene': '长安城郊外',
                    'recent_error': '无',
                    'runtime': '00:12:36'
                },
                'taskState': current_snapshot,
            }
            return self._json({
                **STATE,
                'config': CONFIG,
                'debug': debug,
                'taskList': get_task_list_payload(),
                'steps': get_current_steps(),
            })
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/config/save':
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))

            if 'window' in data:
                CONFIG['window']['title_keyword'] = data['window'].get('title_keyword', CONFIG['window']['title_keyword'])
            else:
                CONFIG['window']['title_keyword'] = data.get('title_keyword', CONFIG['window']['title_keyword'])

            if 'tasks' in data:
                for key in ['dig_treasure', 'master_task', 'ghost_hunt_leader']:
                    if key in data['tasks']:
                        CONFIG['tasks'][key]['enabled'] = bool(data['tasks'][key].get('enabled', CONFIG['tasks'][key]['enabled']))
                        CONFIG['tasks'][key]['max_rounds'] = int(data['tasks'][key].get('max_rounds', CONFIG['tasks'][key]['max_rounds']))
            else:
                CONFIG['tasks']['dig_treasure']['enabled'] = bool(data.get('dig_enabled', True))
                CONFIG['tasks']['dig_treasure']['max_rounds'] = int(data.get('dig_rounds', 20))
                CONFIG['tasks']['master_task']['enabled'] = bool(data.get('master_enabled', True))
                CONFIG['tasks']['master_task']['max_rounds'] = int(data.get('master_rounds', 20))
                CONFIG['tasks']['ghost_hunt_leader']['enabled'] = bool(data.get('ghost_enabled', True))
                CONFIG['tasks']['ghost_hunt_leader']['max_rounds'] = int(data.get('ghost_rounds', 20))

            if 'safety' in data:
                CONFIG['safety']['stop_hotkey'] = data['safety'].get('stop_hotkey', CONFIG['safety']['stop_hotkey'])
                CONFIG['safety']['pause_hotkey'] = data['safety'].get('pause_hotkey', CONFIG['safety']['pause_hotkey'])
                CONFIG['safety']['timeout_seconds'] = int(data['safety'].get('timeout_seconds', CONFIG['safety']['timeout_seconds']))
            else:
                CONFIG['safety']['stop_hotkey'] = data.get('stop_hotkey', CONFIG['safety']['stop_hotkey'])
                CONFIG['safety']['pause_hotkey'] = data.get('pause_hotkey', CONFIG['safety']['pause_hotkey'])
                CONFIG['safety']['timeout_seconds'] = int(data.get('timeout_seconds', CONFIG['safety']['timeout_seconds']))

            if 'navigation' in data:
                CONFIG['navigation']['route_profile'] = data['navigation'].get('route_profile', CONFIG['navigation']['route_profile'])
            else:
                CONFIG['navigation']['route_profile'] = data.get('route_profile', CONFIG['navigation']['route_profile'])

            if 'ocr' in data and 'task_text_region' in data['ocr']:
                CONFIG['ocr']['task_text_region'] = [int(x) for x in data['ocr']['task_text_region']]
            else:
                CONFIG['ocr']['task_text_region'] = [
                    int(data.get('ocr_x', CONFIG['ocr']['task_text_region'][0])),
                    int(data.get('ocr_y', CONFIG['ocr']['task_text_region'][1])),
                    int(data.get('ocr_w', CONFIG['ocr']['task_text_region'][2])),
                    int(data.get('ocr_h', CONFIG['ocr']['task_text_region'][3])),
                ]

            save_config(CONFIG)
            STATE['logs'].append(f"[{time.strftime('%H:%M:%S')}] [config] 已保存参数")
            STATE['logs'] = STATE['logs'][-40:]
            return self._json({'ok': True, 'config': CONFIG, 'taskList': get_task_list_payload()})

        if self.path.startswith('/api/action/'):
            action = self.path.split('/api/action/', 1)[1]
            now = time.strftime('%H:%M:%S')
            if action == 'bind':
                result = WINDOW_SERVICE.bind_game_window()
                STATE['boundWindow'] = result['window_title']
                STATE['logs'].append(f"[{now}] [bind] 已绑定窗口: {result['window_title']} ({result['mode']})")
            elif action == 'start-dig':
                STATE['running'] = True
                STATE['currentTask'] = '自动打图'
                STATE['currentTaskKey'] = 'dig_treasure'
                STATE['logs'].append(f'[{now}] [task] 启动 自动打图（预演）')
                task = TASKS.get('dig_treasure')
                for line in task.run_preview():
                    STATE['logs'].append(line)
                STATE['taskSnapshots']['dig_treasure'] = task.get_debug_snapshot()
            elif action == 'start-master':
                STATE['running'] = True
                STATE['currentTask'] = '自动师门'
                STATE['currentTaskKey'] = 'master_task'
                STATE['logs'].append(f'[{now}] [task] 启动 自动师门（预演）')
                task = TASKS.get('master_task')
                for line in task.run_preview():
                    STATE['logs'].append(line)
                STATE['taskSnapshots']['master_task'] = task.get_debug_snapshot()
            elif action == 'start-ghost':
                STATE['running'] = True
                STATE['currentTask'] = '自动抓鬼（队长）'
                STATE['currentTaskKey'] = 'ghost_hunt_leader'
                STATE['logs'].append(f'[{now}] [task] 启动 自动抓鬼（队长）（预演）')
                task = TASKS.get('ghost_hunt_leader')
                for line in task.run_preview():
                    STATE['logs'].append(line)
                STATE['taskSnapshots']['ghost_hunt_leader'] = task.get_debug_snapshot()
            elif action.startswith('select-task:'):
                key = action.split(':', 1)[1]
                if key in TASK_ORDER:
                    STATE['currentTaskKey'] = key
                    STATE['currentTask'] = TASK_BLUEPRINTS[key]['label']
                    STATE['logs'].append(f'[{now}] [ui] 切换任务视图: {TASK_BLUEPRINTS[key]["label"]}')
            elif action == 'pause':
                STATE['running'] = False
                STATE['logs'].append(f'[{now}] [control] 已暂停')
            elif action == 'stop':
                STATE['running'] = False
                STATE['currentTask'] = '空闲'
                STATE['logs'].append(f'[{now}] [control] 已停止')
            else:
                return self._json({'error': 'unknown action'}, 404)
            STATE['logs'] = STATE['logs'][-40:]
            return self._json({'ok': True, 'state': STATE, 'taskList': get_task_list_payload(), 'steps': get_current_steps()})
        return self._json({'error': 'not found'}, 404)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8765
    url = f'http://{host}:{port}'
    print(f'mhxy-bot-win10 prototype: {url}')

    if os.environ.get('MHXY_BOT_NO_BROWSER') != '1':
        def _open():
            time.sleep(1.0)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=_open, daemon=True).start()

    ThreadingHTTPServer((host, port), Handler).serve_forever()
