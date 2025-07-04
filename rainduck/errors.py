class RainDuckError(Exception):
    """Exception raised when error in RainDuck code found
    """

    message: str
    line_pos: int
    char_pos: int

    def __init__(self, message: str, line_pos: int, char_pos: int) -> None:
        super().__init__(message)
        self.message = message
        self.line_pos = line_pos
        self.char_pos = char_pos

    def __str__(self) -> str:
        return f"""{self.name}: {self.message}
        on line {self.line_pos}, character {self.char_pos}"""

    @property
    def name(self) -> str:
        cls_name = type(self).__name__
        return cls_name[8:] if cls_name.startswith("RainDuck") else cls_name


class RainDuckTokenError(RainDuckError):
    """Exception raised when error with tokenization of RainDuck code found.
    """
    pass
