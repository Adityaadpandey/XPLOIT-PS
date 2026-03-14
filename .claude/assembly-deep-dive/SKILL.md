---
name: assembly-deep-dive
description: >
  Skill for analyzing, understanding, and manipulating low-level assembly code (x86, x86_64, ARM)
  to achieve specific objectives. Use whenever a challenge involves: disassembly, reverse engineering
  binaries, reading/writing assembly instructions, patching machine code, understanding calling
  conventions, stack frames, or register usage. Trigger on: "assembly", "disassemble", "binary
  analysis", "machine code", "registers", "objdump", "gdb", "reverse engineer this binary",
  "what does this binary do", "patch this executable", or any task involving low-level code analysis.
---

# Assembly Deep Dive — Low-Level Code Analysis & Manipulation

## Essential Tool Commands

### Disassembly

```bash
# Disassemble entire binary (Intel syntax — easier to read)
objdump -d -M intel binary

# Disassemble just main
objdump -d -M intel binary | sed -n '/<main>:/,/^$/p'

# Disassemble specific function
objdump -d -M intel binary | sed -n '/<function_name>:/,/^$/p'

# With source interleaving (if compiled with -g)
objdump -d -S -M intel binary

# Show all sections
objdump -h binary

# Show only .text (code) section
objdump -d -j .text -M intel binary
```

### Binary Inspection

```bash
readelf -h binary        # ELF header (arch, entry point)
readelf -s binary        # Symbol table
readelf -S binary        # Section headers
readelf -l binary        # Program headers (segments)
nm binary               # Symbols (functions, globals)
nm -C binary            # Demangled C++ symbols
strings binary          # All printable strings
strings -t x binary     # Strings with hex offsets
```

### GDB Essentials

```bash
gdb ./binary
# Inside GDB:
set disassembly-flavor intel
disas main                    # Disassemble main
break *0x401234               # Break at address
break main                    # Break at function
run                           # Start execution
run arg1 arg2                 # Run with arguments
stepi                         # Step one instruction
nexti                         # Step over call
info registers                # Show all registers
x/20i $rip                    # Show 20 instructions from current position
x/10wx $rsp                   # Show 10 words on stack
x/s 0x402000                  # Show string at address
print $rax                    # Print register value
set $rax = 0x1                # Modify register
set *(int*)0x601040 = 42      # Modify memory
```

---

## x86_64 Quick Reference

### Registers

| Register | Purpose | Calling Convention |
|---|---|---|
| rax | Return value | Return value |
| rdi | General | 1st argument |
| rsi | General | 2nd argument |
| rdx | General | 3rd argument |
| rcx | General | 4th argument |
| r8 | General | 5th argument |
| r9 | General | 6th argument |
| rsp | Stack pointer | — |
| rbp | Base pointer | — |
| rip | Instruction pointer | — |

32-bit lower halves: eax, edi, esi, edx, ecx, esp, ebp
16-bit: ax, di, si, dx, cx, sp, bp
8-bit: al, ah, dl, dh, cl, ch

### Common Instruction Patterns

**Function prologue:**
```asm
push   rbp
mov    rbp, rsp
sub    rsp, 0x20      ; Allocate 32 bytes of local space
```

**Function epilogue:**
```asm
leave                  ; mov rsp, rbp; pop rbp
ret                    ; Pop return address, jump to it
```

**Function call (System V AMD64 ABI):**
```asm
mov    edi, 5          ; arg1 = 5
mov    esi, 10         ; arg2 = 10
call   my_function     ; Return value in rax
```

**If/else:**
```asm
cmp    eax, 5          ; Compare eax with 5
jne    .else_branch    ; Jump if not equal
; ... then block ...
jmp    .end_if
.else_branch:
; ... else block ...
.end_if:
```

**For loop (i = 0; i < n; i++):**
```asm
mov    ecx, 0          ; i = 0
.loop_start:
cmp    ecx, [rbp-4]    ; i < n?
jge    .loop_end        ; Exit if i >= n
; ... loop body ...
inc    ecx              ; i++
jmp    .loop_start
.loop_end:
```

**Array access arr[i]:**
```asm
mov    eax, [rbx + rcx*4]   ; Load arr[i] (4 bytes per int)
; rbx = base address, rcx = index, *4 = sizeof(int)
```

### Jump Condition Cheat Sheet

