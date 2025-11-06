import os
import pickle
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from model.train_model import train_model

DATA_DIR = "data/auto_data"
KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBED_INDEX_FILE = "embeddings/knowledge.index"
VECTOR_FILE = "embeddings/vectorizer.pkl"
LINES_FILE = "embeddings/lines.pkl"
CONVERSATION_LOG = "data/conversations.log"

def gather_new_data():
    new_lines = []
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".txt"):
                with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            new_lines.append(line)
    return new_lines

def gather_from_conversations():
    new_lines = []
    if os.path.exists(CONVERSATION_LOG):
        with open(CONVERSATION_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    new_lines.append(line)
    return new_lines

def update_knowledge(new_lines):
    if not new_lines:
        return []
    if not os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            pass
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        existing = set(f.read().splitlines())
    updated = existing.union(set(new_lines))
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        for line in updated:
            f.write(line + "\n")
    return list(updated)

def update_embeddings(lines):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(lines).toarray().astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, EMBED_INDEX_FILE)
    with open(VECTOR_FILE, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(LINES_FILE, "wb") as f:
        pickle.dump(lines, f)

def auto_learn_cycle():
    local_lines = gather_new_data()
    convo_lines = gather_from_conversations()
    total_new = local_lines + convo_lines
    if total_new:
        all_lines = update_knowledge(total_new)
        update_embeddings(all_lines)
        print(f"Learning {len(total_new)} new lines from local & conversation logs...")
        train_model(KNOWLEDGE_FILE)
        print("MoonAI has improved itself from local data and conversations.")
    else:
        print("No new local/conversation knowledge found.")

if __name__ == "__main__":
    auto_learn_cycle()
