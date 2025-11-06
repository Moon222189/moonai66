import os
import random
from collections import defaultdict

class Brain:
    def __init__(self, knowledge_file="brainknowledge.txt"):
        self.knowledge_file = knowledge_file
        self.words_dict = defaultdict(list)
        self.load_knowledge()

    def load_knowledge(self):
        """Read knowledge file and build Markov chain."""
        if not os.path.exists(self.knowledge_file):
            raise FileNotFoundError(f"{self.knowledge_file} not found.")
        
        with open(self.knowledge_file, "r", encoding="utf-8") as f:
            text = f.read().replace("\n", " ")
        words = text.split()
        
        # Build a simple 2-word Markov chain
        for i in range(len(words) - 2):
            key = (words[i], words[i+1])
            self.words_dict[key].append(words[i+2])
        print(f"Brain loaded with {len(words)} words.")

    def generate_response(self, message, max_words=30):
        """Generate a sentence based on the Markov chain."""
        words = message.split()
        if len(words) < 2:
            # pick random starting point
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
