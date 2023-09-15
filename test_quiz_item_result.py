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


def test_correct_result_reply(correct_result):
    assert correct_result.get_reply() == 'That is correct!'


def test_wrong_and_missing_give_full_solution_reply(incorrect_result):
    replies = [
            'The correct solution is Fire, Earth',
            'The correct solution is Earth, Fire']
    assert incorrect_result.get_reply() in replies


def test_only_wrong_give_wrong_reply():
    result = QuizItemResult(answer=['Fire', 'Foo', 'Bar'], solution=['Fire'])
    replies = [
            'You answered Foo, Bar wrong.',
            'You answered Bar, Foo wrong.']
    assert result.get_reply() in replies


def test_only_missing_give_missing_reply():
    result = QuizItemResult(answer=['Fire'], solution=['Fire', 'Foo', 'Bar'])
    replies = [
            'You forgot Foo, Bar.',
            'You forgot Bar, Foo.']
    assert result.get_reply() in replies
