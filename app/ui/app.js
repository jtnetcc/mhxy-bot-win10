async function refresh() {
  const res = await fetch('/api/status');
  const data = await res.json();
  document.getElementById('boundWindow').textContent = data.boundWindow;
  document.getElementById('currentTask').textContent = data.currentTask;
  document.getElementById('running').textContent = data.running ? '是' : '否';
  document.getElementById('logs').textContent = data.logs.join('\n');
}

async function act(name) {
  await fetch('/api/action/' + name, { method: 'POST' });
  await refresh();
}

refresh();
setInterval(refresh, 2000);
