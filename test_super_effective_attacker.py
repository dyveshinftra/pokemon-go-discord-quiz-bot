import super_effective_attacker
import pogoapi
import pytest


@pytest.fixture
def item():
    return super_effective_attacker.SuperEffectiveAttacker()


# normal is not super effective against any type
def test_item_question_type_is_not_normal(item):
    assert item.qtype != 'Normal'


def test_item_question_type_exist(item):
    assert item.qtype in pogoapi.type_effectiveness.keys()


def test_item_answer_types_all_matches_all_types(item):
    assert item.get_all_answer_words() == pogoapi.type_effectiveness.keys()


def test_item_answer_types_correct_has_at_least_one_type(item):
    assert len(item.atypes_correct) > 0


def test_item_answer_types_correct_are_all_super_effective(item):
    effectiveness = pogoapi.type_effectiveness[item.qtype]
    for t in item.atypes_correct:
        assert effectiveness[t] == pogoapi.SUPER_EFFECTIVE


def test_item_question_is_well_formed(item):
    assert item.qtype in item.question()


def test_item_correct_answer_contains_all_correct_types(item):
    correct_answer = item.correct_answer()
    for t in item.atypes_correct:
        assert t in correct_answer


def test_item_empty_answer_is_not_correct(item):
    assert not item.is_answer_correct('')


def test_item_answer_correct_with_correct_types(item):
    assert item.is_answer_correct(' '.join(item.atypes_correct))


def test_item_answer_all_types_is_not_correct(item):
    assert not item.is_answer_correct(' '.join(item.get_all_answer_words()))
