/**
 * Unlimited AI Agent - Frontend Application
 * Deployed on: https://ai.taagc.site
 */

const API_BASE = '/api';
const DOMAIN = 'ai.taagc.site';

// ============================================
// 1. Initialize on Page Load
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log(`🤖 Unlimited AI Agent - ${DOMAIN}`);
    loadStatus();
    loadTasks();
    loadStats();
    setupEventListeners();
});

// ============================================
// 2. Load Stats
// ============================================

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const agent = data.agent || {};
            
            // Fix: Use correct field names from your backend
            document.getElementById('statTasks').textContent = agent.tasks_completed || 0;
            document.getElementById('statDomains').textContent = agent.domains?.length || 14;
            
            // Fix: Memory data is nested correctly
            const memory = agent.memory || {};
            document.getElementById('statMemory').textContent = memory.knowledge_graph?.total_concepts || 0;
            
            const successRate = memory.experience_db?.success_rate || 0;
            document.getElementById('statSuccess').textContent = (successRate * 100).toFixed(1) + '%';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// ============================================
// 3. Load Status
// ============================================

async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayStatus(data);
        } else {
            displayError('statusContainer', 'Failed to load status: ' + data.message);
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
// 4. Load Tasks
// ============================================

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayTasks(data.tasks, data.count);
        } else {
            displayError('tasksContainer', 'Failed to load tasks: ' + data.message);
        }
    } catch (error) {
        displayError('tasksContainer', 'Error: ' + error.message);
    }
}

function displayTasks(tasks, count) {
    const container = document.getElementById('tasksContainer');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No tasks found. Add one below!</p>
            </div>
        `;
        return;
    }
    
    let html = `<div class="task-count">📋 ${count} tasks</div>`;
    
    // Show last 5 tasks
    const recent = tasks.slice(-5);
    recent.forEach(task => {
        const statusClass = task.status === 'completed' ? 'completed' : 'pending';
        html += `
            <div class="task-item">
                <div class="task-header">
                    <span class="task-priority">Priority: ${task.priority || 3}</span>
                    <span class="task-status ${statusClass}">${task.status}</span>
                </div>
                <div class="task-description">${task.description || task.task || 'No description'}</div>
                <div class="task-meta">
                    <span>Created: ${formatDate(task.created || task.timestamp)}</span>
                    ${task.completed ? `<span>Completed: ${formatDate(task.completed)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
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
// 5. Setup Event Listeners
// ============================================

function setupEventListeners() {
    document.getElementById('processBtn').addEventListener('click', processTask);
    document.getElementById('createBotBtn').addEventListener('click', createBot);
    document.getElementById('learnBtn').addEventListener('click', learnText);
    
    // Ctrl+Enter support
    document.getElementById('taskInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) processTask();
    });
}

// ============================================
// 6. Process Task
// ============================================

async function processTask() {
    const input = document.getElementById('taskInput');
    const priority = document.getElementById('taskPriority');
    const deadline = document.getElementById('taskDeadline');
    const task = input.value.trim();
    const resultDiv = document.getElementById('taskResult');
    const btn = document.getElementById('processBtn');
    
    if (!task) {
        resultDiv.innerHTML = '❌ Please enter a task description';
        resultDiv.style.display = 'block';
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Processing...';
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '⏳ Processing task...';
    
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
            resultDiv.innerHTML = `
✅ Task processed successfully!

📋 Task: ${task}
🎯 Result: ${result.success ? 'Success' : 'Failed'}

${JSON.stringify(result, null, 2)}
            `;
            
            loadStatus();
            loadTasks();
            loadStats();
        } else {
            resultDiv.innerHTML = `❌ Error: ${data.message}`;
        }
    } catch (error) {
        resultDiv.innerHTML = `❌ Error: ${error.message}`;
    }
    
    btn.disabled = false;
    btn.textContent = '▶ Process Task';
}

// ============================================
// 7. Create Bot
// ============================================

async function createBot() {
    const requirements = document.getElementById('botRequirements').value.trim();
    const location = document.getElementById('botLocation').value;
    const name = document.getElementById('botName').value.trim();
    const resultDiv = document.getElementById('botResult');
    const btn = document.getElementById('createBotBtn');
    
    if (!requirements) {
        resultDiv.innerHTML = '❌ Please enter bot requirements';
        resultDiv.style.display = 'block';
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '⏳ Creating bot...';
    
    try {
        const response = await fetch(`${API_BASE}/create_bot`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                requirements: requirements,
                location: location,
                name: name || undefined
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const bot = data.bot || {};
            resultDiv.innerHTML = `
✅ Bot created successfully!

🤖 Name: ${bot.name || 'Unnamed'}
📍 Location: ${bot.location || 'local'}
📝 Requirements: ${requirements}

${bot.code ? `📄 Code:\n${bot.code}` : ''}
            `;
            
            loadStatus();
        } else {
            resultDiv.innerHTML = `❌ Error: ${data.message}`;
        }
    } catch (error) {
        resultDiv.innerHTML = `❌ Error: ${error.message}`;
    }
    
    btn.disabled = false;
    btn.textContent = '🤖 Create Bot';
}

// ============================================
// 8. Learn Text
// ============================================

async function learnText() {
    const text = document.getElementById('learnText').value.trim();
    const category = document.getElementById('learnCategory').value;
    const source = document.getElementById('learnSource').value.trim();
    const resultDiv = document.getElementById('learnResult');
    const btn = document.getElementById('learnBtn');
    
    if (!text) {
        resultDiv.innerHTML = '❌ Please enter text to learn';
        resultDiv.style.display = 'block';
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Learning...';
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '⏳ Processing text...';
    
    try {
        const response = await fetch(`${API_BASE}/learn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                category: category,
                source: source || 'user_input'
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultDiv.innerHTML = `
✅ Learning successful!

📚 Category: ${data.category}
📖 Source: ${data.source}
📝 Learned: ${data.text || text.substring(0, 200) + '...'}

The AI has learned this information and will use it in future tasks.
            `;
            
            loadStatus();
            loadStats();
        } else {
            resultDiv.innerHTML = `❌ Error: ${data.message}`;
        }
    } catch (error) {
        resultDiv.innerHTML = `❌ Error: ${error.message}`;
    }
    
    btn.disabled = false;
    btn.textContent = '📚 Learn';
}

// ============================================
// 9. Utility Functions
// ============================================

function displayError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="error-state">
            <p>${message}</p>
        </div>
    `;
}
