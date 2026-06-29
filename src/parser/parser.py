"""
Recursive descent parser for the SCG language.

Consumes a flat list of Token objects produced by the Lexer and
builds an Abstract Syntax Tree (AST) rooted at a ProgramNode.

Usage:
    parser = Parser(tokens, filename)
    ast    = parser.parse()
    if parser.errors:
        for err in parser.errors:
            print(err)
"""
from ..lexer.token import Token
from ..lexer.token_type import TokenType
from .ast_nodes import (
    ASTNode, ProgramNode, ImportNode, FunctionDefNode, BlockNode,
    AssignmentNode, OutputStatementNode, InputStatementNode,
    ReturnStatementNode, IfStatementNode, WhileStatementNode,
    ForStatementNode, BinaryOpNode, UnaryOpNode,
    LiteralNode, IdentifierNode, FunctionCallNode,
)
from .errors import ParseError


class Parser:

    def __init__(self, tokens: list[Token], filename: str) -> None:
        self.tokens: list[Token] = tokens
        self.filename: str = filename
        self.current: int = 0
        self.errors: list[ParseError] = []

    # ------------------------------------------------------------------ #
    #  Cursor helpers                                                      #
    # ------------------------------------------------------------------ #

    def at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def advance(self) -> Token:
        if not self.at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def check(self, token_type: TokenType) -> bool:
        if self.at_end():
            return False
        return self.peek().type == token_type

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def expect(self, token_type: TokenType, message: str | None = None) -> Token:
        token = self.peek()
        if token.type == token_type:
            return self.advance()
        if message is None:
            message = (
                f"Expected '{token_type.name}' "
                f"but found '{token.type.name}'"
            )
        self.report_error(ParseError(
            message=message,
            line=token.line,
            column=token.column,
            filename=self.filename,
            expected=token_type,
            found=token.type,
        ))
        return Token(
            type=TokenType.ERROR,
            lexeme=token.lexeme,
            literal=None,
            line=token.line,
            column=token.column,
        )

    # ------------------------------------------------------------------ #
    #  Error handling                                                      #
    # ------------------------------------------------------------------ #

    def report_error(self, error: ParseError) -> None:
        self.errors.append(error)

    # ------------------------------------------------------------------ #
    #  Expressions                                                         #
    # ------------------------------------------------------------------ #

    def parse_primary(self) -> ASTNode:
        token = self.peek()

        if self.match(TokenType.INT_LITERAL):
            return LiteralNode(line=token.line, column=token.column, value=token.literal)
        if self.match(TokenType.FLOAT_LITERAL):
            return LiteralNode(line=token.line, column=token.column, value=token.literal)
        if self.match(TokenType.STRING_LITERAL):
            return LiteralNode(line=token.line, column=token.column, value=token.literal)
        if self.match(TokenType.CHAR_LITERAL):
            return LiteralNode(line=token.line, column=token.column, value=token.literal)
        if self.match(TokenType.BOOL_LITERAL):
            return LiteralNode(line=token.line, column=token.column, value=token.literal)

        if self.check(TokenType.IDENTIFIER):
            if (
                self.current + 1 < len(self.tokens)
                and self.tokens[self.current + 1].type == TokenType.LPAREN
            ):
                return self.parse_function_call()
            token = self.advance()
            return IdentifierNode(line=token.line, column=token.column, name=token.lexeme)

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        token = self.peek()
        self.report_error(ParseError(
            message="Expected expression",
            line=token.line,
            column=token.column,
            filename=self.filename,
        ))
        self.advance()
        return LiteralNode(line=token.line, column=token.column, value=None)

    def parse_function_call(self) -> FunctionCallNode:
        name_token = self.expect(TokenType.IDENTIFIER, "Expected function name")
        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        arguments: list[ASTNode] = []
        if not self.check(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())
        self.expect(TokenType.RPAREN, "Expected ')' after arguments")
        return FunctionCallNode(
            line=name_token.line,
            column=name_token.column,
            name=name_token.lexeme,
            arguments=arguments,
        )

    def parse_unary(self) -> ASTNode:
        if self.match(TokenType.BANG, TokenType.MINUS,
                      TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
            operator = self.tokens[self.current - 1]
            operand  = self.parse_unary()
            return UnaryOpNode(
                line=operator.line, column=operator.column,
                operator=operator.lexeme, operand=operand,
            )
        return self.parse_primary()

    def parse_multiplication(self) -> ASTNode:
        expr = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.tokens[self.current - 1]
            right    = self.parse_unary()
            expr = BinaryOpNode(
                line=operator.line, column=operator.column,
                left=expr, operator=operator.lexeme, right=right,
            )
        return expr

    def parse_addition(self) -> ASTNode:
        expr = self.parse_multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.tokens[self.current - 1]
            right    = self.parse_multiplication()
            expr = BinaryOpNode(
                line=operator.line, column=operator.column,
                left=expr, operator=operator.lexeme, right=right,
            )
        return expr

    def parse_comparison(self) -> ASTNode:
        expr = self.parse_addition()
        while self.match(TokenType.EQ_EQ, TokenType.BANG_EQ,
                         TokenType.LT, TokenType.GT,
                         TokenType.LT_EQ, TokenType.GT_EQ):
            operator = self.tokens[self.current - 1]
            right    = self.parse_addition()
            expr = BinaryOpNode(
                line=operator.line, column=operator.column,
                left=expr, operator=operator.lexeme, right=right,
            )
        return expr

    def parse_logical_and(self) -> ASTNode:
        expr = self.parse_comparison()
        while self.match(TokenType.AMP_AMP):
            operator = self.tokens[self.current - 1]
            right    = self.parse_comparison()
            expr = BinaryOpNode(
                line=operator.line, column=operator.column,
                left=expr, operator=operator.lexeme, right=right,
            )
        return expr

    def parse_expression(self) -> ASTNode:
        expr = self.parse_logical_and()
        while self.match(TokenType.PIPE_PIPE):
            operator = self.tokens[self.current - 1]
            right    = self.parse_logical_and()
            expr = BinaryOpNode(
                line=operator.line, column=operator.column,
                left=expr, operator=operator.lexeme, right=right,
            )
        return expr

    # ------------------------------------------------------------------ #
    #  Statements                                                          #
    # ------------------------------------------------------------------ #

    def parse_block(self) -> BlockNode:
        left_brace = self.expect(TokenType.LBRACE, "Expected '{'")
        statements: list[ASTNode] = []
        while not self.check(TokenType.RBRACE) and not self.at_end():
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE, "Expected '}' after block")
        return BlockNode(
            line=left_brace.line, column=left_brace.column,
            statements=statements,
        )

    def parse_return_stmt(self) -> ReturnStatementNode:
        token = self.expect(TokenType.SAKKIYO)
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after return statement")
        return ReturnStatementNode(line=token.line, column=token.column, value=value)

    def parse_output_stmt(self) -> OutputStatementNode:
        token = self.expect(TokenType.DEKHA)
        self.expect(TokenType.LPAREN)
        expression = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return OutputStatementNode(
            line=token.line, column=token.column, expression=expression,
        )

    def parse_input_stmt(self) -> InputStatementNode:
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        self.expect(TokenType.LIM)
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return InputStatementNode(
            line=identifier.line, column=identifier.column,
            target=IdentifierNode(
                line=identifier.line, column=identifier.column,
                name=identifier.lexeme,
            ),
        )

    def parse_assignment(self) -> AssignmentNode:
        identifier = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        self.expect(TokenType.ASSIGN, "Expected '=' after identifier")
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after assignment")
        return AssignmentNode(
            line=identifier.line, column=identifier.column,
            target=IdentifierNode(
                line=identifier.line, column=identifier.column,
                name=identifier.lexeme,
            ),
            value=value,
        )

    def parse_while_stmt(self) -> WhileStatementNode:
        token = self.expect(TokenType.JABASAMMA)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatementNode(
            line=token.line, column=token.column,
            condition=condition, body=body,
        )

    def parse_if_stmt(self) -> IfStatementNode:
        token = self.expect(TokenType.YADI)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_block = self.parse_block()
        elif_branches: list[tuple[ASTNode, BlockNode]] = []
        while self.match(TokenType.NATRA_VAYE):
            self.expect(TokenType.LPAREN)
            elif_condition = self.parse_expression()
            self.expect(TokenType.RPAREN)
            elif_block = self.parse_block()
            elif_branches.append((elif_condition, elif_block))
        else_block = None
        if self.match(TokenType.NATRA):
            else_block = self.parse_block()
        return IfStatementNode(
            line=token.line, column=token.column,
            condition=condition, then_block=then_block,
            elif_branches=elif_branches, else_block=else_block,
        )

    def parse_for_stmt(self) -> ForStatementNode:
        token = self.expect(TokenType.GARIRAKH)
        self.expect(TokenType.LPAREN)
        initialization = self.parse_assignment()
        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after loop condition")
        increment = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return ForStatementNode(
            line=token.line, column=token.column,
            initialization=initialization, condition=condition,
            increment=increment, body=body,
        )

    def parse_statement(self) -> ASTNode:
        if self.check(TokenType.SAKKIYO):
            return self.parse_return_stmt()
        if self.check(TokenType.DEKHA):
            return self.parse_output_stmt()
        if self.check(TokenType.YADI):
            return self.parse_if_stmt()
        if self.check(TokenType.JABASAMMA):
            return self.parse_while_stmt()
        if self.check(TokenType.GARIRAKH):
            return self.parse_for_stmt()
        if self.check(TokenType.IDENTIFIER):
            if (
                self.current + 2 < len(self.tokens)
                and self.tokens[self.current + 1].type == TokenType.ASSIGN
                and self.tokens[self.current + 2].type == TokenType.LIM
            ):
                return self.parse_input_stmt()
            return self.parse_assignment()
        token = self.peek()
        self.report_error(ParseError(
            message=f"Unexpected token '{token.lexeme}'",
            line=token.line,
            column=token.column,
            filename=self.filename,
        ))
        self.advance()
        return LiteralNode(line=token.line, column=token.column, value=None)

    # ------------------------------------------------------------------ #
    #  Program structure                                                   #
    # ------------------------------------------------------------------ #

    def parse_param_list(self) -> list[str]:
        parameters: list[str] = []
        if self.check(TokenType.IDENTIFIER):
            token = self.expect(TokenType.IDENTIFIER)
            parameters.append(token.lexeme)
            while self.match(TokenType.COMMA):
                token = self.expect(
                    TokenType.IDENTIFIER,
                    "Expected parameter name after ','",
                )
                parameters.append(token.lexeme)
        return parameters

    def parse_function_def(self) -> FunctionDefNode:
        if self.match(TokenType.SURU):
            keyword = self.tokens[self.current - 1]
            return_type = "int"
        elif self.match(TokenType.SURUF):
            keyword = self.tokens[self.current - 1]
            return_type = "float"
        elif self.match(TokenType.SURUD):
            keyword = self.tokens[self.current - 1]
            return_type = "double"
        else:
            token = self.peek()
            self.report_error(ParseError(
                message="Expected function declaration",
                line=token.line, column=token.column,
                filename=self.filename,
            ))
            self.advance()
            return FunctionDefNode(
                line=token.line, column=token.column,
                name="<error>", parameters=[],
                return_type="int",
                body=BlockNode(line=token.line, column=token.column, statements=[]),
            )
        name = self.expect(TokenType.IDENTIFIER, "Expected function name")
        self.expect(TokenType.LPAREN)
        parameters = self.parse_param_list()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDefNode(
            line=keyword.line, column=keyword.column,
            name=name.lexeme, parameters=parameters,
            return_type=return_type, body=body,
        )

    def parse_import(self) -> ImportNode:
        keyword = self.expect(TokenType.RAKHAM)
        path = self.expect(TokenType.IMPORT_PATH, "Expected import path after 'rakham'")
        return ImportNode(
            line=keyword.line, column=keyword.column,
            path=path.literal,
        )

    def parse(self) -> ProgramNode:
        imports: list[ImportNode] = []
        while self.check(TokenType.RAKHAM):
            imports.append(self.parse_import())
        functions: list[FunctionDefNode] = []
        while not self.at_end():
            functions.append(self.parse_function_def())
        return ProgramNode(line=1, column=1, imports=imports, functions=functions)