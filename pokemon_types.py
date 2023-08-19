# Pokemon types


import json


_type_effectiveness = json.load(open('type_effectiveness.json'))


def is_valid(pokemon_type):
    return pokemon_type.capitalize() in _type_effectiveness


def valid_types():
    return _type_effectiveness.keys()
