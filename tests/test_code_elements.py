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
    assert tokenized == rest
    for elem in code_elements:
        if elem is element:
            break
        assert elem.take(list(tokenized2)) is None
