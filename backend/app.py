from flask import Flask, request, jsonify
from flask_cors import CORS
from brain import Brain

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

moon_brain = Brain()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = moon_brain.query(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
