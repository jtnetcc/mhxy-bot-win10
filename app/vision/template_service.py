class TemplateService:
    def __init__(self, config: dict):
        self.config = config

    def detect_main_ui(self):
        return {
            'ok': True,
            'mode': 'mock',
            'detections': [
                {'name': '背包按钮', 'score': 0.98},
                {'name': '任务栏', 'score': 0.96},
                {'name': '挂机按钮', 'score': 0.93},
            ]
        }

    def detect_map_target(self):
        return {
            'ok': True,
            'mode': 'mock',
            'target_map': '长安城郊外',
            'confidence': 0.91,
        }
