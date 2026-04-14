from pathlib import Path
from datetime import datetime

from app.core.pathing import LOGS_DIR

LOG_DIR = LOGS_DIR
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'runtime.log'


def log_line(text: str):
    line = f"[{datetime.now().strftime('%F %T')}] {text}"
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(line + '\n')
    return line