| Instruction | Condition | Meaning |
|---|---|---|
| je / jz | ZF=1 | Equal / Zero |
| jne / jnz | ZF=0 | Not equal / Not zero |
| jg / jnle | ZF=0, SF=OF | Greater (signed) |
| jge / jnl | SF=OF | Greater or equal (signed) |
| jl / jnge | SF≠OF | Less (signed) |
| jle / jng | ZF=1 or SF≠OF | Less or equal (signed) |
| ja / jnbe | CF=0, ZF=0 | Above (unsigned) |
| jae / jnb | CF=0 | Above or equal (unsigned) |
| jb / jnae | CF=1 | Below (unsigned) |
| jbe / jna | CF=1 or ZF=1 | Below or equal (unsigned) |

---

## ARM Quick Reference (if needed)

```
Registers: r0-r12 (general), r13/sp, r14/lr, r15/pc
Arguments: r0-r3 (first 4 args), stack for rest
Return: r0

Common instructions:
  MOV r0, #5        ; r0 = 5
  LDR r0, [r1]      ; r0 = *r1
  STR r0, [r1]      ; *r1 = r0
  ADD r0, r1, r2     ; r0 = r1 + r2
  CMP r0, #10        ; Compare r0 with 10
  BEQ label          ; Branch if equal
  BL function        ; Branch and link (call)
  BX lr              ; Return
```

---

## Pattern Recognition — What Does This Code Do?

### String comparison
```asm
; Often uses repe cmpsb or a loop comparing byte-by-byte
mov    rsi, addr1     ; String 1
mov    rdi, addr2     ; String 2
mov    rcx, length
repe   cmpsb          ; Compare strings
je     strings_equal
```

### Password/key check
```asm
; XOR or arithmetic transformation then comparison
movzx  eax, byte [rdi + rcx]   ; Load input char
xor    eax, 0x42                ; Transform it
cmp    al, byte [rsi + rcx]    ; Compare with expected
jne    wrong_password
```

### malloc + initialization
```asm
mov    edi, 100       ; Size = 100
call   malloc
mov    [rbp-8], rax   ; Store pointer
; Then typically memset or loop initialization
```

---

## Binary Patching Techniques

### Method 1 — Patch with Python

```python
# Read binary, modify bytes, write back
with open('binary', 'rb') as f:
    data = bytearray(f.read())

# NOP out an instruction (0x90 = NOP in x86)
offset = 0x1234  # File offset of instruction
data[offset] = 0x90
data[offset+1] = 0x90

# Change a conditional jump to unconditional
# JNE (0x75) -> JMP short (0xEB)
data[offset] = 0xEB

# Invert a condition: JE (0x74) -> JNE (0x75) or vice versa
data[offset] = 0x75

# Write patched binary
with open('binary_patched', 'wb') as f:
    f.write(data)

import os
os.chmod('binary_patched', 0o755)
```

### Method 2 — Patch with dd

```bash
# Write single byte at offset
printf '\xEB' | dd of=binary bs=1 seek=$((0x1234)) count=1 conv=notrunc
```

### Method 3 — Patch in GDB at runtime

```bash
# In GDB, skip a check entirely:
break *0x401234
commands
  set $rip = 0x401240    # Jump past the check
  continue
end
run
```

### Common Patch Patterns

| Goal | Original | Patched |
|---|---|---|
| Skip a check | `jne fail` (75 XX) | `jmp over` (EB XX) or NOP (90 90) |
| Invert condition | `je target` (74 XX) | `jne target` (75 XX) |
| Always true | `test eax,eax; jne` | `xor eax,eax; je` (31 C0 + 74 XX) |
| Always return 1 | function body | `mov eax,1; ret` (B8 01 00 00 00 C3) |
| Always return 0 | function body | `xor eax,eax; ret` (31 C0 C3) |
| NOP slide | any instruction | 90 90 90 ... (fill with NOPs) |

### Offset Calculation

```bash
# File offset vs Virtual address
# VA = file_offset - section_file_offset + section_vaddr
# Use readelf to get section info:
readelf -S binary | grep .text
# Example: .text at file offset 0x1000, vaddr 0x401000
# To patch VA 0x401234: file_offset = 0x401234 - 0x401000 + 0x1000 = 0x1234
```

---

## Decompilation Strategy

When you can't use Ghidra/IDA, mentally decompile:

1. **Identify function boundaries** (prologue/epilogue)
2. **Map registers to variables** (rdi=arg1, [rbp-4]=local_var)
3. **Identify control flow** (jumps = if/else/loops)
4. **Recognize library calls** (call printf, call malloc)
5. **Reconstruct in pseudocode**, then refine to C

```
Example mental decompilation:
  mov    edi, [rbp-4]     →  arg = local_var
  call   validate         →  result = validate(arg)
  test   eax, eax         →  if (result == 0)
  je     .fail            →      goto fail
  ⇒ if (validate(local_var) != 0) { ... }
```
