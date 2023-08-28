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
    assert item.answer('') != 'That is correct!'


def test_item_solution_is_correct(item):
    assert item.answer(' '.join(item.get_solution())) == 'That is correct!'


def test_item_but_all_possible_solution_is_not_correct(item):
    answer = ' '.join(item.get_all_possible_solutions())
    assert item.answer(answer) != 'That is correct!'


def test_db_super_effective_attack():
    item = quiz_items.SuperEffectiveAttack('Water')
    assert item.get_solution() == ['Fire', 'Ground', 'Rock']


def test_db_super_effective_defense():
    item = quiz_items.SuperEffectiveDefense('Water')
    assert item.get_solution() == ['Electric', 'Grass']


def test_db_super_effective_defense_dual_type_ground_water():
    item = quiz_items.SuperEffectiveDefenseDualType('Ground and Water')
    assert item.get_solution() == ['Grass']


def test_db_correct_quiz_response_on_completely_wrong_answer():
    item = quiz_items.SuperEffectiveDefenseDualType('Ground and Water')
    assert item.answer('Poison') == (
        'Grass is super effective against Ground and Water.'
    )


def test_db_correct_quiz_response_on_forgotten_answer():
    item = quiz_items.SuperEffectiveDefenseDualType('Ground and Water')
    assert item.answer('') == 'You forgot Grass.'


def test_db_correct_quiz_response_on_wrong_answer():
    item = quiz_items.SuperEffectiveDefenseDualType('Ground and Water')
    assert item.answer('Poison Grass') == (
        'You answered Poison wrong.'
    )


def test_db_super_effective_defense_dual_type_fire_ground():
    item = quiz_items.SuperEffectiveDefenseDualType('Fire and Ground')
    assert item.get_solution() == ['Ground', 'Water']


def test_db_not_very_ineffective_attack():
    item = quiz_items.NotVeryEffectiveAttack('Water')
    assert item.get_solution() == ['Dragon', 'Grass', 'Water']


def test_db_not_very_effective_defense():
    item = quiz_items.NotVeryEffectiveDefense('Water')
    assert item.get_solution() == ['Fire', 'Ice', 'Steel', 'Water']


def test_db_not_very_effective_defense_dual_type_ground_water():
    item = quiz_items.NotVeryEffectiveDefenseDualType('Ground and Water')
    assert item.get_solution() == [
        'Electric', 'Fire', 'Poison', 'Rock', 'Steel'
    ]


def test_db_not_very_effective_defense_dual_type_fire_ground():
    item = quiz_items.NotVeryEffectiveDefenseDualType('Fire and Ground')
    assert item.get_solution() == [
        'Bug', 'Electric', 'Fairy', 'Fire', 'Poison', 'Steel'
    ]


def test_db_weather_boost():
    item = quiz_items.WeatherBoost('Clear')
    assert item.get_solution() == ['Grass', 'Ground', 'Fire']
