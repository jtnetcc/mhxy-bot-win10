from app.tasks.dig_treasure import DigTreasureTask
from app.tasks.master_task import MasterTask
from app.tasks.ghost_hunt_leader import GhostHuntLeaderTask

class TaskRegistry:
    def __init__(self, config, window_service, template_service, route_engine):
        self.tasks = {
            'dig_treasure': DigTreasureTask(config, window_service, template_service, route_engine),
            'master_task': MasterTask(),
            'ghost_hunt_leader': GhostHuntLeaderTask(),
        }

    def get(self, key: str):
        return self.tasks[key]
