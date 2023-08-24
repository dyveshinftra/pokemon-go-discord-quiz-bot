# A quiz item is a quiz question plus the corresponding answer.


import abc
import pogoapi
import random


def get_all_quiz_item_classes():
    return QuizItem.__subclasses__()


class QuizItem(abc.ABC):

    # all quiz items for this class
    #   - key   the actual question (string)
    #   - value the correct answer  (list of words)
    db = {}

    def __init__(self, key=None):
        if not key:
            key = random.choice(list(self.db.keys()))
        self._key = key

    def get_key(self):
        return self._key

    def get_solution(self):
        return self.db[self._key]

    def is_answer_correct(self, answer):
        # split answer in words, capitalize them, and remove duplicates
        words = set(map(lambda w: w.capitalize(), answer.split()))

        # filter out all possible solutions
        words = words.intersection(self.get_all_possible_solutions())

        # filter out the solution
        if len(words) == len(self.get_solution()):
            words = words.intersection(self.get_solution())

        # make sure to have the full solution
        return len(words) == len(self.get_solution())

    @abc.abstractmethod
    def ask_question(self): pass

    @abc.abstractmethod
    def give_solution(self): pass

    @abc.abstractmethod
    def get_all_possible_solutions(self): pass


class SuperEffectiveAttack(QuizItem):

    # build quiz items
    db = {}
    for attack_type, attack_type_data in pogoapi.type_effectiveness.items():
        for defense_type, effectiveness in attack_type_data.items():
            if effectiveness == pogoapi.SUPER_EFFECTIVE:
                db.setdefault(attack_type, []).append(defense_type)

    def ask_question(self):
        return f'What is {self._key} super effective against?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{self._key} is super effective against {solution}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()


class SuperEffectiveDefense(QuizItem):

    # build quiz items
    db = {}
    for attack_type, attack_type_data in pogoapi.type_effectiveness.items():
        for defense_type, effectiveness in attack_type_data.items():
            if effectiveness == pogoapi.SUPER_EFFECTIVE:
                db.setdefault(defense_type, []).append(attack_type)

    def ask_question(self):
        return f'What is super effective against {self._key}?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{solution} is super effective against {self._key}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()


class WeatherBoost(QuizItem):

    # build quiz_items
    db = pogoapi.weather_boosts

    def ask_question(self):
        return f'What is boosted by {self._key} weather?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{self._key} boosts {solution}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()
