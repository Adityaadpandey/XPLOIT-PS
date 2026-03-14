---
name: surprise-challenge
description: >
  Meta-skill for tackling unknown, multi-faceted competitive programming challenges worth maximum points.
  Use this skill whenever facing an unfamiliar problem that spans multiple domains, requires creative
  problem-solving, or doesn't fit neatly into other categories. Trigger on: "surprise challenge",
  "wildcard", "mystery problem", "multi-part challenge", "I don't know what category this is",
  or any complex problem requiring rapid decomposition and cross-domain thinking.
---

# Surprise Challenge — 250pt Wildcard Skill

The surprise challenge is the highest-value problem. It rewards creative thinking, speed of
decomposition, and ability to combine techniques from multiple domains. This skill provides
a systematic framework for attacking unknown problems under time pressure.

---

## Phase 1: Rapid Reconnaissance (First 3-5 minutes)

Before writing a single line of code, classify what you're dealing with.

### Step 1 — Identify ALL inputs

```bash
# What files were given?
ls -la
file *            # Identify file types
xxd <file> | head -30   # Check binary headers
strings <file> | head -50  # Extract readable strings
```

### Step 2 — Classify the problem domain

Ask these questions in order:

1. **Is there a binary/executable?** → Likely reverse engineering / patching
2. **Is there source code with bugs?** → Likely code surgery / debugging
3. **Is there encrypted/encoded data?** → Likely crypto / encoding challenge
4. **Is there a network component?** → Likely protocol / communication challenge
5. **Is there a math/logic puzzle?** → Likely algorithmic challenge
6. **Multiple of the above?** → Multi-stage — solve in dependency order

### Step 3 — Map dependencies

Draw a quick dependency graph: what must be solved first to unlock the next stage?
Many surprise challenges are pipelines:
`decode something → patch something → extract flag → prove answer`

---

## Phase 2: Attack Frameworks

### Framework A — Reverse Pipeline

Work BACKWARDS from the desired output:

1. What does the answer look like? (flag format, expected output)
2. What produces that answer? (which function, which file)
3. What does THAT need? (what input, what state)
4. Trace back to what you have

### Framework B — Divide and Conquer

Split multi-part problems:

1. Identify independent subproblems
2. Solve the easiest one first (build momentum + may reveal hints)
3. Look for information leakage between parts

### Framework C — Pattern Recognition

Common surprise challenge archetypes:

- **Layered encoding**: base64 → hex → rot13 → XOR (peel one layer at a time)
- **Polyglot files**: file that's valid in multiple formats
- **Steganography + code**: hidden data in images/audio that feeds into a program
- **Broken crypto**: weak key, known-plaintext, ECB mode, reused nonce
- **State machine puzzles**: navigate states to reach a goal

---

## Phase 3: Essential Toolbox

### Python — Swiss Army Knife

```python
# Quick decode chains
import base64, binascii, codecs, struct, hashlib, itertools

# Decode base64
data = base64.b64decode(encoded)

# XOR with key
def xor_bytes(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

# Brute force single-byte XOR
for k in range(256):
    result = bytes(b ^ k for b in data)
    if b'flag' in result or result.isascii():
        print(f"Key {k}: {result}")

# Frequency analysis
from collections import Counter
Counter(data).most_common(10)

# Struct unpacking (read binary formats)
val = struct.unpack('<I', data[0:4])[0]  # little-endian uint32
```

### C/C++ — Performance-Critical Parts

```c
// Quick compile-and-test cycle
// gcc -o sol sol.c -lm -lpthread && ./sol

// Read entire file into buffer
FILE *f = fopen(argv[1], "rb");
fseek(f, 0, SEEK_END);
long sz = ftell(f);
rewind(f);
char *buf = malloc(sz);
fread(buf, 1, sz, f);
fclose(f);
```

### Binary Inspection

```bash
# Quick binary analysis
objdump -d binary | less          # Disassemble
readelf -a binary                 # ELF structure
strace ./binary 2>&1              # System calls at runtime
ltrace ./binary 2>&1              # Library calls at runtime
gdb -batch -ex 'disas main' binary  # Disassemble main
nm binary                         # Symbol table
```

### Encoding/Crypto Detection

```bash
# Detect encoding
echo "data" | base64 -d 2>/dev/null && echo "Valid base64"
echo "data" | xxd -r -p 2>/dev/null && echo "Valid hex"

# Entropy check (high entropy = encrypted/compressed)
ent <file>

# Check for known file signatures embedded in data
binwalk <file>
```

---

## Phase 4: Time Management Strategy

For a 250pt problem, assume it has 2-4 parts:

| Time Block | Activity                           |
| ---------- | ---------------------------------- |
| 0-5 min    | Reconnaissance — classify and plan |
| 5-20 min   | Solve Part 1 (easiest subproblem)  |
| 20-40 min  | Solve Part 2 (medium subproblem)   |
| 40-55 min  | Solve Part 3+ (hardest parts)      |
| 55-60 min  | Clean up, verify answer, submit    |

**Rules:**

- If stuck on a subpart for >10 min, skip and try another angle
- Re-read the problem statement every 15 min — you may have missed a hint
- Partial credit is better than no credit — submit what you have

---

## Phase 5: Common Traps and Anti-Patterns

1. **Overengineering**: Don't build elegant solutions — build working ones
2. **Tunnel vision**: If your approach isn't working after 10 min, step back
3. **Ignoring hints**: Challenge descriptions often contain critical clues
4. **Not reading error messages**: They frequently reveal what's expected
5. **Forgetting endianness**: x86 is little-endian — watch byte order
6. **Assuming encoding**: Always verify — what looks like base64 might not be
7. **Not checking partial results**: Print intermediates to verify each step

---

## Phase 6: Emergency Techniques

When completely stuck:

```bash
# Grep for anything useful
strings <file> | grep -iE 'flag|key|pass|secret|win|correct'

# Check for hidden files or data
binwalk -e <file>         # Extract embedded files
foremost -i <file>        # Carve files from binary data

# Diff against known-good versions if available
diff -u original.c modified.c
cmp -l file1 file2        # Byte-level comparison

# Brute force if search space is small
python3 -c "
import itertools, string
charset = string.ascii_lowercase + string.digits
for length in range(1, 5):
    for combo in itertools.product(charset, repeat=length):
        candidate = ''.join(combo)
        # test candidate...
"
```

---

## Quick Reference: File Signature Magic Bytes

| Bytes (hex)    | Format                |
| -------------- | --------------------- |
| 89 50 4E 47    | PNG image             |
| FF D8 FF       | JPEG image            |
| 50 4B 03 04    | ZIP / DOCX / JAR      |
| 7F 45 4C 46    | ELF binary            |
| 4D 5A          | PE/Windows executable |
| 23 21          | Shebang script (#!)   |
| 1F 8B          | Gzip compressed       |
| FD 37 7A 58 5A | XZ compressed         |
