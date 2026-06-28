from enum import Enum, auto


class TokenType(Enum):
    # ==========================
    # Keywords
    # ==========================
    RAKHAM = auto()
    SURU = auto()
    SURUF = auto()
    SURUD = auto()
    DEKHA = auto()
    LIM = auto()

    SAKKIYO = auto()
    YADI = auto()
    NATRA = auto()
    NATRA_VAYE = auto()

    JABASAMMA = auto()
    GARIRAKH = auto()

    SACHO = auto()
    JHUTO = auto()

    # ==========================
    # Literals
    # ==========================
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    BOOL_LITERAL = auto()

    # ==========================
    # Identifiers
    # ==========================
    IDENTIFIER = auto()

    # ==========================
    # Operators
    # ==========================
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    PLUS_PLUS = auto()
    MINUS_MINUS = auto()

    EQ_EQ = auto()
    BANG_EQ = auto()

    LT = auto()
    GT = auto()
    LT_EQ = auto()
    GT_EQ = auto()

    AMP_AMP = auto()
    PIPE_PIPE = auto()
    BANG = auto()

    ASSIGN = auto()

    # ==========================
    # Delimiters
    # ==========================
    LPAREN = auto()
    RPAREN = auto()

    LBRACE = auto()
    RBRACE = auto()

    SEMICOLON = auto()
    COMMA = auto()

    # ==========================
    # Import
    # ==========================
    IMPORT_PATH = auto()

    # ==========================
    # Special
    # ==========================
    EOF = auto()
    ERROR = auto()