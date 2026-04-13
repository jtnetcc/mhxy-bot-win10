function fillConfig(cfg) {
  document.getElementById('title_keyword').value = cfg.window.title_keyword;
  document.getElementById('dig_rounds').value = cfg.tasks.dig_treasure.max_rounds;
  document.getElementById('master_rounds').value = cfg.tasks.master_task.max_rounds;
  document.getElementById('ghost_rounds').value = cfg.tasks.ghost_hunt_leader.max_rounds;
  document.getElementById('stop_hotkey').value = cfg.safety.stop_hotkey;
  document.getElementById('pause_hotkey').value = cfg.safety.pause_hotkey;
  document.getElementById('timeout_seconds').value = cfg.safety.timeout_seconds;
  document.getElementById('route_profile').value = cfg.navigation.route_profile;
  document.getElementById('ocr_x').value = cfg.ocr.task_text_region[0];
  document.getElementById('ocr_y').value = cfg.ocr.task_text_region[1];
  document.getElementById('ocr_w').value = cfg.ocr.task_text_region[2];
  document.getElementById('ocr_h').value = cfg.ocr.task_text_region[3];
  document.getElementById('dig_enabled').checked = cfg.tasks.dig_treasure.enabled;
  document.getElementById('master_enabled').checked = cfg.tasks.master_task.enabled;
  document.getElementById('ghost_enabled').checked = cfg.tasks.ghost_hunt_leader.enabled;
}

function fillDebug(debug) {
  document.getElementById('vision_debug').textContent = [
    '窗口: ' + debug.window.title,
    '识别元素: ' + debug.vision.detections.join(' / '),
    '目标地图: ' + debug.vision.target_map,
  ].join('\n');
  document.getElementById('stat_completed').textContent = debug.stats.completed_rounds;
  document.getElementById('stat_scene').textContent = debug.stats.current_scene;
  document.getElementById('stat_error').textContent = debug.stats.recent_error;
  document.getElementById('stat_runtime').textContent = debug.stats.runtime;
  document.getElementById('ocr_debug').textContent = [
    'OCR 文本: ' + debug.vision.ocr_text,
    'OCR 区域: 使用配置中的 task_text_region',
  ].join('\n');
  document.getElementById('route_debug').textContent = [
    '巡线模板: ' + debug.route.profile,
    '路线步骤:',
    ...debug.route.steps.map((x, i) => `${i + 1}. ${x}`),
  ].join('\n');
}

async function refresh() {
  const res = await fetch('/api/status');
  const data = await res.json();
  document.getElementById('boundWindow').textContent = data.boundWindow;
  document.getElementById('currentTask').textContent = data.currentTask;
  document.getElementById('running').textContent = data.running ? '是' : '否';
  document.getElementById('logs').textContent = data.logs.join('\n');
  fillConfig(data.config);
  fillDebug(data.debug);
}

async function act(name) {
  await fetch('/api/action/' + name, { method: 'POST' });
  await refresh();
}

async function saveConfig() {
  const payload = {
    title_keyword: document.getElementById('title_keyword').value,
    dig_rounds: Number(document.getElementById('dig_rounds').value || 20),
    master_rounds: Number(document.getElementById('master_rounds').value || 20),
    ghost_rounds: Number(document.getElementById('ghost_rounds').value || 20),
    stop_hotkey: document.getElementById('stop_hotkey').value,
    pause_hotkey: document.getElementById('pause_hotkey').value,
    timeout_seconds: Number(document.getElementById('timeout_seconds').value || 120),
    route_profile: document.getElementById('route_profile').value,
    ocr_x: Number(document.getElementById('ocr_x').value || 0),
    ocr_y: Number(document.getElementById('ocr_y').value || 0),
    ocr_w: Number(document.getElementById('ocr_w').value || 300),
    ocr_h: Number(document.getElementById('ocr_h').value || 120),
    dig_enabled: document.getElementById('dig_enabled').checked,
    master_enabled: document.getElementById('master_enabled').checked,
    ghost_enabled: document.getElementById('ghost_enabled').checked,
  };
  await fetch('/api/config/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  await refresh();
}

refresh();
setInterval(refresh, 2000);
