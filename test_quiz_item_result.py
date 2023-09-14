import pytest


from quiz_item_result import QuizItemResult


fire_water = ['Fire', 'Water']
fire_earth = ['Fire', 'Earth']


@pytest.fixture
def correct_result():
    return QuizItemResult(answer=fire_water, solution=fire_water)


@pytest.fixture
def incorrect_result():
    return QuizItemResult(answer=fire_water, solution=fire_earth)


def test_is_correct_when_result_is_correct(correct_result):
    assert correct_result.is_correct()


def test_is_incorrect_when_result_is_uncorrect(incorrect_result):
    assert not incorrect_result.is_correct()


def test_get_missing_when_result_is_correct(correct_result):
    assert correct_result.get_missing() == set()


def test_get_missing_when_result_is_incorrect(incorrect_result):
    assert incorrect_result.get_missing() == {'Earth'}


def test_get_wrong_when_result_is_correct(correct_result):
    assert not correct_result.get_wrong()


def test_get_wrong_when_result_is_incorrect(incorrect_result):
    assert incorrect_result.get_wrong() == {'Water'}
