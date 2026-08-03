"""
Agent Status API
================
Returns the current status of the AI agent.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent


def handler(request):
    """
    Get agent status
    
    Returns:
        dict: Agent status information
    """
    try:
        agent = UnlimitedAgent()
        status = agent.get_status()
        
        return {
            "status": "success",
            "agent": status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }