# Bad Compiler Challenge Solution

## Initial Analysis

### File Identification
```bash
file broken_compiler.exe
# Output: PE32 executable (console) Intel 80386, for MS Windows
```

The compiler is a Windows executable. Since we're on macOS, we need to either:
1. Use Wine to run it
2. Reverse engineer it and rewrite it
3. Use a Windows VM

### String Analysis
```bash
strings broken_compiler.exe | grep -i "error\|usage"
```

Key findings:
- "Error: stack overflow"
- "Error: stack underflow"  
- "Error: stack empty"
- "Error: unmatched *"
- "Usage: %s <source file>"

This indicates a **stack-based language interpreter**.

### Program Analysis

The `program.wut` file contains:
```
~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`
```

Expected output:
```
This is right! Congratulations!
```

## Language Specification (Reverse Engineered)

Based on the error messages and the program structure, the `.wut` language appears to be:

### Token Types
- `(N` - Push number N onto stack
- `#` - Some operation (possibly print char or operation separator)
- `%` - Operation marker
- `^` - End of operation/statement
- `~` - Start/end of block
- `@` - Operation (possibly add/multiply)
- `*` - Operation (possibly multiply or loop end)
- `!` - Operation (possibly print or negate)
- `$` - Operation (possibly duplicate or swap)
- `` ` `` - End of program

### Analyzing the Program

Let's break down `program.wut`:
```
~~                    # Start block
%(46#%^               # Push 46, operation
(3&@*                 # Push 3, operation with @*
%(20%^                # Push 20, operation
~~#%%!^               # Block with operations
(0$                   # Push 0, $ operation
%(10%^                # Push 10, operation
(83#%^                # Push 83, operation
(2&@*                 # Push 2, operation with @*
%(73%^                # Push 73, operation
(10%^                 # Push 10, operation
(83#%^                # Push 83, operation
(82%^                 # Push 82, operation
~~#%%                 # Block start
(9#%^@@^!^            # Push 9, operations
(12%^                 # Push 12, operation
(1&@*                 # Push 1, operation with @*
%(83#%^@^             # Push 83, operations
(35%^                 # Push 35, operation
(44%^@^               # Push 44, operations
(7#%^                 # Push 7, operation
(11%^                 # Push 11, operation
(17#%^                # Push 17, operation
(19%^!^               # Push 19, operations
(9#%^                 # Push 9, operation
(11#%^                # Push 11, operation
(19%^                 # Push 19, operation
(11#%^                # Push 11, operation
(6%^@^                # Push 6, operations
(5%^                  # Push 5, operation
~~#%`                 # End block and program
```

### Hypothesis: ASCII Character Generation

The expected output "This is right! Congratulations!" has these ASCII values:
- T = 84
- h = 104
- i = 105
- s = 115
- (space) = 32
- etc.

Looking at the numbers in the program:
- 46, 3, 20, 0, 10, 83, 2, 73, 10, 83, 82, 9, 12, 1, 83, 35, 44, 7, 11, 17, 19, 9, 11, 19, 11, 6, 5

These might be:
1. Direct ASCII values
2. Values to be computed (added, multiplied)
3. Offsets or deltas

## The Bug in the Compiler

Since the task is to "fix/rewrite the compiler", there must be a bug in how it interprets the `.wut` language.

Possible bugs:
1. **Wrong operation implementation** - e.g., `@` should add but it multiplies
2. **Wrong stack operation** - push/pop order is incorrect
3. **Wrong character output** - off-by-one error in ASCII conversion
4. **Missing operation** - some operations aren't implemented
5. **Wrong operator precedence** - operations execute in wrong order

## Solution Strategy

### Step 1: Run the Broken Compiler (if possible)

```bash
wine broken_compiler.exe program.wut > current_output.txt
```

Compare `current_output.txt` with `expected_output.txt` to see what's wrong.

### Step 2: Reverse Engineer the Compiler

Use a decompiler like Ghidra or objdump (if we can get it working on macOS):
```bash
objdump -d broken_compiler.exe > disassembly.txt
```

Or use `strings` to find the operation handlers.

### Step 3: Identify the Bug

Common bugs in stack-based interpreters:
- **Off-by-one in ASCII**: Output is shifted by 1 (e.g., 'U' instead of 'T')
- **Wrong arithmetic**: Addition instead of subtraction
- **Stack order**: LIFO vs FIFO confusion
- **Operator confusion**: `@` and `*` swapped

### Step 4: Fix the Compiler

Once we identify the bug, we can either:
1. **Patch the binary** - Change the buggy instruction
2. **Rewrite in C/Python** - Implement the correct interpreter

### Step 5: Write a New Program

Create a program that prints our team name, e.g., "XPLOIT":
```
# Pseudo-code for "XPLOIT"
(88#%^    # X = 88
(80#%^    # P = 80
(76#%^    # L = 76
(79#%^    # O = 79
(73#%^    # I = 73
(84#%^    # T = 84
```

## Deliverables

1. **Fixed Compiler** - Either patched binary or rewritten interpreter
2. **New Program** - `team_name.wut` that prints "XPLOIT" or similar
3. **Documentation** - This file explaining:
   - How we identified the bug
   - What the bug was
   - How we fixed it
   - How the language works
   - How our new program works

## Next Steps

To complete this challenge, we need to:
1. Get the compiler running (Wine, VM, or reverse engineer)
2. See what the current output is
3. Compare with expected output
4. Identify the pattern of the bug
5. Fix it
6. Write new program
7. Document everything

## Language Reference (To Be Completed)

### Operations
- `(N` - Push number N
- `#` - [To be determined]
- `%` - [To be determined]
- `^` - [To be determined]
- `@` - [To be determined]
- `*` - [To be determined]
- `!` - [To be determined]
- `$` - [To be determined]
- `~` - [To be determined]
- `` ` `` - End program

### Example Programs

**Hello World (hypothetical):**
```wut
(72#%^(101#%^(108#%^(108#%^(111#%^`
```

**Team Name:**
```wut
[To be written after understanding the language]
```
