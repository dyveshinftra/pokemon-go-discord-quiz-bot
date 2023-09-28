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
        self.players_answered_correctly: list[str] = []
        self.players_answered_falsly: list[str] = []
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

    def show_answers_multiple_players(self):
        # All players have answered, ask next question
        s = ""
        if self.players_answered_correctly:
            names = ",".join(self.players_answered_correctly)
            s += f"{names} answered correctly\n"
        if self.players_answered_falsly:
            names = ",".join(self.players_answered_falsly)
            s += f"{names} answered incorrectly\n"
            s += f"{self.quiz_item.get_readible_solution()}\n"
        return s

    def show_next_question(self):
        if self.has_remaining_questions():
            return self.ask_question()
        else:
            self.is_finished = True
            return self.show_score()

    def answer(self, player_name: str, content: str):
        if not self.quiz_item:
            return ""
        result = self.quiz_item.verify_answer(content)
        player = self.players.get(player_name)
        if not player:
            return "You are not joined in the quiz, to join type /join"
        if player in [
            self.players_answered_correctly,
            self.players_answered_falsly,
        ]:
            return "You have already answered this question, "
            "wait for the other players"
        is_correct = result.is_correct()
        player.answer(is_correct)
        if is_correct:
            self.players_answered_correctly.append(player_name)
        else:
            self.players_answered_falsly.append(player_name)
        if len(self.players_answered_correctly) + len(
            self.players_answered_falsly
        ) != len(self.players):
            return "We registered your answer, wait for the other players"

        if len(self.players) > 1:
            s = self.show_answers_multiple_players()
        else:
            s = result.get_reply() + "\n"
        s += self.show_next_question()
        self.players_answered_correctly = []
        self.players_answered_falsly = []
        return s

    def show_score(self):
        s = ""
        for player in self.players.values():
            s += (
                f"{player.name} scored {player.current_quiz_score}"
                f" out of {player.current_quiz_questions}\n"
            )
        return s
