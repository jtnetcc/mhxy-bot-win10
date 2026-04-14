async function apiGetStatus() {
  if (window.__TAURI__?.core?.invoke) {
    return await window.__TAURI__.core.invoke('get_status');
  }
  const res = await fetch('/api/status');
  return await res.json();
}

async function apiRunAction(name) {
  if (window.__TAURI__?.core?.invoke) {
    return await window.__TAURI__.core.invoke('run_action', { action: name });
  }
  await fetch('/api/action/' + name, { method: 'POST' });
  return { ok: true };
}

async function apiSaveConfig(payload) {
  if (window.__TAURI__?.core?.invoke) {
    return await window.__TAURI__.core.invoke('save_config', { payload });
  }
  const res = await fetch('/api/config/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return await res.json();
}

function renderTasks(taskList = []) {
  const el = document.getElementById('task_list');
  if (!el) return;
  el.innerHTML = taskList.map(t => `
    <div class="task-item ${t.active ? 'active' : ''}" onclick="selectTask('${t.key}')">
      <input type="checkbox" ${t.enabled ? 'checked' : ''} onclick="event.stopPropagation()" />
      <div>
        <div>${t.label}</div>
        <div class="muted">步骤数: ${t.stepCount}</div>
      </div>
    </div>
  `).join('');
}

function renderSteps(steps = []) {
  const el = document.getElementById('step_table');
  if (!el) return;
  el.innerHTML = steps.map((s, i) => `
    <tr>
      <td>${i + 1}</td>
      <td>${s.type}</td>
      <td>${s.name}</td>
      <td>${s.desc}</td>
    </tr>
  `).join('');
}

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
    debug.taskState?.current ? '任务状态: ' + debug.taskState.current : '',
  ].filter(Boolean).join('\n');
  document.getElementById('stat_completed').textContent = debug.stats.completed_rounds;
  document.getElementById('stat_scene').textContent = debug.stats.current_scene;
  document.getElementById('stat_error').textContent = debug.stats.recent_error;
  document.getElementById('stat_runtime').textContent = debug.stats.runtime;
  document.getElementById('ocr_debug').textContent = [
    'OCR 文本: ' + debug.vision.ocr_text,
    'OCR 区域: task_text_region',
  ].join('\n');
  document.getElementById('route_debug').textContent = [
    '巡线模板: ' + debug.route.profile,
    '路线步骤:',
    ...debug.route.steps.map((x, i) => `${i + 1}. ${x}`),
  ].join('\n');
}

async function refresh() {
  const data = await apiGetStatus();
  document.getElementById('boundWindow').textContent = data.boundWindow;
  document.getElementById('currentTask').textContent = data.currentTask;
  document.getElementById('running').textContent = data.running ? '是' : '否';
  document.getElementById('logs').textContent = data.logs.join('\n');
  fillConfig(data.config);
  fillDebug(data.debug);
  renderTasks(data.taskList || []);
  renderSteps(data.steps || []);
}

async function act(name) {
  await apiRunAction(name);
  await refresh();
}

async function selectTask(key) {
  await apiRunAction(`select-task:${key}`);
  await refresh();
}

async function saveConfig() {
  const payload = {
    window: { title_keyword: document.getElementById('title_keyword').value },
    tasks: {
      dig_treasure: {
        enabled: document.getElementById('dig_enabled').checked,
        max_rounds: Number(document.getElementById('dig_rounds').value || 20),
      },
      master_task: {
        enabled: document.getElementById('master_enabled').checked,
        max_rounds: Number(document.getElementById('master_rounds').value || 20),
      },
      ghost_hunt_leader: {
        enabled: document.getElementById('ghost_enabled').checked,
        max_rounds: Number(document.getElementById('ghost_rounds').value || 20),
      }
    },
    navigation: { route_profile: document.getElementById('route_profile').value },
    ocr: {
      task_text_region: [
        Number(document.getElementById('ocr_x').value || 0),
        Number(document.getElementById('ocr_y').value || 0),
        Number(document.getElementById('ocr_w').value || 300),
        Number(document.getElementById('ocr_h').value || 120),
      ]
    },
    safety: {
      stop_hotkey: document.getElementById('stop_hotkey').value,
      pause_hotkey: document.getElementById('pause_hotkey').value,
      timeout_seconds: Number(document.getElementById('timeout_seconds').value || 120),
    }
  };
  await apiSaveConfig(payload);
  await refresh();
}

refresh();
setInterval(refresh, 2000);
