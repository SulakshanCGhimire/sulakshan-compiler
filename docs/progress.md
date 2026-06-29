# Sulakshan Compiler — Project Progress

---

## Milestone 0 — Language Design ✅ Complete

### Decisions Made

#### Keywords
| SCG | C Equivalent | Purpose |
|---|---|---|
| `rakham` | `#include` | Import |
| `suru` | `int` / `void` | Function (default int, void if no sakkiyo) |
| `suruf` | `float` | Float-returning function |
| `surud` | `double` | Double-returning function |
| `dekha` | `printf` | Print output |
| `lim` | `scanf` | Read input |
| `sakkiyo` | `return` | Return statement |
| `yadi` | `if` | Conditional |
| `natra vaye` | `else if` | Else-if |
| `natra` | `else` | Else |
| `jabasamma` | `while` | While loop |
| `garirakh` | `for` | For loop |
| `sacho` | `1` / `true` | Boolean true |
| `jhuto` | `0` / `false` | Boolean false |

#### Type System
- Statically typed with type inference
- Type inferred from first assignment, locked permanently
- Reassignment to different type → compile error
- No explicit type annotations for variables

#### Primitive Types
- INT, FLOAT, DOUBLE, STRING, CHAR, BOOL

#### Variable Style
- Python-style: `x = 5` (no declaration keyword)

#### Scoping
- Function-level scope
- Global scope for variables declared outside functions
- Local variables shadow globals
- Scope chain for lookup

#### Symbol Table
- Hash map per scope
- Stores: name, type, scope, line number
- Scope stack for nested lookups

#### Functions and Polymorphism
- Parameter types inferred from call site
- Consistent types enforced across all call sites
- Multiple type call sites → name mangling → separate C functions
- Two-pass analysis for recursive functions

#### Operators
- Arithmetic: `+ - * / % ++ --`
- Comparison: `== != < > <= >=`
- Logical: `&& || !`
- String concatenation: `+`

### Concepts Learned
- Language design trade-offs
- Static vs dynamic typing
- Type inference
- Symbol tables and scope chains
- Name mangling
- Two-pass semantic analysis
- Ad-hoc polymorphism via function overloading
- Compiler vs interpreter distinction
- Compile-time vs runtime error detection

---

## Milestone 1 — Formal Grammar (EBNF) ✅ Complete

### What Was Built
Complete EBNF grammar for SCG — see `grammar.md`

### Grammar Rules Written
- Primitives: `digit`, `letter`, `integer_literal`, `float_literal`, `char_literal`, `string_literal`, `bool_literal`, `literal`, `identifier`
- Expressions: `primary`, `unary`, `multiplication`, `addition`, `comparison`, `logical_and`, `expression`
- Statements: `block`, `assignment`, `output_stmt`, `input_stmt`, `return_stmt`, `if_stmt`, `while_stmt`, `for_stmt`, `statement`
- Program: `param_list`, `func_keyword`, `function_def`, `program`

### Concepts Learned
- EBNF notation: terminals, non-terminals, production rules
- Operator precedence via rule layering
- Mutual recursion in grammars (`primary` → `expression` → `primary`)
- Maximal munch principle
- Word boundary rule (keyword vs identifier distinction)
- Grammar traces / derivations
- Block vs simple statements and semicolon placement
- Postfix notation and evaluation order

### Key Insight
Operator precedence is not a runtime concept — it is encoded structurally in the grammar. Lower precedence operators sit in higher-level rules. The parser enforces precedence automatically by the order in which it tries rules.

---

## Milestone 2 — Lexer ✅ Complete

### Goal
Implement the tokenizer that converts raw SCG source text into a stream of tokens.

### What We Know Going In
- Nine token categories: KEYWORD, IDENTIFIER, INT_LITERAL, FLOAT_LITERAL, STRING_LITERAL, CHAR_LITERAL, BOOL_LITERAL, OPERATOR, DELIMITER
- Whitespace and comments are discarded
- Maximal munch determines token boundaries
- Keyword list is hardcoded; identifiers are anything else matching `letter { letter | digit | "_" }`

---

## Milestone 3 — Parser ✅ Complete

---

## Milestone 4 — AST Construction ⏳ Pending

---

## Milestone 5 — Semantic Analysis ⏳ Pending

---

## Milestone 6 — Code Generation ⏳ Pending

---

## Session Log

### Session 1
- Designed full SCG v1.0 language specification
- Made all core language design decisions
- Learned: type inference, symbol tables, scope chains, name mangling, two-pass analysis, polymorphism, compiler vs interpreter
- Set up project structure and documentation

### Session 2
- Learned EBNF notation from scratch
- Built complete SCG grammar collaboratively
- Learned: operator precedence via layering, mutual recursion, maximal munch, grammar traces
- Completed full program derivation trace
- Next: Milestone 2 — Lexer