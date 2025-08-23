from rainduck.code_elements import parse_list
from rainduck.tokens import tokenize


def transpile(code: str) -> str:
    return "".join(
        "".join(str(y) for y in x.transpile()) for x in parse_list(tokenize(code))
    )
