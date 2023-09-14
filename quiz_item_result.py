"""
The result of a quiz item, when an answer is given by a player to a
certain question.
"""


class QuizItemResult():

    def __init__(self, answer, solution):
        """
        Store the answer, given by the player, together with the
        expected solution from the quiz item.
        """
        self._answer = set(answer)
        self._solution = set(solution)

    def is_correct(self):
        """
        Check if the answer is correct.
        """
        return self._answer == self._solution

    def get_missing(self):
        """
        Return what the answer is missing to be correct.
        """
        return self._solution - self._answer

    def get_wrong(self):
        """
        Return what the answer got wrong, e.g. not part of the solution.
        """
        return self._answer - self._solution
