"""
Reserved keywords for the SCG language.

Design Decision:
----------------
'sacho' and 'jhuto' are stored here because they are reserved words and
cannot be used as identifiers.

Although they represent boolean literal values (True and False), they are
still recognized lexically as keywords. When the lexer encounters them,
it should create a BOOL_LITERAL token with the corresponding Python
literal value:

    sacho -> literal=True
    jhuto -> literal=False

Similarly, 'natra vaye' is included as a compound keyword. The lexer first
recognizes 'natra', then performs lookahead to see whether it is followed
by 'vaye'. If so, it upgrades the token to NATRA_VAYE.
"""

from .token_type import TokenType


KEYWORDS = {
    # Variable declarations
    "rakham": TokenType.RAKHAM,

    # Program structure
    "suru": TokenType.SURU,
    "suruf": TokenType.SURUF,
    "surud": TokenType.SURUD,
    "sakkiyo": TokenType.SAKKIYO,

    # Input / Output
    "dekha": TokenType.DEKHA,
    "lim": TokenType.LIM,

    # Conditionals
    "yadi": TokenType.YADI,
    "natra": TokenType.NATRA,
    "natra vaye": TokenType.NATRA_VAYE,

    # Loops
    "jabasamma": TokenType.JABASAMMA,
    "garirakh": TokenType.GARIRAKH,

    # Boolean literals (reserved words)
    "sacho": TokenType.BOOL_LITERAL,
    "jhuto": TokenType.BOOL_LITERAL,
}