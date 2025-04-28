import json
import os

class Persistence:
    """Guarda preguntas y respuestas en un JSON para persistencia."""
    def __init__(self, path="questions.json"):
        self.path = path
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def has_answer(self, question: str) -> bool:
        return question in self.data

    def store(self, question: str, answer: str):
        self.data[question] = answer
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, question: str) -> str | None:
        return self.data.get(question)
