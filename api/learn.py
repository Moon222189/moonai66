import json
import subprocess

def handler(request):
    try:
        # Run auto_master.py
        result = subprocess.run(
            ["python", "auto_master.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!",
                "output": result.stdout
            })
        }

    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error during auto-learn",
                "error": e.stderr
            })
        }
