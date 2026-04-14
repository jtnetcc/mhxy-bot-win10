from app.core.config import load_route_profile


class RouteEngine:
    def __init__(self, config: dict):
        self.config = config
        navigation = config.get('navigation', {})
        self.route_profile = navigation.get('route_profile', 'default')
        self.route_data = load_route_profile('dig', self.route_profile)
        self.maps = self._normalize_maps(self.route_data.get('maps', {}))
        self.strategy = self.route_data.get('strategy', {})

    @staticmethod
    def _normalize_maps(raw_maps):
        if isinstance(raw_maps, dict):
            return raw_maps
        normalized = {}
        for item in raw_maps or []:
            name = item.get('name')
            if name:
                normalized[name] = {k: v for k, v in item.items() if k != 'name'}
        return normalized

    def get_available_maps(self):
        return list(self.maps.keys())

    def resolve_map_name(self, target_map: str):
        if target_map in self.maps:
            return target_map
        for name, meta in self.maps.items():
            aliases = meta.get('aliases', [])
            if target_map in aliases:
                return name
        return None

    def plan_dig_route(self, target_map: str):
        resolved = self.resolve_map_name(target_map)
        if not resolved:
            return {
                'ok': False,
                'mode': 'route-template',
                'target_map': target_map,
                'available_maps': self.get_available_maps(),
                'steps': ['未找到目标地图对应路线模板'],
            }

        meta = self.maps[resolved]
        scene_steps = meta.get('travel_steps') or [f'切换到目标场景：{resolved}']
        waypoints = meta.get('waypoints', [])
        steps = [
            '打开地图',
            *scene_steps,
            f'执行路线模板 {self.route_profile}',
            f'按 {len(waypoints)} 个 waypoint 接近目标点',
            '到达挖图点附近',
        ]
        return {
            'ok': True,
            'mode': 'route-template',
            'profile': self.route_profile,
            'target_map': resolved,
            'waypoints': waypoints,
            'strategy': self.strategy,
            'steps': steps,
        }
