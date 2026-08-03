"""
Tasks API
=========
List and manage tasks.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent
from src.tasks.task_manager import TaskManager


def handler(request):
    """
    List all tasks
    
    Returns:
        dict: List of tasks
    """
    try:
        agent = UnlimitedAgent()
        task_manager = TaskManager(agent)
        
        tasks = task_manager.get_all_tasks()
        
        return {
            "status": "success",
            "count": len(tasks),
            "tasks": tasks
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }