"""
Unlimited AI Agent - API Handler
Deployed at: https://ai.taagc.site
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    """Main API handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]
        print(f"📥 GET {path}")
        
        # ============================================
        # API ROUTES - Return JSON
        # ============================================
        if path == '/api/status':
            self._send_json({
                "status": "success",
                "domain": "ai.taagc.site",
                "server": "Vercel",
                "timestamp": datetime.now().isoformat(),
                "agent": {
                    "name": "UnlimitedAI",
                    "version": "2.0.0",
                    "state": "online",
                    "tasks_completed": 0,
                    "uptime": 0,
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
                    ]
                }
            })
        
        elif path == '/api/tasks':
            self._send_json({
                "status": "success",
                "count": 0,
                "tasks": []
            })
        
        elif path == '/api/test':
            self._send_json({
                "status": "success",
                "message": "API is working!",
                "path": path,
                "timestamp": datetime.now().isoformat()
            })
        
        # ============================================
        # DASHBOARD - Return HTML
        # ============================================
        elif path == '/' or path == '':
            self._serve_dashboard()
        
        elif path == '/style.css':
            self._serve_static('style.css', 'text/css')
        
        elif path == '/app.js':
            self._serve_static('app.js', 'application/javascript')
        
        # ============================================
        # 404 - Return JSON for API, HTML for pages
        # ============================================
        elif path.startswith('/api/'):
            self._send_error(404, f"API endpoint not found: {path}")
        
        else:
            self._send_error(404, f"Page not found: {path}")
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path.split('?')[0]
        print(f"📥 POST {path}")
        
        if path == '/api/task':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body) if body else {}
                
                task = data.get('task') or data.get('description')
                
                if not task:
                    self._send_error(400, "Task description is required")
                    return
                
                self._send_json({
                    "status": "success",
                    "task": task,
                    "result": {
                        "success": True,
                        "message": f"Task processed: {task}",
                        "domain": "general",
                        "analysis": f"AI analyzed: {task[:100]}...",
                        "suggestions": [
                            "Break the task into smaller steps",
                            "Use relevant data sources",
                            "Monitor progress regularly"
                        ],
                        "timestamp": datetime.now().isoformat()
                    }
                })
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON body")
            except Exception as e:
                self._send_error(500, str(e))
        
        elif path == '/api/create_bot':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body) if body else {}
                
                requirements = data.get('requirements')
                
                if not requirements:
                    self._send_error(400, "Bot requirements are required")
                    return
                
                self._send_json({
                    "status": "success",
                    "bot": {
                        "name": f"Bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "requirements": requirements,
                        "location": data.get('location', 'local'),
                        "created": datetime.now().isoformat(),
                        "status": "active"
                    }
                })
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON body")
            except Exception as e:
                self._send_error(500, str(e))
        
        elif path == '/api/learn':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body) if body else {}
                
                text = data.get('text')
                
                if not text:
                    self._send_error(400, "Text to learn is required")
                    return
                
                self._send_json({
                    "status": "success",
                    "message": "Learning successful",
                    "text": text[:200] + "..." if len(text) > 200 else text,
                    "category": data.get('category', 'general'),
                    "source": data.get('source', 'user_input'),
                    "timestamp": datetime.now().isoformat()
                })
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON body")
            except Exception as e:
                self._send_error(500, str(e))
        
        else:
            self._send_error(404, f"POST endpoint not found: {path}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    # ============================================
    # HELPERS
    # ============================================
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
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
    
    def _serve_dashboard(self):
        """Serve the HTML dashboard"""
        try:
            from pathlib import Path
            file_path = Path(__file__).parent.parent / 'public' / 'index.html'
            if file_path.exists():
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self._send_error(404, "Dashboard not found")
        except:
            self._send_error(404, "Dashboard not found")
    
    def _serve_static(self, filename, content_type):
        try:
            from pathlib import Path
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
        except:
            self._send_error(404, f"File not found: {filename}")
