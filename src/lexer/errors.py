from dataclasses import dataclass

@dataclass
class LexicalError(Exception):
    """
    Represents a lexical error encountered during tokenization.

    Although SCG collects lexical errors instead of raising them
    immediately, this class inherits from Exception so it can also be
    used in contexts where immediate termination is desirable (e.g.,
    REPL mode or future compiler versions).
    """
    
    
    message: str
    line: int
    column: int
    filename: str

    def __post_init__(self):
        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"[LexicalError] {self.message} "
            f"at line {self.line}, column {self.column} "
            f"in {self.filename}"
        )