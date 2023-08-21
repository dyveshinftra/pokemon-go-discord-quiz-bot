# This quiz item checks what type(s) a type is super effective against.


import pogoapi
import random


class IsSuperEffectiveAgainst:

    def __init__(self):
        all_types = list(pogoapi.type_effectiveness.keys())

        # normal is not effective against any type
        qtype = all_types.copy()
        qtype.remove('Normal')
        self.qtype = random.choice(qtype)

        # all types are possible answers
        self.atypes_all = all_types

        # but these are the correct answers
        self.atypes_correct = [
                k
                for k, v in pogoapi.type_effectiveness[self.qtype].items()
                if v == pogoapi.SUPER_EFFECTIVE]

    def question(self):
        return f'What is {self.qtype} super effective against?'

    def correct_answer(self):
        atypes_correct_str = ', '.join(self.atypes_correct)
        return f'{self.qtype} is super effective against {atypes_correct_str}.'
