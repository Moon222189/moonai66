import requests
from bs4 import BeautifulSoup
import re
import os

KNOWLEDGE_FILE = "data/brainknowledge.txt"

# --- Clean text helper ---
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)      # Remove citations
    text = re.sub(r'\s+', ' ', text)        # Remove extra whitespace
    return text.strip()

# --- Load existing knowledge to avoid duplicates ---
def load_existing_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return set()
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

# --- Append new knowledge safely ---
def append_knowledge(new_text, existing_knowledge):
    if not new_text or new_text in existing_knowledge:
        return
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    existing_knowledge.add(new_text)
    print("Added knowledge:", new_text[:60], "...")

# --- Fetch Wikipedia summary ---
def fetch_wikipedia_intro(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return clean_text(data.get("extract", ""))
    except Exception as e:
        print(f"Failed Wikipedia topic {topic}: {e}")
        return ""

# --- Fetch Project Gutenberg text (first 5000 chars) ---
def fetch_gutenberg_text(book_url):
    try:
        response = requests.get(book_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return clean_text(text[:5000])
    except Exception as e:
        print(f"Failed Gutenberg book: {e}")
        return ""

# --- Main auto-learn routine ---
def auto_learn():
    existing_knowledge = load_existing_knowledge()

    # --- Wikipedia topics ---
    wikipedia_topics = [
        "Artificial_intelligence",
        "Machine_learning",
        "Python_(programming_language)",
        "Neural_network",
        "Reinforcement_learning",
        "Data_science",
        "Computer_vision",
        "Natural_language_processing"
    ]
    for topic in wikipedia_topics:
        text = fetch_wikipedia_intro(topic)
        append_knowledge(f"Topic: {topic}\nInfo: {text}", existing_knowledge)

    # --- Project Gutenberg books ---
    gutenberg_books = {
        "Pride_and_Prejudice": "https://www.gutenberg.org/files/1342/1342-0.txt",
        "Frankenstein": "https://www.gutenberg.org/files/84/84-0.txt",
        "The_Adventures_of_Sherlock_Holmes": "https://www.gutenberg.org/files/1661/1661-0.txt"
    }
    for title, url in gutenberg_books.items():
        book_text = fetch_gutenberg_text(url)
        append_knowledge(f"Topic: {title}\nInfo: {book_text}", existing_knowledge)

    print(f"Auto-learn complete. Total knowledge entries: {len(existing_knowledge)}")

# --- Run if called directly ---
if __name__ == "__main__":
    auto_learn()
