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
- **Statically typed with type inference**
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
- Language design trade-offs (minimal vs expressive)
- Static vs dynamic typing
- Type inference
- Symbol tables and scope chains
- Name mangling
- Two-pass semantic analysis
- Ad-hoc polymorphism via function overloading
- Compiler vs interpreter distinction
- Compile-time vs runtime error detection

---

## Milestone 1 — Formal Grammar (EBNF) 🔄 In Progress

### Goal
Write the complete EBNF grammar for SCG that will guide the lexer and parser implementation.

### Concepts to Learn
- What is EBNF?
- How grammars define languages
- Terminals vs non-terminals
- Production rules
- Ambiguity in grammars
- How parsers derive from grammars

---

## Milestone 2 — Lexer ⏳ Pending

### Goal
Implement the tokenizer that converts raw SCG source text into a stream of tokens.

---

## Milestone 3 — Parser ⏳ Pending

### Goal
Implement a recursive descent parser that consumes tokens and builds an AST.

---

## Milestone 4 — AST Construction ⏳ Pending

### Goal
Define AST node types and build the tree during parsing.

---

## Milestone 5 — Semantic Analysis ⏳ Pending

### Goal
Implement the symbol table, scope chain, type checker, and two-pass analysis.

---

## Milestone 6 — Code Generation ⏳ Pending

### Goal
Traverse the AST and emit valid C code into `generated.c`.

---

## Open Questions

- None currently. All Milestone 0 decisions are finalized.

---

## Session Log

### Session 1
- Designed the full SCG v1.0 language specification
- Made all core language design decisions
- Learned: type inference, symbol tables, scope chains, name mangling, two-pass analysis, polymorphism, compiler vs interpreter
- Set up project structure and documentation
- Next: Milestone 1 — Formal Grammar (EBNF)