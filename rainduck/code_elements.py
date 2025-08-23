from abc import ABCMeta, abstractmethod
from typing import Any, Self

from rainduck.tokens import Char, Token


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
