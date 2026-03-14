#!/usr/bin/env python3
"""
Analyze the .wut program to understand the language structure
"""

program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"

expected = "This is right! Congratulations!"

print("Program length:", len(program))
print("Expected output:", expected)
print("Expected length:", len(expected))
print()

# Analyze character frequencies
from collections import Counter
freq = Counter(program)
print("Character frequencies:")
for char, count in sorted(freq.items(), key=lambda x: -x[1]):
    print(f"  '{char}': {count}")
print()

# Try to identify tokens
print("Potential tokens:")
tokens = []
i = 0
while i < len(program):
    if program[i] == '(':
        # Number token
        num = ""
        i += 1
        while i < len(program) and program[i].isdigit():
            num += program[i]
            i += 1
        tokens.append(('NUM', int(num)))
    elif program[i] in '#%^@*!$~`':
        tokens.append(('OP', program[i]))
        i += 1
    elif program[i] == '&':
        tokens.append(('OP', '&'))
        i += 1
    else:
        i += 1

print(f"Total tokens: {len(tokens)}")
print("\nFirst 30 tokens:")
for i, token in enumerate(tokens[:30]):
    print(f"  {i}: {token}")

print("\n\nNumbers in program:")
numbers = [t[1] for t in tokens if t[0] == 'NUM']
print(numbers)

print("\n\nASCII values of expected output:")
ascii_vals = [ord(c) for c in expected]
print(ascii_vals)

print("\n\nComparing numbers to ASCII values:")
print(f"Numbers in program: {len(numbers)}")
print(f"Characters in output: {len(expected)}")

# Check if numbers match ASCII values
if len(numbers) >= len(expected):
    print("\nDirect ASCII match check:")
    for i, (num, char) in enumerate(zip(numbers, expected)):
        print(f"  {i}: {num} vs {ord(char)} ('{char}') - {'✓' if num == ord(char) else '✗'}")
