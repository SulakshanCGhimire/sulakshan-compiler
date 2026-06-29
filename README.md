# Sulakshan Compiler

A complete compiler for the SCG programming language — a minimal, Nepali-keyword language that compiles to C and then to a native executable.

## Pipeline

```
.scg source file
      ↓
   Lexer          ← turns raw text into tokens
      ↓
   Parser         ← turns tokens into structure
      ↓
    AST           ← structured representation of the program
      ↓
Semantic Analysis ← checks types, scopes, and rules
      ↓
Code Generation   ← outputs C code
      ↓
 generated.c
      ↓
    VCC           ← compiles C to native executable
      ↓
Native Executable
```

## Language

- File extension: `.scg`
- Keywords: Nepali-based (`suru`, `dekha`, `yadi`, `natra`, etc.)
- Typing: Statically typed with type inference
- Target: C code generation via VCC

## Project Structure

```
sulakshan-compiler/
├── docs/
│   ├── language-spec.md   ← full language specification
│   ├── grammar.md         ← formal EBNF grammar
│   └── progress.md        ← milestone tracking
├── src/
│   ├── lexer/             ← tokenizer
│   ├── parser/            ← recursive descent parser
│   ├── ast/               ← AST node definitions
│   ├── semantic/          ← type checker and symbol table
│   └── codegen/           ← C code generator
├── tests/
│   └── samples/           ← .scg test programs
├── output/
│   └── generated.c        ← compiler output
└── README.md
```

## Milestones

| # | Milestone | Status |
|---|---|---|
| 0 | Language Design | ✅ Complete |
| 1 | Formal Grammar (EBNF) | ✅ Complete |
| 2 | Lexer | ✅ Complete |
| 3 | Parser | ✅ Complete |
| 4 | AST Construction | ⏳ Pending |
| 5 | Semantic Analysis | ⏳ Pending |
| 6 | Code Generation | ⏳ Pending |

## Author

Sulakshan Ghimire — [sulakshan.com.np](https://sulakshan.com.np) — [GitHub](https://github.com/SulakshanCGhimire)
