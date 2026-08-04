/**
 * Unlimited AI Agent - Frontend Application
 * Complete frontend logic for https://ai.taagc.site
 */

const API_BASE = '/api';
const DOMAIN = 'ai.taagc.site';
let refreshTimer = null;
let settings = {};

// ============================================
// 1. INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log(`🤖 Unlimited AI Agent - ${DOMAIN}`);
    
    // Load settings
    loadSettings();
    
    // Load data
    loadAllData();
    
    // Setup navigation
    setupNavigation();
    
    // Setup tabs
    setupTabs();
    
    // Setup auto-refresh
    setupAutoRefresh();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
});

// ============================================
// 2. NAVIGATION
// ============================================

function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            
            // Update nav
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Update page
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(`page-${page}`).classList.add('active');
        });
    });
}

// ============================================
// 3. TABS
// ============================================

function setupTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            const parent = btn.closest('.card');
            
            // Update buttons
            parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update panels
            parent.querySelectorAll('.learn-panel').forEach(p => p.classList.remove('active'));
            parent.querySelector(`#learn-${tab}`).classList.add('active');
        });
    });
}

// ============================================
// 4. LOAD ALL DATA
// ============================================

function loadAllData() {
    loadStats();
    loadStatus();
    loadTasks();
    loadAllTasks();
    loadBots();
    loadKnowledge();
    loadLogs();
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const agent = data.agent || {};
            const memory = agent.memory || {};
            
            document.getElementById('statTasks').textContent = agent.tasks_completed || 0;
            document.getElementById('statDomains').textContent = agent.domains?.length || 14;
            document.getElementById('statMemory').textContent = memory.knowledge_graph?.total_concepts || 0;
            
            const successRate = memory.experience_db?.success_rate || 0;
            document.getElementById('statSuccess').textContent = (successRate * 100).toFixed(1) + '%';
            
            document.getElementById('statBots').textContent = agent.bots_created || 0;
            document.getElementById('statUptime').textContent = formatUptime(agent.uptime || 0);
            
            // Update status dot
            const dot = document.getElementById('statusDot');
            dot.className = 'status-dot online';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('statusDot').className = 'status-dot offline';
    }
}

// ============================================
// 5. STATUS
// ============================================

async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayStatus(data);
        } else {
            displayError('statusContainer', 'Failed to load status');
        }
    } catch (error) {
        displayError('statusContainer', 'Error: ' + error.message);
    }
}

function displayStatus(data) {
    const container = document.getElementById('statusContainer');
    const agent = data.agent || {};
    const memory = agent.memory || {};
    
    container.innerHTML = `
        <div class="status-grid">
            <div><strong>Domain:</strong> ${data.domain || DOMAIN}</div>
            <div><strong>State:</strong> ${agent.state || 'idle'}</div>
            <div><strong>Tasks:</strong> ${agent.tasks_completed || 0}</div>
            <div><strong>Domains:</strong> ${agent.domains?.length || 0}</div>
            <div><strong>Concepts:</strong> ${memory.knowledge_graph?.total_concepts || 0}</div>
            <div><strong>Experiences:</strong> ${memory.experience_db?.total || 0}</div>
            <div><strong>Success Rate:</strong> ${(memory.experience_db?.success_rate || 0) * 100}%</div>
            <div><strong>Uptime:</strong> ${formatUptime(agent.uptime || 0)}</div>
            <div><strong>Version:</strong> ${agent.version || '1.0.0'}</div>
            <div><strong>Bots:</strong> ${agent.bots_created || 0}</div>
        </div>
    `;
}

function formatUptime(seconds) {
    if (seconds < 60) return Math.floor(seconds) + 's';
    if (seconds < 3600) return Math.floor(seconds / 60) + 'm';
    if (seconds < 86400) return Math.floor(seconds / 3600) + 'h';
    return Math.floor(seconds / 86400) + 'd';
}

// ============================================
// 6. TASKS
// ============================================

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayTasks(data.tasks, data.count);
        } else {
            displayError('tasksContainer', 'Failed to load tasks');
        }
    } catch (error) {
        displayError('tasksContainer', 'Error: ' + error.message);
    }
}

