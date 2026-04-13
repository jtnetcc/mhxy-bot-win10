class OCRService:
    def __init__(self, config: dict):
        self.config = config

    def read_task_text(self):
        return {
            'ok': True,
            'mode': 'mock',
            'text': '去长安城郊外挖宝',
            'confidence': 0.89,
        }
