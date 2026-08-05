from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="Unlimited AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "name": "Unlimited AI",
        "status": "online",
        "version": "2.0.0"
    }

@app.get("/api/status")
def status():
    return {
        "status": "success",
        "server": "Vercel",
        "domain": "ai.taagc.site",
        "timestamp": datetime.utcnow().isoformat(),
        "agent": {
            "name": "UnlimitedAI",
            "version": "2.0.0",
            "state": "online",
            "capabilities": [
                "Self-learning",
                "Self-repair",
                "Self-upgrade",
                "Bot creation"
            ]
        }
    }

@app.get("/api/tasks")
def tasks():
    return {
        "status": "success",
        "count": 0,
        "tasks": []
    }

@app.get("/api/test")
def test():
    return {
        "status": "success",
        "message": "API Working",
        "time": datetime.utcnow().isoformat()
    }

@app.post("/api/task")
def create_task(data: dict):
    task = data.get("task") or data.get("description")
    if not task:
        return {"status": "error", "message": "Task is required"}

    return {
        "status": "success",
        "task": task,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/create_bot")
def create_bot(data: dict):
    req = data.get("requirements")
    if not req:
        return {"status": "error", "message": "Requirements required"}

    return {
        "status": "success",
        "bot": {
            "name": "UnlimitedBot",
            "requirements": req,
            "status": "active",
            "created": datetime.utcnow().isoformat()
        }
    }

@app.post("/api/learn")
def learn(data: dict):
    text = data.get("text")
    if not text:
        return {"status": "error", "message": "Text required"}

    return {
        "status": "success",
        "message": "Learning completed",
        "characters": len(text),
        "timestamp": datetime.utcnow().isoformat()
    }
