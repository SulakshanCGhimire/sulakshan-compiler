from .token import Token
from .token_type import TokenType
from .keywords import KEYWORDS
from .errors import LexicalError


class Lexer:
    """
    Lexer for the SCG language.

    Converts a raw source string into a flat list of Token objects.
    Errors are collected and never raised mid-scan, so the lexer
    always produces the longest valid token stream it can before
    reporting problems.

    Usage:
        lexer  = Lexer(source, filename)
        tokens = lexer.tokenize()
        if lexer.errors:
            for err in lexer.errors:
                print(err)
    """

    def __init__(self, source: str, filename: str) -> None:
        self.source = source
        self.filename = filename
        self.start = 0            # start index of the token being scanned
        self.current = 0          # current read position
        self.line = 1             # current line (1-based)
        self.column = 0           # starts at 0; first advance() gives column 1
        self.token_column = 1     # column saved at the START of each token
        self.tokens: list[Token] = []
        self.errors: list[LexicalError] = []

    # ------------------------------------------------------------------ #
    #  Cursor helpers                                                      #
    # ------------------------------------------------------------------ #

    def at_end(self) -> bool:
        """Return True when the cursor has passed the end of source."""
        return self.current >= len(self.source)

    def advance(self) -> str:
        """
        Consume and return the current character.
        Tracks line and column numbers automatically.
        Returns '\\0' when called at end-of-source.
        """
        if self.at_end():
            return "\0"
        ch = self.source[self.current]
        self.current += 1
        if ch == "\n":
            self.line += 1
            self.column = 0       # next character will be column 1
        else:
            self.column += 1
        return ch

    def peek(self) -> str:
        """Return the current character without consuming it."""
        return "\0" if self.at_end() else self.source[self.current]

    def peek_next(self) -> str:
        """Return the character one ahead of current without consuming."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        """
        Consume the current character only if it equals `expected`.
        Used for two-character operators such as == <= !=.
        """
        if self.at_end() or self.peek() != expected:
            return False
        self.advance()
        return True

    # ------------------------------------------------------------------ #
    #  Token factory                                                       #
    # ------------------------------------------------------------------ #

    def make_token(self, token_type: TokenType, literal=None) -> Token:
        """Build a Token from the current start/current window."""
        lexeme = self.source[self.start:self.current]
        return Token(token_type, lexeme, literal, self.line, self.token_column)

    def emit(self, token_type: TokenType, literal=None) -> None:
        """Append a new token to the token list."""
        self.tokens.append(self.make_token(token_type, literal))

    def report_error(self, message: str) -> None:
        """Record a lexical error without stopping the scan."""
        self.errors.append(
            LexicalError(message, self.line, self.column, self.filename)
        )

    # ------------------------------------------------------------------ #
    #  Whitespace and comments                                             #
    # ------------------------------------------------------------------ #

    def skip_whitespace(self) -> None:
        """
        Advance past spaces, tabs, carriage returns, newlines, and
        single-line comments ( // ... end-of-line ).
        """
        while not self.at_end():
            c = self.peek()
            if c in (" ", "\t", "\r", "\n"):
                self.advance()
            elif c == "/" and self.peek_next() == "/":
                # consume everything up to (but not including) the newline
                while not self.at_end() and self.peek() != "\n":
                    self.advance()
            else:
                break

    # ------------------------------------------------------------------ #
    #  Scanners                                                            #
    # ------------------------------------------------------------------ #

    def scan_word(self) -> None:
        """
        Scan an identifier or keyword.
        Precondition: the first character has already been consumed by
        scan_token() so self.start points at it.
        """
        # Consume remaining letters, digits, and underscores
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        word = self.source[self.start:self.current]

        # ── Compound keyword: natra vaye ──────────────────────────────
        # After scanning "natra", skip horizontal whitespace and peek at
        # the next word. If it is "vaye", merge into NATRA_VAYE.
        if word == "natra":
            saved_current = self.current
            saved_column = self.column

            # Skip horizontal whitespace only — do not cross a newline
            while self.peek() in (" ", "\t", "\r"):
                self.advance()

            next_start = self.current

            if self.peek().isalpha() or self.peek() == "_":
                while self.peek().isalnum() or self.peek() == "_":
                    self.advance()

                next_word = self.source[next_start:self.current]

                if next_word == "vaye":
                    self.emit(TokenType.NATRA_VAYE)
                    return

            # "vaye" not found — restore cursor and fall through to NATRA
            self.current = saved_current
            self.column = saved_column

        # ── Boolean literals ──────────────────────────────────────────
        if word == "sacho":
            self.emit(TokenType.BOOL_LITERAL, True)
            return

        if word == "jhuto":
            self.emit(TokenType.BOOL_LITERAL, False)
            return

        # ── All other reserved keywords and plain identifiers ─────────
        token_type = KEYWORDS.get(word)
        if token_type is not None:
            self.emit(token_type)
        else:
            self.emit(TokenType.IDENTIFIER)

    def scan_number(self) -> None:
        """
        Scan an integer or float literal.
        Precondition: the first digit has already been consumed.
        Emits INT_LITERAL  with a Python int  value, or
              FLOAT_LITERAL with a Python float value.
        """
        # Consume remaining digits of the integer part
        while self.peek().isdigit():
            self.advance()

        is_float = False

        # Check for a fractional part: digit(s) after a '.'
        # peek_next() guards against consuming a lone trailing '.'
        if self.peek() == "." and self.peek_next().isdigit():
            is_float = True
            self.advance()             # consume '.'
            while self.peek().isdigit():
                self.advance()

        lexeme = self.source[self.start:self.current]

        if is_float:
            self.emit(TokenType.FLOAT_LITERAL, float(lexeme))
        else:
            self.emit(TokenType.INT_LITERAL, int(lexeme))

    def scan_string(self) -> None:
        """
        Scan a double-quoted string literal.
        Precondition: the opening '"' has already been consumed.
        Emits STRING_LITERAL with the inner string value (quotes excluded).
        Reports a LexicalError for an unterminated string.
        """
        while not self.at_end() and self.peek() != '"':
            self.advance()

        if self.at_end():
            self.report_error("Unterminated string literal")
            return

        self.advance()               # consume closing '"'

        # Strip surrounding quotes to get the raw string value
        value = self.source[self.start + 1:self.current - 1]
        self.emit(TokenType.STRING_LITERAL, value)

    def scan_char(self) -> None:
        """
        Scan a single-quoted character literal.
        Precondition: the opening \"'\" has already been consumed.
        Emits CHAR_LITERAL with a single-character string value.
        Reports a LexicalError for unterminated or multi-character literals.
        """
        if self.at_end():
            self.report_error("Unterminated character literal")
            return

        value = self.advance()       # consume the character itself

        if self.peek() != "'":
            # More than one character — report error and recover
            self.report_error(
                "Character literal must contain exactly one character"
            )
            while not self.at_end() and self.peek() != "'":
                self.advance()
            if not self.at_end():
                self.advance()       # consume closing "'"
            return

        self.advance()               # consume closing "'"
        self.emit(TokenType.CHAR_LITERAL, value)

    def scan_import_path(self) -> None:
        """
        Scan <filename> as a single IMPORT_PATH token.
        Called immediately after RAKHAM is emitted.
        Precondition: cursor is positioned at the '<'.
        Emits IMPORT_PATH with the path string (angle brackets excluded).
        """
        if self.peek() != "<":
            self.report_error("Expected '<' after rakham")
            return

        self.advance()               # consume '<'
        self.start = self.current    # path content starts here

        while not self.at_end() and self.peek() != ">":
            self.advance()

        if self.at_end():
            self.report_error("Unterminated import path — missing '>'")
            return

        path = self.source[self.start:self.current]
        self.advance()               # consume '>'
        self.emit(TokenType.IMPORT_PATH, path)

    # ------------------------------------------------------------------ #
    #  Dispatcher                                                          #
    # ------------------------------------------------------------------ #

    def scan_token(self) -> None:
        """
        Scan and emit a single token.
        The current character determines which scanner or token to use.
        """
        c = self.advance()

        # ── Identifiers and keywords ──────────────────────────────────
        if c.isalpha() or c == "_":
            self.scan_word()

        # ── Numeric literals ──────────────────────────────────────────
        elif c.isdigit():
            self.scan_number()

        # ── String literal ────────────────────────────────────────────
        elif c == '"':
            self.scan_string()

        # ── Character literal ─────────────────────────────────────────
        elif c == "'":
            self.scan_char()

        # ── Arithmetic operators ──────────────────────────────────────
        elif c == "+":
            self.emit(TokenType.PLUS_PLUS if self.match("+") else TokenType.PLUS)
        elif c == "-":
            self.emit(TokenType.MINUS_MINUS if self.match("-") else TokenType.MINUS)
        elif c == "*":
            self.emit(TokenType.STAR)
        elif c == "/":
            self.emit(TokenType.SLASH)
        elif c == "%":
            self.emit(TokenType.PERCENT)

        # ── Comparison and assignment operators ───────────────────────
        elif c == "=":
            self.emit(TokenType.EQ_EQ if self.match("=") else TokenType.ASSIGN)
        elif c == "!":
            self.emit(TokenType.BANG_EQ if self.match("=") else TokenType.BANG)
        elif c == "<":
            self.emit(TokenType.LT_EQ if self.match("=") else TokenType.LT)
        elif c == ">":
            self.emit(TokenType.GT_EQ if self.match("=") else TokenType.GT)

        # ── Logical operators ─────────────────────────────────────────
        elif c == "&":
            if self.match("&"):
                self.emit(TokenType.AMP_AMP)
            else:
                self.report_error("Unexpected character '&' — did you mean '&&'?")
        elif c == "|":
            if self.match("|"):
                self.emit(TokenType.PIPE_PIPE)
            else:
                self.report_error("Unexpected character '|' — did you mean '||'?")

        # ── Delimiters ────────────────────────────────────────────────
        elif c == "(":
            self.emit(TokenType.LPAREN)
        elif c == ")":
            self.emit(TokenType.RPAREN)
        elif c == "{":
            self.emit(TokenType.LBRACE)
        elif c == "}":
            self.emit(TokenType.RBRACE)
        elif c == ";":
            self.emit(TokenType.SEMICOLON)
        elif c == ",":
            self.emit(TokenType.COMMA)

        # ── Unknown character ─────────────────────────────────────────
        else:
            self.report_error(f"Unexpected character '{c}'")

    # ------------------------------------------------------------------ #
    #  Main entry point                                                    #
    # ------------------------------------------------------------------ #

    def tokenize(self) -> list[Token]:
        """
        Scan the entire source and return a list of tokens.
        The list always ends with an EOF token.
        Check self.errors after calling this method.
        """
        while not self.at_end():
            self.skip_whitespace()
            if self.at_end():
                break
            self.start = self.current
            self.token_column = self.column
            self.scan_token()

            # ── Import path immediately follows rakham ────────────────
            if self.tokens and self.tokens[-1].type == TokenType.RAKHAM:
                self.skip_whitespace()
                self.start = self.current
                self.token_column = self.column
                self.scan_import_path()

        # Always emit EOF so the parser knows where the source ends
        self.start = self.current
        self.token_column = self.column
        self.emit(TokenType.EOF)
        return self.tokens