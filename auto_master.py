import os
import pickle
from auto_web_learn import auto_learn
from embeddings import create_embeddings

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"

def run_auto_master(log_enabled=False):
    logs = []
    log = lambda msg: logs.append(msg) if log_enabled else print(msg)

    log("🚀 MoonAI: Starting auto-learn cycle...")

    # Step 1: Fetch new knowledge
    log("📚 Fetching new knowledge...")
    auto_learn_logs = auto_learn(log_enabled=True)  # Update auto_web_learn to support logs
    logs.extend(auto_learn_logs)
    log("✅ Knowledge update complete!")

    # Step 2: Load all knowledge
    if not os.path.exists(KNOWLEDGE_FILE):
        os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
        open(KNOWLEDGE_FILE, "w").close()

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge_lines = [line.strip() for line in f if line.strip()]

    log(f"📝 Loaded {len(knowledge_lines)} knowledge entries.")

    # Step 3: Generate embeddings
    log("🔗 Generating embeddings...")
    embeddings = create_embeddings(knowledge_lines)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)
    log(f"💾 Embeddings saved to {EMBEDDINGS_FILE}")

    log("✅ Auto-master cycle complete.")
    return {"knowledge_entries": len(knowledge_lines), "logs": logs}
