from app.core.logger import log_line
from app.tasks.task_blueprints import get_task_blueprint


class MasterTask:
    def __init__(self, config=None, window_service=None, template_service=None, route_engine=None, ocr_service=None):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine
        self.ocr_service = ocr_service
        self.last_snapshot = {'task': 'master_task', 'current': 'idle', 'history': []}

    def run_preview(self):
        logs = []
        history = []
        logs.append(log_line('[master] 开始自动师门预演'))
        bind = self.window_service.bind_game_window()
        history.append({'state': 'bind_window', 'reason': '绑定师门任务窗口'})
        logs.append(log_line(f"[master] 绑定窗口: {bind['window_title']} ({bind['mode']})"))
        history.append({'state': 'detect_master_ui', 'reason': '识别师门相关 UI'})
        logs.append(log_line('[master] 识别师门入口 / 任务栏 / 包裹按钮'))
        history.append({'state': 'accept_task', 'reason': '模拟领取师门任务'})
        logs.append(log_line('[master] 模拟领取师门任务'))
        text = '去长寿村找NPC送信'
        history.append({'state': 'read_task_text', 'reason': 'OCR读取师门任务文本'})
        logs.append(log_line(f'[master] OCR读取任务文本: {text}'))
        history.append({'state': 'dispatch_task', 'reason': '按任务类型分流'})
        logs.append(log_line('[master] 任务分流: 送信类'))
        history.append({'state': 'plan_route', 'reason': '规划前往目标 NPC 路线'})
        logs.append(log_line('[master] 路线步骤: 师门 -> 场景切换 -> 长寿村NPC'))
        history.append({'state': 'submit_task', 'reason': '模拟交接任务'})
        logs.append(log_line('[master] 模拟交接任务并返回师门'))
        history.append({'state': 'return_loop', 'reason': '准备下一轮师门'})
        logs.append(log_line('[master] 预演结束：当前为任务骨架，未执行真实点击'))
        self.last_snapshot = {'task': 'master_task', 'current': 'return_loop', 'history': history}
        return logs

    def get_debug_snapshot(self):
        return self.last_snapshot

    def get_step_blueprint(self):
        return get_task_blueprint('master_task')['steps']
