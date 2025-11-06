from flask import Flask, render_template, request
import torch
from model.small_transformer import SmallTransformer
import pickle
import faiss
import numpy as np
from reasoning.logic_engine import infer_logic

# Load model
with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
stoi = tokenizer["stoi"]
itos = tokenizer["itos"]
vocab_size = len(stoi)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SmallTransformer(vocab_size).to(device)
model.load_state_dict(torch.load("model/moonai_model.pt", map_location=device))
model.eval()

# Load FAISS embeddings
index = faiss.read_index("embeddings/knowledge.index")
with open("embeddings/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("embeddings/lines.pkl", "rb") as f:
    knowledge_lines = pickle.load(f)

app = Flask(__name__)

def generate_response(prompt, max_len=200):
    model_input = [stoi.get(c, 0) for c in prompt.lower()]
    x = torch.tensor(model_input).unsqueeze(0).to(device)
    for _ in range(max_len):
        logits = model(x)
        next_id = torch.argmax(logits[0, -1]).item()
        x = torch.cat([x, torch.tensor([[next_id]]).to(device)], dim=1)
    return ''.join([itos[i] for i in x[0].tolist()])

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        query = request.form["query"]

        # 1. Reasoning from rules
        logic_results = infer_logic(query, knowledge_lines)
        
        # 2. Use transformer to generate text
        generated_text = generate_response(query)
        
        # 3. Combine logic and generation
        response = "Logic Results:\n" + "\n".join(logic_results) + "\n\nAI Says:\n" + generated_text
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
