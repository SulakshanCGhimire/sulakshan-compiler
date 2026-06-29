"""
AST node definitions for the SCG compiler.

Every node inherits from ASTNode which carries source location
(line, column) for error reporting in later compiler stages.

Field ordering in dataclasses follows Python's rule:
parent fields (line, column) come first in __init__.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


# ------------------------------------------------------------------ #
#  Base                                                                #
# ------------------------------------------------------------------ #

@dataclass
class ASTNode:
    """Base class for every node in the SCG AST."""
    line: int
    column: int


# ------------------------------------------------------------------ #
#  Expressions                                                         #
# ------------------------------------------------------------------ #

@dataclass
class LiteralNode(ASTNode):
    """
    A literal value written directly in source code.

    Examples:
        5        → value=5       (int)
        3.14     → value=3.14    (float)
        "hello"  → value="hello" (str)
        'A'      → value='A'     (str, length 1)
        sacho    → value=True    (bool)
        jhuto    → value=False   (bool)
    """
    value: Any


@dataclass
class IdentifierNode(ASTNode):
    """
    A variable or function name reference.

    Example:
        x
        main
        result
    """
    name: str


@dataclass
class UnaryOpNode(ASTNode):
    """
    A unary operation applied to a single operand.

    Examples:
        -x       → operator="-",  operand=IdentifierNode("x")
        !flag    → operator="!",  operand=IdentifierNode("flag")
        ++i      → operator="++", operand=IdentifierNode("i")
        --i      → operator="--", operand=IdentifierNode("i")

    operator is stored as a string so the code generator can emit
    it directly into C without conversion.
    """
    operator: str
    operand: ASTNode


@dataclass
class BinaryOpNode(ASTNode):
    """
    A binary operation between two expressions.

    Examples:
        a + b    → operator="+"
        x > 3   → operator=">"
        x && y  → operator="&&"

    operator is stored as a string for direct C emission.
    """
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class FunctionCallNode(ASTNode):
    """
    A function call expression.

    Examples:
        add(a, b)      → name="add",  arguments=[a, b]
        dekha("Hello") → name="dekha", arguments=["Hello"]
        lim()          → name="lim",  arguments=[]
    """
    name: str
    arguments: list[ASTNode]


# ------------------------------------------------------------------ #
#  Statements                                                          #
# ------------------------------------------------------------------ #

@dataclass
class AssignmentNode(ASTNode):
    """
    A variable assignment statement.

    Example:
        x = 5;
        name = "Sulakshan";
    """
    target: IdentifierNode
    value: ASTNode


@dataclass
class OutputStatementNode(ASTNode):
    """
    A dekha() output statement.
    Takes exactly one expression — dekha is single-argument in SCG.

    Examples:
        dekha("Hello");
        dekha(x);
        dekha(x + 5);
    """
    expression: ASTNode


@dataclass
class InputStatementNode(ASTNode):
    """
    A lim() input statement. Reads one value into target.
    lim() takes no arguments in SCG.

    Example:
        name = lim();
    """
    target: IdentifierNode


@dataclass
class ReturnStatementNode(ASTNode):
    """
    A sakkiyo return statement.

    Examples:
        sakkiyo;          → value=None  (return 0)
        sakkiyo 42;       → value=LiteralNode(42)
        sakkiyo a + b;    → value=BinaryOpNode(...)
    """
    value: ASTNode | None


@dataclass
class BlockNode(ASTNode):
    """
    A sequence of statements enclosed in { }.
    Used as the body of functions, if branches, loops.
    """
    statements: list[ASTNode]


@dataclass
class IfStatementNode(ASTNode):
    """
    A full yadi / natra vaye / natra conditional.

    Example:
        yadi(a > b){ ... }
        natra vaye(b > c){ ... }
        natra { ... }

    elif_branches holds zero or more (condition, block) pairs.
    else_block is None when there is no natra clause.
    """
    condition: ASTNode
    then_block: BlockNode
    elif_branches: list[tuple[ASTNode, BlockNode]]
    else_block: BlockNode | None


@dataclass
class WhileStatementNode(ASTNode):
    """
    A jabasamma while loop.

    Example:
        jabasamma(i > 0){ ... }
    """
    condition: ASTNode
    body: BlockNode


@dataclass
class ForStatementNode(ASTNode):
    """
    A garirakh for loop.

    Example:
        garirakh(i = 0; i < 3; i++){ ... }

    All three header parts are optional to handle edge cases.
    """
    initialization: ASTNode | None
    condition: ASTNode | None
    increment: ASTNode | None
    body: BlockNode


# ------------------------------------------------------------------ #
#  Program Structure                                                   #
# ------------------------------------------------------------------ #

@dataclass
class ImportNode(ASTNode):
    """
    An import declaration.

    Example:
        rakham <io.s>   → path="io.s"
    """
    path: str


@dataclass
class FunctionDefNode(ASTNode):
    """
    A complete function definition.

    Example:
        suru add(a, b){ sakkiyo a + b; }

    return_type holds the SCG keyword that determined the C return type.
    Valid values: "int" | "float" | "double" | None (void)
    """
    name: str
    parameters: list[str]
    return_type: str | None   # "int" | "float" | "double" | None (void)
    body: BlockNode


@dataclass
class ProgramNode(ASTNode):
    """
    Root node of the entire AST.
    Every valid SCG file produces exactly one ProgramNode.

    The code generator processes imports first, then functions.
    """
    imports: list[ImportNode]
    functions: list[FunctionDefNode]