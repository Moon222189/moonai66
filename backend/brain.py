import os
import random
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class Brain:
    def __init__(self, knowledge_file="brainknowledge.txt"):
        self.knowledge_file = knowledge_file
        self.sentences = []
        self.embeddings = None
        self.index = None
        self.words_dict = defaultdict(list)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.load_knowledge()

    # --- Load knowledge and create embeddings ---
    def load_knowledge(self):
        if not os.path.exists(self.knowledge_file):
            raise FileNotFoundError(f"{self.knowledge_file} not found.")

        with open(self.knowledge_file, "r", encoding="utf-8") as f:
            text = f.read()
            # Split into sentences for embeddings
            self.sentences = [line.strip() for line in text.split("\n") if line.strip() != ""]

        # --- Create embeddings for semantic search ---
        self.embeddings = self.model.encode(self.sentences, convert_to_numpy=True)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        print(f"Loaded {len(self.sentences)} knowledge sentences.")

        # --- Build Markov chain for creative generation ---
        words = text.replace("\n", " ").split()
        for i in range(len(words) - 2):
            key = (words[i], words[i+1])
            self.words_dict[key].append(words[i+2])
        print(f"Markov chain created with {len(self.words_dict)} entries.")

    # --- Semantic search ---
    def search_relevant(self, message, top_k=3):
        vec = self.model.encode([message], convert_to_numpy=True)
        distances, indices = self.index.search(vec, top_k)
        results = [self.sentences[i] for i in indices[0]]
        return " ".join(results)

    # --- Generate creative sentence using Markov chain ---
    def generate_markov(self, seed_text, max_words=30):
        words = seed_text.split()
        if len(words) < 2:
            key = random.choice(list(self.words_dict.keys()))
        else:
            key = (words[-2], words[-1])
            if key not in self.words_dict:
                key = random.choice(list(self.words_dict.keys()))

        response = [key[0], key[1]]
        for _ in range(max_words - 2):
            next_words = self.words_dict.get(key)
            if not next_words:
                break
            next_word = random.choice(next_words)
            response.append(next_word)
            key = (key[1], next_word)
        return " ".join(response)

    # --- Main response method ---
    def generate_response(self, message):
        # 1. Find relevant knowledge
        relevant_text = self.search_relevant(message)
        # 2. Generate creative response based on that knowledge
        response = self.generate_markov(relevant_text)
        return response
