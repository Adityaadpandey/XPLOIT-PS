#!/usr/bin/env python3
"""
.wut language interpreter - trying to reverse engineer the language
"""

import sys
import re

def parse_tokens(program):
    """Parse the program into tokens"""
    tokens = []
    i = 0
    while i < len(program):
        if program[i] == '(':
            # Number token
            i += 1
            num = ""
            while i < len(program) and program[i].isdigit():
                num += program[i]
                i += 1
            tokens.append(('NUM', int(num)))
        elif program[i] in '#%^@*!$~`&':
            tokens.append(('OP', program[i]))
            i += 1
        else:
            i += 1
    return tokens

def interpret_v1(tokens):
    """
    Hypothesis 1: Stack-based language
    - (N pushes N
    - # prints top as character
    - @ adds top two
    - * multiplies top two
    - % might be a separator or operation marker
    - ^ might be end of statement
    - ~ might be block markers
    - ! might be print
    - $ might be dup
    - & might be another operation
    """
    stack = []
    output = []
    
    i = 0
    while i < len(tokens):
        tok_type, tok_val = tokens[i]
        
        if tok_type == 'NUM':
            stack.append(tok_val)
        elif tok_val == '#':
            # Print top as character
            if stack:
                output.append(chr(stack.pop()))
        elif tok_val == '@':
            # Add
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        elif tok_val == '*':
            # Multiply
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        elif tok_val == '!':
            # Print without popping?
            if stack:
                output.append(chr(stack[-1]))
        elif tok_val == '$':
            # Duplicate
            if stack:
                stack.append(stack[-1])
        elif tok_val == '&':
            # Maybe swap or another operation
            if len(stack) >= 2:
                stack[-1], stack[-2] = stack[-2], stack[-1]
        # Ignore %, ^, ~, ` for now
        
        i += 1
    
    return ''.join(output)

def interpret_v2(tokens):
    """
    Hypothesis 2: Different operation meanings
    Maybe @ is multiply and * is something else
    """
    stack = []
    output = []
    
    i = 0
    while i < len(tokens):
        tok_type, tok_val = tokens[i]
        
        if tok_type == 'NUM':
            stack.append(tok_val)
        elif tok_val == '#':
            if stack:
                output.append(chr(stack.pop()))
        elif tok_val == '@':
            # Try multiply instead
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        elif tok_val == '*':
            # Try add instead
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        elif tok_val == '!':
            if stack:
                output.append(chr(stack[-1]))
        elif tok_val == '$':
            if stack:
                stack.append(stack[-1])
        elif tok_val == '&':
            if len(stack) >= 2:
                stack[-1], stack[-2] = stack[-2], stack[-1]
        
        i += 1
    
    return ''.join(output)

def interpret_v3(tokens):
    """
    Hypothesis 3: % and ^ are important
    Maybe %...^ is a block that does something
    """
    stack = []
    output = []
    
    i = 0
    while i < len(tokens):
        tok_type, tok_val = tokens[i]
        
        if tok_type == 'NUM':
            stack.append(tok_val)
        elif tok_val == '#':
            if stack:
                val = stack.pop()
                output.append(chr(val))
        elif tok_val == '@':
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        elif tok_val == '*':
            # Maybe this means "execute the operation"
            pass
        elif tok_val == '!':
            if stack:
                output.append(chr(stack[-1]))
        elif tok_val == '$':
            if stack:
                stack.append(stack[-1])
        elif tok_val == '&':
            # Maybe this is part of a compound operation
            pass
        
        i += 1
    
    return ''.join(output)

if __name__ == '__main__':
    program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
    expected = "This is right! Congratulations!"
    
    tokens = parse_tokens(program)
    
    print("Expected:", expected)
    print()
    
    result1 = interpret_v1(tokens)
    print("Version 1 (@ = add, * = mul):", result1)
    print("Match:", result1 == expected)
    print()
    
    result2 = interpret_v2(tokens)
    print("Version 2 (@ = mul, * = add):", result2)
    print("Match:", result2 == expected)
    print()
    
    result3 = interpret_v3(tokens)
    print("Version 3 (different logic):", result3)
    print("Match:", result3 == expected)
