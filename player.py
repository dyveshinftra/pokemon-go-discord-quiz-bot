import abc


class Player(abc.ABC):
    def __init__(
        self,
        name: str,
    ):
        self.current_streak = 0
        self.biggest_streak = 0
        self.score = 0
        self.questions = 0
        self.name = name

    def answer(self, was_right):
        self.questions += 1
        if was_right:
            self.score += 1
            self.current_streak += 1
            if self.current_streak > self.biggest_streak:
                self.biggest_streak = self.current_streak
        else:
            self.current_streak = 0

    def get_stats(self):
        biggest_streak = self.biggest_streak
        current_streak = self.current_streak
        return f"{self.name}\n{current_streak=}\n{biggest_streak=}\nScore = {self.score}/{self.questions}\n"


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
