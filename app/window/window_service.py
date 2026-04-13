class WindowService:
    def __init__(self, config: dict):
        self.config = config

    def bind_game_window(self):
        keyword = self.config.get('window', {}).get('title_keyword', '梦幻西游')
        return {
            'ok': True,
            'window_title': f'{keyword} - 模拟窗口',
            'mode': 'mock',
            'note': '当前环境未接入 Win32 真实窗口绑定，先走 mock。'
        }
