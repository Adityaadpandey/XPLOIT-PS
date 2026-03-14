#!/usr/bin/env python3
"""
Reverse engineer the .wut language by analyzing patterns
"""

program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
expected = "This is right! Congratulations!"

print("Expected output:", expected)
print("ASCII values:", [ord(c) for c in expected])
print()

# Let's look at the numbers and see if there's arithmetic
numbers = [46, 3, 20, 0, 10, 83, 2, 73, 10, 83, 82, 9, 12, 1, 83, 35, 44, 7, 11, 17, 19, 9, 11, 19, 11, 6, 5]

print("Numbers in program:", numbers)
print()

# Expected ASCII values
target = [84, 104, 105, 115, 32, 105, 115, 32, 114, 105, 103, 104, 116, 33, 32, 67, 111, 110, 103, 114, 97, 116, 117, 108, 97, 116, 105, 111, 110, 115, 33]

print("Let's try to find patterns:")
print()

# Hypothesis 1: Stack-based with operations
# @ might be add, * might be multiply, etc.

# Let's trace through manually
print("Manual trace (hypothesis: stack-based calculator):")
print()

# Looking at the structure:
# ~~%(46#%^(3&@*%(20%^
# ~~ - start
# % - operation marker?
# (46 - push 46
# # - operation?
# % - operation marker?
# ^ - end operation?
# (3 - push 3
# & - operation?
# @ - operation (add?)
# * - operation (multiply?)
# % - operation marker?
# (20 - push 20
# % - operation marker?
# ^ - end operation?

# Let's try: @ = add, * = multiply
# 46 + 3 = 49, then * 20 = 980? No, that's too big

# Maybe: @ = add, but there's a different order
# Or maybe the operations work differently

# Let's look at the first character: 'T' = 84
# Numbers before first output might be: 46, 3, 20
# 46 + 3 = 49, 49 + 20 = 69, still not 84
# 46 + 3 * 20 = 46 + 60 = 106, not 84
# (46 + 3) * 20 = 980, not 84
# 46 * 3 - 20 = 138 - 20 = 118, not 84
# 46 + 20 + 3 = 69, not 84
# 46 + 38 = 84! So maybe 20 + 3 = 23, then 46 + 38 = 84?

print("First character 'T' = 84")
print("First numbers: 46, 3, 20")
print("Trying: 46 + (20 + 3*something) = 84")
print("  46 + 38 = 84, so we need 38 from 3 and 20")
print("  20 + 3*6 = 38? But where's 6?")
print()

# Let's look at the second character: 'h' = 104
# Next numbers might be: 0, 10, 83
print("Second character 'h' = 104")
print("Next numbers: 0, 10, 83")
print("  0 + 10 + 83 = 93, not 104")
print("  83 + 10 + 0 = 93, not 104")
print("  83 + 21 = 104, so we need 21 from 0 and 10")
print("  10 * 2 + 0 = 20, close but not 21")
print()

# Maybe the operations are more complex
# Let's look at the operators between numbers:
print("Analyzing operator patterns:")
print()

# Parse more carefully
import re
tokens = re.findall(r'\((\d+)|([~#%^@*!$&`])', program)
flat_tokens = []
for num, op in tokens:
    if num:
        flat_tokens.append(('NUM', int(num)))
    else:
        flat_tokens.append(('OP', op))

print("Token sequence:")
for i, tok in enumerate(flat_tokens[:50]):
    print(f"{i:3d}: {tok}")
