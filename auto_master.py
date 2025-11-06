import os
import pickle
from auto_web_learn import auto_learn
from model import train_model  # your training logic
from embeddings import create_embeddings  # your embeddings logic

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"

# --- Step 1: Auto-learn new knowledge ---
print("Fetching new knowledge from trusted sources...")
auto_learn()
print("Knowledge update complete!")

# --- Step 2: Load knowledge ---
if not os.path.exists(KNOWLEDGE_FILE):
    print(f"No knowledge file found at {KNOWLEDGE_FILE}, creating empty file.")
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    open(KNOWLEDGE_FILE, "w").close()

with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
    knowledge_lines = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(knowledge_lines)} knowledge entries.")

# --- Step 3: Generate embeddings ---
print("Generating embeddings...")
embeddings = create_embeddings(knowledge_lines)
with open(EMBEDDINGS_FILE, "wb") as f:
    pickle.dump(embeddings, f)
print(f"Embeddings saved to {EMBEDDINGS_FILE}")

# --- Step 4: Train / retrain model ---
print("Training AI model...")
train_model(knowledge_lines, embeddings)
print("Model training complete!")

# --- Step 5: Finish ---
print("MoonAI auto-master cycle complete!")
