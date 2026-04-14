from dataclasses import dataclass, field
from enum import Enum


class DigState(str, Enum):
    IDLE = 'idle'
    BIND_WINDOW = 'bind_window'
    DETECT_UI = 'detect_ui'
    READ_TARGET = 'read_target'
    PLAN_ROUTE = 'plan_route'
    MOVE_TO_TARGET = 'move_to_target'
    EXECUTE_DIG = 'execute_dig'
    HANDLE_BATTLE = 'handle_battle'
    HANDLE_REWARD = 'handle_reward'
    RETURN_LOOP = 'return_loop'
    ERROR = 'error'
    PAUSED = 'paused'
    STOPPED = 'stopped'


ALLOWED_TRANSITIONS = {
    DigState.IDLE: {DigState.BIND_WINDOW, DigState.STOPPED},
    DigState.BIND_WINDOW: {DigState.DETECT_UI, DigState.ERROR, DigState.STOPPED},
    DigState.DETECT_UI: {DigState.READ_TARGET, DigState.ERROR, DigState.STOPPED},
    DigState.READ_TARGET: {DigState.PLAN_ROUTE, DigState.ERROR, DigState.STOPPED},
    DigState.PLAN_ROUTE: {DigState.MOVE_TO_TARGET, DigState.ERROR, DigState.STOPPED},
    DigState.MOVE_TO_TARGET: {DigState.EXECUTE_DIG, DigState.ERROR, DigState.STOPPED},
    DigState.EXECUTE_DIG: {DigState.HANDLE_BATTLE, DigState.HANDLE_REWARD, DigState.ERROR, DigState.STOPPED},
    DigState.HANDLE_BATTLE: {DigState.HANDLE_REWARD, DigState.ERROR, DigState.STOPPED},
    DigState.HANDLE_REWARD: {DigState.RETURN_LOOP, DigState.ERROR, DigState.STOPPED},
    DigState.RETURN_LOOP: {DigState.BIND_WINDOW, DigState.STOPPED, DigState.PAUSED},
    DigState.PAUSED: {DigState.RETURN_LOOP, DigState.STOPPED},
    DigState.ERROR: {DigState.STOPPED},
    DigState.STOPPED: set(),
}


@dataclass
class DigStateMachine:
    state: DigState = DigState.IDLE
    history: list[dict] = field(default_factory=lambda: [{'state': DigState.IDLE.value, 'reason': 'init'}])

    def transition(self, next_state: DigState, reason: str):
        allowed = ALLOWED_TRANSITIONS.get(self.state, set())
        if next_state not in allowed:
            raise ValueError(f'invalid dig transition: {self.state.value} -> {next_state.value}')
        self.state = next_state
        event = {'state': next_state.value, 'reason': reason}
        self.history.append(event)
        return event

    def snapshot(self):
        return {
            'current': self.state.value,
            'history': list(self.history),
        }
