import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load knowledge
with open("data/brainknowledge.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(lines).toarray().astype('float32')

# FAISS index for semantic search
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Save embeddings
faiss.write_index(index, "embeddings/knowledge.index")
with open("embeddings/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
with open("embeddings/lines.pkl", "wb") as f:
    pickle.dump(lines, f)
