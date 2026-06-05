const API_BASE = '';

async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(res.statusText);
        return await res.json();
    } catch (e) {
        console.error(`API error (${url}):`, e);
        return null;
    }
}

function parseCPU(cpuStr) {
    if (!cpuStr || cpuStr === '-') return 0;
    return parseFloat(cpuStr.replace('%', '')) || 0;
}

function parseMem(memStr) {
    if (!memStr || memStr === '-') return 0;
    return parseFloat(memStr.replace('%', '')) || 0;
}

async function refreshDashboard() {
    const data = await fetchJSON(`${API_BASE}/api/status`);
    if (!data) return;

    const server = data.server;
    const container = data.container;

    // Server indicator in nav
    const indicator = document.getElementById('server-indicator');
    if (indicator) {
        const dot = indicator.querySelector('span');
        const text = indicator.querySelector('span:last-child');
        if (server.online) {
            dot.className = 'w-2 h-2 rounded-full bg-green-500';
            text.textContent = 'Online';
        } else {
            dot.className = 'w-2 h-2 rounded-full bg-red-500';
            text.textContent = 'Offline';
        }
    }

    // Status badge
    const statusBadge = document.getElementById('status-badge');
    if (statusBadge) {
        if (server.online) {
            statusBadge.innerHTML = '<span class="text-green-400">● Online</span>';
        } else {
            statusBadge.innerHTML = '<span class="text-red-400">● Offline</span>';
        }
    }

    // Player count
    const playerCount = document.getElementById('player-count');
    if (playerCount) {
        playerCount.textContent = server.player_count + ' / 20';
    }

    // Player list
    const playerList = document.getElementById('player-list');
    if (playerList) {
        if (server.players && server.players.length > 0) {
            playerList.innerHTML = server.players.map(p =>
                `<span class="inline-block bg-gray-800 px-3 py-1 rounded-full text-xs mr-2 mb-2">${p}</span>`
            ).join('');
        } else {
            playerList.innerHTML = '<span class="text-gray-500 italic">No players online</span>';
        }
    }

    // Memory
    const memEl = document.getElementById('memory-usage');
    if (memEl && container) {
        memEl.textContent = container.mem_usage || '-';
    }

    // World size
    const wsEl = document.getElementById('world-size');
    if (wsEl) {
        wsEl.textContent = data.world_size || '-';
    }

    // CPU
    const cpuEl = document.getElementById('cpu-usage');
    const cpuBar = document.getElementById('cpu-bar');
    if (cpuEl && cpuBar && container) {
        const cpu = parseCPU(container.cpu);
        cpuEl.textContent = container.cpu || '0%';
        cpuBar.style.width = Math.min(cpu, 100) + '%';
    }

    // RAM
    const ramEl = document.getElementById('ram-usage');
    const ramBar = document.getElementById('ram-bar');
    if (ramEl && ramBar && container) {
        const ram = parseMem(container.mem_percent);
        ramEl.textContent = container.mem_percent || '0%';
        ramBar.style.width = Math.min(ram, 100) + '%';
    }

    // Net I/O
    const netEl = document.getElementById('net-io');
    if (netEl && container) {
        netEl.textContent = container.net_io || '-';
    }

    // PIDs
    const pidsEl = document.getElementById('pids');
    if (pidsEl && container) {
        pidsEl.textContent = container.pids || '-';
    }
}

async function refreshLogs() {
    const level = document.getElementById('level-filter')?.value || '';
    const search = document.getElementById('search-input')?.value || '';
    const container = document.getElementById('log-container') || document.getElementById('recent-logs');
    if (!container) return;

    const isRecent = container.id === 'recent-logs';
    const tail = isRecent ? 30 : 200;

    const data = await fetchJSON(`${API_BASE}/api/logs?tail=${tail}&level=${level}&search=${encodeURIComponent(search)}`);
    if (!data) return;

    if (data.lines.length === 0) {
        container.innerHTML = '<span class="text-gray-500 italic">No matching logs found</span>';
        return;
    }

    container.innerHTML = data.lines.map(line => {
        const escaped = line.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        if (escaped.includes('[WARN]') || escaped.includes('[ERROR]')) {
            const color = escaped.includes('[ERROR]') ? 'text-red-400' : 'text-yellow-400';
            return `<span class="${color}">${escaped}</span>`;
        }
        if (escaped.includes('[INFO]')) {
            return `<span class="text-gray-300">${escaped}</span>`;
        }
        return `<span class="text-gray-500">${escaped}</span>`;
    }).join('');

    container.scrollTop = container.scrollHeight;
}

