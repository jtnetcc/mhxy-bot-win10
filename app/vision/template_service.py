from app.core.config import load_template_manifest


class TemplateService:
    def __init__(self, config: dict):
        self.config = config
        self.profile = config.get('templates', {}).get('profile', 'dig-ui')
        self.catalog = load_template_manifest(self.profile)

    def list_templates(self):
        return self.catalog.get('templates', {})

    def detect_main_ui(self):
        templates = self.list_templates()
        preferred = ['bag_button', 'task_bar', 'map_button', 'hangup_button']
        detections = []
        for name in preferred:
            item = templates.get(name)
            if not item:
                continue
            detections.append({
                'name': item.get('label', name),
                'key': name,
                'score': item.get('threshold', 0.9),
                'path': item.get('path'),
            })
        return {
            'ok': True,
            'mode': 'mock',
            'profile': self.profile,
            'detections': detections,
        }

    def detect_map_target(self):
        mock_target = self.config.get('ocr', {}).get('mock_target_map', '长安城郊外')
        return {
            'ok': True,
            'mode': 'mock',
            'target_map': mock_target,
            'confidence': 0.91,
            'profile': self.profile,
        }
