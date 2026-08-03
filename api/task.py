"""
Task Processing API
===================
Process a task with the AI agent.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent


def handler(request):
    """
    Process a task
    
    Request body:
    {
        "task": "Task description",
        "context": {"key": "value"}  # Optional
    }
    
    Returns:
        dict: Task execution result
    """
    try:
        # Parse request body
        if request.method == "POST":
            body = json.loads(request.body)
        else:
            return {
                "status": "error",
                "message": "Please use POST method"
            }
        
        task = body.get("task")
        context = body.get("context", {})
        
        if not task:
            return {
                "status": "error",
                "message": "Task description is required"
            }
        
        # Initialize agent and process task
        agent = UnlimitedAgent()
        result = agent.process_task(task, context)
        
        return {
            "status": "success",
            "task": task,
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }