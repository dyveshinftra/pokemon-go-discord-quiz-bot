import pytest


from type import Type


@pytest.fixture
def fire():
    return Type('Fire')


def test_fire_string(fire):
    assert str(fire) == 'Fire'


def test_fire_repr(fire):
    assert eval(repr(fire)) == fire


def test_fire_equals_fire(fire):
    assert fire == Type('Fire')


def test_fire_equals_fire_case_insensitive(fire):
    assert fire == Type('FIRE')


def test_fire_equals_string(fire):
    assert fire == 'fire'


def test_fire_super_effective(fire):
    assert fire.super_effective() == ['bug', 'grass', 'ice', 'steel']


def test_fire_is_super_effective_against_bug(fire):
    assert 'bug' in fire.super_effective()


def test_fire_normal(fire):
    assert fire.normal() == [
            'dark', 'electric', 'fairy', 'fighting', 'flying', 'ghost',
            'ground', 'normal', 'poison', 'psychic']


def test_fire_not_very_effective(fire):
    assert fire.not_very_effective() == ['dragon', 'fire', 'rock', 'water']


def test_fire_ineffective(fire):
    assert fire.ineffective() == []


def test_ghost_ineffective():
    assert Type('Ghost').ineffective() == ['normal']
