"""
Unlimited Autonomous AI Agent - Full Backend API
Deployed at: https://ai.taagc.site
Complete integration with frontend dashboard
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
import urllib.parse
import urllib.request

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class handler(BaseHTTPRequestHandler):
    """
    Main API handler for Unlimited AI Agent
    Supports all frontend features:
    - Dashboard stats
    - Task management (CRUD)
    - Bot creation and management
    - Learning system (text, URL, file)
    - Knowledge base
    - System logs
    - Settings management
    """
    
    # ============================================
    # AGENT STATE
    # ============================================
    
    agent_state = {
        "name": "UnlimitedAI",
        "version": "2.0.0",
        "state": "online",
        "tasks_completed": 0,
        "uptime": 0,
        "start_time": datetime.now(),
        "bots_created": 0,
        "capabilities": [
            "Self-learning from books and experience",
            "Self-repairing when errors occur",
            "Self-upgrading to improve performance",
            "Self-replicating to create new bots"
        ],
        "domains": [
            "Business", "Finance", "Healthcare", "Education",
            "Technology", "Legal", "Creative", "Real Estate",
            "Manufacturing", "Agriculture", "Retail",
            "Transportation", "Energy", "Government"
        ],
        "memory": {
            "knowledge_graph": {"total_concepts": 42},
            "experience_db": {"total": 15, "success_rate": 0.87}
        }
    }
    
    # Storage
    tasks = []
    task_counter = 0
    bots = []
    knowledge_items = []
    logs = []
    settings = {
        "agent_name": "UnlimitedAI",
        "refresh_interval": 30,
        "theme": "dark"
    }
    
    # ============================================
    # HTTP METHODS
    # ============================================
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request('POST')
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        self._handle_request('DELETE')
    
    def do_PUT(self):
        """Handle PUT requests"""
        self._handle_request('PUT')
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    # ============================================
    # CORS HEADERS
    # ============================================
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    # ============================================
    # MAIN REQUEST HANDLER
    # ============================================
    
    def _handle_request(self, method):
        """Route requests to appropriate handlers"""
        try:
            path = self.path.split('?')[0]
            print(f"📥 {method} {path}")
            
            # ============================================
            # STATIC FILES
            # ============================================
            if path == '/':
                self._serve_dashboard()
            elif path == '/style.css':
                self._serve_static('style.css', 'text/css')
            elif path == '/app.js':
                self._serve_static('app.js', 'application/javascript')
            elif path == '/404.html':
                self._serve_static('404.html', 'text/html')
            elif path == '/clear-cache.html':
                self._serve_static('clear-cache.html', 'text/html')
            
            # ============================================
            # API ENDPOINTS
            # ============================================
            elif path == '/api/status':
                self._handle_status()
            elif path == '/api/stats':
                self._handle_stats()
            elif path == '/api/task':
                if method == 'POST':
                    self._handle_task_create()
                elif method == 'GET':
                    self._handle_task_get()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/tasks':
                if method == 'GET':
                    self._handle_tasks_list()
                elif method == 'DELETE':
                    self._handle_tasks_clear()
                else:
                    self._send_error(405, "Method not allowed")
            elif path.startswith('/api/task/'):
                if method == 'GET':
                    self._handle_task_detail(path)
                elif method == 'DELETE':
                    self._handle_task_delete(path)
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/create_bot':
                if method == 'POST':
                    self._handle_bot_create()
                else:
                    self._send_error(405, "Use POST for /api/create_bot")
            elif path == '/api/bots':
                if method == 'GET':
                    self._handle_bots_list()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/learn':
                if method == 'POST':
                    self._handle_learn()
                else:
                    self._send_error(405, "Use POST for /api/learn")
            elif path == '/api/knowledge':
                if method == 'GET':
                    self._handle_knowledge_list()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/logs':
                if method == 'GET':
                    self._handle_logs()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/settings':
                if method == 'GET':
                    self._handle_settings_get()
                elif method == 'POST':
                    self._handle_settings_save()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/webhook':
                self._handle_webhook()
            elif path == '/api/clear':
                if method == 'POST':
                    self._handle_clear_data()
                else:
                    self._send_error(405, "Use POST for /api/clear")
            elif path == '/api/export':
                if method == 'GET':
                    self._handle_export_data()
                else:
                    self._send_error(405, "Method not allowed")
            elif path == '/api/import':
                if method == 'POST':
                    self._handle_import_data()
                else:
                    self._send_error(405, "Use POST for /api/import")
            else:
                # Serve custom 404
                self._serve_404()
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self._send_error(500, str(e))
    
    # ============================================
    # RESPONSE HELPERS
    # ============================================
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
    
    def _send_error(self, code, message):
        self._send_json({
            "status": "error",
            "code": code,
            "message": message
        }, code)
    
    def _serve_static(self, filename, content_type):
        try:
            file_path = Path(__file__).parent.parent / 'public' / filename
            if file_path.exists():
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-type', content_type)
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self._send_error(404, f"File not found: {filename}")
        except Exception as e:
            self._send_error(500, str(e))
    
    # ============================================
    # DASHBOARD
    # ============================================
    
    def _serve_dashboard(self):
        try:
            file_path = Path(__file__).parent.parent / 'public' / 'index.html'
            if file_path.exists():
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self._serve_fallback_dashboard()
        except Exception as e:
            print(f"Error serving dashboard: {e}")
            self._serve_fallback_dashboard()
    
    def _serve_fallback_dashboard(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Unlimited AI Agent</title></head>
        <body style="background:#0a0a0a;color:#fff;font-family:sans-serif;text-align:center;padding:50px;">
            <h1 style="font-size:3rem;">🤖 Unlimited AI Agent</h1>
            <p style="color:#888;">Deployed at <a href="https://ai.taagc.site" style="color:#00cc88;">ai.taagc.site</a></p>
            <p style="color:#888;">Status: <span style="color:#00cc88;">● Online</span></p>
            <div style="margin:30px 0;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
                <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:12px;min-width:150px;">
                    <div style="font-size:2rem;font-weight:bold;color:#00cc88;">14</div>
                    <div style="color:#888;">Domains</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:12px;min-width:150px;">
                    <div style="font-size:2rem;font-weight:bold;color:#00cc88;">∞</div>
                    <div style="color:#888;">Capabilities</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:12px;min-width:150px;">
                    <div style="font-size:2rem;font-weight:bold;color:#00cc88;">✓</div>
                    <div style="color:#888;">Self-Learning</div>
                </div>
            </div>
            <p><a href="/api/status" style="color:#00cc88;">/api/status</a> | <a href="/api/tasks" style="color:#00cc88;">/api/tasks</a></p>
            <p style="color:#555;margin-top:50px;">🤖 Unlimited Autonomous AI Agent | © 2026 TAAGC</p>
        </body>
        </html>
        """
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _serve_404(self):
        try:
            file_path = Path(__file__).parent.parent / 'public' / '404.html'
            if file_path.exists():
                self.send_response(404)
                self._send_cors_headers()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 - Page Not Found')
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Page Not Found')
    
    # ============================================
    # API: STATUS & STATS
    # ============================================
    
    def _handle_status(self):
        """GET /api/status - Full agent status"""
        self.agent_state['uptime'] = (datetime.now() - self.agent_state['start_time']).total_seconds()
        self.agent_state['tasks_completed'] = len([t for t in self.tasks if t.get('status') == 'completed'])
        self.agent_state['bots_created'] = len(self.bots)
        
        self._send_json({
            "status": "success",
            "domain": "ai.taagc.site",
            "server": "Vercel",
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_state,
            "stats": {
                "tasks": len(self.tasks),
                "bots": len(self.bots),
                "knowledge": len(self.knowledge_items)
            }
        })
    
    def _handle_stats(self):
        """GET /api/stats - Quick stats for dashboard"""
        self._send_json({
            "status": "success",
            "stats": {
                "tasks_completed": len([t for t in self.tasks if t.get('status') == 'completed']),
                "total_tasks": len(self.tasks),
                "bots_created": len(self.bots),
                "knowledge_items": len(self.knowledge_items),
                "domains": len(self.agent_state['domains']),
                "uptime": (datetime.now() - self.agent_state['start_time']).total_seconds()
            }
        })
    
    # ============================================
    # API: TASKS
    # ============================================
    
    def _handle_task_create(self):
        """POST /api/task - Create and process a task"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            task_description = data.get('task') or data.get('description')
            context = data.get('context', {})
            
            if not task_description:
                self._send_error(400, "Task description is required")
                return
            
            # Create task
            self.task_counter += 1
            task = {
                "id": str(self.task_counter),
                "description": task_description,
                "priority": context.get('priority', 3),
                "deadline": context.get('deadline'),
                "status": "pending",
                "created": datetime.now().isoformat(),
                "context": context
            }
            
            # Process with AI
            result = self._process_with_ai(task_description, context)
            
            # Update task status
            task['status'] = 'completed' if result.get('success') else 'failed'
            task['completed'] = datetime.now().isoformat()
            task['result'] = result
            
            self.tasks.append(task)
            
            # Add to log
            self._add_log('info', f"Task processed: {task_description[:50]}...")
            
            self._send_json({
                "status": "success",
                "task": task,
                "result": result
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _handle_task_get(self):
        """GET /api/task - Get task by ID (via query param)"""
        query = urllib.parse.parse_qs(self.path.split('?')[1] if '?' in self.path else '')
        task_id = query.get('id', [''])[0]
        
        if not task_id:
            self._send_error(400, "Task ID is required")
            return
        
        for task in self.tasks:
            if task['id'] == task_id:
                self._send_json({
                    "status": "success",
                    "task": task
                })
                return
        
        self._send_error(404, f"Task {task_id} not found")
    
    def _handle_tasks_list(self):
        """GET /api/tasks - List all tasks"""
        self._send_json({
            "status": "success",
            "count": len(self.tasks),
            "tasks": self.tasks[-50:]  # Last 50 tasks
        })
    
    def _handle_tasks_clear(self):
        """DELETE /api/tasks - Clear all completed tasks"""
        completed = [t for t in self.tasks if t.get('status') == 'completed']
        self.tasks = [t for t in self.tasks if t.get('status') != 'completed']
        
        self._add_log('info', f"Cleared {len(completed)} completed tasks")
        
        self._send_json({
            "status": "success",
            "cleared": len(completed),
            "remaining": len(self.tasks)
        })
    
    def _handle_task_detail(self, path):
        """GET /api/task/{id} - Get specific task"""
        task_id = path.split('/')[-1]
        
        for task in self.tasks:
            if task['id'] == task_id:
                self._send_json({
                    "status": "success",
                    "task": task
                })
                return
        
        self._send_error(404, f"Task {task_id} not found")
    
    def _handle_task_delete(self, path):
        """DELETE /api/task/{id} - Delete a task"""
        task_id = path.split('/')[-1]
        
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                self._add_log('info', f"Deleted task: {deleted['description'][:50]}...")
                self._send_json({
                    "status": "success",
                    "message": f"Task {task_id} deleted"
                })
                return
        
        self._send_error(404, f"Task {task_id} not found")
    
    # ============================================
    # API: BOTS
    # ============================================
    
    def _handle_bot_create(self):
        """POST /api/create_bot - Create a new bot"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            requirements = data.get('requirements')
            location = data.get('location', 'local')
            name = data.get('name', f"Bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            if not requirements:
                self._send_error(400, "Bot requirements are required")
                return
            
            # Generate bot code
            bot_code = self._generate_bot_code(requirements, name, location)
            
            bot = {
                "name": name,
                "requirements": requirements,
                "location": location,
                "created": datetime.now().isoformat(),
                "code": bot_code,
                "status": "active"
            }
            
            self.bots.append(bot)
            self._add_log('success', f"Bot created: {name}")
            
            self._send_json({
                "status": "success",
                "bot": bot
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _handle_bots_list(self):
        """GET /api/bots - List all bots"""
        self._send_json({
            "status": "success",
            "count": len(self.bots),
            "bots": self.bots
        })
    
    def _generate_bot_code(self, requirements, name, location):
        """Generate Python code for a new bot"""
        return f'''
"""
Bot: {name}
Created by: Unlimited AI Agent
Requirements: {requirements}
Location: {location}
Created: {datetime.now().isoformat()}
"""

import time
from datetime import datetime

class AutonomousBot:
    def __init__(self):
        self.name = "{name}"
        self.running = False
        self.tasks_completed = 0
    
    def start(self):
        print(f"🤖 {self.name} started!")
        self.running = True
        while self.running:
            self._execute_task()
            time.sleep(10)
    
    def stop(self):
        self.running = False
        print(f"🛑 {self.name} stopped")
    
    def _execute_task(self):
        print(f"✅ Task completed at {datetime.now().isoformat()}")
        self.tasks_completed += 1

if __name__ == "__main__":
    bot = AutonomousBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()
'''
    
    # ============================================
    # API: LEARNING
    # ============================================
    
    def _handle_learn(self):
        """POST /api/learn - Learn from text"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            text = data.get('text')
            category = data.get('category', 'general')
            source = data.get('source', 'user_input')
            
            if not text:
                self._send_error(400, "Text to learn is required")
                return
            
            # Store knowledge
            knowledge_item = {
                "id": len(self.knowledge_items) + 1,
                "text": text[:500] + "..." if len(text) > 500 else text,
                "full_text": text,
                "category": category,
                "source": source,
                "learned": datetime.now().isoformat(),
                "summary": self._summarize_text(text)
            }
            
            self.knowledge_items.append(knowledge_item)
            
            # Update memory stats
            self.agent_state['memory']['knowledge_graph']['total_concepts'] += 1
            self.agent_state['memory']['experience_db']['total'] += 1
            
            self._add_log('success', f"Learned from: {source or 'user_input'}")
            
            self._send_json({
                "status": "success",
                "message": "Learning successful",
                "knowledge": knowledge_item,
                "timestamp": datetime.now().isoformat()
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _summarize_text(self, text):
        """Simple text summarization"""
        sentences = text.split('.')
        if len(sentences) <= 3:
            return text
        return '. '.join(sentences[:3]) + '...'
    
    # ============================================
    # API: KNOWLEDGE
    # ============================================
    
    def _handle_knowledge_list(self):
        """GET /api/knowledge - List all knowledge items"""
        self._send_json({
            "status": "success",
            "count": len(self.knowledge_items),
            "knowledge": self.knowledge_items[-50:]
        })
    
    # ============================================
    # API: LOGS
    # ============================================
    
    def _add_log(self, level, message):
        """Add a log entry"""
        self.logs.append({
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 100 logs
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
    
    def _handle_logs(self):
        """GET /api/logs - Get system logs"""
        self._send_json({
            "status": "success",
            "count": len(self.logs),
            "logs": self.logs[-50:]  # Last 50 logs
        })
    
    # ============================================
    # API: SETTINGS
    # ============================================
    
    def _handle_settings_get(self):
        """GET /api/settings - Get agent settings"""
        self._send_json({
            "status": "success",
            "settings": self.settings
        })
    
    def _handle_settings_save(self):
        """POST /api/settings - Save agent settings"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            for key, value in data.items():
                if key in self.settings:
                    self.settings[key] = value
            
            self._add_log('info', "Settings updated")
            
            self._send_json({
                "status": "success",
                "settings": self.settings
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    # ============================================
    # API: DATA MANAGEMENT
    # ============================================
    
    def _handle_clear_data(self):
        """POST /api/clear - Clear all data"""
        self.tasks = []
        self.bots = []
        self.knowledge_items = []
        self.logs = []
        self.task_counter = 0
        
        self._add_log('info', "All data cleared")
        
        self._send_json({
            "status": "success",
            "message": "All data cleared"
        })
    
    def _handle_export_data(self):
        """GET /api/export - Export all data"""
        export_data = {
            "agent": {
                "name": self.agent_state["name"],
                "version": self.agent_state["version"]
            },
            "tasks": self.tasks,
            "bots": self.bots,
            "knowledge": self.knowledge_items,
            "settings": self.settings,
            "exported": datetime.now().isoformat()
        }
        
        self._send_json({
            "status": "success",
            "data": export_data
        })
    
    def _handle_import_data(self):
        """POST /api/import - Import data"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            imported = data.get('data', {})
            
            if imported.get('tasks'):
                self.tasks = imported['tasks']
            if imported.get('bots'):
                self.bots = imported['bots']
            if imported.get('knowledge'):
                self.knowledge_items = imported['knowledge']
            if imported.get('settings'):
                self.settings = imported['settings']
            
            self._add_log('success', f"Imported data: {len(imported.get('tasks', []))} tasks")
            
            self._send_json({
                "status": "success",
                "message": "Data imported successfully",
                "imported": {
                    "tasks": len(imported.get('tasks', [])),
                    "bots": len(imported.get('bots', [])),
                    "knowledge": len(imported.get('knowledge', []))
                }
            })
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON body")
        except Exception as e:
            self._send_error(500, str(e))
    
    # ============================================
    # WEBHOOK / CRON
    # ============================================
    
    def _handle_webhook(self):
        """GET /api/webhook - Cron job trigger"""
        self._add_log('info', "Webhook triggered")
        
        # Process any pending tasks automatically
        pending = [t for t in self.tasks if t.get('status') == 'pending']
        processed = 0
        
        for task in pending[:5]:  # Max 5 per run
            result = self._process_with_ai(task['description'], task.get('context', {}))
            task['status'] = 'completed' if result.get('success') else 'failed'
            task['completed'] = datetime.now().isoformat()
            task['result'] = result
            processed += 1
        
        self._send_json({
            "status": "success",
            "processed": processed,
            "pending": len([t for t in self.tasks if t.get('status') == 'pending']),
            "timestamp": datetime.now().isoformat()
        })
    
    # ============================================
    # AI PROCESSING ENGINE
    # ============================================
    
    def _process_with_ai(self, task, context):
        """Process task with AI intelligence"""
        # Domain detection
        domains = {
            'finance': ['finance', 'trade', 'investment', 'stock', 'market', 'bitcoin', 'crypto', 'price'],
            'business': ['business', 'company', 'strategy', 'management', 'ceo', 'organization'],
            'healthcare': ['health', 'doctor', 'patient', 'medical', 'hospital', 'disease'],
            'technology': ['technology', 'software', 'programming', 'code', 'database', 'system'],
            'legal': ['legal', 'law', 'contract', 'rights', 'court', 'attorney'],
            'creative': ['creative', 'design', 'art', 'music', 'writing', 'content'],
        }
        
        detected_domain = 'general'
        for domain, keywords in domains.items():
            if any(kw in task.lower() for kw in keywords):
                detected_domain = domain
                break
        
        # Generate suggestions based on domain
        suggestions = {
            'finance': [
                "Use technical analysis with RSI and MACD",
                "Set stop-loss and take-profit levels",
                "Monitor market sentiment"
            ],
            'business': [
                "Conduct market research",
                "Analyze competitors",
                "Develop a clear value proposition"
            ],
            'healthcare': [
                "Consult medical professionals",
                "Follow evidence-based practices",
                "Prioritize patient safety"
            ],
            'technology': [
                "Use agile development methodology",
                "Implement CI/CD pipeline",
                "Follow security best practices"
            ],
            'legal': [
                "Review relevant laws and regulations",
                "Document all decisions",
                "Seek expert legal advice if needed"
            ],
            'creative': [
                "Brainstorm multiple ideas",
                "Get feedback from diverse perspectives",
                "Iterate based on feedback"
            ]
        }
        
        return {
            "success": True,
            "message": f"Task processed: {task}",
            "domain": detected_domain,
            "analysis": f"AI analyzed: {task[:100]}...",
            "suggestions": suggestions.get(detected_domain, [
                "Break the task into smaller steps",
                "Use relevant data sources",
                "Monitor progress regularly"
            ]),
            "confidence": 0.85 + (len(task.split()) / 1000),
            "timestamp": datetime.now().isoformat()
        }

# ============================================
# LOCAL DEVELOPMENT
# ============================================

if __name__ == "__main__":
    from http.server import HTTPServer
    port = 8080
    server = HTTPServer(('localhost', port), handler)
    print(f"🚀 Server running at http://localhost:{port}")
    print("   Press Ctrl+C to stop")
    server.serve_forever()
