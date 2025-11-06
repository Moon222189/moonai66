import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class Brain:
    def __init__(self, knowledge_folder="knowledge"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.knowledge_folder = knowledge_folder
        self.texts = []
        self.embeddings = None
        self.index = None
        self.load_knowledge()

    def load_knowledge(self):
        """Load text files and create embeddings."""
        self.texts = []
        for filename in os.listdir(self.knowledge_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.knowledge_folder, filename), "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    self.texts.extend([line for line in lines if line.strip() != ""])
        if self.texts:
            self.embeddings = self.model.encode(self.texts, convert_to_numpy=True)
            dim = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(self.embeddings)
            print(f"Loaded {len(self.texts)} knowledge entries.")

    def query(self, message, top_k=3):
        """Find closest knowledge and return as response."""
        vec = self.model.encode([message], convert_to_numpy=True)
        distances, indices = self.index.search(vec, top_k)
        responses = [self.texts[i] for i in indices[0]]
        return " ".join(responses)
