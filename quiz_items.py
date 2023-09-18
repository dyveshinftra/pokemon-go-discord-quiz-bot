# A quiz item is a quiz question plus the corresponding answer.


import abc
import random

import pogoapi
from quiz_item_result import QuizItemResult


def get_all_quiz_item_classes():
    return QuizItem.__subclasses__()


def get_quiz_item_classes(
    super_eff: int,
    not_very_eff: int,
    weather: bool = True,
):
    classes = []
    if super_eff in [1, 3]:
        classes.append(SuperEffectiveAttack)
        classes.append(SuperEffectiveDefense)
    if super_eff in [2, 3]:
        classes.append(SuperEffectiveDefenseDualType)
    if not_very_eff in [1, 3]:
        classes.append(NotVeryEffectiveAttack)
        classes.append(NotVeryEffectiveDefense)
    if not_very_eff in [2, 3]:
        classes.append(NotVeryEffectiveDefenseDualType)
    if weather:
        classes.append(WeatherBoost)

    return classes


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

    def verify_answer(self, answer):
        # split answer in words, capitalize them, and remove duplicates
        words = set(map(lambda w: w.capitalize(), answer.split()))

        # filter out all possible solutions
        words = words.intersection(self.get_all_possible_solutions())

        return QuizItemResult(answer=words, solution=self.get_solution())

    @abc.abstractmethod
    def ask_question(self):
        pass

    @abc.abstractmethod
    def get_all_possible_solutions(self):
        pass


class SuperEffectiveAttack(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype, effectiveness in atype_data.items():
            if effectiveness == pogoapi.SUPER_EFFECTIVE:
                db.setdefault(atype, []).append(dtype)

    def ask_question(self):
        return f"What is {self._key} super effective against?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class SuperEffectiveDefense(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype, effectiveness in atype_data.items():
            if effectiveness == pogoapi.SUPER_EFFECTIVE:
                db.setdefault(dtype, []).append(atype)

    def ask_question(self):
        return f"What is super effective against {self._key}?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class SuperEffectiveDefenseDualType(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype1, effectiveness1 in atype_data.items():
            for dtype2, effectiveness2 in atype_data.items():
                if dtype1 == dtype2:
                    continue
                if f"{dtype2} and {dtype1}" in db:
                    continue
                if effectiveness1 * effectiveness2 >= pogoapi.SUPER_EFFECTIVE:
                    db.setdefault(f"{dtype1} and {dtype2}", []).append(atype)

    def ask_question(self):
        return f"What is super effective against {self._key}?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class NotVeryEffectiveAttack(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype, effectiveness in atype_data.items():
            if effectiveness <= pogoapi.NOT_VERY_EFFECTIVE:
                db.setdefault(atype, []).append(dtype)

    def ask_question(self):
        return f"What is {self._key} not very effective against?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class NotVeryEffectiveDefense(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype, effectiveness in atype_data.items():
            if effectiveness <= pogoapi.NOT_VERY_EFFECTIVE:
                db.setdefault(dtype, []).append(atype)

    def ask_question(self):
        return f"What is not very effective against {self._key}?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class NotVeryEffectiveDefenseDualType(QuizItem):
    # build quiz items
    db = {}
    for atype, atype_data in pogoapi.get_type_effectiveness().items():
        for dtype1, eff1 in atype_data.items():
            for dtype2, eff2 in atype_data.items():
                if dtype1 == dtype2:
                    continue
                if f"{dtype2} and {dtype1}" in db:
                    continue
                if eff1 * eff2 <= pogoapi.NOT_VERY_EFFECTIVE:
                    db.setdefault(f"{dtype1} and {dtype2}", []).append(atype)

    def ask_question(self):
        return f"What is not very effective against {self._key}?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()


class WeatherBoost(QuizItem):
    # build quiz_items
    db = pogoapi.weather_boosts

    def ask_question(self):
        return f"What is boosted by {self._key} weather?"

    def get_all_possible_solutions(self):
        return pogoapi.get_type_effectiveness().keys()
