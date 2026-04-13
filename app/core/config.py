from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[2] / 'config' / 'default.yaml'

def load_config():
    with CONFIG_PATH.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_config(data: dict):
    with CONFIG_PATH.open('w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
