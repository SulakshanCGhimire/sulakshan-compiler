# SCG Language Specification — v1.0

**Language Name:** SCG (Sulakshan Compiler Grammar)
**File Extension:** `.scg`
**Target:** C code via VCC
**Design Philosophy:** Minimal, Nepali-keyword language with static typing and type inference

---

## 1. Program Structure

Every SCG program follows this structure:

```
rakham <io.s>

suru main(){
    // code here
    sakkiyo;
}
```

---

## 2. Imports

```
rakham <io.s>       // like #include <stdio.h>
                    // provides: dekha() and lim()
```

---

## 3. Functions

### Keywords

| Keyword | C Equivalent | Meaning |
|---|---|---|
| `suru` | `int` | integer-returning function (default) |
| `suruf` | `float` | float-returning function |
| `surud` | `double` | double-returning function |
| `suru` (no sakkiyo) | `void` | void function — no return needed |

### Syntax

```
suru main(){
    sakkiyo;           // return 0
}

suru add(a, b){
    sakkiyo a + b;     // return value
}

suruf getPI(){
    sakkiyo 3.14;
}

suru greet(){
    dekha("Hello");    // void — no sakkiyo
}
```

### Return Statement

```
sakkiyo;           // return 0 (implicit, for main)
sakkiyo 42;        // return specific value
sakkiyo a + b;     // return expression
```

---

## 4. Variables

### Declaration Style
Python-style — no explicit type annotation. Type is **inferred from first assignment**.

```
x = 5                  // INT
pi = 3.14              // FLOAT
name = "Sulakshan"     // STRING
letter = 'A'           // CHAR
flag = sacho           // BOOL
```

### Type Rules
- First assignment **locks** the type permanently
- Reassignment to the **same type** is allowed
- Reassignment to a **different type** is a compile error

```
x = 5       // OK — x is INT
x = 10      // OK — still INT
x = "hello" // COMPILE ERROR — x was INT
```

---

## 5. Primitive Types

| SCG Inferred Type | Example Literal | C Equivalent |
|---|---|---|
| INT | `5`, `42`, `-3` | `int` |
| FLOAT | `3.14`, `2.71` | `float` |
| DOUBLE | (via suruf/surud context) | `double` |
| STRING | `"Sulakshan"` | `char*` |
| CHAR | `'A'` | `char` |
| BOOL | `sacho`, `jhuto` | `int` (0/1) |

---

## 6. Boolean Literals

```
flag = sacho       // true  → 1 in C
flag = jhuto       // false → 0 in C
```

---

## 7. Input and Output

```
dekha("Hello World");      // print string literal
dekha(x);                  // print variable
dekha("Value: " + x);     // print concatenated

name = lim();              // read input into variable
```

Both `dekha` and `lim` are provided by `rakham <io.s>`.

---

## 8. Operators

### Arithmetic
```
+   -   *   /   %
++  --
```

### Comparison
```
==   !=   <   >   <=   >=
```

### Logical
```
&&   ||   !
```

### String Concatenation
```
full = first + " " + last      // Python-style, using +
```

---

## 9. Control Flow

### If / Else-If / Else

```
yadi(a > b){
    dekha("a");
}
natra vaye(b > a){
    dekha("b");
}
natra{
    dekha("equal");
}
```

### While Loop

```
jabasamma(i > 0){
    dekha(i);
    i--;
}
```

### For Loop

```
garirakh(i = 0; i < 3; i++){
    dekha(i);
}
```

---

## 10. Scoping Rules

- Variables are scoped to the function they are declared in
- Global variables (declared outside all functions) are accessible everywhere
- Local variables shadow global variables of the same name
- Accessing a variable outside its scope is a compile error

```
x = 10                  // global

suru main(){
    x = 20              // local x — shadows global
    dekha(x);           // prints 20
}

suru other(){
    dekha(x);           // prints 10 — sees global x
}
```

---

## 11. Function Parameters and Polymorphism

- Parameter types are **inferred from the call site**
- All call sites must use **consistent types**
- If a function is called with different types across call sites, the compiler generates **separate C functions** via **name mangling**

```
suru add(a, b){
    sakkiyo a + b;
}

result1 = add(3, 5)          // generates: add_int
result2 = add(3.14, 2.71)    // generates: add_float
```

Mixed-type calls are a compile error:
```
result = add(3, "hello")     // COMPILE ERROR
```

---

## 12. Semantic Rules Summary

| Rule | Behavior |
|---|---|
| First assignment | Locks variable type |
| Type mismatch in assignment | Compile error |
| Undefined variable | Compile error |
| Out-of-scope variable access | Compile error |
| Mixed-type function call | Compile error |
| Consistent-type overloaded call | Generates mangled C function |
| Recursive functions | Resolved via two-pass analysis |

---

## 13. Hello World

```
rakham <io.s>

suru main(){
    dekha("Hello World");
    sakkiyo;
}
```

Compiles to:

```c
#include <stdio.h>

int main(){
    printf("Hello World");
    return 0;
}
```