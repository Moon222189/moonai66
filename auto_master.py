import time
from auto_learn import gather_new_data, gather_from_conversations, update_knowledge, update_embeddings, train_model
from auto_web_learn import fetch_text_from_url

KNOWLEDGE_FILE = "data/brainknowledge.txt"

TRUSTED_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Physics",
    "https://en.wikipedia.org/wiki/Mathematics",
    "https://en.wikipedia.org/wiki/History",
    "https://en.wikipedia.org/wiki/Computer_science",
    "https://en.wikipedia.org/wiki/Chemistry",
    "https://en.wikipedia.org/wiki/Biology",
    "https://en.wikipedia.org/wiki/Space",
    "https://en.wikipedia.org/wiki/Technology",
]

def gather_from_web():
    all_new_lines = []
    for url in TRUSTED_URLS:
        print(f"Fetching data from {url}...")
        lines = fetch_text_from_url(url)
        all_new_lines.extend(lines)
    return all_new_lines

def auto_master_loop():
    while True:
        print("=== MoonAI Self-Learning Cycle Started ===")
        local_lines = gather_new_data()
        convo_lines = gather_from_conversations()
        web_lines = gather_from_web()
        total_new = local_lines + convo_lines + web_lines
        print(f"Total new lines found: {len(total_new)}")
        if total_new:
            all_lines = update_knowledge(total_new)
            update_embeddings(all_lines)
            print("Retraining model on updated knowledge...")
            train_model(KNOWLEDGE_FILE)
            print("=== MoonAI Self-Learning Cycle Complete ===\n")
        else:
            print("No new knowledge found. MoonAI is up to date.\n")
        time.sleep(6 * 60 * 60)

if __name__ == "__main__":
    auto_master_loop()
