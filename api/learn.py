import json
from auto_master import run_auto_master  # Directly import your auto-master logic

def handler(request):
    """
    Vercel serverless function to trigger MoonAI auto-learning with detailed logs.
    """
    try:
        # Run auto-master and collect logs
        result = run_auto_master(log_enabled=True)  # Ensure auto_master supports logging
        logs = result.get("logs", [])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!",
                "knowledge_entries": result.get("knowledge_entries", 0),
                "logs": logs
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
