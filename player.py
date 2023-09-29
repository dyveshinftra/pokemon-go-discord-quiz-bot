import abc
from decimal import Decimal


class Player(abc.ABC):
    def __init__(
        self,
        name: str,
    ):
        self.current_streak = 0
        self.biggest_streak = 0
        self.score = 0
        self.questions = 0
        self.current_quiz_score = 0
        self.current_quiz_questions = 0
        self.name = name
        self.score_per_question: dict[str, tuple] = {}

    def answer(self, question: str, was_right: bool):
        if question not in self.score_per_question:
            self.score_per_question[question] = (0, 0)
        correct, questions = self.score_per_question[question]
        questions += 1
        self.questions += 1
        if was_right:
            correct += 1
            self.score += 1
            self.current_quiz_score += 1
            self.current_streak += 1
            if self.current_streak > self.biggest_streak:
                self.biggest_streak = self.current_streak
        else:
            self.current_streak = 0
        self.score_per_question[question] = (correct, questions)

    def get_stats(self):
        biggest_streak = self.biggest_streak
        current_streak = self.current_streak
        return f"""{self.name}
{current_streak=}
{biggest_streak=}
Score = {self.score}/{self.questions}"""

    def get_best_questions(self, amount=5):
        sorted_questions = sorted(
            self.score_per_question.items(),
            key=lambda x: Decimal(x[1][0] + 1) / Decimal(x[1][1] + 2),
        )
        s = "You scored the best in following questions\n"
        for item in sorted_questions[-amount:]:
            s += f"{item[0]} ({item[1][0]}/{item[1][1]})"
        return s

    def get_worst_questions(self, amount=5):
        sorted_questions = sorted(
            self.score_per_question.items(),
            key=lambda x: Decimal(x[1][0] + 1) / Decimal(x[1][1] + 2),
        )
        s = "You scored the worst in following questions\n"
        for item in sorted_questions[:amount]:
            s += f"{item[0]} ({item[1][0]}/{item[1][1]})\n"
        return s

    def get_detail(self):
        s = ""
        s += self.get_best_questions() + "\n\n"
        s += self.get_worst_questions()
        return s


players: dict[str, Player] = {}


def get_player(name: str) -> Player:
    global players
    if name not in players:
        players[name] = Player(name)
    return players[name]


def get_all_player_stats():
    s: str = ""
    for player in players.values():
        s += player.get_stats() + "\n"
    return s


def get_current_player_stats(name: str):
    return get_player(name).get_stats()


def get_all_player_detail():
    s: str = ""
    for player in players.values():
        s += player.get_detail()
    return s


def get_current_player_detail(name: str):
    return get_player(name).get_detail()
