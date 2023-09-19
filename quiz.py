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
        player.current_quiz_score
        self.players[name] = player
        player.current_quiz_score = 0

    def has_remaining_questions(self):
        return bool(self.remaining_questions)

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
        if len(self.players_answered) == len(self.players):
            self.players_answered = []
            return result.get_reply()
        else:
            return "We registered your answer, wait for the other players"

    def show_score(self):
        for player in self.players.values():
            return f"{player.name} scored {player.current_quiz_score} out of {self.questions}"
