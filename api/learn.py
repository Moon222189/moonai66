import json
import sys
import os

# Add root folder to Python path
sys.path.append(os.getcwd())

# Import your auto-learn function
from auto_web_learn import auto_learn

def handler(request):
    try:
        logs = auto_learn(log_enabled=True)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!",
                "logs": logs
            }, indent=2)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error during auto-learn",
                "error": str(e)
            }, indent=2)
        }
