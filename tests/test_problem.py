from statelint.problem.problem import Problem


def test_repr():
    problem = Problem("description")
    assert repr(problem) == "Problem(description, unknown)"
