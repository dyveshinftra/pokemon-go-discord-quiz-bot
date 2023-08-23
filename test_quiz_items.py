import pytest
import quiz_items


@pytest.fixture(params=quiz_items.get_all_quiz_item_classes())
def item(request):
    return request.param()


def test_item_has_at_least_one_solution(item):
    assert len(item.get_solution()) > 0


def test_item_question_is_well_formed(item):
    assert item.get_key() in item.ask_question()


def test_item_give_solution_is_well_formed(item):
    for solution in item.get_solution():
        assert solution in item.give_solution()


def test_item_empty_answer_is_not_correct(item):
    assert not item.is_answer_correct('')


def test_item_solution_is_correct(item):
    assert item.is_answer_correct(' '.join(item.get_solution()))


def test_item_but_all_possible_solution_is_not_correct(item):
    answer = ' '.join(item.get_all_possible_solutions())
    assert not item.is_answer_correct(answer)


def test_db_super_effective_attack():
    item = quiz_items.SuperEffectiveAttack('Water')
    assert item.get_solution() == ['Fire', 'Ground', 'Rock']


def test_db_super_effective_defense():
    item = quiz_items.SuperEffectiveDefense('Water')
    assert item.get_solution() == ['Electric', 'Grass']
