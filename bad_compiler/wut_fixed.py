#!/usr/bin/env python3
"""
Fixed .wut interpreter
Based on reverse engineering the language
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
        
        # Operations
        ch = program[i]
        
        if ch == '#':
            # Print top of stack as character
            if stack:
                output.append(chr(stack.pop()))
        
        elif ch == '@':
            # Multiply top two
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        
        elif ch == '*':
            # Add top two (FIXED: was multiply, should be add)
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        
        elif ch == '&':
            # Swap top two
            if len(stack) >= 2:
                stack[-1], stack[-2] = stack[-2], stack[-1]
        
        elif ch == '!':
            # Print top without popping
            if stack:
                output.append(chr(stack[-1]))
        
        elif ch == '$':
            # Duplicate top
            if stack:
                stack.append(stack[-1])
        
        # Ignore %, ^, ~, ` (structure markers)
        
        i += 1
    
    return ''.join(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            program = f.read()
    else:
        program = "~~%(46#%^(3&@*%(20%^~~#%%!^(0$%(10%^(83#%^(2&@*%(73%^(10%^(83#%^(82%^~~#%%(9#%^@@^!^(12%^(1&@*%(83#%^@^(35%^(44%^@^(7#%^(11%^(17#%^(19%^!^(9#%^(11#%^(19%^(11#%^(6%^@^(5%^~~#%`"
    
    result = interpret(program)
    print(result)
