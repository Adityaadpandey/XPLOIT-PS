---
name: jailbreak-bypass
description: >
  Techniques for breaking through software restrictions, bypassing protections, and unlocking
  disabled features in competitive challenge contexts. Use this skill when a challenge requires:
  bypassing license checks, circumventing access controls, removing feature gates, cracking
  simple protection schemes, disabling anti-tampering checks, or unlocking hidden functionality.
  Trigger on: "bypass", "unlock", "jailbreak", "crack", "remove restriction", "disable check",
  "get past protection", "license bypass", "access denied but need access", or any challenge
  involving defeating software protection mechanisms.
---

# Jailbreaking — Bypassing Protections & Unlocking Features

## Phase 1: Identify the Protection

### Step 1 — Find the gate

Every protection has a decision point. Find it.

```bash
# Search for telltale strings
strings binary | grep -iE 'license|trial|expire|invalid|denied|locked|premium|register|key|serial|access|unauthorized|disabled'

# Search in source code
grep -rn 'if.*license\|if.*auth\|if.*valid\|if.*check\|if.*verify\|is_registered\|is_premium\|FEATURE_' .

# Find comparison/check functions
objdump -d -M intel binary | grep -B5 -A5 'call.*check\|call.*valid\|call.*verify\|call.*auth'
```

### Step 2 — Classify the protection type

| Type               | Indicators                        | Approach                                |
| ------------------ | --------------------------------- | --------------------------------------- |
| Boolean flag check | `if (licensed)`, `if (flag == 1)` | Flip the flag                           |
| String comparison  | `strcmp(input, "secret")`         | Extract the secret or bypass compare    |
| Crypto validation  | Hash, HMAC, signature check       | Find weakness or bypass check           |
| Time-based trial   | `time()`, date comparison         | Patch time check or set system time     |
| Environment check  | `getenv()`, file existence        | Set env var or create expected file     |
| Network validation | `connect()`, HTTP request         | Patch out network call or fake response |
| Obfuscated check   | Encoded strings, indirect calls   | Deobfuscate first, then bypass          |

---

## Phase 2: Bypass Techniques

### Technique 1 — Conditional Flip (fastest, most common)

```bash
# Find the critical jump in disassembly
objdump -d -M intel binary | grep -B10 'Licensed\|Access Denied\|Invalid'
```

```python
# Flip JNE (75) to JE (74) or vice versa
with open('binary', 'rb') as f:
    data = bytearray(f.read())
data[offset] = 0x74 if data[offset] == 0x75 else 0x75
with open('binary_patched', 'wb') as f:
    f.write(data)
```

### Technique 2 — NOP Sled (remove the check entirely)

```python
# NOP out the entire check (replace with 0x90)
for i in range(length):
    data[start + i] = 0x90
```

### Technique 3 — Return Value Override

```python
# Make check function always return 1 (success)
# Replace start with: mov eax, 1; ret → B8 01 00 00 00 C3
patch = b'\xB8\x01\x00\x00\x00\xC3'
data[func_offset:func_offset+len(patch)] = patch
```

### Technique 4 — GDB Runtime Bypass

```bash
gdb ./binary
break *check_license
commands
  set $rax = 1      # Force return success
  return
end
run
```

### Technique 5 — Environment Manipulation

```bash
# If program checks for license file, env var, etc.
echo "VALID" > /tmp/license.key
export LICENSE_KEY="anything"
export REGISTERED=1

# Run with modified environment
env LICENSE=1 PREMIUM=true ./binary
```

### Technique 6 — LD_PRELOAD Override

```c
// bypass.c — Override library functions
// gcc -shared -fPIC -o bypass.so bypass.c
#include <string.h>
#include <time.h>

int strcmp(const char *s1, const char *s2) { return 0; }  // Always match
time_t time(time_t *t) {                                    // Fake time
    time_t fake = 1609459200;
    if (t) *t = fake;
    return fake;
}
int check_license() { return 1; }
int is_registered() { return 1; }
```

```bash
gcc -shared -fPIC -o bypass.so bypass.c
LD_PRELOAD=./bypass.so ./binary
```

### Technique 7 — Python Source Bypass

```python
# Just modify the check directly
def check_license(key):
    return True

# Or extract expected values by adding debug prints
def check_license(key):
    valid_hash = "a1b2c3d4e5..."
    print(f"Expected: {valid_hash}")  # Now we know the target
    return hashlib.sha256(key.encode()).hexdigest() == valid_hash
```

---

## Phase 3: Feature Unlocking

### Finding disabled features

```bash
# Source code feature flags
grep -rn 'ENABLE_\|DISABLE_\|FEATURE_\|#ifdef\|#if 0' . --include='*.c' --include='*.h'
grep -rn '//.*menu\|#.*route\|//.*case' .

# Binary: unreferenced strings may be hidden features
strings binary | sort > all_strings.txt
```

### Activation patterns

```c
// Change these:
#define PREMIUM_FEATURES 0    // → 1
#if 0                         // → #if 1
if (config.trial_mode) {      // → if (!config.trial_mode)
```

```python
FEATURES = {'basic': True, 'premium': False}  # → Set False to True
if user.plan == 'premium':  # → if True:
```

---

## Phase 4: Anti-Debugging Countermeasures

Some challenges detect debugging. Common tricks and counters:

```bash
# ptrace anti-debug: program calls ptrace(PTRACE_TRACEME) to detect debugger
# Counter: LD_PRELOAD a fake ptrace
cat > anti_anti.c << 'EOF'
long ptrace(int request, ...) { return 0; }
EOF
gcc -shared -fPIC -o anti_anti.so anti_anti.c
LD_PRELOAD=./anti_anti.so gdb ./binary
```

```bash
# Timing-based anti-debug: program measures execution time
# Counter: patch out the timing check or set breakpoint after it

# /proc/self/status check: program reads TracerPid
# Counter: run without debugger, use LD_PRELOAD instead
```

---

## Quick Decision Flowchart

```
Protection found
├── Is it a simple boolean check?
│   └── YES → Flip the conditional jump (Technique 1)
├── Is it a function that returns pass/fail?
│   └── YES → Override return value (Technique 3)
├── Does it compare strings?
│   └── YES → Extract expected string, or LD_PRELOAD strcmp (Technique 6)
├── Does it check time/date?
│   └── YES → Fake time with LD_PRELOAD or set system clock
├── Does it check a file/env var?
│   └── YES → Create the expected file/variable (Technique 5)
├── Is it too complex to understand?
│   └── YES → NOP out the entire check (Technique 2)
└── Is it Python/scripted?
    └── YES → Just edit the source (Technique 7)
```
