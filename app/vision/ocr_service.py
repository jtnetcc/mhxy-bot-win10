class OCRService:
    def __init__(self, config: dict):
        self.config = config
        self.ocr_config = config.get('ocr', {})
        self.scene_aliases = self.ocr_config.get('dig_scene_aliases', {})

    def read_task_text(self):
        mock_text = self.ocr_config.get('mock_text', '去长安城郊外挖宝')
        return {
            'ok': True,
            'mode': self.ocr_config.get('provider', 'mock'),
            'text': mock_text,
            'confidence': 0.89,
        }

    def extract_dig_target(self, text: str):
        normalized = (text or '').strip()
        for canonical, aliases in self.scene_aliases.items():
            candidates = [canonical, *(aliases or [])]
            if any(name and name in normalized for name in candidates):
                return {
                    'ok': True,
                    'target_map': canonical,
                    'source': 'ocr-text',
                    'matched_text': normalized,
                }
        return {
            'ok': False,
            'target_map': None,
            'source': 'ocr-text',
            'matched_text': normalized,
        }
