# Bad Compiler Challenge - Solution Approach

## Problem Summary

We have:
- `broken_compiler.exe` - A Windows executable (stack-based interpreter)
- `program.wut` - A program in the `.wut` language
- `expected_output.txt` - Should print "This is right! Congratulations!"

Currently, the program produces wrong output (we can't run it on macOS without Wine).

## What We Need To Do

1. **Run the broken compiler** to see current output
2. **Identify the bug** in the compiler
3. **Fix the compiler** (patch binary or rewrite)
4. **Write a new program** that prints our team name
5. **Document everything**

## Analysis So Far

### Language Structure

The `.wut` language appears to be **stack-based** with these tokens:

- `(N` - Push number N onto stack
- `#` - Print top of stack as ASCII character
- `@` - Binary operation (add or multiply?)
- `*` - Binary operation (multiply or add?)
- `&` - Binary operation (swap or multiply?)
- `!` - Print without popping
- `$` - Duplicate top of stack
- `%` - Operation marker/separator
- `^` - End of operation/statement
- `~` - Block marker
- `` ` `` - End of program

### The Bug Hypothesis

Based on analysis, the most likely bugs are:

**Hypothesis 1: Swapped Operations**
- `@` and `*` are swapped (@ should multiply, * should add)
- Or `&` and `@` are swapped

**Hypothesis 2: Wrong Operation Order**
- Operations execute in wrong order (LIFO vs FIFO)

**Hypothesis 3: Off-by-One in ASCII**
- Characters are shifted by some offset

### Evidence

Looking at the program:
```
~~%(46#%^(3&@*%(20%^...
```

- First number with `#` is 46 (prints as '.')
- But we need 'T' = 84
- Difference: 84 - 46 = 38

The numbers 3 and 20 appear between operations `&@*`.
- If `&` = multiply, `@` = add, `*` = execute: 3 * something + 20 = 38?
- 3 * 6 + 20 = 38, but where's 6?

## Solution Steps

### Step 1: Get Current Output

Since we're on macOS, we need to either:
1. Install Wine: `brew install wine-stable`
2. Use a Windows VM
3. Use Docker with Wine

```bash
# With Wine
wine broken_compiler.exe program.wut

# Or Docker
docker run -v $(pwd):/work -w /work tobix/pywine:3.9 \
  wine broken_compiler.exe program.wut
```

### Step 2: Compare Outputs

```bash
wine broken_compiler.exe program.wut > current_output.txt
diff current_output.txt expected_output.txt
```

### Step 3: Identify the Bug

Common bugs in stack interpreters:
- Wrong operation implementation
- Stack order issues
- Off-by-one errors
- Operator precedence

### Step 4: Fix Options

**Option A: Patch the Binary**
If the bug is a simple operation swap:
```python
# Find the operation handlers in the binary
# Swap the opcodes or operation implementations
```

**Option B: Rewrite the Interpreter**
Write a correct interpreter in Python/C:
```python
# See wut_fixed.py for template
```

### Step 5: Write New Program

Once we understand the language, write a program that prints "XPLOIT" or team name:

```wut
# Pseudo-code (actual syntax depends on what we learn)
(88#  # X = 88
(80#  # P = 80
(76#  # L = 76
(79#  # O = 79
(73#  # I = 73
(84#  # T = 84
`
```

## Next Steps

1. **Install Wine** or set up Windows environment
2. **Run the broken compiler** to see actual output
3. **Identify the specific bug** by comparing outputs
4. **Fix the compiler**
5. **Test with program.wut**
6. **Write team name program**
7. **Document the bug and fix**

## Deliverables

1. **Fixed compiler** - Either:
   - Patched `broken_compiler.exe`
   - Or new interpreter (`wut_interpreter.py` or `wut_interpreter.c`)

2. **New program** - `team_name.wut` that prints team name

3. **Documentation** - Explaining:
   - How the language works
   - What the bug was
   - How we fixed it
   - How our new program works

## Tools Needed

- Wine (for running Windows .exe on macOS/Linux)
- Python (for analysis and possibly rewriting)
- Hex editor (if patching binary)
- Disassembler (if reverse engineering binary)

## Current Status

- ✅ Analyzed program structure
- ✅ Identified token types
- ✅ Created analysis scripts
- ❌ Need to run broken compiler to see actual output
- ❌ Need to identify specific bug
- ❌ Need to fix compiler
- ❌ Need to write new program
