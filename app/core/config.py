from pathlib import Path
from typing import Any
import yaml

from app.core.pathing import CONFIG_DIR

CONFIG_PATH = CONFIG_DIR / 'default.yaml'


def load_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def dump_yaml(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _ensure_default_config_exists():
    if CONFIG_PATH.exists():
        return
    default_data = {
        'app': {'name': 'mhxy-bot-win10', 'version': '0.3.0-dev', 'mode': 'prototype'},
        'window': {'title_keyword': '梦幻西游', 'single_instance': True, 'resolution': {'width': 1280, 'height': 720}},
        'tasks': {
            'dig_treasure': {'enabled': True, 'max_rounds': 20, 'route_profile': 'default'},
            'master_task': {'enabled': True, 'max_rounds': 20},
            'ghost_hunt_leader': {'enabled': True, 'max_rounds': 20},
        },
        'navigation': {'mode': 'route-template', 'route_profile': 'default'},
        'ocr': {
            'provider': 'mock',
            'language': 'zh-CN',
            'task_text_region': [0, 0, 300, 120],
            'mock_text': '去长安城郊外挖宝',
            'mock_target_map': '长安城郊外',
            'dig_scene_aliases': {
                '长安城郊外': ['长安郊外', '郊外'],
                '江南野外': ['江南', '江南野'],
            },
        },
        'templates': {'profile': 'dig-ui.example'},
        'safety': {'stop_hotkey': 'F8', 'pause_hotkey': 'F9', 'timeout_seconds': 120},
        'runtime': {'log_dir': 'logs', 'screenshot_dir': 'screenshots'},
    }
    dump_yaml(CONFIG_PATH, default_data)


def load_config():
    _ensure_default_config_exists()
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
