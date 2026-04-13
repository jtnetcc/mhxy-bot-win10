function fillConfig(cfg) {
  document.getElementById('title_keyword').value = cfg.window.title_keyword;
  document.getElementById('dig_rounds').value = cfg.tasks.dig_treasure.max_rounds;
  document.getElementById('master_rounds').value = cfg.tasks.master_task.max_rounds;
  document.getElementById('ghost_rounds').value = cfg.tasks.ghost_hunt_leader.max_rounds;
  document.getElementById('stop_hotkey').value = cfg.safety.stop_hotkey;
  document.getElementById('pause_hotkey').value = cfg.safety.pause_hotkey;
  document.getElementById('timeout_seconds').value = cfg.safety.timeout_seconds;
  document.getElementById('dig_enabled').checked = cfg.tasks.dig_treasure.enabled;
  document.getElementById('master_enabled').checked = cfg.tasks.master_task.enabled;
  document.getElementById('ghost_enabled').checked = cfg.tasks.ghost_hunt_leader.enabled;
}

async function refresh() {
  const res = await fetch('/api/status');
  const data = await res.json();
  document.getElementById('boundWindow').textContent = data.boundWindow;
  document.getElementById('currentTask').textContent = data.currentTask;
  document.getElementById('running').textContent = data.running ? '是' : '否';
  document.getElementById('logs').textContent = data.logs.join('\n');
  fillConfig(data.config);
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
