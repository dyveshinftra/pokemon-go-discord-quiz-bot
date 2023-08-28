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

    def give_answered_correct(self):
        return 'That is correct!'

    def give_answered_wrong_answers(self, wrong_answers):
        if not wrong_answers:
            return ''
        solution = ', '.join(wrong_answers)
        return f'You answered {solution} wrong.'

    def give_answered_forgotten_answers(self, forgotten_answers):
        if not forgotten_answers:
            return ''
        solution = ', '.join(forgotten_answers)
        return f'You forgot {solution}.'

    def answer(self, answer):
        # split answer in words, capitalize them, and remove duplicates
        words = set(map(lambda w: w.capitalize(), answer.split()))

        # filter out all possible solutions
        words = words.intersection(self.get_all_possible_solutions())
        forgotten_answers = set(self.get_solution())
        forgotten_answers.difference_update(words)
        wrong_answers = words
        wrong_answers.difference_update(self.get_solution())

        # make sure to have the full solution
        if not forgotten_answers and not wrong_answers:
            return self.give_answered_correct()
        elif not forgotten_answers:
            return self.give_answered_wrong_answers(wrong_answers)
        elif not wrong_answers:
            return self.give_answered_forgotten_answers(forgotten_answers)
        else:
            return self.give_solution()

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


class SuperEffectiveDefenseDualType(QuizItem):

    # build quiz items
    db = {}
    for atype, attack_type_data in pogoapi.type_effectiveness.items():
        for dtype1, effectiveness1 in attack_type_data.items():
            for dtype2, effectiveness2 in attack_type_data.items():
                if dtype1 == dtype2:
                    continue
                if f'{dtype2} and {dtype1}' in db:
                    continue
                if effectiveness1 * effectiveness2 >= pogoapi.SUPER_EFFECTIVE:
                    db.setdefault(f'{dtype1} and {dtype2}', []).append(atype)

    def ask_question(self):
        return f'What is super effective against {self._key}?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{solution} is super effective against {self._key}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()


class NotVeryEffectiveAttack(QuizItem):

    # build quiz items
    db = {}
    for attack_type, attack_type_data in pogoapi.type_effectiveness.items():
        for defense_type, effectiveness in attack_type_data.items():
            if effectiveness <= pogoapi.NOT_VERY_EFFECTIVE:
                db.setdefault(attack_type, []).append(defense_type)

    def ask_question(self):
        return f'What is {self._key} not very effective against?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{self._key} is not very effective against {solution}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()


class NotVeryEffectiveDefense(QuizItem):

    # build quiz items
    db = {}
    for attack_type, attack_type_data in pogoapi.type_effectiveness.items():
        for defense_type, effectiveness in attack_type_data.items():
            if effectiveness <= pogoapi.NOT_VERY_EFFECTIVE:
                db.setdefault(defense_type, []).append(attack_type)

    def ask_question(self):
        return f'What is not very effective against {self._key}?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{solution} is not very effective against {self._key}.'

    def get_all_possible_solutions(self):
        return pogoapi.type_effectiveness.keys()


class NotVeryEffectiveDefenseDualType(QuizItem):

    # build quiz items
    db = {}
    for atype, attack_type_data in pogoapi.type_effectiveness.items():
        for dtype1, eff1 in attack_type_data.items():
            for dtype2, eff2 in attack_type_data.items():
                if dtype1 == dtype2:
                    continue
                if f'{dtype2} and {dtype1}' in db:
                    continue
                if eff1 * eff2 <= pogoapi.NOT_VERY_EFFECTIVE:
                    db.setdefault(f'{dtype1} and {dtype2}', []).append(atype)

    def ask_question(self):
        return f'What is not very effective against {self._key}?'

    def give_solution(self):
        solution = ', '.join(self.get_solution())
        return f'{solution} is not very effective against {self._key}.'

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
