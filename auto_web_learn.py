import requests
from bs4 import BeautifulSoup
import re
import os

KNOWLEDGE_FILE = "data/brainknowledge.txt"

# --- Helper to clean text ---
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)  # Remove citation marks [1], [2], etc.
    text = re.sub(r'\s+', ' ', text)     # Remove extra whitespace
    return text.strip()

# --- Fetch Wikipedia intro text ---
def fetch_wikipedia_intro(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return clean_text(data.get("extract", ""))
    except Exception as e:
        print(f"Failed to fetch Wikipedia topic {topic}: {e}")
        return ""

# --- Fetch Project Gutenberg text (example: public domain book) ---
def fetch_gutenberg_text(book_url):
    try:
        response = requests.get(book_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return clean_text(text[:5000])  # take first 5000 chars
    except Exception as e:
        print(f"Failed to fetch Gutenberg book: {e}")
        return ""

# --- Append new knowledge safely ---
def append_knowledge(new_text):
    if not new_text:
        return
    if not os.path.exists(KNOWLEDGE_FILE):
        os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
        open(KNOWLEDGE_FILE, "w").close()
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    print("Knowledge added successfully.")

# --- Main auto-learn routine ---
def auto_learn():
    # Wikipedia topics
    topics = ["Artificial_intelligence", "Machine_learning", "Python_(programming_language)", "Neural_network"]
    for topic in topics:
        text = fetch_wikipedia_intro(topic)
        append_knowledge(f"Topic: {topic}\nInfo: {text}")

    # Project Gutenberg example book
    gutenberg_url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Pride and Prejudice
    book_text = fetch_gutenberg_text(gutenberg_url)
    append_knowledge(f"Topic: Pride_and_Prejudice\nInfo: {book_text}")

if __name__ == "__main__":
    auto_learn()
