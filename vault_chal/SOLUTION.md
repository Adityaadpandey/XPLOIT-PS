# Vault Challenge Solution

## Initial Reconnaissance

### File Analysis
```bash
file chal
# Output: ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
```

The binary is a 64-bit Linux ELF executable that's not stripped, meaning function names are preserved.

### String Analysis
```bash
strings chal | grep -i "vault\|clear\|bypass\|success"
```

Key findings:
- Target message: "VAULT SYSTEM CLEARED."
- "All authentication layers bypassed successfully."
- Function names: `unlock_vault_sequence`, `check_vault_state`, `unlock_backup_vault`
- Anti-debugging: "[-] FATAL: Kernel level debugger detected"
- Uses ptrace for anti-debugging

### Disassembly Overview
```bash
objdump -d chal -M intel > disassembly.txt
```

## Function Map

### Main Function (0x1b0e)
The main function calls multiple security checks in sequence:
1. `emit_system_diagnostics` - Prints system info
2. `check_vault_state` - Checks for `.vault_state` file
3. `initialize_telemetry` - Sets up monitoring
4. `verify_network_cert` - Checks for certificate
5. `init_secure_channel` - Initializes crypto
6. `scan_memory_integrity` - Memory checks
7. `load_crypto_module` - Loads crypto module
8. `compute_session_hash` - Computes session hash
9. `destroy_secure_channel` - Cleanup
10. `omega_protocol_legacy` - Legacy protocol handler
11. `security_watchdog` - Anti-debugging check (calls ptrace)
12. `user_authentication_module` - Calls `unlock_vault_sequence`

### Critical Function: unlock_vault_sequence (0x19f2)

This is where the vault unlock logic resides.

**Pseudocode:**
```c
void unlock_vault_sequence() {
    uint8_t g_pid_seed = *0x4028;      // Global variable
    uint8_t g_vault_byte = *0x4029;    // Global variable
    char *argv0 = g_argv0;              // Program name
    
    // Compute expected unlock code
    uint8_t expected = g_pid_seed ^ g_vault_byte ^ strlen(argv0);
    
    printf("Vault Unlock Code: ");
    char input[16];
    fgets(input, 16, stdin);
    
    // Convert input to long, take lowest byte
    uint8_t user_code = (uint8_t)strtol(input, NULL, 0);
    
    // Compare
    if (user_code == expected) {
        puts("****");
        puts("  VAULT SYSTEM CLEARED.");
        puts("  All authentication layers bypassed successfully.");
        puts("  Document ID: XPLOIT-2026-VAULT-OMEGA");
        puts("  Timestamp: [REDACTED]");
        puts("  Operator: Level 999 Admin");
        exit(0);
    } else {
        puts("[-] Vault unlock failed. Access denied.");
        exit(1);
    }
}
```

### Anti-Debugging: security_watchdog (0x18ef)

```c
void security_watchdog() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        puts("[-] FATAL: Kernel level debugger detected. Self-destructing.");
        exit(1);
    }
}
```

This function calls `ptrace(PTRACE_TRACEME)` which fails if a debugger is already attached.

## Solution Approaches

### Approach 1: Calculate the Correct Unlock Code (Recommended)

Since we need to find `g_pid_seed`, `g_vault_byte`, and `strlen(argv[0])`:

1. **Extract global variables from binary:**
```bash
objdump -s -j .data chal
objdump -s -j .bss chal
```

2. **Find where these are initialized:**
```bash
objdump -d chal -M intel | grep -A 10 "4028\|4029"
```

Looking at the code, these values are set by earlier functions in main.

3. **Trace the initialization:**
- `g_pid_seed` (0x4028) is set by `getpid()` in one of the init functions
- `g_vault_byte` (0x4029) is set from the `.vault_state` file or computed
- `argv[0]` is stored at `g_argv0` (0x4020)

### Approach 2: Patch the Binary (Bypass)

**Change 1: Skip the anti-debugging check**

Location: `0x1a8f` in `unlock_vault_sequence`
```
Original: 75 64    jne 0x1af5  (jump if not equal -> fail)
Patched:  74 64    je  0x1af5  (jump if equal -> inverted logic)
```

Or better:
```
Original: 75 64    jne 0x1af5
Patched:  90 90    nop nop     (never jump, always succeed)
```

**Change 2: Bypass ptrace anti-debug**

Location: In `security_watchdog` function
Find the check after ptrace call and NOP it out, or use LD_PRELOAD.

**Python patching script:**
```python
#!/usr/bin/env python3
with open('chal', 'rb') as f:
    data = bytearray(f.read())

# Find file offset for virtual address 0x1a8f
# Using: readelf -S chal | grep .text
# .text section: file offset 0x1000, vaddr 0x1000
# So file offset = 0x1a8f - 0x1000 + 0x1000 = 0x1a8f

# Patch: change JNE to JE (or NOP)
offset = 0x1a8f
data[offset] = 0x90  # NOP
data[offset+1] = 0x90  # NOP

with open('chal_patched', 'wb') as f:
    f.write(data)

import os
os.chmod('chal_patched', 0o755)
```

### Approach 3: LD_PRELOAD Bypass

Create a library that overrides ptrace and strcmp:

```c
// bypass.c
#include <sys/ptrace.h>

long ptrace(enum __ptrace_request request, ...) {
    return 0;  // Always succeed
}
```

Compile and use:
```bash
gcc -shared -fPIC -o bypass.so bypass.c
LD_PRELOAD=./bypass.so ./chal
```

## The Unlock Code Calculation

To find the actual unlock code, we need to:

1. **Run the binary once to create `.vault_state` file**
2. **Extract the values from memory or the state file**
3. **Calculate: code = g_pid_seed ^ g_vault_byte ^ strlen(argv[0])**

The program name length varies based on how it's invoked:
- `./chal` = 6 characters
- `/full/path/to/chal` = varies

## Final Solution Steps

1. Create `.vault_state` file if needed (run once and let it fail)
2. Use GDB to extract runtime values:
```bash
gdb ./chal
break *0x1a31  # Right after expected code is computed
run
x/xb $rbp-0x32  # Print expected value
```

3. Or patch the binary to always succeed (see Approach 2)

4. Or calculate manually by tracing all initialization functions

## Verification

Success output:
```
****
  VAULT SYSTEM CLEARED.
  All authentication layers bypassed successfully.
  Document ID: XPLOIT-2026-VAULT-OMEGA
  Timestamp: [REDACTED]
  Operator: Level 999 Admin
```

## Tools Used
- `file` - Identify binary type
- `strings` - Extract readable strings
- `objdump` - Disassemble and analyze sections
- `readelf` - Analyze ELF structure
- `gdb` - Dynamic analysis
- Python - Binary patching
- `nm` - Symbol table analysis

## Key Insights

1. The binary uses multiple layers of obfuscation but the core logic is simple XOR
2. Anti-debugging via ptrace can be bypassed with LD_PRELOAD
3. The "correct" solution involves understanding the full initialization chain
4. The "fast" solution is to patch the conditional jump
5. All security checks are sequential - bypassing one doesn't affect others
