"""
Webhook Endpoint
================
This is triggered by Vercel Cron Jobs.
Runs the agent autonomously.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent


def handler(request):
    """
    Run the agent autonomously (cron trigger)
    
    Returns:
        dict: Execution result
    """
    try:
        # Initialize agent
        agent = UnlimitedAgent()
        
        # Get pending tasks
        pending = agent.task_manager.get_pending_tasks()
        
        results = []
        for task in pending:
            result = agent.process_task(task['description'], task.get('context'))
            agent.task_manager.mark_completed(task['id'], result)
            results.append({
                'task_id': task['id'],
                'success': result['success']
            })
        
        return {
            "status": "success",
            "processed": len(results),
            "results": results,
            "timestamp": str(datetime.now())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }