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
