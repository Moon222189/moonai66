import json
import os
import subprocess

def handler(request):
    try:
        # Step 1: Auto-learn new knowledge
        subprocess.run(["python", "auto_web_learn.py"], check=True)

        # Step 2: Run auto_master to update embeddings and model
        subprocess.run(["python", "auto_master.py"], check=True)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "MoonAI auto-learn executed successfully!"
            })
        }

    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Error during auto-learn: {e}"
            })
        }
