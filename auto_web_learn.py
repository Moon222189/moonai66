# auto_web_learn.py

import requests
from bs4 import BeautifulSoup
import re
import os
import pickle
from embeddings import create_embeddings, cosine_similarity

KNOWLEDGE_FILE = "data/brainknowledge.txt"
EMBEDDINGS_FILE = "embeddings/lines.pkl"
SIMILARITY_THRESHOLD = 0.8

def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

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

def append_new_knowledge(new_text, existing_lines, existing_embeddings, log_enabled=False):
    logs = []
    new_emb = create_embeddings([new_text])[0]
    for emb in existing_embeddings:
        if cosine_similarity(new_emb, emb) > SIMILARITY_THRESHOLD:
            return existing_lines, existing_embeddings, logs
    os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    existing_lines.append(new_text)
    existing_embeddings.append(new_emb)
    msg = "Added knowledge: " + new_text[:60] + "..."
    if log_enabled:
        logs.append(msg)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(existing_embeddings, f)
    return existing_lines, existing_embeddings, logs

def fetch_wikipedia_intro(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return clean_text(data.get("extract", ""))
    except:
        return ""

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
        except:
            continue
    return topics[:limit_per_category * len(categories)]

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
    except:
        pass
    return summaries[:5]

def auto_learn(log_enabled=False):
    existing_lines, existing_embeddings = load_existing_knowledge_and_embeddings()
    logs = []

    # Wikipedia topics
    for topic in fetch_dynamic_wiki_topics():
        text = fetch_wikipedia_intro(topic)
        if text:
            new_text = f"Topic: {topic}\nInfo: {text}"
            existing_lines, existing_embeddings, new_logs = append_new_knowledge(
                new_text, existing_lines, existing_embeddings, log_enabled
            )
            logs.extend(new_logs)

    # News summaries
    for summary in fetch_news_summaries():
        new_text = f"News: {summary}"
        existing_lines, existing_embeddings, new_logs = append_new_knowledge(
            new_text, existing_lines, existing_embeddings, log_enabled
        )
        logs.extend(new_logs)

    return logs if log_enabled else []
