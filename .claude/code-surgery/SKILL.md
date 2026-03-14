---
name: frankenstein-fusion
description: >
  Techniques for combining components from multiple programs into a working hybrid solution.
  Use this skill when a challenge requires: merging code from different sources, integrating
  modules with different interfaces, resolving dependency conflicts between combined codebases,
  creating adapter layers between incompatible components, or building a working program from
  parts of several programs. Trigger on: "combine", "merge programs", "integrate", "hybrid",
  "Frankenstein", "stitch together", "use parts from both", "make these work together",
  or any task involving fusing components from multiple software sources.
---

# Frankenstein Fusion — Combining Components Into Hybrid Solutions

## Phase 1: Component Inventory

### Step 1 — Map each program's pieces

For each source program, identify:

```bash
# List all functions/classes and their signatures
grep -n 'def \|class ' program_a/*.py
grep -n '^[a-zA-Z_].*(' program_a/*.c | grep '{'

# Identify inputs and outputs of each component
# What does it read? (stdin, files, args, env)
grep -n 'input\|argv\|open\|read\|stdin\|getenv' program_a/*

# What does it produce? (stdout, files, return values)
grep -n 'print\|write\|return\|stdout' program_a/*

# What dependencies does each have?
grep -n 'import\|#include\|require' program_a/*
```

### Step 2 — Identify the fusion targets

Decide which component from which program:

```
Program A: [ Module 1 ] → [ Module 2 ] → [ Module 3 ]
Program B: [ Module X ] → [ Module Y ] → [ Module Z ]

Goal:      [ Module 1 ] → [ Module Y ] → [ Module 3 ]
                            ↑ from B        ↑ from A
```

### Step 3 — Check interface compatibility

```python
# Compare function signatures at the join points
# Program A's Module 2 output → must match → Program B's Module Y input

# A outputs:
def module_2_output() -> list[int]:  # returns list of ints

# B expects:
def module_y_input(data: str):  # expects a string!

# → INCOMPATIBLE: need an adapter (see Phase 2)
```

---

## Phase 2: Fusion Techniques

### Technique 1 — Direct Splice (compatible interfaces)

When components have matching input/output types:

```python
# From program A
from program_a.parser import parse_input

# From program B
from program_b.processor import process_data

# From program A
from program_a.formatter import format_output

# Fused pipeline
def main():
    raw = parse_input(sys.argv[1])      # A's parser
    result = process_data(raw)            # B's processor
    output = format_output(result)        # A's formatter
    print(output)
```

```c
// C version — include headers from both, link objects
#include "program_a/parser.h"
#include "program_b/processor.h"
#include "program_a/formatter.h"

int main(int argc, char **argv) {
    Data *raw = parse_input(argv[1]);
    Result *res = process_data(raw);
    format_output(res);
    return 0;
}
```

```bash
# Compile and link objects from both programs
gcc -c program_a/parser.c -o parser.o
gcc -c program_b/processor.c -o processor.o
gcc -c program_a/formatter.c -o formatter.o
gcc -c fused_main.c -o main.o
gcc main.o parser.o processor.o formatter.o -o hybrid
```

### Technique 2 — Adapter Layer (incompatible interfaces)

```python
# A outputs dict, B expects list of tuples
def adapt_a_to_b(a_output: dict) -> list:
    """Bridge between A's output format and B's input format"""
    return [(k, v) for k, v in a_output.items()]

# Use in pipeline
raw = program_a_function(input)
adapted = adapt_a_to_b(raw)
result = program_b_function(adapted)
```

```c
// C adapter: convert between struct types
struct TypeA { int x; int y; };       // From program A
struct TypeB { float coords[2]; };     // Expected by program B

struct TypeB adapt(struct TypeA a) {
    struct TypeB b;
    b.coords[0] = (float)a.x;
    b.coords[1] = (float)a.y;
    return b;
}
```

### Technique 3 — Process Pipeline (keep programs separate)

When integration is too complex, pipe between processes:

```bash
# Run A's output into B's input
./program_a input.txt | ./program_b > output.txt

# With intermediate processing
./program_a input.txt | python3 adapter.py | ./program_b > output.txt
```

```python
# adapter.py — transform between formats
import sys, json

# Read A's output format
data = json.loads(sys.stdin.read())

# Convert to B's expected format
converted = {"values": [item["val"] for item in data["items"]]}

# Write B's input format
print(json.dumps(converted))
```

### Technique 4 — Shared State (when components need to communicate)

```python
# Create a shared context object
class FusionContext:
    def __init__(self):
        self.data = {}
        self.state = {}

ctx = FusionContext()

# Component from A writes
program_a.initialize(ctx)
ctx.data['parsed'] = program_a.parse(input_file)

# Component from B reads and writes
result = program_b.process(ctx.data['parsed'])
ctx.data['processed'] = result

# Component from A reads
program_a.output(ctx.data['processed'])
```

```c
// C: shared state via global struct or passed pointer
typedef struct {
    int *data;
    int size;
    int flags;
} SharedState;

// Both components receive the same state pointer
void component_a_init(SharedState *s);
void component_b_process(SharedState *s);
void component_a_finalize(SharedState *s);
```

### Technique 5 — Namespace Collision Resolution

```bash
# Both programs define a function with the same name!
# Check for collisions
comm -12 <(nm program_a.o | awk '{print $3}' | sort) \
         <(nm program_b.o | awk '{print $3}' | sort)
```

```c
// Fix: rename at source level
// In program_b's code, rename conflicting function
#define helper_function program_b_helper_function
#include "program_b/utils.c"
#undef helper_function

// Or use static to limit scope
// Modify the source to make conflicting functions static
static int helper_function(int x) { ... }
```

```python
# Python: use aliased imports
from program_a.utils import process as process_a
from program_b.utils import process as process_b

result = process_a(data)    # A's version
result = process_b(data)    # B's version
```

---

## Phase 3: Dependency Resolution

### Resolving conflicting includes/imports

```bash
# Find all dependencies for each component
# C: recursively find includes
gcc -M program_a/component.c   # Lists all headers needed
gcc -M program_b/component.c

# Check for conflicts (same header name, different content)
find . -name '*.h' | xargs md5sum | sort | uniq -D -w32
```

### Resolving conflicting globals

```c
// Both programs define 'int count;' globally
// Fix 1: Make one static
static int count;  // Now scoped to this file

// Fix 2: Rename
int count_a;  // For program A's component
int count_b;  // For program B's component

// Fix 3: Wrap in namespace struct
struct ProgramA { int count; } a_state;
struct ProgramB { int count; } b_state;
```

---

## Phase 4: Integration Testing

```bash
# Test each component individually first
echo "test" | ./component_a    # Does A's part work alone?
echo "test" | ./component_b    # Does B's part work alone?

# Test the adapter
echo "test" | ./component_a | python3 adapter.py  # Does conversion work?

# Test the full pipeline
echo "test" | ./hybrid

# Compare against expected output
diff <(echo "test" | ./hybrid) expected_output.txt
```

---

## Fusion Checklist

Before submitting, verify:

- [ ] All components compile/import without errors
- [ ] No symbol/name collisions
- [ ] Data flows correctly between components (types match or are adapted)
- [ ] No memory leaks from mismatched alloc/free between components
- [ ] Error handling bridges between different error conventions
- [ ] The hybrid produces correct output for known test inputs
