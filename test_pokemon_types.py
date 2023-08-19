# test pokemon_types.py


import pokemon_types


# fire is a valid type!
def test_fire_is_valid():
    assert pokemon_types.is_valid('fire')


# foo is not a valid type :-(
def test_foo_is_invalid():
    assert not pokemon_types.is_valid('foo')


# there are 18 Pokémon types
def test_number_of_valid_types():
    assert len(pokemon_types.valid_types()) == 18
