import json

def handler(request):
    # Load knowledge
    with open("data/brainknowledge.txt") as f:
        knowledge = f.read()

    # Here you can call your auto_master.py logic or auto_web_learn.py
    # Example: just return the knowledge length
    return {
        "statusCode": 200,
        "body": json.dumps({
            "knowledge_length": len(knowledge),
            "message": "MoonAI auto-learn triggered!"
        })
    }