function displayTasks(tasks, count) {
    const container = document.getElementById('tasksContainer');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `<div class="empty-state"><span class="icon">📋</span><p>No tasks yet</p></div>`;
        return;
    }
    
    let html = `<div class="task-count">📋 ${count || tasks.length} tasks</div>`;
    const recent = tasks.slice(-5).reverse();
    
    recent.forEach(task => {
        const statusClass = task.status || 'pending';
        html += `
            <div class="task-item">
                <div class="task-header">
                    <span class="task-priority">Priority: ${task.priority || 3}</span>
                    <span class="task-status ${statusClass}">${statusClass}</span>
                </div>
                <div class="task-description">${task.description || task.task || 'No description'}</div>
                <div class="task-meta">
                    <span>🕐 ${formatDate(task.created || task.timestamp)}</span>
                    ${task.completed ? `<span>✅ ${formatDate(task.completed)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function loadAllTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayAllTasks(data.tasks, data.count);
        }
    } catch (error) {
        console.error('Error loading all tasks:', error);
    }
}

function displayAllTasks(tasks, count) {
    const container = document.getElementById('allTasksContainer');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `<div class="empty-state"><span class="icon">📋</span><p>No tasks found</p></div>`;
        return;
    }
    
    let html = `<div class="task-count">📋 Total: ${count || tasks.length} tasks</div>`;
    
    tasks.slice().reverse().forEach(task => {
        const statusClass = task.status || 'pending';
        html += `
            <div class="task-item">
                <div class="task-header">
                    <span class="task-priority">ID: ${task.id || 'N/A'} | Priority: ${task.priority || 3}</span>
                    <span class="task-status ${statusClass}">${statusClass}</span>
                </div>
                <div class="task-description">${task.description || task.task || 'No description'}</div>
                <div class="task-meta">
                    <span>🕐 ${formatDate(task.created || task.timestamp)}</span>
                    ${task.completed ? `<span>✅ ${formatDate(task.completed)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// ============================================
// 7. PROCESS TASK
// ============================================

async function processTask() {
    const input = document.getElementById('taskInput');
    const priority = document.getElementById('taskPriority');
    const deadline = document.getElementById('taskDeadline');
    const task = input.value.trim();
    const resultDiv = document.getElementById('taskResult');
    const btn = document.querySelector('#page-tasks button');
    
    if (!task) {
        showResult(resultDiv, '❌ Please enter a task description', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Processing...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task: task,
                context: {
                    priority: parseInt(priority.value),
                    deadline: deadline.value || null
                }
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const result = data.result || {};
            showResult(resultDiv, `
✅ Task processed successfully!

📋 Task: ${task}
🎯 Result: ${result.success ? 'Success' : 'Failed'}

${JSON.stringify(result, null, 2)}
            `, 'success');
            
            loadAllData();
            input.value = '';
            deadline.value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '▶ Process Task';
}

async function processQuickTask() {
    const input = document.getElementById('quickTaskInput');
    const task = input.value.trim();
    const resultDiv = document.getElementById('quickTaskResult');
    const btn = document.querySelector('.quick-task button');
    
    if (!task) {
        showResult(resultDiv, '❌ Please enter a task', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/task`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showResult(resultDiv, `
✅ ${task}\n${JSON.stringify(data.result, null, 2)}
            `, 'success');
            loadAllData();
            input.value = '';
        } else {
            showResult(resultDiv, `❌ ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '▶ Execute';
}

// ============================================
// 8. CREATE BOT
// ============================================

async function createBot() {
    const requirements = document.getElementById('botRequirements').value.trim();
    const location = document.getElementById('botLocation').value;
    const name = document.getElementById('botName').value.trim();
    const resultDiv = document.getElementById('botResult');
    const btn = document.querySelector('#page-bots .bot-form button');
    
    if (!requirements) {
        showResult(resultDiv, '❌ Please enter bot requirements', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/create_bot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                requirements,
                location,
                name: name || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const bot = data.bot || {};
            showResult(resultDiv, `
✅ Bot created successfully!

🤖 Name: ${bot.name || 'Unnamed'}
📍 Location: ${bot.location || 'local'}
📝 Requirements: ${requirements}

${bot.code ? `📄 Code:\n${bot.code}` : ''}
            `, 'success');
            
            loadAllData();
            document.getElementById('botRequirements').value = '';
            document.getElementById('botName').value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '🤖 Create Bot';
}

// ============================================
// 9. LOAD BOTS
// ============================================

async function loadBots() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        const container = document.getElementById('botsContainer');
        const tasks = data.tasks || [];
        const botTasks = tasks.filter(t => 
            t.description && t.description.toLowerCase().includes('bot')
        );
        
        if (botTasks.length === 0) {
            container.innerHTML = `<div class="empty-state"><span class="icon">🤖</span><p>No bots created yet</p></div>`;
            return;
        }
        
        let html = '';
        botTasks.slice(-5).reverse().forEach(task => {
            html += `
                <div class="bot-item">
                    <div class="bot-name">🤖 ${task.description || 'Bot'}</div>
                    <div class="bot-location">Status: ${task.status || 'pending'} | Created: ${formatDate(task.created)}</div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading bots:', error);
    }
}

// ============================================
// 10. LEARN
// ============================================

async function learnText() {
    const text = document.getElementById('learnText').value.trim();
    const category = document.getElementById('learnCategory').value;
    const source = document.getElementById('learnSource').value.trim();
    const resultDiv = document.getElementById('learnResult');
    const btn = document.querySelector('#learn-text button');
    
    if (!text) {
        showResult(resultDiv, '❌ Please enter text to learn', 'error');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Learning...';
    resultDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                category,
                source: source || 'user_input'
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showResult(resultDiv, `
✅ Learning successful!

📚 Category: ${data.category}
📖 Source: ${data.source}
📝 Learned: ${data.text || text.substring(0, 200) + '...'}

The AI has learned this information and will use it in future tasks.
            `, 'success');
            
            loadAllData();
            document.getElementById('learnText').value = '';
            document.getElementById('learnSource').value = '';
        } else {
            showResult(resultDiv, `❌ Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
    
    btn.disabled = false;
    btn.textContent = '📚 Learn';
}

async function learnFromUrl() {
    const url = document.getElementById('learnUrl').value.trim();
    const resultDiv = document.getElementById('learnResult');
    
    if (!url) {
        showResult(resultDiv, '❌ Please enter a URL', 'error');
        return;
    }
    
    showResult(resultDiv, '⏳ Fetching and learning from URL...', 'success');
    
    try {
        // This is a placeholder - you'd need a backend endpoint to fetch URLs
        const response = await fetch(`${API_BASE}/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: `Content from URL: ${url}`,
                category: 'web',
                source: url
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showResult(resultDiv, `✅ Learned from: ${url}\n\n${JSON.stringify(data, null, 2)}`, 'success');
            loadAllData();
        } else {
            showResult(resultDiv, `❌ Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
}

async function learnFromFile() {
    const fileInput = document.getElementById('learnFile');
    const resultDiv = document.getElementById('learnResult');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        showResult(resultDiv, '❌ Please select a file', 'error');
        return;
    }
    
    const file = fileInput.files[0];
    
    try {
        const text = await file.text();
        
        const response = await fetch(`${API_BASE}/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text.substring(0, 5000), // Limit size
                category: 'file',
                source: file.name
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showResult(resultDiv, `✅ Learned from file: ${file.name}\n\n${JSON.stringify(data, null, 2)}`, 'success');
            loadAllData();
        } else {
            showResult(resultDiv, `❌ Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showResult(resultDiv, `❌ Error: ${error.message}`, 'error');
    }
}

// ============================================
// 11. KNOWLEDGE
// ============================================

async function loadKnowledge() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        const container = document.getElementById('knowledgeContainer');
        
        if (data.status === 'success') {
            const memory = data.agent?.memory || {};
            container.innerHTML = `
                <div class="status-grid">
                    <div><strong>Total Concepts:</strong> ${memory.knowledge_graph?.total_concepts || 0}</div>
                    <div><strong>Experiences:</strong> ${memory.experience_db?.total || 0}</div>
                    <div><strong>Success Rate:</strong> ${(memory.experience_db?.success_rate || 0) * 100}%</div>
                    <div><strong>Domains:</strong> ${data.agent?.domains?.length || 0}</div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading knowledge:', error);
    }
}

// ============================================
// 12. LOGS
// ============================================

async function loadLogs() {
    try {
        const container = document.getElementById('logsContainer');
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const tasks = data.tasks || [];
            let html = '';
            tasks.slice(-10).reverse().forEach(task => {
                const status = task.status || 'pending';
                const icon = status === 'completed' ? '✅' : status === 'failed' ? '❌' : '⏳';
                html += `
                    <div class="log-entry">
                        <span class="time">${formatDate(task.created || task.timestamp)}</span>
                        <span class="${status}">${icon} ${task.description || 'Task'}</span>
                    </div>
                `;
            });
            
            if (!html) {
                html = '<div class="empty-state">No logs available</div>';
            }
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// ============================================
// 13. SETTINGS
// ============================================

function loadSettings() {
    const saved = localStorage.getItem('aiAgentSettings');
    if (saved) {
        settings = JSON.parse(saved);
        document.getElementById('agentName').value = settings.agentName || 'UnlimitedAI';
        document.getElementById('refreshInterval').value = settings.refreshInterval || 30;
        document.getElementById('themeSelect').value = settings.theme || 'dark';
        applyTheme(settings.theme || 'dark');
    }
}

function saveSettings() {
    settings = {
        agentName: document.getElementById('agentName').value,
        refreshInterval: parseInt(document.getElementById('refreshInterval').value) || 30,
        theme: document.getElementById('themeSelect').value
    };
    
    localStorage.setItem('aiAgentSettings', JSON.stringify(settings));
    applyTheme(settings.theme);
    setupAutoRefresh();
    
    showResult(document.getElementById('learnResult'), '✅ Settings saved successfully!', 'success');
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
}

// ============================================
// 14. AUTO-REFRESH
// ============================================

function setupAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    
    const interval = (parseInt(document.getElementById('refreshInterval')?.value) || 30) * 1000;
    
    refreshTimer = setInterval(() => {
        if (!document.hidden) {
            loadAllData();
        }
    }, interval);
}

// ============================================
// 15. KEYBOARD SHORTCUTS
// ============================================

function setupKeyboardShortcuts() {
    // Ctrl+Enter for quick task
    document.getElementById('quickTaskInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            processQuickTask();
        }
    });
    
    document.getElementById('taskInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            processTask();
        }
    });
    
    document.getElementById('learnText').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            learnText();
        }
    });
    
    // Ctrl+Shift+R to clear cache
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'R') {
            e.preventDefault();
            clearCacheAndRefresh();
        }
    });
    
    // Ctrl+1-5 for navigation
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && !e.shiftKey) {
            const pages = ['dashboard', 'tasks', 'bots', 'learn', 'settings'];
            const idx = parseInt(e.key) - 1;
            if (idx >= 0 && idx < pages.length) {
                e.preventDefault();
                const link = document.querySelector(`.nav-link[data-page="${pages[idx]}"]`);
                if (link) link.click();
            }
        }
    });
}

// ============================================
// 16. CACHE MANAGEMENT
// ============================================

function clearCacheAndRefresh() {
    if (confirm('Clear all cache and refresh?')) {
        // Clear service workers
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(registrations => {
                registrations.forEach(r => r.unregister());
            });
        }
        
        // Clear caches
        if ('caches' in window) {
            caches.keys().then(keys => {
                keys.forEach(key => caches.delete(key));
            });
        }
        
        // Clear storage
        localStorage.clear();
        sessionStorage.clear();
        
        // Clear cookies
        document.cookie.split(";").forEach(c => {
            document.cookie = c.replace(/^ +/, "")
                .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        });
        
        // Refresh
        window.location.reload(true);
    }
}

function clearAllData() {
    if (confirm('⚠️ This will delete ALL data. Are you sure?')) {
        localStorage.clear();
        sessionStorage.clear();
        document.cookie.split(";").forEach(c => {
            document.cookie = c.replace(/^ +/, "")
                .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        });
        
        // Also try to clear from backend
        fetch(`${API_BASE}/clear`, { method: 'POST' }).catch(() => {});
        
        alert('✅ All data cleared!');
        window.location.reload();
    }
}

function exportData() {
    const data = {
        settings: settings,
        tasks: JSON.parse(localStorage.getItem('tasks') || '[]'),
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai_agent_data_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const data = JSON.parse(event.target.result);
                    if (data.settings) {
                        localStorage.setItem('aiAgentSettings', JSON.stringify(data.settings));
                        loadSettings();
                    }
                    alert('✅ Data imported successfully!');
                    window.location.reload();
                } catch (err) {
                    alert('❌ Invalid file format');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

// ============================================
// 17. UTILITY FUNCTIONS
// ============================================

function showResult(container, message, type = 'success') {
    container.className = type;
    container.textContent = message;
    container.style.display = 'block';
}

function displayError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="error-state"><p>❌ ${message}</p></div>`;
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    try {
        const date = new Date(dateStr);
        return date.toLocaleString();
    } catch {
        return dateStr;
    }
}

// ============================================
// 18. EXPOSE TO GLOBAL SCOPE
// ============================================

window.processTask = processTask;
window.processQuickTask = processQuickTask;
window.createBot = createBot;
window.learnText = learnText;
window.learnFromUrl = learnFromUrl;
window.learnFromFile = learnFromFile;
window.clearCacheAndRefresh = clearCacheAndRefresh;
window.clearAllData = clearAllData;
window.exportData = exportData;
window.importData = importData;
window.saveSettings = saveSettings;
window.loadAllData = loadAllData;

console.log('🚀 Unlimited AI Agent frontend loaded');
console.log('📌 Keyboard shortcuts:');
console.log('  Ctrl+1-5  - Navigate pages');
console.log('  Ctrl+Enter - Submit task');
console.log('  Ctrl+Shift+R - Clear cache and refresh');
