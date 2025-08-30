import pytest

from rainduck.transpiler import transpile

bf_codes = ["", "<>+-,.", "+[<>>[[-+]],]..", "[[[]]]", "."]


@pytest.mark.parametrize("code", bf_codes)
def test_bf_to_bf(code):
    """Test if braifuck code traspiles to itself"""
    assert transpile(code) == code


def inversion(code: str):
    return "".join([{"+": "-", "-": "+", "<": ">", ">": "<"}.get(c, c) for c in code[::-1]])


@pytest.mark.parametrize(
    ("first", "rest", "num", "block"),
    [
        (",", "[,]", -3, False),
        ("[[++++]<<<]", "--", 5, False),
        ("[[,],>]", "", 0, False),
        ("<", "[,]", -1, False),
        ("+-.,<>", "+", -2, True),
        ("", "[[-]>]", 7, True),
    ],
)
def test_multiplication(first, rest, num, block):
    """Test if RainDuck multiplication works same as python int * str"""
    transpiled = transpile(str(num) + ("{" + first + "}" if block else first) + rest)
    if num >= 0:
        assert transpiled == num * first + rest
    else:
        assert transpiled == abs(num) * inversion(first) + rest
