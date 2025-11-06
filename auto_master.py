import requests
from bs4 import BeautifulSoup
import re
import os
import pickle
import hashlib
import math
from datetime import datetime

# ----- CONFIG -----
KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"
LOGS_DIR = "logs"
SIMILARITY_THRESHOLD = 0.8

# ----- UTILITY FUNCTIONS -----
def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def create_embeddings(lines):
    embeddings = []
    for line in lines:
        h = hashlib.sha256(line.encode()).hexdigest()
        vec = [int(h[i:i+2],16)/255 for i in range(0, 64, 2)]
        embeddings.append(vec)
    return embeddings

def cosine_similarity(vec1, vec2):
    dot = sum(a*b for a,b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a*a for a in vec1))
    norm2 = math.sqrt(sum(b*b for b in vec2))
    return dot / (norm1*norm2 + 1e-10)

# ----- LOAD / SAVE -----
def load_existing_knowledge():
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

def append_new_knowledge(text, existing_lines, existing_embeddings, log_enabled=False):
    logs = []
    new_emb = create_embeddings([text])[0]
    for emb in existing_embeddings:
        if cosine_similarity(new_emb, emb) > SIMILARITY_THRESHOLD:
            return existing_lines, existing_embeddings, logs
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n\n")
    existing_lines.append(text)
    existing_embeddings.append(new_emb)
    msg = "Added knowledge: " + text[:60] + "..."
    if log_enabled:
        logs.append(msg)
    os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(existing_embeddings, f)
    return existing_lines, existing_embeddings, logs

# ----- DATA SOURCES -----
def fetch_wikipedia_intro(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return clean_text(data.get("extract",""))
    except:
        return ""

def fetch_wiki_topics(categories=None, limit_per_category=10):
    if categories is None:
        categories = ["Artificial_intelligence","Physics","Mathematics","Computer_science"]
    topics = []
    for cat in categories:
        url = f"https://en.wikipedia.org/wiki/Category:{cat}"
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text,"html.parser")
            for li in soup.select(".mw-category li a"):
                t = li.get("title")
                if t:
                    topics.append(t.replace(" ","_"))
        except:
            continue
    return topics[:limit_per_category*len(categories)]

def fetch_news_summaries():
    url = "https://www.bbc.com/news/technology"
    summaries = []
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text,"html.parser")
        for article in soup.select("h3 a"):
            title = article.get_text()
            link = "https://www.bbc.com" + article.get("href","")
            summaries.append(f"{title} ({link})")
    except:
        pass
    return summaries[:5]

# ----- AUTO LEARN -----
def auto_learn(log_enabled=False):
    existing_lines, existing_embeddings = load_existing_knowledge()
    logs = []

    # Wikipedia topics
    for topic in fetch_wiki_topics():
        text = fetch_wikipedia_intro(topic)
        if text:
            new_text = f"Topic: {topic}\nInfo: {text}"
            existing_lines, existing_embeddings, new_logs = append_new_knowledge(new_text, existing_lines, existing_embeddings, log_enabled)
            logs.extend(new_logs)

    # News summaries
    for summary in fetch_news_summaries():
        new_text = f"News: {summary}"
        existing_lines, existing_embeddings, new_logs = append_new_knowledge(new_text, existing_lines, existing_embeddings, log_enabled)
        logs.extend(new_logs)

    return logs if log_enabled else []

# ----- MAIN -----
def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    logs = auto_learn(log_enabled=True)
    print(f"[MoonAI] Total entries added: {len(logs)}")
    for log in logs:
        print(log)
    if logs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logfile = os.path.join(LOGS_DIR, f"moonai_log_{timestamp}.txt")
        with open(logfile,"w",encoding="utf-8") as f:
            for log in logs:
                f.write(log + "\n")
        print(f"[MoonAI] Logs saved to {logfile}")

if __name__ == "__main__":
    main()
