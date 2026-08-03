"""
Learning API
============
Learn from books or text sources.
"""

import json
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unlimited_agent import UnlimitedAgent


def handler(request):
    """
    Learn from text
    
    Request body:
    {
        "text": "Text to learn from",
        "category": "finance",
        "source": "book_name"
    }
    
    Returns:
        dict: Learning result
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
        
        text = body.get("text")
        category = body.get("category", "general")
        source = body.get("source", "user_input")
        
        if not text:
            return {
                "status": "error",
                "domain": domain,
                "message": "Text to learn is required"
            }
        
        agent = UnlimitedAgent()
        result = agent.memory.learn_from_text(text, category, source)
        
        return {
            "status": "success",
            "domain": domain,
            "message": "Learning successful",
            "text": text[:200] + "..." if len(text) > 200 else text,
            "category": category,
            "source": source
        }
        
    except Exception as e:
        return {
            "status": "error",
            "domain": domain,
            "message": str(e)
        }