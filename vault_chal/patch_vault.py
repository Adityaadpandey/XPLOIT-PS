#!/usr/bin/env python3
"""
Vault Challenge Patcher
Patches the binary to call the hidden unlock_vault_sequence function
"""

def patch_binary():
    print("[*] Reading binary...")
    with open('chal', 'rb') as f:
        data = bytearray(f.read())
    
    print("[*] Original size:", len(data), "bytes")
    
    # Strategy: Replace user_authentication_module with a jump to unlock_vault_sequence
    # user_authentication_module is at 0x1936
    # unlock_vault_sequence is at 0x19f2
    
    # Calculate relative offset for JMP instruction
    # JMP is E9 [4-byte relative offset]
    # Offset is calculated from the END of the JMP instruction
    
    source_addr = 0x1936
    target_addr = 0x19f2
    jmp_size = 5  # E9 + 4 bytes
    
    relative_offset = target_addr - (source_addr + jmp_size)
    
    print(f"[*] Patching at offset 0x{source_addr:x}")
    print(f"[*] Target function at 0x{target_addr:x}")
    print(f"[*] Relative offset: 0x{relative_offset:x} ({relative_offset})")
    
    # Create the JMP instruction
    jmp_instruction = bytearray([
        0xE9,  # JMP opcode
        relative_offset & 0xFF,
        (relative_offset >> 8) & 0xFF,
        (relative_offset >> 16) & 0xFF,
        (relative_offset >> 24) & 0xFF
    ])
    
    print(f"[*] JMP instruction bytes: {' '.join(f'{b:02x}' for b in jmp_instruction)}")
    
    # Apply the patch
    data[source_addr:source_addr + jmp_size] = jmp_instruction
    
    # Write patched binary
    output_file = 'chal_patched'
    print(f"[*] Writing patched binary to {output_file}...")
    with open(output_file, 'wb') as f:
        f.write(data)
    
    # Make executable
    import os
    os.chmod(output_file, 0o755)
    
    print("[+] Patching complete!")
    print(f"[+] Run the patched binary: ./{output_file}")
    print()
    print("Note: This binary is for Linux. On macOS, use:")
    print("  - Docker: docker run -it --rm -v $(pwd):/work ubuntu:latest /work/chal_patched")
    print("  - Or transfer to a Linux system")

if __name__ == '__main__':
    try:
        patch_binary()
    except FileNotFoundError:
        print("[!] Error: 'chal' binary not found in current directory")
        print("[!] Make sure you're running this from the vault_chal directory")
    except Exception as e:
        print(f"[!] Error: {e}")
