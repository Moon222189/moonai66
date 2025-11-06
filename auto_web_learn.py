import requests
from bs4 import BeautifulSoup
import re
import os
import pickle
from moonai_core.embeddings import create_embeddings, cosine_similarity  # updated import

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"
SIMILARITY_THRESHOLD = 0.8  # Only add knowledge if unique enough

# --- Helper: clean text ---
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)  # remove references like [1]
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

# --- Append new knowledge if unique ---
def append_new_knowledge(new_text, existing_lines, existing_embeddings, log_enabled=False):
    logs = []
    new_emb = create_embeddings([new_text])[0]
    for emb in existing_embeddings:
        if cosine_similarity(new_emb, emb) > SIMILARITY_THRESHOLD:
            return existing_lines, existing_embeddings, logs  # skip duplicate
    # Save knowledge
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    existing_lines.append(new_text)
    existing_embeddings.append(new_emb)
    msg = "Added knowledge: " + new_text[:60] + "..."
    if log_enabled:
        logs.append(msg)
    # Save embeddings
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(existing_embeddings, f)
    return existing_lines, existing_embeddings, logs

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
        text = response.text
        return clean_text(text[:5000])
    except Exception as e:
        print(f"Failed Gutenberg book: {e}")
        return ""

# --- Fetch dynamic Wikipedia topics ---
def fetch_dynamic_wiki_topics(categories=None, limit_per_category=10):
    if categories is None:
        categories = ["Artificial_intelligence", "Physics", "Mathematics", "Computer_science"]
    topics = []
    for category in categories:
        url = f"https://en.wikipedia.org/wiki/Category:{category}"
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            for li in soup.select(".mw-category li a"):
                topic_name = li.get("title")
                if topic_name:
                    topics.append(topic_name.replace(" ", "_"))
        except Exception as e:
            print(f"Failed to fetch dynamic topics from {category}: {e}")
    return topics[:limit_per_category * len(categories)]

# --- Fetch short news summaries ---
def fetch_news_summaries():
    url = "https://www.bbc.com/news/technology"
    summaries = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select("h3 a"):
            title = article.get_text()
            link = "https://www.bbc.com" + article.get("href", "")
            summaries.append(f"{title} ({link})")
    except Exception as e:
        print("Failed to fetch news:", e)
    return summaries[:5]

# --- Main auto-learn ---
def auto_learn(log_enabled=False):
    """
    Fetches new knowledge from Wikipedia, Gutenberg, and news,
    adds it to brainknowledge.txt if unique, and returns logs.
    """
    existing_lines, existing_embeddings = load_existing_knowledge_and_embeddings()
    logs = []

    # Wikipedia topics
    dynamic_topics = fetch_dynamic_wiki_topics()
    for topic in dynamic_topics:
        text = fetch_wikipedia_intro(topic)
        if text:
            new_text = f"Topic: {topic}\nInfo: {text}"
            existing_lines, existing_embeddings, new_logs = append_new_knowledge(
                new_text, existing_lines, existing_embeddings, log_enabled
            )
            logs.extend(new_logs)

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
            existing_lines, existing_embeddings, new_logs = append_new_knowledge(
                new_text, existing_lines, existing_embeddings, log_enabled
            )
            logs.extend(new_logs)

    # News summaries
    news_summaries = fetch_news_summaries()
    for summary in news_summaries:
        new_text = f"News: {summary}"
        existing_lines, existing_embeddings, new_logs = append_new_knowledge(
            new_text, existing_lines, existing_embeddings, log_enabled
        )
        logs.extend(new_logs)

    return logs if log_enabled else []
