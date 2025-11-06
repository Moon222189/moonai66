import random

class MoonAI:
    def __init__(self):
        self.greetings = ["Hello!", "Hi there!", "Hey!"]
        self.farewells = ["Goodbye!", "See you later!", "Bye!"]
        self.default_responses = [
            "Interesting… tell me more!",
            "I see.",
            "Can you elaborate?",
            "Hmm…"
        ]

    def get_response(self, message):
        msg = message.lower()
        if any(word in msg for word in ["hi", "hello", "hey"]):
            return random.choice(self.greetings)
        elif any(word in msg for word in ["bye", "goodbye", "see you"]):
            return random.choice(self.farewells)
        else:
            return random.choice(self.default_responses)
