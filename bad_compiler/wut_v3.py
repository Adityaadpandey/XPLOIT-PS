#!/usr/bin/env python3
"""
.wut interpreter v3 - different hypothesis
Maybe %(...)%^ is a special block
"""
import sys

def interpret(program):
    stack = []
    output = []
    i = 0
    
    while i < len(program):
        # Parse number
        if program[i] == '(':
            i += 1
            num = ""
            while i < len(program) and program[i].isdigit():
                num += program[i]
                i += 1
            stack.append(int(num))
            continue
        
        ch = program[i]
        
        if ch == '#':
            # Print and pop
            if stack:
                output.append(chr(stack.pop()))
        
        elif ch == '@':
            # Add
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        
        elif ch == '*':
            # Add (not multiply!)
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        
        elif ch == '&':
            # Multiply
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        
        elif ch == '!':
            # Print without pop
            if stack:
                output.append(chr(stack[-1]))
        
        elif ch == '$':
            # Dup
            if stack:
                stack.append(stack[-1])
        
        i += 1
    
    return ''.join(output)

if __name__ == '__main__':
    program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
    result = interpret(program)
    print(result)
    print("Expected: This is right! Congratulations!")
