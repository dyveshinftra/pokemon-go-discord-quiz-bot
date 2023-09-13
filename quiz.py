# A quiz item is a quiz question plus the corresponding answer.


import abc
import random

import quiz_items


class Quiz(abc.ABC):
    def __init__(self, remaining_questions):
        self.remaining_questions = int(remaining_questions)
        self.questions = int(remaining_questions)
        self.score = 0

    def has_remaining_questions(self):
        return self.remaining_questions > 0

    def ask_question(self):
        self.quiz_item = random.choice(quiz_items.get_all_quiz_item_classes())()
        return self.quiz_item.ask_question()

    def answer(self, content):
        self.remaining_questions -= 1
        is_correct, s = self.quiz_item.answer(content)
        if is_correct:
            self.score += 1
        return s

    def show_score(self):
        return f"You scored {self.score} out of {self.questions}"
