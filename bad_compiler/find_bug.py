#!/usr/bin/env python3
"""
Find the bug by comparing what we get vs what we expect
"""

import re

program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
expected = "This is right! Congratulations!"

# Extract numbers followed by #
hash_numbers = [int(x) for x in re.findall(r'\((\d+)#', program)]
print("Numbers followed by # (direct prints):")
print(hash_numbers)
print()

# Expected ASCII values
expected_ascii = [ord(c) for c in expected]
print("Expected ASCII values:")
print(expected_ascii)
print()

# Check if there's a pattern
print("Comparing (assuming # prints directly):")
print()

# We have 10 numbers with #, but 31 expected characters
# So # is not the only way to print

# Let's look at the pattern more carefully
# Maybe &@* is a compound operation that computes and prints

# Pattern: (N&@*(M
# This appears 3 times: (3&@*(20), (2&@*(73), (1&@*(83)

compound = [(3, 20), (2, 73), (1, 83)]
print("Compound operations (N&@*(M):")
for a, b in compound:
    print(f"  {a} & @ * {b}")
    print(f"    {a} * {b} = {a * b}")
    print(f"    {a} + {b} = {a + b}")
    print()

# Let's see if these match expected characters
# First char 'T' = 84
# We have 46 followed by (3&@*(20)
# Maybe: 46 + (3 * 20) = 46 + 60 = 106? No
# Maybe: 46 - (3 * 20) = 46 - 60 = -14? No
# Maybe: (46 + 3) + 20 = 69? No
# Maybe: 46 + 20 + something = 84, so something = 18
# 3 * 6 = 18? But where's 6?

print("Hypothesis: The bug is in how &@* is computed")
print()
print("Expected first char: 'T' = 84")
print("We have: 46, then (3&@*(20)")
print()
print("If the CORRECT operation is:")
print(f"  46 + (20 + 3*6) = 46 + 38 = 84 ✓")
print("  But we don't have 6...")
print()
print(f"  46 + 20 + 18 = 84, where 18 = ?")
print(f"  46 + 38 = 84, where 38 = 20 + 18")
print()

# Wait! Maybe the bug is simpler
# What if @ and * are swapped?
# Or what if & means something different?

print("Let's try: & means 'multiply by', @ means 'add', * means 'execute'")
print(f"  46 + (3 * 20) = 46 + 60 = 106 (wrong)")
print()

print("Let's try: the operations are applied in wrong order")
print(f"  20 + 3 = 23, then 46 + 23 = 69 (wrong)")
print(f"  20 * 3 = 60, then 46 + 60 = 106 (wrong)")
print()

# Maybe there's an off-by-one in the arithmetic?
print("Off-by-one hypothesis:")
print(f"  If we got 46 but need 84: difference = {84 - 46} = 38")
print(f"  If we got 83 but need 104: difference = {104 - 83} = 21")
print(f"  If we got 83 but need 105: difference = {105 - 83} = 22")
print()

# Let's check all the # numbers
print("All # numbers vs expected (if they map 1-to-1):")
for i, num in enumerate(hash_numbers):
    if i < len(expected):
        exp_val = ord(expected[i])
        diff = exp_val - num
        print(f"  {i}: got {num} ('{chr(num) if 32 <= num <= 126 else '?'}'), need {exp_val} ('{expected[i]}'), diff = {diff}")
