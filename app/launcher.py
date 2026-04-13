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

BASE_DIR = Path(__file__).resolve().parent
CONFIG = load_config()
WINDOW_SERVICE = WindowService(CONFIG)
TEMPLATE_SERVICE = TemplateService(CONFIG)
ROUTE_ENGINE = RouteEngine(CONFIG)
TASKS = TaskRegistry(CONFIG, WINDOW_SERVICE, TEMPLATE_SERVICE, ROUTE_ENGINE)

STATE = {
    'app': 'mhxy-bot-win10',
    'version': '0.2.0-dig-preview',
    'boundWindow': '未绑定',
    'currentTask': '空闲',
    'running': False,
    'logs': [
        '[init] dig preview ready',
        '[hint] 当前版本已接入自动打图任务底座（mock 接口层）',
    ],
}

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
            debug = {
                'window': {'title': STATE['boundWindow'], 'mode': 'mock'},
                'vision': {
                    'detections': ['背包按钮', '任务栏', '挂机按钮'],
                    'ocr_text': '去长安城郊外挖宝',
                    'target_map': '长安城郊外'
                },
                'route': {
                    'profile': CONFIG['navigation']['route_profile'],
                    'steps': ['打开地图', '切换到目标场景', '执行路线模板 default', '到达挖图点附近']
                },
                'stats': {
                    'completed_rounds': 3,
                    'current_scene': '长安城郊外',
                    'recent_error': '无',
                    'runtime': '00:12:36'
                }
            }
            return self._json({**STATE, 'config': CONFIG, 'debug': debug})
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/config/save':
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
            CONFIG['window']['title_keyword'] = data.get('title_keyword', CONFIG['window']['title_keyword'])
            CONFIG['tasks']['dig_treasure']['enabled'] = bool(data.get('dig_enabled', True))
            CONFIG['tasks']['dig_treasure']['max_rounds'] = int(data.get('dig_rounds', 20))
            CONFIG['tasks']['master_task']['enabled'] = bool(data.get('master_enabled', True))
            CONFIG['tasks']['master_task']['max_rounds'] = int(data.get('master_rounds', 20))
            CONFIG['tasks']['ghost_hunt_leader']['enabled'] = bool(data.get('ghost_enabled', True))
            CONFIG['tasks']['ghost_hunt_leader']['max_rounds'] = int(data.get('ghost_rounds', 20))
            CONFIG['safety']['stop_hotkey'] = data.get('stop_hotkey', CONFIG['safety']['stop_hotkey'])
            CONFIG['safety']['pause_hotkey'] = data.get('pause_hotkey', CONFIG['safety']['pause_hotkey'])
            CONFIG['safety']['timeout_seconds'] = int(data.get('timeout_seconds', CONFIG['safety']['timeout_seconds']))
            CONFIG['navigation']['route_profile'] = data.get('route_profile', CONFIG['navigation']['route_profile'])
            CONFIG['ocr']['task_text_region'] = [
                int(data.get('ocr_x', CONFIG['ocr']['task_text_region'][0])),
                int(data.get('ocr_y', CONFIG['ocr']['task_text_region'][1])),
                int(data.get('ocr_w', CONFIG['ocr']['task_text_region'][2])),
                int(data.get('ocr_h', CONFIG['ocr']['task_text_region'][3])),
            ]
            save_config(CONFIG)
            STATE['logs'].append(f"[{time.strftime('%H:%M:%S')}] [config] 已保存可视化参数")
            STATE['logs'] = STATE['logs'][-20:]
            return self._json({'ok': True, 'config': CONFIG})
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
                STATE['logs'].append(f'[{now}] [task] 启动 自动打图（预演）')
                for line in TASKS.get('dig_treasure').run_preview():
                    STATE['logs'].append(line)
            elif action == 'start-master':
                STATE['running'] = True
                STATE['currentTask'] = '自动师门'
                STATE['logs'].append(f'[{now}] [task] 启动 自动师门（预演）')
                for line in TASKS.get('master_task').run_preview():
                    STATE['logs'].append(line)
            elif action == 'start-ghost':
                STATE['running'] = True
                STATE['currentTask'] = '自动抓鬼（队长）'
                STATE['logs'].append(f'[{now}] [task] 启动 自动抓鬼（队长）（预演）')
                for line in TASKS.get('ghost_hunt_leader').run_preview():
                    STATE['logs'].append(line)
            elif action == 'pause':
                STATE['running'] = False
                STATE['logs'].append(f'[{now}] [control] 已暂停')
            elif action == 'stop':
                STATE['running'] = False
                STATE['currentTask'] = '空闲'
                STATE['logs'].append(f'[{now}] [control] 已停止')
            elif action == 'simulate-route':
                STATE['logs'].append(f'[{now}] [route] 执行路线模板：长安城 -> 酒店 -> 郊外 -> 任务点')
            elif action == 'simulate-battle':
                STATE['logs'].append(f'[{now}] [battle] 检测到战斗结束，准备回链')
            else:
                return self._json({'error': 'unknown action'}, 404)
            STATE['logs'] = STATE['logs'][-20:]
            return self._json({'ok': True, 'state': STATE})
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
