#!/usr/bin/env python3
"""
Detailed analysis of the .wut program structure
"""

program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
expected = "This is right! Congratulations!"

print("Let's look at the structure more carefully:")
print()

# Split by common patterns
segments = program.split('~~')
print(f"Split by '~~': {len(segments)} segments")
for i, seg in enumerate(segments):
    print(f"  Segment {i}: {seg[:50]}...")
print()

# Look for patterns around #
import re
hash_patterns = re.findall(r'\((\d+)#', program)
print(f"Numbers followed by #: {hash_patterns}")
print(f"Count: {len(hash_patterns)}")
print()

# These might be direct character outputs
print("If these are ASCII values:")
for num_str in hash_patterns:
    num = int(num_str)
    if 32 <= num <= 126:
        print(f"  {num} = '{chr(num)}'")
    else:
        print(f"  {num} = (non-printable)")
print()

# Look for patterns with &@*
compound_patterns = re.findall(r'\((\d+)&@\*%\((\d+)', program)
print(f"Patterns like (N&@*(M: {compound_patterns}")
for a, b in compound_patterns:
    print(f"  ({a}&@*({b})")
    print(f"    If @ = add, * = mul: ({a} + {b}) * ? = ?")
    print(f"    If @ = mul, * = add: ({a} * {b}) + ? = ?")
print()

# Let's manually trace the first few operations
print("Manual trace of first part:")
print("~~%(46#%^(3&@*%(20%^")
print()
print("Tokens:")
print("  ~~ - start block")
print("  % - operation marker")
print("  (46 - push 46")
print("  # - print as char? -> '.' (46)")
print("  % - operation marker")
print("  ^ - end operation")
print("  (3 - push 3")
print("  & - operation")
print("  @ - operation")
print("  * - operation")
print("  % - operation marker")
print("  (20 - push 20")
print("  % - operation marker")
print("  ^ - end operation")
print()

# Expected first char is 'T' = 84
# We have 46, 3, 20
# 46 + 3 * 20 = 46 + 60 = 106 (wrong)
# (46 + 3) * 20 = 980 (wrong)
# 46 + 20 + 3 = 69 (wrong)
# 20 * 3 + 46 = 106 (wrong)
# 20 + 3 + 46 = 69 (wrong)
# Hmm, none of these give 84

# Wait, maybe the bug is in the operations!
# What if @ and * are swapped?
# Or what if the order is wrong?

print("Trying different combinations for 'T' = 84:")
nums = [46, 3, 20]
print(f"  {nums[0]} + {nums[1]} + {nums[2]} = {nums[0] + nums[1] + nums[2]}")
print(f"  {nums[0]} + {nums[1]} * {nums[2]} = {nums[0] + nums[1] * nums[2]}")
print(f"  ({nums[0]} + {nums[1]}) * {nums[2]} = {(nums[0] + nums[1]) * nums[2]}")
print(f"  {nums[0]} * {nums[1]} + {nums[2]} = {nums[0] * nums[1] + nums[2]}")
print(f"  {nums[2]} * {nums[1]} + {nums[0]} = {nums[2] * nums[1] + nums[0]}")
print(f"  {nums[2]} + {nums[1]} * {nums[0]} = {nums[2] + nums[1] * nums[0]}")
print()

# Let's check if there's an off-by-one error
print("Off-by-one check:")
print(f"  84 - 1 = 83 (nope, not in our numbers)")
print(f"  84 + 1 = 85 (nope)")
print(f"  84 - 20 = 64 (nope)")
print(f"  84 / 2 = 42 (nope)")
print()

# Maybe the operations work on a stack differently
print("What if it's: push 46, push 3, push 20, then operations?")
print("  Stack: [46, 3, 20]")
print("  &: swap? -> [46, 20, 3]")
print("  @: add top two? -> [46, 23]")
print("  *: multiply top two? -> [1058] (wrong)")
print()
print("  Or maybe:")
print("  &: something else")
print("  @: add -> [46, 23]")
print("  *: print? -> print 46+23=69 (wrong)")
