import abc
import random

import quiz_items
from player import Player, get_player


class Quiz(abc.ABC):
    def __init__(
        self,
        questions,
        super_eff: int,
        not_very_eff: int,
        weather: bool,
        player_name,
    ):
        self.remaining_questions = []
        self.is_finished = False
        self.quiz_item = None
        classes = quiz_items.get_quiz_item_classes(
            super_eff=super_eff,
            not_very_eff=not_very_eff,
            weather=weather,
        )
        for _ in range(questions):
            self.remaining_questions.append(random.choice(classes)())
        self.questions = int(questions)
        self.players_answered: list[Player] = []
        self.players: dict[str, Player] = {}
        self.join(player_name)

    def join(self, name):
        player = get_player(name)
        self.players[name] = player
        player.current_quiz_score = 0
        player.current_quiz_questions = self.get_unanswered_questions()

    def has_remaining_questions(self):
        return bool(self.remaining_questions)

    def get_unanswered_questions(self):
        if self.quiz_item:
            return len(self.remaining_questions) + 1
        else:
            return len(self.remaining_questions)

    def ask_question(self):
        self.quiz_item = self.remaining_questions.pop()
        return self.quiz_item.ask_question()

    def answer(self, player_name: str, content: str):
        result = self.quiz_item.verify_answer(content)
        player = self.players.get(player_name)
        if not player:
            return "You are not joined in the quiz, to join type /join"
        if player in self.players_answered:
            return "You have already answered this question, wait for the other players"
        player.answer(result.is_correct())
        self.players_answered.append(player)
        if len(self.players_answered) != len(self.players):
            return "We registered your answer, wait for the other players"

        # All players have answered, ask next question
        self.players_answered = []
        s = f"{result.get_reply()}\n"
        if self.has_remaining_questions():
            s += self.ask_question()
        else:
            s += self.show_score()
            self.is_finished = True
        return s

    def show_score(self):
        s = ""
        for player in self.players.values():
            s += (
                f"{player.name} scored {player.current_quiz_score}"
                f" out of {player.current_quiz_questions}\n"
            )
        return s
