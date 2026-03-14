# Vault Challenge - Quick Start Guide

## TL;DR

The success function exists but is never called. Patch the binary to call it.

## 3-Step Solution

### Step 1: Run the Patcher
```bash
cd vault_chal
python3 patch_vault.py
```

### Step 2: Test on Linux
```bash
# Using Docker (easiest on macOS)
docker run -it --rm -v $(pwd):/work ubuntu:latest /work/chal_patched

# Or copy to Linux system
scp chal_patched user@linux-box:~/
ssh user@linux-box './chal_patched'
```

### Step 3: See Success
```
Vault Unlock Code: 123
****
  VAULT SYSTEM CLEARED.
  All authentication layers bypassed successfully.
```

## What the Patch Does

```
Before:  main() → user_authentication_module() → [asks for ID] → exit
After:   main() → user_authentication_module() → JMP → unlock_vault_sequence() → SUCCESS!
```

## Files You Need

- `chal` - Original binary (provided)
- `patch_vault.py` - Patcher script (created)
- `chal_patched` - Patched binary (generated)
- `COMPLETE_SOLUTION.md` - Full writeup (for submission)

## For Submission

Include:
1. `chal_patched` - The working binary
2. `patch_vault.py` - Your patch script
3. `COMPLETE_SOLUTION.md` - Your writeup
4. Screenshots showing:
   - The hidden function in disassembly
   - Proof it's never called
   - Your patch being applied
   - The success message

## Why This Works

The binary has a function called `unlock_vault_sequence` at address `0x19f2` that prints the success message. But nothing ever calls it - it's **dead code**. 

Our patch adds a single JMP instruction at the start of `user_authentication_module` (address `0x1936`) that jumps directly to the hidden function.

## The Key Insight

This isn't about:
- ❌ Calculating the correct unlock code
- ❌ Bypassing anti-debugging
- ❌ Cracking encryption

It's about:
- ✅ Finding dead/orphaned code
- ✅ Resurrecting unused functions
- ✅ Understanding program flow

The challenge tests if you can find code that exists but is never executed, then make it execute.
