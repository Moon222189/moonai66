import json
import sys
import os

sys.path.append(os.getcwd())  # so root scripts can be imported

from auto_web_learn import auto_learn

def handler(request):
    try:
        logs = auto_learn(log_enabled=True)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!",
                "logs": logs,
                "entries_added": len(logs)
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
