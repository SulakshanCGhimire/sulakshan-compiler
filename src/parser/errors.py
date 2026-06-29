"""
Parser error definitions for the SCG compiler.
"""
from dataclasses import dataclass
from ..lexer.token_type import TokenType


@dataclass
class ParseError(Exception):
    """
    Represents a syntax error encountered during parsing.

    Example:
        [ParseError] Expected '(' but found 'SURU'
        at line 3, column 5 in hello.scg
    """
    message: str
    line: int
    column: int
    filename: str
    expected: TokenType | None = None
    found: TokenType | None = None

    def __post_init__(self):
        super().__init__(str(self))

    def __str__(self) -> str:
        if self.expected is not None and self.found is not None:
            return (
                f"[ParseError] {self.message} "
                f"(expected '{self.expected.name}', "
                f"found '{self.found.name}') "
                f"at line {self.line}, column {self.column} "
                f"in {self.filename}"
            )
        return (
            f"[ParseError] {self.message} "
            f"at line {self.line}, column {self.column} "
            f"in {self.filename}"
        )