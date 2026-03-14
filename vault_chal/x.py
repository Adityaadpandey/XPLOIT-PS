#!/usr/bin/env python3
"""
Vault Challenge Patcher v2
Patches the unlock_vault_sequence function to bypass the code check
"""

def patch_binary():
    print("[*] Reading binary...")
    with open('chal', 'rb') as f:
        data = bytearray(f.read())
    
    print("[*] Original size:", len(data), "bytes")
    
    # Strategy: Patch the comparison in unlock_vault_sequence
    # At 0x1a8f, there's a JNE (jump if not equal) instruction
    # Original: 75 64 (jne 0x1af5) - jumps to failure if codes don't match
    # We'll change it to: 74 64 (je 0x1af5) - jumps to failure if codes DO match (inverted)
    # Or better: 90 90 (nop nop) - never jump, always continue to success
    
    # First, let's also patch user_authentication_module to call unlock_vault_sequence
    print("\n[*] Patch 1: Redirect user_authentication_module to unlock_vault_sequence")
    source_addr = 0x1936
    target_addr = 0x19f2
    jmp_size = 5
    
    relative_offset = target_addr - (source_addr + jmp_size)
    
    jmp_instruction = bytearray([
        0xE9,  # JMP opcode
        relative_offset & 0xFF,
        (relative_offset >> 8) & 0xFF,
        (relative_offset >> 16) & 0xFF,
        (relative_offset >> 24) & 0xFF
    ])
    
    data[source_addr:source_addr + jmp_size] = jmp_instruction
    print(f"    Patched at 0x{source_addr:x}: JMP to 0x{target_addr:x}")
    
    # Second, patch the comparison to always succeed
    print("\n[*] Patch 2: Bypass unlock code verification")
    comparison_addr = 0x1a8f
    
    # Original: 75 64 (JNE - jump if not equal)
    # Patched:  90 90 (NOP NOP - never jump, always continue)
    data[comparison_addr] = 0x90  # NOP
    data[comparison_addr + 1] = 0x90  # NOP
    
    print(f"    Patched at 0x{comparison_addr:x}: JNE -> NOP NOP")
    print("    Effect: Code check always passes")
    
    # Write patched binary
    output_file = 'chal_patched'
    print(f"\n[*] Writing patched binary to {output_file}...")
    with open(output_file, 'wb') as f:
        f.write(data)
    
    # Make executable
    import os
    os.chmod(output_file, 0o755)
    
    print("[+] Patching complete!")
    print(f"[+] Run the patched binary: ./{output_file}")
    print()
    print("Expected behavior:")
    print("  1. Program jumps directly to unlock_vault_sequence")
    print("  2. Asks for unlock code (enter anything)")
    print("  3. Code check is bypassed (always succeeds)")
    print("  4. Prints: VAULT SYSTEM CLEARED")
    print()
    print("Note: This binary is for Linux. On macOS, use:")
    print("  docker run -it --rm -v $(pwd):/work ubuntu:latest /work/chal_patched")

if __name__ == '__main__':
    try:
        patch_binary()
    except FileNotFoundError:
        print("[!] Error: 'chal' binary not found in current directory")
        print("[!] Make sure you're running this from the vault_chal directory")
    except Exception as e:
        print(f"[!] Error: {e}")
