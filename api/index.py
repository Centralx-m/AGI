"""
Unlimited AI Agent - Production API
Deployed on Vercel with FastAPI
"""

import time
from datetime import datetime
from typing import Optional, List, Dict, Any

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

# --- FastAPI App Initialization ---
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A self-learning, self-repairing autonomous AI agent.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --- CORS Configuration ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://ai.taagc.site",
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request Validation ---
class TaskRequest(BaseModel):
    task: str = Field(..., description="The task description to process.")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context for the task.")

class CreateBotRequest(BaseModel):
    requirements: str = Field(..., description="The requirements for the new bot.")
    location: str = Field("local", description="Deployment location (local, cloud, remote).")
    name: Optional[str] = Field(None, description="Optional name for the bot.")

class LearnRequest(BaseModel):
    text: str = Field(..., description="The text content to learn from.")
    category: str = Field("general", description="Category of the knowledge.")
    source: Optional[str] = Field("user_input", description="Source of the text.")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's chat message.")
    session_id: Optional[str] = Field(None, description="Optional session ID for chat history.")

# --- In-Memory Storage (for demonstration) ---
tasks_db: List[Dict] = []
bots_db: List[Dict] = []
knowledge_db: List[Dict] = []
logs_db: List[Dict] = []
task_counter = 0

# --- Helper Functions ---
def add_log(level: str, message: str):
    """Add an entry to the logs."""
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
    from pathlib import Path
    file_path = Path(__file__).parent.parent / 'public' / 'index.html'
    if file_path.exists():
        with open(file_path, 'r') as f:
            return HTMLResponse(content=f.read())
    else:
        html_content = """
        <!DOCTYPE html>
        <html><head><title>Unlimited AI Agent</title></head>
        <body style="background:#0a0a0a;color:#fff;font-family:sans-serif;text-align:center;padding:50px;">
            <h1>🤖 Unlimited AI Agent</h1>
            <p>API is running. Visit <a href="/api/docs">/api/docs</a> for the interactive documentation.</p>
            <p>Status: <span style="color:#00cc88;">● Online</span></p>
            <p>© 2026 TAAGC</p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Vercel and monitoring."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/version")
async def get_version():
    """Return the current API version and deployment info."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "domain": DOMAIN,
        "deployment": DEPLOYMENT,
        "uptime": time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0
    }

@app.get("/api/metrics")
async def get_metrics():
    """Return basic system metrics."""
    return {
        "tasks_total": len(tasks_db),
        "tasks_completed": len([t for t in tasks_db if t.get('status') == 'completed']),
        "bots_created": len(bots_db),
        "knowledge_items": len(knowledge_db),
        "logs_count": len(logs_db)
    }

@app.get("/api/status")
async def get_status():
    """Return the full status of the agent."""
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
    return {"status": "success", "count": len(tasks_db), "tasks": tasks_db[-50:]}

@app.get("/api/test")
async def test_endpoint():
    """A simple test endpoint to verify the API is working."""
    return {"status": "success", "message": "FastAPI is working!", "timestamp": datetime.now().isoformat()}

@app.post("/api/task")
async def create_task(request: TaskRequest):
    """Create and process a new task."""
    global task_counter
    task_counter += 1
    
    # Simulate AI processing
    domain = "general"
    for d in ["finance", "business", "healthcare", "technology"]:
        if d in request.task.lower():
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
    
    return {"status": "success", "task": task_entry, "result": result}

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
    return {"status": "success", "bot": bot}

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
    return {"status": "success", "message": "Learning successful", "knowledge": knowledge_item}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """A simple chat endpoint for the AI."""
    # Placeholder chat response
    response = {
        "session_id": request.session_id or "new-session",
        "response": f"AI received your message: '{request.message}'. This is a placeholder response.",
        "timestamp": datetime.now().isoformat()
    }
    return {"status": "success", "chat": response}

# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

# --- Lifespan Events ---
@app.on_event("startup")
async def startup_event():
    app.state.start_time = time.time()
    add_log('info', "Application started successfully on Vercel")
    print(f"🚀 {APP_NAME} v{APP_VERSION} started at {datetime.now().isoformat()}")

@app.on_event("shutdown")
async def shutdown_event():
    add_log('info', "Application shutting down")

# --- This is the handler that Vercel expects ---
handler = app

# --- Local Development ---
if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
