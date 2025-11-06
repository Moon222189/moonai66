import os
import pickle
from auto_web_learn import auto_learn
from embeddings import create_embeddings

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"

def run_auto_master():
    print("🚀 MoonAI: Starting auto-learn cycle...")

    # Step 1: Fetch new knowledge
    print("📚 Fetching new knowledge...")
    auto_learn()
    print("✅ Knowledge update complete!")

    # Step 2: Load all knowledge
    if not os.path.exists(KNOWLEDGE_FILE):
        os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
        open(KNOWLEDGE_FILE, "w").close()

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge_lines = [line.strip() for line in f if line.strip()]

    print(f"📝 Loaded {len(knowledge_lines)} knowledge entries.")

    # Step 3: Generate embeddings
    print("🔗 Generating embeddings...")
    embeddings = create_embeddings(knowledge_lines)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)
    print(f"💾 Embeddings saved to {EMBEDDINGS_FILE}")

    print("✅ Auto-master cycle complete.")
    return {"knowledge_entries": len(knowledge_lines)}

if __name__ == "__main__":
    run_auto_master()
