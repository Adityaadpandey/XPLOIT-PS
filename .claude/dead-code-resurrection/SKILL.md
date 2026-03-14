---
name: dead-code-resurrection
description: >
  Finding and reactivating commented-out, removed, or orphaned functionality in large codebases.
  Use this skill when a challenge involves: finding hidden or disabled code, reactivating removed
  features, tracing git history to recover deleted functions, identifying unreachable code paths,
  or reconnecting orphaned functions. Trigger on: "dead code", "commented out", "find removed feature",
  "resurrect", "reactivate", "git history", "deleted function", "orphan code", "unused function",
  or any task about recovering and re-enabling previously existing functionality.
---

# Dead Code Resurrection — Finding & Reactivating Hidden Functionality

## Phase 1: Archaeological Survey

### Hunting commented-out code

```bash
# C/C++ block comments
grep -rn '/\*' . --include='*.c' --include='*.h' | head -30

# C/C++ line comments hiding code (lines that look like code)
grep -rn '//.*return\|//.*if\|//.*for\|//.*while\|//.*printf\|//.*call' . --include='*.c'

# Python commented code
grep -rn '#.*def \|#.*return\|#.*import\|#.*class \|#.*if \|#.*for ' . --include='*.py'

# Multi-line disabled blocks
grep -rn '#if 0' . --include='*.c' --include='*.h'

# Find triple-quoted strings that might be disabled code (Python)
grep -rn '"""' . --include='*.py' | head -20
```

### Finding orphaned functions

```bash
# C: Functions defined but never called
# Step 1: List all function definitions
grep -rn '^[a-zA-Z_].*(' . --include='*.c' | grep -v '//' | grep '{' > all_defs.txt

# Step 2: For each function, check if it's called anywhere
while IFS= read -r line; do
    func=$(echo "$line" | sed 's/.*\s\+\([a-zA-Z_][a-zA-Z_0-9]*\)\s*(.*/\1/')
    count=$(grep -rn "$func" . --include='*.c' --include='*.h' | grep -v 'define\|^.*:.*\bint\b\|^.*:.*\bvoid\b\|^.*:.*\bchar\b' | wc -l)
    if [ "$count" -le 1 ]; then
        echo "ORPHANED: $func — $line"
    fi
done < all_defs.txt

# Python: Functions defined but never called
grep -rn 'def ' . --include='*.py' | while read line; do
    func=$(echo "$line" | sed 's/.*def \([a-zA-Z_]*\).*/\1/')
    count=$(grep -rn "$func" . --include='*.py' | wc -l)
    if [ "$count" -le 1 ]; then
        echo "ORPHANED: $func — $line"
    fi
done
```

### Git archaeology (if repo has history)

```bash
# Find deleted functions
git log --all --diff-filter=D -- '*.c' '*.py'     # Deleted files
git log -p --all -S 'function_name'                 # When a string was added/removed
git log -p --all --grep='remove\|disable\|delete'   # Commits about removal

# Recover a deleted file
git log --all --full-history -- '**/filename*'       # Find the commit
git show <commit>^:path/to/file > recovered_file     # Recover it

# See what changed in a specific file over time
git log -p --follow -- path/to/file

# Find when a specific function was removed
git log -p --all -S 'void secret_feature' -- '*.c'

# Diff between versions to see what was removed
git diff HEAD~10 HEAD -- file.c | grep '^-' | grep -v '^---'
```

---

## Phase 2: Resurrection Techniques

### Technique 1 — Uncomment and reconnect

```c
// FOUND: commented-out function
/*
void secret_feature(int x) {
    printf("Secret: %d\n", x * 42);
}
*/

// STEP 1: Uncomment it
void secret_feature(int x) {
    printf("Secret: %d\n", x * 42);
}

// STEP 2: Find where it should be called
// Look for similar functions that ARE called — the dead code likely
// was called from the same place
grep -n 'regular_feature\|normal_feature' main.c
// If regular_feature() is called at line 100, secret_feature() probably goes nearby

// STEP 3: Add the call
// In main() or wherever appropriate:
secret_feature(input);
```

### Technique 2 — Reactivate #if 0 blocks

```c
// FOUND:
#if 0
void hidden_mode(void) {
    // ... lots of code ...
}
#endif

// FIX: Change to #if 1
#if 1
void hidden_mode(void) {
    // ... lots of code ...
}
#endif

// Then call it from the appropriate location
```

### Technique 3 — Reconnect orphaned functions

```python
# FOUND: Function exists but is never called
def process_secret_data(data):
    return [chr(b ^ 0x42) for b in data]

# STEP 1: Find where similar functions are called
# grep for 'process_' to find the call pattern
# Example: process_normal_data(data) is called in main()

# STEP 2: Add the call at the right place
def main():
    data = read_input()
    result = process_normal_data(data)
    secret = process_secret_data(data)  # ADD THIS
    print(secret)                        # AND THIS
```

### Technique 4 — Recover from git and integrate

```bash
# 1. Find the removed code
git log -p --all -S 'feature_name' > history.txt

# 2. Extract the old version
git show <old_commit>:path/to/file > old_version.c

# 3. Diff to see exactly what was removed
diff -u old_version.c current_version.c

# 4. Carefully reapply the removed parts
# Watch for API changes since the code was removed!
```

---

## Phase 3: Making It Work Again

### Common resurrection problems

**Problem 1: Missing dependencies**

```bash
# Dead code references functions/variables that were also removed
grep -rn 'undefined reference' build_output.txt
# Fix: find and resurrect dependencies too, or implement stubs
```

**Problem 2: API changes since code was disabled**

```c
// Old code used old_api_v1() which no longer exists
// Find what replaced it:
grep -rn 'old_api\|new_api\|v2' . --include='*.h'
// Update the dead code to use the current API
```

**Problem 3: Missing includes/imports**

```bash
# Compiler errors about unknown types or functions
# Check what headers the dead code needs
grep -B20 'dead_function' file.c | grep '#include'
```

**Problem 4: Type mismatches**

```c
// Dead code expected int, current code uses size_t
// Fix: add appropriate casts
size_t result = (size_t)dead_function(args);
```

---

## Phase 4: Validation

```bash
# Compile and check for warnings
gcc -Wall -Wextra -o resurrected *.c

# Run and verify the dead code actually does something
./resurrected

# Compare output with and without the resurrected code
diff <(./original_binary) <(./resurrected)
```

---

## Search Pattern Quick Reference

| Looking for...        | Command                                            |
| --------------------- | -------------------------------------------------- |
| Commented C code      | `grep -rn '//.*return\|/\*' --include='*.c'`       |
| Commented Python code | `grep -rn '#.*def \|#.*return' --include='*.py'`   |
| #if 0 blocks          | `grep -rn '#if 0' --include='*.c' --include='*.h'` |
| Orphan functions      | Compare definitions vs call sites                  |
| Git-deleted code      | `git log -p --all -S 'search_term'`                |
| TODO/FIXME markers    | `grep -rn 'TODO\|FIXME\|DISABLED\|REMOVED' .`      |
| Dead imports          | `grep -rn 'import' --include='*.py'` + check usage |