async function refreshBackups() {
    const tbody = document.getElementById('backup-list');
    if (!tbody) return;

    const data = await fetchJSON(`${API_BASE}/api/backups`);
    if (!data || !data.backups || data.backups.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-gray-500 py-8 italic">No backups found</td></tr>';
        return;
    }

    tbody.innerHTML = data.backups.map(b =>
        `<tr class="text-sm">
            <td class="py-2">${b.name}</td>
            <td class="py-2 text-gray-400">${b.size}</td>
            <td class="py-2 text-gray-400">${new Date(b.date).toLocaleString()}</td>
            <td class="py-2">
                <button onclick="deleteBackup('${b.name}')" class="text-red-400 hover:text-red-300 text-xs">Delete</button>
            </td>
        </tr>`
    ).join('');
}

async function createBackup() {
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';

    const data = await fetchJSON(`${API_BASE}/api/backups`, { method: 'POST' });
    if (data && data.status === 'success') {
        showBackupStatus(`✅ Backup created: ${data.name} (${data.size})`, 'text-green-400');
        refreshBackups();
    } else {
        showBackupStatus('❌ Backup failed', 'text-red-400');
    }
    btn.disabled = false;
    btn.textContent = '+ Create Backup';
}

async function deleteBackup(name) {
    if (!confirm(`Delete backup "${name}"?`)) return;
    try {
        const res = await fetch(`${API_BASE}/api/backups/${name}`, { method: 'DELETE' });
        if (res.ok) {
            showBackupStatus(`🗑️ Deleted: ${name}`, 'text-yellow-400');
            refreshBackups();
        }
    } catch (e) {
        showBackupStatus('❌ Delete failed', 'text-red-400');
    }
}

function showBackupStatus(msg, cls) {
    const el = document.getElementById('backup-status');
    if (el) {
        el.className = `mb-3 text-sm ${cls}`;
        el.textContent = msg;
        el.classList.remove('hidden');
        setTimeout(() => el.classList.add('hidden'), 5000);
    }
}

// RCON
document.addEventListener('DOMContentLoaded', () => {
    const rconForm = document.getElementById('rcon-form');
    if (rconForm) {
        rconForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = document.getElementById('rcon-input');
            const cmd = input.value.trim();
            if (!cmd) return;

            const output = document.getElementById('rcon-output');
            output.innerHTML += `\n<span class="text-green-400">> ${cmd}</span>`;

            const res = await fetchJSON(`${API_BASE}/api/rcon`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd }),
            });

            if (res) {
                if (res.dangerous) {
                    output.innerHTML += `\n<span class="text-yellow-400">⚠️ Command executed: ${cmd}</span>`;
                }
                const resp = (res.response || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                output.innerHTML += `\n<span class="text-gray-300">${resp}</span>`;
            } else {
                output.innerHTML += `\n<span class="text-red-400">Error: Authentication may be required (401)</span>`;
            }

            output.scrollTop = output.scrollHeight;
            input.value = '';
        });
    }

    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(refreshLogs, 300);
        });
    }

    const levelFilter = document.getElementById('level-filter');
    if (levelFilter) {
        levelFilter.addEventListener('change', refreshLogs);
    }
});

function sendCommand(cmd) {
    const input = document.getElementById('rcon-input');
    if (input) {
        input.value = cmd;
        input.focus();
    }
}

// Polling intervals
if (document.getElementById('player-count')) {
    refreshDashboard();
    setInterval(refreshDashboard, 5000);
}

if (document.getElementById('log-container')) {
    refreshLogs();
    setInterval(refreshLogs, 10000);
}

if (document.getElementById('recent-logs')) {
    refreshLogs();
    setInterval(refreshLogs, 10000);
}

if (document.getElementById('backup-list')) {
    refreshBackups();
}
