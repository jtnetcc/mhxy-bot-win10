use dirs::data_local_dir;
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::fs;
use std::path::PathBuf;

#[derive(Serialize, Deserialize, Clone)]
struct AppState {
    app: String,
    version: String,
    boundWindow: String,
    currentTask: String,
    running: bool,
    logs: Vec<String>,
    config: serde_json::Value,
}

fn app_root() -> PathBuf {
    data_local_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join("mhxy-bot-win10")
}

fn config_path() -> PathBuf {
    app_root().join("config.json")
}

fn default_config() -> serde_json::Value {
    json!({
        "window": { "title_keyword": "梦幻西游" },
        "tasks": {
            "dig_treasure": { "enabled": true, "max_rounds": 20 },
            "master_task": { "enabled": true, "max_rounds": 20 },
            "ghost_hunt_leader": { "enabled": true, "max_rounds": 20 }
        },
        "navigation": { "route_profile": "default" },
        "ocr": { "task_text_region": [0, 0, 300, 120] },
        "safety": { "stop_hotkey": "F8", "pause_hotkey": "F9", "timeout_seconds": 120 }
    })
}

fn ensure_config() -> serde_json::Value {
    let root = app_root();
    let _ = fs::create_dir_all(&root);
    let path = config_path();
    if !path.exists() {
        let cfg = default_config();
        let _ = fs::write(&path, serde_json::to_vec_pretty(&cfg).unwrap());
        return cfg;
    }
    let content = fs::read_to_string(&path).unwrap_or_else(|_| "{}".to_string());
    serde_json::from_str(&content).unwrap_or_else(|_| default_config())
}

#[tauri::command]
fn get_status() -> serde_json::Value {
    let config = ensure_config();
    json!({
        "app": "mhxy-bot-win10",
        "version": "0.4.0-tauri-preview",
        "boundWindow": "未绑定",
        "currentTask": "空闲",
        "running": false,
        "logs": [
            "[init] tauri desktop preview ready",
            "[hint] 当前版本为 Tauri 桌面壳预演版"
        ],
        "config": config,
        "debug": {
            "window": { "title": "未绑定", "mode": "desktop-preview" },
            "vision": {
                "detections": ["背包按钮", "任务栏", "地图按钮", "挂机按钮"],
                "ocr_text": "去长安城郊外挖宝",
                "target_map": "长安城郊外"
            },
            "route": {
                "profile": "default",
                "steps": [
                    "打开地图",
                    "切换到长安城郊外",
                    "执行路线模板 default",
                    "到达挖图点附近"
                ]
            },
            "stats": {
                "completed_rounds": 0,
                "current_scene": "长安城郊外",
                "recent_error": "无",
                "runtime": "00:00:00"
            }
        }
    })
}

#[tauri::command]
fn run_action(action: String) -> serde_json::Value {
    let msg = match action.as_str() {
        "bind" => "[bind] 已绑定窗口: 梦幻西游 - 模拟窗口 (desktop-preview)",
        "start-dig" => "[task] 启动 自动打图（Tauri 预演）",
        "start-master" => "[task] 启动 自动师门（Tauri 预演）",
        "start-ghost" => "[task] 启动 自动抓鬼（队长）（Tauri 预演）",
        "pause" => "[control] 已暂停",
        "stop" => "[control] 已停止",
        _ => "[warn] 未知动作",
    };
    json!({ "ok": true, "message": msg })
}

#[tauri::command]
fn save_config(payload: serde_json::Value) -> serde_json::Value {
    let root = app_root();
    let _ = fs::create_dir_all(&root);
    let path = config_path();
    let _ = fs::write(&path, serde_json::to_vec_pretty(&payload).unwrap());
    json!({ "ok": true })
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_status, run_action, save_config])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
