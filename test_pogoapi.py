# test pogoapi.py


import pogoapi


def test_number_of_types():
    assert len(pogoapi.type_effectiveness.keys()) == 18
