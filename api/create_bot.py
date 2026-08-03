"""
Create Bot API
==============
Create a new autonomous bot.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent, Task_CreateBot


def handler(request):
    """
    Create a new bot
    
    Request body:
    {
        "requirements": "What the bot should do",
        "location": "local"  # Optional: local, cloud, remote
    }
    
    Returns:
        dict: Bot creation result
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
        
        requirements = body.get("requirements")
        location = body.get("location", "local")
        
        if not requirements:
            return {
                "status": "error",
                "message": "Bot requirements are required"
            }
        
        # Create bot
        agent = UnlimitedAgent()
        creator = Task_CreateBot(agent)
        result = creator.execute(requirements, location)
        
        return {
            "status": "success",
            "bot": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }