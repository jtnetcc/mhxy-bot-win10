from pathlib import Path
import sys


def _bundle_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


ROOT = _bundle_root()
APP_DIR = ROOT / 'app'
UI_DIR = APP_DIR / 'ui'
CONFIG_DIR = ROOT / 'config'
ASSETS_DIR = ROOT / 'assets'
LOGS_DIR = ROOT / 'logs'
SCREENSHOTS_DIR = ROOT / 'screenshots'

for p in (CONFIG_DIR, ASSETS_DIR, LOGS_DIR, SCREENSHOTS_DIR):
    p.mkdir(parents=True, exist_ok=True)
