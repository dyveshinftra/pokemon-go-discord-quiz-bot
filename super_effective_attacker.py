# This quiz item checks what type(s) a type is super effective against.


import pogoapi
import random


class SuperEffectiveAttacker:

    def __init__(self):
        all_types = list(pogoapi.type_effectiveness.keys())

        # normal is not effective against any type
        qtype = all_types.copy()
        qtype.remove('Normal')
        self.qtype = random.choice(qtype)

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

    def is_answer_correct(self, answer):
        # split answer in words and capitalise like the types in
        # pogoapi and remove duplicates
        words = set(map(lambda w: w.capitalize(), answer.split()))

        # filter out all types
        words = words.intersection(self.get_all_answer_words())

        # filter out the correct types
        if len(words) == len(self.atypes_correct):
            words = words.intersection(self.atypes_correct)

        # make sure to have all the correct types
        return len(words) == len(self.atypes_correct)

    def get_all_answer_words(self):
        return pogoapi.type_effectiveness.keys()
