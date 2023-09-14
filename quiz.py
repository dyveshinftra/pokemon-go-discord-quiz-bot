# A quiz item is a quiz question plus the corresponding answer.


import abc
import random

import quiz_items


class Quiz(abc.ABC):
    def __init__(
        self,
        questions,
        super_eff: bool = True,
        not_very_eff: bool = True,
        dual: bool = True,
        weather: bool = True,
    ):
        self.remaining_questions = []
        for _ in range(questions):
            self.remaining_questions.append(
                random.choice(
                    quiz_items.get_quiz_item_classes(
                        super_eff=super_eff,
                        not_very_eff=not_very_eff,
                        dual=dual,
                        weather=weather,
                    )
                )()
            )
        self.questions = int(questions)
        self.score = 0

    def has_remaining_questions(self):
        return bool(self.remaining_questions)

    def ask_question(self):
        self.quiz_item = self.remaining_questions.pop()
        return self.quiz_item.ask_question()

    def answer(self, content):
        is_correct, s = self.quiz_item.answer(content)
        if is_correct:
            self.score += 1
        return s

    def show_score(self):
        return f"You scored {self.score} out of {self.questions}"
