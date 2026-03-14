#!/usr/bin/env python3

with open('chal', 'rb') as f:
    data = bytearray(f.read())

# Jump to unlock_vault_sequence
offset = 0x1936
rel_offset = 0x19f2 - (0x1936 + 5)
data[offset:offset+5] = [0xE9, rel_offset & 0xFF, (rel_offset >> 8) & 0xFF, (rel_offset >> 16) & 0xFF, (rel_offset >> 24) & 0xFF]

# NOP the check inside unlock_vault_sequence
offset2 = 0x1a8f
data[offset2] = 0x90
data[offset2+1] = 0x90

with open('chal_patched', 'wb') as f:
    f.write(data)

import os
os.chmod('chal_patched', 0o755)
print("Patched with NOPs successfully")
