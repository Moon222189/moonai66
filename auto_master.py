import os
from auto_learn import gather_new_data, update_knowledge, update_embeddings, train_model
from auto_web_learn import fetch_text_from_url
import time

KNOWLEDGE_FILE = "data/brainknowledge.txt"

# Trusted websites for self-learning
TRUSTED_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Physics",
    "https://en.wikipedia.org/wiki/Mathematics",
    "https://en.wikipedia.org/wiki/History",
]

# File for conversation logs
CONVERSATION_LOG = "data/conversations.log"

def gather_from_conversations():
    if not os.path.exists(CONVERSATION_LOG):
        return []
    new_lines = []
    with open(CONVERSATION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                new_lines.append(line)
    return new_lines

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

        # Gather local files
        local_lines = gather_new_data()
        print(f"Local files found: {len(local_lines)} lines")

        # Gather conversation logs
        convo_lines = gather_from_conversations()
        print(f"Conversation lines found: {len(convo_lines)} lines")

        # Gather web knowledge
        web_lines = gather_from_web()
        print(f"Web lines found: {len(web_lines)} lines")

        # Combine all new knowledge
        total_new = local_lines + convo_lines + web_lines
        if total_new:
            all_lines = update_knowledge(total_new)
            update_embeddings(all_lines)
            print("Retraining model on updated knowledge...")
            train_model(KNOWLEDGE_FILE)
            print("=== MoonAI Self-Learning Cycle Complete ===\n")
        else:
            print("No new knowledge found. MoonAI is up to date.\n")

        # Repeat after 6 hours
        time.sleep(6 * 60 * 60)

if __name__ == "__main__":
    auto_master_loop()
