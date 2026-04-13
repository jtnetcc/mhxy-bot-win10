#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import time
import threading
import webbrowser
import os

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / 'ui'
STATE = {
    'app': 'mhxy-bot-win10',
    'version': '0.1.0-prototype',
    'boundWindow': '未绑定',
    'currentTask': '空闲',
    'running': False,
    'logs': [
        '[init] prototype ready',
        '[hint] 当前版本仅用于演示界面与流程，不包含真实游戏控制',
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
            return self._json(STATE)
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/action/'):
            action = self.path.split('/api/action/', 1)[1]
            now = time.strftime('%H:%M:%S')
            if action == 'bind':
                STATE['boundWindow'] = '梦幻西游 - 示例窗口'
                STATE['logs'].append(f'[{now}] [bind] 已绑定示例窗口')
            elif action == 'start-dig':
                STATE['running'] = True
                STATE['currentTask'] = '自动打图'
                STATE['logs'].append(f'[{now}] [task] 启动 自动打图（演示）')
            elif action == 'start-master':
                STATE['running'] = True
                STATE['currentTask'] = '自动师门'
                STATE['logs'].append(f'[{now}] [task] 启动 自动师门（演示）')
            elif action == 'start-ghost':
                STATE['running'] = True
                STATE['currentTask'] = '自动抓鬼（队长）'
                STATE['logs'].append(f'[{now}] [task] 启动 自动抓鬼（队长）（演示）')
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
