import json
import sys
import os

# Add root folder to Python path to import your scripts
sys.path.append(os.getcwd())

# Import your existing auto-learn function
from auto_web_learn import auto_learn

def handler(request):
    """
    Vercel serverless function that triggers MoonAI auto-learning.
    Returns JSON logs of new knowledge added.
    """
    try:
        logs = auto_learn(log_enabled=True)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!",
                "logs": logs,
                "knowledge_entries_added": len(logs)
            }, indent=2)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error during MoonAI auto-learn",
                "error": str(e)
            }, indent=2)
        }
