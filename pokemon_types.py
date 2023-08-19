# Pokemon types


import json


_type_effectiveness = json.load(open('type_effectiveness.json'))


def is_valid(pokemon_type):
    return pokemon_type in _type_effectiveness


def valid_types():
    return _type_effectiveness.keys()


def super_effective(pokemon_type):
    return [key
            for key, value in _type_effectiveness[pokemon_type].items()
            if value > 1.0]


def not_very_effective(pokemon_type):
    return [key
            for key, value in _type_effectiveness[pokemon_type].items()
            if value < 1.0]
