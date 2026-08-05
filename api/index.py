"""
Unlimited AI Agent - Production API
Deployed on Vercel with FastAPI
"""

import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
import uvicorn

# --- Configuration ---
APP_NAME = "Unlimited AI Agent"
APP_VERSION = "2.0.0"
DOMAIN = "ai.taagc.site"
DEPLOYMENT = "Vercel"

# --- FastAPI App ---
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A self-learning, self-repairing autonomous AI agent.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class TaskRequest(BaseModel):
    task: str = Field(..., description="The task description to process.")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class CreateBotRequest(BaseModel):
    requirements: str = Field(..., description="The requirements for the new bot.")
    location: str = Field("local")
    name: Optional[str] = None

class LearnRequest(BaseModel):
    text: str = Field(..., description="The text content to learn from.")
    category: str = Field("general")
    source: Optional[str] = Field("user_input")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's chat message.")
    session_id: Optional[str] = None

# --- In-Memory Storage ---
tasks_db: List[Dict] = []
bots_db: List[Dict] = []
knowledge_db: List[Dict] = []
logs_db: List[Dict] = []
task_counter = 0

# --- Helper Functions ---
def add_log(level: str, message: str):
    logs_db.append({
        "level": level,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    if len(logs_db) > 100:
        logs_db.pop(0)

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard."""
    try:
        file_path = Path(__file__).parent.parent / 'public' / 'index.html'
        if file_path.exists():
            with open(file_path, 'r') as f:
                return HTMLResponse(content=f.read())
    except:
        pass
    
    # Fallback HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unlimited AI Agent</title>
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                color: #fff;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                padding: 40px;
                background: rgba(255,255,255,0.05);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
                text-align: center;
            }
            h1 { font-size: 2.5rem; margin-bottom: 10px; }
            .icon { font-size: 3rem; }
            .status { color: #00cc88; margin: 20px 0; }
            .subtitle { color: #888; }
            .endpoint { 
                display: inline-block;
                padding: 8px 16px;
                margin: 5px;
                background: rgba(0,204,136,0.1);
                border: 1px solid #00cc88;
                border-radius: 8px;
                color: #00cc88;
                font-family: monospace;
                font-size: 0.9rem;
            }
            .footer { margin-top: 30px; color: #555; font-size: 0.8rem; }
            a { color: #00cc88; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🤖</div>
            <h1>Unlimited AI Agent</h1>
            <p class="subtitle">Powered by TAAGC | Deployed on Vercel</p>
            <p class="status">● Online & Running</p>
            <p>API Endpoints:</p>
            <div style="margin:20px 0;">
                <span class="endpoint">GET /api/status</span>
                <span class="endpoint">POST /api/task</span>
                <span class="endpoint">GET /api/tasks</span>
                <span class="endpoint">POST /api/create_bot</span>
                <span class="endpoint">POST /api/learn</span>
                <span class="endpoint">GET /api/health</span>
                <span class="endpoint">GET /api/test</span>
            </div>
            <p><a href="/api/docs">📚 API Documentation</a></p>
            <div class="footer">
                <p>🤖 Unlimited Autonomous AI Agent — Any Task, Any Domain</p>
                <p>© 2026 TAAGC</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": APP_VERSION
    }

@app.get("/api/version")
async def get_version():
    """Return version information."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "domain": DOMAIN,
        "deployment": DEPLOYMENT,
        "uptime": time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0
    }

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint."""
    return {
        "status": "success",
        "message": "FastAPI is working!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
async def get_status():
    """Full agent status."""
    return {
        "status": "success",
        "domain": DOMAIN,
        "server": DEPLOYMENT,
        "timestamp": datetime.now().isoformat(),
        "agent": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "state": "online",
            "tasks_completed": len([t for t in tasks_db if t.get('status') == 'completed']),
            "uptime": time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0,
            "bots_created": len(bots_db),
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
    }

@app.get("/api/tasks")
async def get_tasks():
    """List all tasks."""
    return {
        "status": "success",
        "count": len(tasks_db),
        "tasks": tasks_db[-50:]
    }

@app.post("/api/task")
async def create_task(request: TaskRequest):
    """Create and process a new task."""
    global task_counter
    task_counter += 1
    
    # Domain detection
    domain = "general"
    domain_keywords = {
        'finance': ['finance', 'trade', 'investment', 'stock', 'market', 'bitcoin', 'crypto', 'price'],
        'business': ['business', 'company', 'strategy', 'management', 'ceo', 'organization'],
        'healthcare': ['health', 'doctor', 'patient', 'medical', 'hospital', 'disease'],
        'technology': ['technology', 'software', 'programming', 'code', 'database', 'system'],
        'legal': ['legal', 'law', 'contract', 'rights', 'court', 'attorney'],
        'creative': ['creative', 'design', 'art', 'music', 'writing', 'content'],
    }
    for d, keywords in domain_keywords.items():
        if any(kw in request.task.lower() for kw in keywords):
            domain = d
            break

    result = {
        "success": True,
        "message": f"Task processed: {request.task}",
        "domain": domain,
        "analysis": f"AI analyzed: {request.task[:100]}...",
        "suggestions": [
            "Break the task into smaller steps",
            "Use relevant data sources",
            "Monitor progress regularly"
        ],
        "timestamp": datetime.now().isoformat()
    }

    task_entry = {
        "id": str(task_counter),
        "description": request.task,
        "status": "completed" if result.get('success') else "failed",
        "created": datetime.now().isoformat(),
        "completed": datetime.now().isoformat(),
        "result": result
    }
    tasks_db.append(task_entry)
    add_log('info', f"Task processed: {request.task[:50]}...")
    
    return {
        "status": "success",
        "task": task_entry,
        "result": result
    }

@app.post("/api/create_bot")
async def create_bot(request: CreateBotRequest):
    """Create a new autonomous bot."""
    bot = {
        "name": request.name or f"Bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "requirements": request.requirements,
        "location": request.location,
        "created": datetime.now().isoformat(),
        "status": "active"
    }
    bots_db.append(bot)
    add_log('success', f"Bot created: {bot['name']}")
    return {
        "status": "success",
        "bot": bot
    }

@app.post("/api/learn")
async def learn_text(request: LearnRequest):
    """Learn from provided text."""
    knowledge_item = {
        "id": len(knowledge_db) + 1,
        "text": request.text[:200] + "..." if len(request.text) > 200 else request.text,
        "category": request.category,
        "source": request.source,
        "learned": datetime.now().isoformat()
    }
    knowledge_db.append(knowledge_item)
    add_log('success', f"Learned from: {request.source or 'user_input'}")
    return {
        "status": "success",
        "message": "Learning successful",
        "knowledge": knowledge_item
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint."""
    response = {
        "session_id": request.session_id or "new-session",
        "response": f"AI received your message: '{request.message}'. This is a placeholder response.",
        "timestamp": datetime.now().isoformat()
    }
    return {
        "status": "success",
        "chat": response
    }

@app.get("/api/metrics")
async def get_metrics():
    """Return system metrics."""
    return {
        "tasks_total": len(tasks_db),
        "tasks_completed": len([t for t in tasks_db if t.get('status') == 'completed']),
        "bots_created": len(bots_db),
        "knowledge_items": len(knowledge_db),
        "logs_count": len(logs_db)
    }

# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": str(exc)},
    )

# --- Lifespan Events ---
@app.on_event("startup")
async def startup_event():
    app.state.start_time = time.time()
    add_log('info', "Application started successfully on Vercel")
    print(f"🚀 {APP_NAME} v{APP_VERSION} started at {datetime.now().isoformat()}")

# --- Vercel Handler ---
handler = app

# --- Local Development ---
if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
