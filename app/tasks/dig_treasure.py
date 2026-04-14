from app.core.logger import log_line
from app.tasks.dig_state_machine import DigState, DigStateMachine
from app.vision.ocr_service import OCRService


class DigTreasureTask:
    def __init__(self, config, window_service, template_service, route_engine):
        self.config = config
        self.window_service = window_service
        self.template_service = template_service
        self.route_engine = route_engine
        self.ocr_service = OCRService(config)
        self.state_machine = DigStateMachine()

    def _step(self, next_state: DigState, reason: str, logs: list[str]):
        event = self.state_machine.transition(next_state, reason)
        logs.append(log_line(f"[dig-state] -> {event['state']} | {event['reason']}"))

    def run_preview(self):
        logs = []
        self.state_machine = DigStateMachine()
        logs.append(log_line('[dig] 开始自动打图预演'))

        self._step(DigState.BIND_WINDOW, '准备绑定游戏窗口', logs)
        bind = self.window_service.bind_game_window()
        logs.append(log_line(f"[dig] 绑定窗口: {bind['window_title']} ({bind['mode']})"))

        self._step(DigState.DETECT_UI, '检查主界面模板', logs)
        ui = self.template_service.detect_main_ui()
        logs.append(log_line(f"[dig] UI识别: {', '.join([d['name'] for d in ui['detections']])}"))

        self._step(DigState.READ_TARGET, 'OCR读取藏宝图目标', logs)
        ocr = self.ocr_service.read_task_text()
        logs.append(log_line(f"[dig] OCR文本: {ocr['text']} (置信度 {ocr['confidence']})"))
        extracted = self.ocr_service.extract_dig_target(ocr['text'])
        target = extracted['target_map'] if extracted['ok'] else self.template_service.detect_map_target()['target_map']
        logs.append(log_line(f"[dig] 目标地图识别: {target} ({'OCR解析' if extracted['ok'] else '模板回退'})"))

        self._step(DigState.PLAN_ROUTE, '根据目标地图生成路线', logs)
        route = self.route_engine.plan_dig_route(target)
        if not route['ok']:
            self._step(DigState.ERROR, '路线模板缺失', logs)
            logs.append(log_line(f"[dig] 路线规划失败，可用地图: {', '.join(route['available_maps'])}"))
            self._step(DigState.STOPPED, '异常结束', logs)
            return logs
        for step in route['steps']:
            logs.append(log_line(f'[dig] 路线步骤: {step}'))

        self._step(DigState.MOVE_TO_TARGET, '模拟移动到挖图点', logs)
        logs.append(log_line(f"[dig] waypoint 数量: {len(route['waypoints'])}，到达阈值: {route['strategy'].get('arrive_threshold', 'n/a')}"))

        self._step(DigState.EXECUTE_DIG, '模拟执行挖图动作', logs)
        logs.append(log_line('[dig] 模拟点击藏宝图 / 挖图动作'))

        self._step(DigState.HANDLE_REWARD, '模拟处理奖励结算', logs)
        logs.append(log_line('[dig] 模拟奖励识别与背包回收检查'))

        self._step(DigState.RETURN_LOOP, '准备下一轮打图循环', logs)
        logs.append(log_line('[dig] 当前轮次结束，等待进入下一轮'))

        self._step(DigState.STOPPED, '预演结束', logs)
        logs.append(log_line('[dig] 预演结束：当前仍为开发骨架，未执行真实点击'))
        return logs

    def get_debug_snapshot(self):
        return self.state_machine.snapshot()
