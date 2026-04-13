from app.core.logger import log_line

class MasterTask:
    def __init__(self, config=None, window_service=None, template_service=None, route_engine=None, ocr_service=None):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine
        self.ocr_service = ocr_service

    def run_preview(self):
        logs = []
        logs.append(log_line('[master] 开始自动师门预演'))
        logs.append(log_line('[master] 模拟领取师门任务'))
        logs.append(log_line('[master] OCR读取任务文本: 去指定NPC处送信'))
        logs.append(log_line('[master] 任务分流: 送信类'))
        logs.append(log_line('[master] 路线步骤: 师门 -> 场景切换 -> 目标NPC'))
        logs.append(log_line('[master] 模拟交接任务并返回师门'))
        logs.append(log_line('[master] 预演结束：当前仅为 mock 流程，未执行真实点击'))
        return logs
