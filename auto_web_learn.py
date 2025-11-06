import requests
from bs4 import BeautifulSoup
import re
import os
import pickle
from embeddings import create_embeddings, cosine_similarity  # You need a similarity function

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"
SIMILARITY_THRESHOLD = 0.8  # Adjust: 0.0 = always add, 1.0 = only exact duplicates

# --- Clean text helper ---
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# --- Load existing knowledge and embeddings ---
def load_existing_knowledge_and_embeddings():
    if not os.path.exists(KNOWLEDGE_FILE):
        return [], []
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "rb") as f:
            embeddings = pickle.load(f)
    else:
        embeddings = create_embeddings(lines)
    return lines, embeddings

# --- Append new knowledge safely ---
def append_new_knowledge(new_text, existing_lines, existing_embeddings):
    new_emb = create_embeddings([new_text])[0]
    for emb in existing_embeddings:
        if cosine_similarity(new_emb, emb) > SIMILARITY_THRESHOLD:
            return existing_lines, existing_embeddings  # Too similar, skip
    # Add new knowledge
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    existing_lines.append(new_text)
    existing_embeddings.append(new_emb)
    print("Added new knowledge:", new_text[:60], "...")
    # Save updated embeddings
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(existing_embeddings, f)
    return existing_lines, existing_embeddings

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

# --- Fetch Gutenberg text (first 5000 chars) ---
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
    existing_lines, existing_embeddings = load_existing_knowledge_and_embeddings()

    # Dynamic Wikipedia topics
    wikipedia_topics = [
        "Artificial_intelligence", "Machine_learning", "Python_(programming_language)",
        "Neural_network", "Reinforcement_learning", "Data_science",
        "Computer_vision", "Natural_language_processing"
    ]
    for topic in wikipedia_topics:
        text = fetch_wikipedia_intro(topic)
        if text:
            new_text = f"Topic: {topic}\nInfo: {text}"
            existing_lines, existing_embeddings = append_new_knowledge(new_text, existing_lines, existing_embeddings)

    # Gutenberg books
    gutenberg_books = {
        "Pride_and_Prejudice": "https://www.gutenberg.org/files/1342/1342-0.txt",
        "Frankenstein": "https://www.gutenberg.org/files/84/84-0.txt",
        "The_Adventures_of_Sherlock_Holmes": "https://www.gutenberg.org/files/1661/1661-0.txt"
    }
    for title, url in gutenberg_books.items():
        book_text = fetch_gutenberg_text(url)
        if book_text:
            new_text = f"Topic: {title}\nInfo: {book_text}"
            existing_lines, existing_embeddings = append_new_knowledge(new_text, existing_lines, existing_embeddings)

    print(f"Auto-learn complete. Total knowledge entries: {len(existing_lines)}")

if __name__ == "__main__":
    auto_learn()
