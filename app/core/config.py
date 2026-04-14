from pathlib import Path
from typing import Any
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / 'config'
CONFIG_PATH = CONFIG_DIR / 'default.yaml'


def load_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def dump_yaml(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def load_config():
    return load_yaml(CONFIG_PATH)


def save_config(data: dict):
    dump_yaml(CONFIG_PATH, data)


def get_route_config_path(task_name: str, profile: str) -> Path:
    return CONFIG_DIR / 'routes' / task_name / f'{profile}.yaml'


def load_route_profile(task_name: str, profile: str) -> dict:
    return load_yaml(get_route_config_path(task_name, profile))


def get_template_manifest_path(profile: str) -> Path:
    return CONFIG_DIR / 'templates' / f'{profile}.yaml'


def load_template_manifest(profile: str) -> dict:
    return load_yaml(get_template_manifest_path(profile))
