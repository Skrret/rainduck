import pytest

from rainduck.code_elements import (
    BrainFuckLoop,
    BrainFuckOperation,
    Multiplication,
    code_elements,
)
from rainduck.tokens import tokenize


@pytest.mark.parametrize(
    ("code", "element", "rest"),
    [
        (">[,>]", BrainFuckOperation, "[,>]"),
        ("[.><]]}", BrainFuckLoop, "]}"),
        ("-31[9<+]5[,]", Multiplication, "5[,]"),
    ],
)
def test_take(code, element, rest):
    """Test if code element classes takes elements correctly
    and element classes with higher precedence don't take it
    """
    tokenized = tokenize(code)
    tokenized2 = list(tokenized)
    assert isinstance(element.take(tokenized), element)
    assert len(tokenized) == len(rest)  # There should be better option
    for elem in code_elements:
        if elem is element:
            break
        tokenized3 = list(tokenized2)
        assert elem.take(tokenized3) is None
        assert tokenized2 == tokenized3
