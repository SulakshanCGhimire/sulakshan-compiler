# SCG Formal Grammar — EBNF

**Status:** ✅ Complete (Milestone 1)
**Version:** 1.0

This is the complete formal grammar for the SCG language in Extended Backus-Naur Form (EBNF).

The parser is derived directly from these rules. Every valid SCG program must match the `program` rule.

---

## EBNF Notation Reference

| Symbol | Meaning | Example |
|---|---|---|
| `=` | is defined as | `digit = "0" \| "1"` |
| `\|` | or | `"a" \| "b"` |
| `{ }` | zero or more | `{ digit }` |
| `[ ]` | optional (zero or one) | `[ "-" ]` |
| `( )` | grouping | `( "a" \| "b" )` |
| `" "` | literal character | `"suru"` |

---

## Complete Grammar

```ebnf
(* ─── Primitives ─── *)

digit           = "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9" ;
letter          = "a"|"b"|...|"z"|"A"|"B"|...|"Z" ;

integer_literal = [ "-" ] digit { digit } ;
float_literal   = [ "-" ] digit { digit } "." digit { digit } ;
char_literal    = "'" letter "'" ;
string_literal  = '"' { letter | digit | " " } '"' ;
bool_literal    = "sacho" | "jhuto" ;

literal         = integer_literal | float_literal | char_literal
                | string_literal  | bool_literal ;

identifier      = letter { letter | digit | "_" } ;


(* ─── Expressions — ordered lowest to highest precedence ─── *)

primary         = literal
                | identifier
                | "(" expression ")" ;

unary           = ( "!" | "-" | "++" | "--" ) unary
                | primary ;

multiplication  = unary { ( "*" | "/" | "%" ) unary } ;

addition        = multiplication { ( "+" | "-" ) multiplication } ;

comparison      = addition { ( "==" | "!=" | "<" | ">" | "<=" | ">=" ) addition } ;

logical_and     = comparison { "&&" comparison } ;

expression      = logical_and { "||" logical_and } ;


(* ─── Statements ─── *)

block           = "{" { statement } "}" ;

assignment      = identifier "=" expression ";" ;
output_stmt     = "dekha" "(" expression ")" ";" ;
input_stmt      = identifier "=" "lim" "(" ")" ";" ;
return_stmt     = "sakkiyo" [ expression ] ";" ;

if_stmt         = "yadi" "(" expression ")" block
                  { "natra vaye" "(" expression ")" block }
                  [ "natra" block ] ;

while_stmt      = "jabasamma" "(" expression ")" block ;

for_stmt        = "garirakh" "(" assignment expression ";" expression ")" block ;

statement       = assignment
                | output_stmt
                | input_stmt
                | return_stmt
                | if_stmt
                | while_stmt
                | for_stmt ;


(* ─── Program Structure ─── *)

param_list      = [ identifier { "," identifier } ] ;
func_keyword    = "suru" | "suruf" | "surud" ;
function_def    = func_keyword identifier "(" param_list ")" block ;

program         = "rakham" "<io.s>"
                  function_def { function_def } ;
```

---

## Precedence Table

From lowest to highest:

| Level | Rule | Operators |
|---|---|---|
| 1 (lowest) | `expression` | `\|\|` |
| 2 | `logical_and` | `&&` |
| 3 | `comparison` | `== != < > <= >=` |
| 4 | `addition` | `+ -` |
| 5 | `multiplication` | `* / %` |
| 6 | `unary` | `! - ++ --` |
| 7 (highest) | `primary` | literals, identifiers, `()` |

---

## Example Trace

Program:
```
rakham <io.s>

suru main(){
    x = 5;
    yadi(x > 3){
        dekha("big");
    }
    sakkiyo;
}
```

Grammar derivation:
```
program
  → "rakham <io.s>" ✓
  → function_def
      → func_keyword "suru" ✓
      → identifier "main" ✓
      → "(" param_list ")" — empty ✓
      → block
          → statement → assignment
              → identifier "x" → "=" → expression → literal "5" → ";" ✓
          → statement → if_stmt
              → "yadi" → "(" → comparison → identifier "x" ">" literal "3" → ")" ✓
              → block
                  → statement → output_stmt
                      → "dekha" → "(" → string_literal "big" → ")" → ";" ✓
          → statement → return_stmt
              → "sakkiyo" → [ expression ] absent → ";" ✓
program accepted ✓
```