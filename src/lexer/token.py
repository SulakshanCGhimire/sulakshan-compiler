from dataclasses import dataclass
from typing import Optional, Union

from .token_type import TokenType


LiteralType = Optional[Union[int, float, str, bool]]


@dataclass
class Token:
    """
    Represents a single token produced by the lexical analyzer.
    """

    type: TokenType
    lexeme: str
    literal: LiteralType
    line: int
    column: int

    def debug_string(self) -> str:
        """
        Returns a human-readable representation of the token.
        Useful when printing the token stream during debugging.
        """
        return (
            f"{self.type.name:<15} "
            f"Lexeme='{self.lexeme}' "
            f"Literal={repr(self.literal)} "
            f"(Line {self.line}, Column {self.column})"
        )