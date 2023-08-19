# test pokemon_types.py


import pokemon_types


def test_fire_is_valid_type():
    assert pokemon_types.is_valid('Fire')


def test_foo_is_invalid_type():
    assert not pokemon_types.is_valid('foo')


def test_number_of_valid_types_is_eighteen():
    assert len(pokemon_types.valid_types()) == 18


def test_fighting_is_super_effective_against_normal():
    assert 'Normal' in pokemon_types.super_effective('Fighting')


def test_fighting_is_not_very_effective_against_bug():
    assert 'Bug' in pokemon_types.not_very_effective('Fighting')
