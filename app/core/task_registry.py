from app.tasks.dig_treasure import DigTreasureTask
from app.tasks.master_task import MasterTask
from app.tasks.ghost_hunt_leader import GhostHuntLeaderTask
from app.vision.ocr_service import OCRService

class TaskRegistry:
    def __init__(self, config, window_service, template_service, route_engine):
        ocr_service = OCRService(config)
        self.tasks = {
            'dig_treasure': DigTreasureTask(config, window_service, template_service, route_engine),
            'master_task': MasterTask(config, window_service, template_service, route_engine, ocr_service),
            'ghost_hunt_leader': GhostHuntLeaderTask(config, window_service, template_service, route_engine, ocr_service),
        }

    def get(self, key: str):
        return self.tasks[key]
