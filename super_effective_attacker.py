# This quiz item checks what type(s) a type is super effective against.


import pogoapi
import random


data = {}
for attack_type, d in pogoapi.type_effectiveness.items():
    for defend_type, v in d.items():
        if v == pogoapi.SUPER_EFFECTIVE:
            data[attack_type] = data.get(attack_type, []) + [defend_type]


class SuperEffectiveAttacker:

    def __init__(self):
        self.data_key = random.choice(list(data.keys()))

    def ask_question(self):
        return f'What is {self.data_key} super effective against?'

    def get_correct_answer(self):
        correct_words = ', '.join(self.get_correct_answer_words())
        return f'{self.data_key} is super effective against {correct_words}.'

    def is_answer_correct(self, answer):
        # split answer in words and capitalise like the types in
        # pogoapi and remove duplicates
        words = set(map(lambda w: w.capitalize(), answer.split()))

        # filter out all types
        words = words.intersection(self.get_all_answer_words())

        # filter out the correct types
        if len(words) == len(self.get_correct_answer_words()):
            words = words.intersection(self.get_correct_answer_words())

        # make sure to have all the correct types
        return len(words) == len(self.get_correct_answer_words())

    def get_all_answer_words(self):
        return pogoapi.type_effectiveness.keys()

    def get_correct_answer_words(self):
        return data[self.data_key]

    def get_data(self):
        return self.data_key
