from dataclasses import dataclass, field
from typing import List

@dataclass
class AppState:
    bound_window: str = '未绑定'
    current_task: str = '空闲'
    running: bool = False
    logs: List[str] = field(default_factory=list)

    def push(self, msg: str):
        self.logs.append(msg)
        self.logs = self.logs[-50:]
