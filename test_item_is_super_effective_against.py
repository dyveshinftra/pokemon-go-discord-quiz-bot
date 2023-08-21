import item_is_super_effective_against
import pogoapi
import pytest


@pytest.fixture
def item():
    return item_is_super_effective_against.IsSuperEffectiveAgainst()


# normal is not super effective against any type
def test_item_question_type_is_not_normal(item):
    assert item.qtype != 'Normal'


def test_item_question_type_exist(item):
    assert item.qtype in pogoapi.type_effectiveness.keys()


def test_item_answer_types_all_matches_all_types(item):
    assert item.atypes_all == list(pogoapi.type_effectiveness.keys())


def test_item_answer_types_correct_has_at_least_one_type(item):
    assert len(item.atypes_correct) > 0


def test_item_answer_types_correct_are_all_super_effective(item):
    effectiveness = pogoapi.type_effectiveness[item.qtype]
    for t in item.atypes_correct:
        assert effectiveness[t] == pogoapi.SUPER_EFFECTIVE


def test_item_question_is_well_formed(item):
    s = f'What is {item.qtype} super effective against?'
    assert item.question() == s
