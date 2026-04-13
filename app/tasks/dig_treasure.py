from app.core.logger import log_line

class DigTreasureTask:
    def __init__(self, config, window_service, template_service, route_engine):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine

    def run_preview(self):
        logs = []
        logs.append(log_line('[dig] 开始自动打图预演'))
        bind = self.window_service.bind_game_window()
        logs.append(log_line(f"[dig] 绑定窗口: {bind['window_title']} ({bind['mode']})"))
        ui = self.template_service.detect_main_ui()
        logs.append(log_line(f"[dig] UI识别: {', '.join([d['name'] for d in ui['detections']])}"))
        target = self.template_service.detect_map_target()
        logs.append(log_line(f"[dig] 目标地图识别: {target['target_map']} (置信度 {target['confidence']})"))
        route = self.route_engine.plan_dig_route(target['target_map'])
        for step in route['steps']:
            logs.append(log_line(f'[dig] 路线步骤: {step}'))
        logs.append(log_line('[dig] 预演结束：当前仅为 mock 流程，未执行真实点击'))
        return logs
