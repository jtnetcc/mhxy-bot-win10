from app.core.logger import log_line
from app.tasks.task_blueprints import get_task_blueprint


class GhostHuntLeaderTask:
    def __init__(self, config=None, window_service=None, template_service=None, route_engine=None, ocr_service=None):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine
        self.ocr_service = ocr_service
        self.last_snapshot = {'task': 'ghost_hunt_leader', 'current': 'idle', 'history': []}

    def run_preview(self):
        logs = []
        history = []
        logs.append(log_line('[ghost] 开始自动抓鬼（队长）预演'))
        bind = self.window_service.bind_game_window()
        history.append({'state': 'bind_window', 'reason': '绑定队长窗口'})
        logs.append(log_line(f"[ghost] 绑定窗口: {bind['window_title']} ({bind['mode']})"))
        history.append({'state': 'check_team', 'reason': '检查队伍状态'})
        logs.append(log_line('[ghost] 模拟检查队伍状态: 5/5'))
        history.append({'state': 'accept_task', 'reason': '领取抓鬼任务'})
        logs.append(log_line('[ghost] 模拟领取抓鬼任务'))
        history.append({'state': 'read_target', 'reason': 'OCR读取目标场景'})
        logs.append(log_line('[ghost] OCR读取目标场景: 北俱芦洲'))
        history.append({'state': 'plan_route', 'reason': '规划抓鬼路线'})
        logs.append(log_line('[ghost] 路线步骤: 当前场景 -> 驿站 -> 北俱芦洲 -> 鬼点附近'))
        history.append({'state': 'enter_battle', 'reason': '触发战斗'})
        logs.append(log_line('[ghost] 模拟进入战斗并等待战斗结束'))
        history.append({'state': 'wait_battle_end', 'reason': '等待战斗结束'})
        logs.append(log_line('[ghost] 检测战斗结束，准备回链'))
        history.append({'state': 'return_loop', 'reason': '继续下一轮抓鬼'})
        logs.append(log_line('[ghost] 预演结束：当前为任务骨架，未执行真实点击'))
        self.last_snapshot = {'task': 'ghost_hunt_leader', 'current': 'return_loop', 'history': history}
        return logs

    def get_debug_snapshot(self):
        return self.last_snapshot

    def get_step_blueprint(self):
        return get_task_blueprint('ghost_hunt_leader')['steps']
