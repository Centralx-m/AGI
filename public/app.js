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
            const agent = data.agent;
            document.getElementById('statTasks').textContent = agent.brain_status?.tasks_executed || 0;
            document.getElementById('statDomains').textContent = agent.brain_status?.domains?.length || 14;
            document.getElementById('statMemory').textContent = agent.memory_status?.knowledge_graph?.total_concepts || 0;
            
            const successRate = agent.memory_status?.experience_db?.success_rate || 0;
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
            displayStatus(data.agent);
        } else {
            displayError('statusContainer', 'Failed to load status: ' + data.message);
        }
    } catch (error) {
        displayError('statusContainer', 'Error: ' + error.message);
    }
}

function displayStatus(status) {
    const container = document.getElementById('statusContainer');
    container.innerHTML = `
        <div class="status-grid">
            <div><strong>Domain:</strong> ${DOMAIN}</div>
            <div><strong>State:</strong> ${status.agent_status?.state || 'idle'}</div>
            <div><strong>Tasks:</strong> ${status.brain_status?.tasks_executed || 0}</div>
            <div><strong>Domains:</strong> ${status.brain_status?.domains?.length || 0}</div>
            <div><strong>Concepts:</strong> ${status.memory_status?.knowledge_graph?.total_concepts || 0}</div>
            <div><strong>Experiences:</strong> ${status.memory_status?.experience_db?.total || 0}</div>
            <div><strong>Success Rate:</strong> ${(status.memory_status?.experience_db?.success_rate * 100 || 0).toFixed(1)}%</div>
            <div><strong>Uptime:</strong> ${formatUptime(status.agent_status?.uptime || 0)}</div>
            <div><strong>Self-Repair:</strong> ${status.system_status?.self_repair || 'active'}</div>
            <div><strong>Self-Upgrade:</strong> ${status.system_status?.self_upgrade || 'active'}</div>
            <div><strong>Self-Replicate:</strong> ${status.system_status?.self_replicate || 'active'}</div>
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
                    <span class="task-priority">Priority: ${task.priority}</span>
                    <span class="task-status ${statusClass}">${task.status}</span>
                </div>
                <div class="task-description">${task.description}</div>
                <div class="task-meta">
                    <span>Created: ${new Date(task.created).toLocaleString()}</span>
                    ${task.completed ? `<span>Completed: ${new Date(task.completed).toLocaleString()}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
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
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Processing...';
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
            resultDiv.innerHTML = `
✅ Task processed successfully!

📋 Task: ${task}
🎯 Result: ${data.result.success ? 'Success' : 'Failed'}

${JSON.stringify(data.result, null, 2)}
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
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';
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
            resultDiv.innerHTML = `
✅ Bot created successfully!

🤖 Name: ${name || 'Unnamed'}
📍 Location: ${location}
${JSON.stringify(data.bot, null, 2)}
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
        return;
    }
    
    btn.disabled = true;
    btn.textContent = '⏳ Learning...';
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
📝 Learned: ${data.text}

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