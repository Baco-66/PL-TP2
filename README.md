# PL-TP2 - Custom Programming Language Compiler

## Description

This project is a custom programming language compiler developed as part of a university course on **"Processamento de Linguagens (PL)"**. The goal was to design a language with specific features and implement a compiler that translates the language into stack-based virtual machine code.

## Features of the Language

1. **Imperative Programming**: The language supports an imperative programming paradigm.
2. **Variable Declaration**: Variables must be declared before use and cannot be redeclared. The language supports:
   - Integer variables
   - Arrays of integers
3. **Control Structures**:
   - `while` loops with nested support
   - `repeat` loops with a fixed number of iterations
   - `if-else` conditional statements
4. **Input/Output Operations**:
   - `read` for input
   - `print` for integer output
   - `printS` for string output
5. **Error Handling**:
   - Lexical errors
   - Syntax errors with suggestions
   - Semantic errors for variable and conditional misuse

## Key Objectives

- Gain experience in language engineering and generative programming.
- Develop grammar rules for context-free and translator grammars.
- Implement a compiler using Python's PLY (Python Lex-Yacc).
- Generate code for a stack-based virtual machine (VM).

## Project Structure

1. **Lexical Analysis**:
   - Recognizes tokens like keywords, identifiers, and operators.
   - Implements error handling for illegal characters.
2. **Syntax Analysis**:
   - Uses grammar rules defined in YACC to parse valid programs.
   - Provides detailed feedback for syntax errors.
3. **Semantic Analysis**:
   - Ensures proper use of variables and control structures.
4. **Code Generation**:
   - Translates source code into VM assembly instructions.
5. **Examples**:
   - Programs demonstrating use cases like finding the LCM of two numbers, drawing a triangle, and identifying square sides.

## Usage Examples

### LCM Calculation
```c
int NumOne, NumTwo, maxValue;
start
printS ("Please Enter two integer Values\n")
read(NumOne)
read(NumTwo)

if (NumOne > NumTwo) {
    maxValue = NumOne;
} else {
    maxValue = NumTwo;
}

while(! (maxValue % NumOne == 0 && maxValue % NumTwo == 0)) {
    maxValue++;
}

printS ("LCM = " + maxValue);
```

### Output VM Code
```assembly
PUSHN 4
START
PUSHS "Please Enter two integer Values\n"
WRITES
READ
ATOI
STOREG 0
...
STOP
```

## Getting Started

1. Install Python with the PLY library.
2. Run the compiler with a source code file:
   ```bash
   python compiler.py source.txt
4. The compiler will generate VM code in a .vm file.
