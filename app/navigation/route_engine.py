class RouteEngine:
    def __init__(self, config: dict):
        self.config = config

    def plan_dig_route(self, target_map: str):
        return {
            'ok': True,
            'mode': 'mock',
            'target_map': target_map,
            'steps': [
                '打开地图',
                '切换到目标场景',
                '执行路线模板 default',
                '到达挖图点附近',
            ]
        }
