from abc import ABCMeta, abstractmethod
from typing import Any, Self

from rainduck.errors import RainDuckSyntaxError
from rainduck.tokens import Char, Number, Token


class _CodeElementMeta(ABCMeta):

    precedence: float = 0
    assign_to_list: bool

    def __init__(cls, name: str, bases: tuple[type], namespace: dict[str, Any]) -> None:
        super().__init__(name, bases, namespace)
        if namespace.get("assign_to_list", True):
            for i in range(len(code_elements)):
                if code_elements[i].precedence >= cls.precedence:
                    code_elements.insert(i, cls)
                    break
            else:
                code_elements.append(cls)

    def take(cls, code: list[Token]) -> "CodeElement | None":
        pass


code_elements: list[_CodeElementMeta] = []


class CodeElement(metaclass=_CodeElementMeta):

    assign_to_list = False

    @abstractmethod
    def transpile(self, inverse: bool = False) -> list["BrainFuck"]:
        pass


class BrainFuck(CodeElement):
    assign_to_list = False


class BrainFuckOperation(BrainFuck):

    precedence = 10
    code: str

    def __init__(self, code: str) -> None:
        self.code = code

    @classmethod
    def take(cls, code: list[Token]) -> Self | None:
        fst = code.pop(0)
        match fst:
            case Char(c) if c in "<>+-,.":
                return cls(c)
        return None

    def transpile(self, inverse: bool = False) -> list["BrainFuck"]:
        return super().transpile(inverse)


class BrainFuckLoop(BrainFuck):

    precedence = 10
    code: list[CodeElement]

    def __init__(self, code: list[CodeElement]):
        self.code = code

    @classmethod
    def take(cls, tokens: list[Token]) -> Self | None:
        match tokens[0]:
            case Char("[", line_pos, char_pos):
                del tokens[0]
                brackets = 0
                code = []
                while tokens:
                    match tokens.pop(0), brackets:
                        case Char("[") as t, _:
                            brackets += 1
                            code.append(t)
                        case Char("]"), 0:
                            break
                        case Char("]") as t, _:
                            brackets -= 1
                            code.append(t)
                        case t, _:
                            code.append(t)
                else:
                    raise RainDuckSyntaxError("Missing ']'", line_pos, char_pos)
                return cls(parse_list(code))

    def transpile(self, inverse: bool = False) -> list["BrainFuck"]:
        return super().transpile(inverse)


class Multiplication(CodeElement):  # Not implemented now, so corresponding test fails

    precedence = 10
    num: int
    code: CodeElement
    line_pos: int | None
    char_pos: int | None

    def __init__(
        self, num: int, code: CodeElement, line_pos: int | None, char_pos: int | None
    ) -> None:
        self.num = num
        self.code = code
        self.line_pos = line_pos
        self.char_pos = char_pos

    @classmethod
    def take(cls, code: list[Token]) -> "CodeElement | None":
        match code[0]:
            case Number(n, line_pos, char_pos):
                del code[0]
                return cls(n, _take_elem(code), line_pos, char_pos)

    def transpile(self, inverse: bool = False) -> list["BrainFuck"]:
        return super().transpile(inverse)


def _take_elem(tokens: list[Token]) -> CodeElement:
    for elem_cls in code_elements:
        elem = elem_cls.take(tokens)
        if not (elem is None):
            return elem
    t = tokens[0]
    raise RainDuckSyntaxError("Unrecognized pattern", t.line_pos, t.char_pos)


def parse_list(tokens: list[Token]) -> list[CodeElement]:
    result = []
    while tokens:
        result.append(_take_elem(tokens))
    return result
