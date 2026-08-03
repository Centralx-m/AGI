"""
Replication API
===============
Create a new bot anywhere.
"""

import json
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent, Task_CreateBot


def handler(request):
    """
    Replicate the agent
    
    Request body:
    {
        "requirements": "What the new bot should do",
        "location": "local"
    }
    
    Returns:
        dict: Replication result
    """
    domain = os.getenv('DOMAIN', 'ai.taagc.site')
    
    try:
        if request.method == "POST":
            body = json.loads(request.body)
        else:
            return {
                "status": "error",
                "domain": domain,
                "message": "Please use POST method"
            }
        
        requirements = body.get("requirements")
        location = body.get("location", "local")
        
        if not requirements:
            return {
                "status": "error",
                "domain": domain,
                "message": "Bot requirements are required"
            }
        
        agent = UnlimitedAgent()
        creator = Task_CreateBot(agent)
        result = creator.execute(requirements, location)
        
        return {
            "status": "success",
            "domain": domain,
            "bot": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "domain": domain,
            "message": str(e)
        }