from pathlib import Path

from rainduck.code_elements import CodeBlock, Comment
from rainduck.errors import RainDuckSyntaxError
from rainduck.tokens import tokenize


def parse(code: str, file_path: Path | None = None) -> CodeBlock:
    tokens = tokenize("{" + code + "}")
    block = CodeBlock.take(tokens, file_path=file_path)
    if tokens:
        t = tokens[0]
        raise RainDuckSyntaxError(line_pos=t.line_pos, char_pos=t.char_pos)
    if block is None:
        raise RainDuckSyntaxError
    return block


def transpile(
    code: str,
    file_path: Path | None = None,
    comments: bool = True,
    optimize: bool = False,
) -> str:
    block = parse(code, file_path)
    bf = block.transpile()
    result = "".join(str(x) for x in bf if comments or not isinstance(x, Comment))
    if optimize:
        result = optimize_bf(result)
    return result


def optimize_bf(code: str) -> str:
    result: list[str] = []
    for char in code:
        if result and result[-1] == {">": "<", "<": ">", "+": "-", "-": "+"}.get(char):
            del result[-1]
            continue
        result += char
    return "".join(result)
