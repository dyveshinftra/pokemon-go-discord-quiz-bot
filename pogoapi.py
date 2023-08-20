# make data from https://pogoapi.net available


import json


type_effectiveness = json.load(open('type_effectiveness.json'))

# type effectiveness multiplier aliases
SUPER_EFFECTIVE = 1.6
NORMAL = 1.0
NOT_VERY_EFFECTIVE = 0.625
INEFFECTIVE = 0.390625
