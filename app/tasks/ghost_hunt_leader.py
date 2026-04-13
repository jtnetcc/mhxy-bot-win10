from app.core.logger import log_line

class GhostHuntLeaderTask:
    def __init__(self, config=None, window_service=None, template_service=None, route_engine=None, ocr_service=None):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine
        self.ocr_service = ocr_service

    def run_preview(self):
        logs = []
        logs.append(log_line('[ghost] 开始自动抓鬼（队长）预演'))
        logs.append(log_line('[ghost] 模拟检查队伍状态: 5/5'))
        logs.append(log_line('[ghost] 模拟领取抓鬼任务'))
        logs.append(log_line('[ghost] OCR读取目标场景: 北俱芦洲'))
        logs.append(log_line('[ghost] 路线步骤: 当前场景 -> 驿站 -> 目标场景 -> 鬼点附近'))
        logs.append(log_line('[ghost] 模拟进入战斗并等待战斗结束'))
        logs.append(log_line('[ghost] 预演结束：当前仅为 mock 流程，未执行真实点击'))
        return logs
