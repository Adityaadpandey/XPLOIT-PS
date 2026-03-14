# XPLOIT Challenge Master Solution Guide

## Overview

This repository contains solutions for multiple competitive programming challenges using specialized skills/agents developed for reverse engineering, binary analysis, code manipulation, and system exploitation.

## Skills/Agents Developed

Located in `.claude/` directory:

1. **assembly-deep-dive** - Low-level binary analysis, disassembly, reverse engineering
2. **frankenstein-fusion** - Combining components from multiple programs
3. **dead-code-resurrection** - Finding and reactivating hidden/disabled code
4. **jailbreak-bypass** - Bypassing protections and unlocking features
5. **surprise-challenge** - Meta-skill for multi-domain complex problems

## Challenges and Solutions

### 1. Vault Challenge (`vault_chal/`)

**Type:** Binary reverse engineering, anti-debugging bypass

**Skills Used:** 
- `jailbreak-bypass` - For bypassing protections
- `assembly-deep-dive` - For binary analysis

**Key Findings:**
- ELF 64-bit binary with anti-debugging (ptrace)
- Stack-based unlock code verification
- Code computed as: `g_pid_seed XOR g_vault_byte XOR strlen(argv[0])`
- Success message at address 0x2355

**Solution Approaches:**
1. **Calculate correct code** - Trace initialization, extract values, compute XOR
2. **Patch binary** - NOP the comparison at 0x1a8f (change `jne` to `nop`)
3. **LD_PRELOAD bypass** - Override ptrace to always return 0

**Files:**
- `vault_chal/SOLUTION.md` - Complete analysis and solution
- `vault_chal/chal` - Original binary
- `vault_chal/disassembly.txt` - Full disassembly

**Target Output:**
```
VAULT SYSTEM CLEARED.
All authentication layers bypassed successfully.
```

---

### 2. Bad Compiler Challenge (`bad_compiler/`)

**Type:** Language implementation, compiler debugging

**Skills Used:**
- `surprise-challenge` - Multi-domain problem
- `dead-code-resurrection` - Finding hidden functionality

**Key Findings:**
- Windows PE32 executable (requires Wine or VM on macOS)
- Stack-based language interpreter
- Language: `.wut` files with custom syntax
- Error messages indicate stack operations

**Language Tokens:**
- `(N` - Push number N
- `#`, `%`, `^` - Operations/delimiters
- `@`, `*`, `!`, `$` - Stack operations
- `~` - Block markers
- `` ` `` - End of program

**Solution Approach:**
1. Run broken compiler to see current output
2. Compare with expected output: "This is right! Congratulations!"
3. Identify the bug (likely off-by-one, wrong operation, or stack order)
4. Fix compiler (patch binary or rewrite)
5. Write new program to print team name

**Files:**
- `bad_compiler/SOLUTION.md` - Analysis and approach
- `bad_compiler/broken_compiler.exe` - Buggy compiler
- `bad_compiler/program.wut` - Test program
- `bad_compiler/expected_output.txt` - Target output

---

### 3. DOOM Companion Bot (`dooooom/`)

**Type:** Game engine modification, AI implementation

**Skills Used:**
- `frankenstein-fusion` - Combining existing DOOM systems
- Understanding state machines and game AI

**Key Findings:**
- Chocolate DOOM source code provided
- DOOM uses state machine-based AI
- Existing monster AI has all needed functionality:
  - `A_Look()` - Target acquisition
  - `A_Chase()` - Pathfinding
  - `P_Move()` - Movement
  - `P_CheckSight()` - Line of sight
  - Attack functions

**Solution Approach:**
1. Add `MF_FRIEND` flag to mark friendly entities
2. Modify `A_Look()` to skip player if friendly
3. Modify `P_DamageMobj()` to prevent friendly fire
4. Create `P_SpawnCompanion()` to spawn bot at level start
5. Implement `A_CompanionThink()` for follow/attack logic
6. Reuse existing pathfinding, combat, and animation systems

**Key Implementation Points:**
- Spawn companion near player in `P_SetupLevel()`
- Use existing `A_Chase()` for following
- Use `P_LookForMonsters()` for target selection
- Handle edge cases: doors, stairs, getting stuck

**Files:**
- `dooooom/SOLUTION.md` - Complete implementation guide
- `dooooom/chocolate-doom.zip` - Source code
- `dooooom/README.md` - Challenge description

**Deliverables:**
- Modified source code
- Writeup explaining DOOM systems used
- Video showing bot in action

---

### 4. APK Audio Interception (`ShhhItsSecret.apk`)

**Type:** Dynamic instrumentation, Android reverse engineering

**Skills Used:**
- `jailbreak-bypass` - Runtime manipulation
- `surprise-challenge` - Multi-phase problem

**Key Findings:**
- Android APK with encrypted audio
- Audio has "Ghost Channel" noise interleaved with voice
- Must use Frida for dynamic instrumentation
- Cannot decompile/recompile APK

**Phase 1: Wiretap (Stabilization)**
1. Hook `AudioTrack.write()` method with Frida
2. Intercept PCM audio buffer before speaker
3. Analyze buffer structure to identify noise pattern
4. Strip noise (likely every Nth sample or channel)
5. Write cleaned buffer to speaker

**Phase 2: DJ (Exploitation)**
Creative audio manipulation:
- **Double speed** - Skip every other sample
- **Reverse** - Reverse the array
- **Echo** - Mix with delayed copy
- **Pitch shift** - Interpolate or skip samples
- **Distortion** - Amplify and clip

**Frida Hook Template:**
```javascript
Java.perform(function() {
    var AudioTrack = Java.use("android.media.AudioTrack");
    AudioTrack.write.overload('[B', 'int', 'int').implementation = function(audioData, offsetInBytes, sizeInBytes) {
        // Clean audio (Phase 1)
        var cleanBuffer = stripGhostChannel(audioData, sizeInBytes);
        
        // Manipulate audio (Phase 2)
        var finalBuffer = applyEffect(cleanBuffer);
        
        // Play modified audio
        var javaArray = Java.array('byte', finalBuffer);
        return this.write(javaArray, 0, finalBuffer.length);
    };
});
```

**Files:**
- `XPLOIT_APK_SOLUTION.md` - Complete Frida guide
- `ShhhItsSecret.apk` - Target APK
- `XPLOIT Secret Message.md` - Challenge description

**Deliverables:**
- Frida script (`.js` file)
- Screen/audio recording of Phase 2
- Link to APK

---

## Methodology

### General Approach (from `surprise-challenge` skill)

1. **Rapid Reconnaissance (3-5 min)**
   - Identify all inputs
   - Classify problem domain
   - Map dependencies

2. **Attack Frameworks**
   - Reverse Pipeline: Work backwards from desired output
   - Divide and Conquer: Split into subproblems
   - Pattern Recognition: Identify common archetypes

3. **Essential Toolbox**
   - Python for quick prototyping
   - Binary tools: objdump, readelf, strings, nm
   - GDB for dynamic analysis
   - Hex editors for patching

4. **Time Management**
   - 0-5 min: Reconnaissance
   - 5-20 min: Easiest subproblem
   - 20-40 min: Medium subproblem
   - 40-55 min: Hardest parts
   - 55-60 min: Verify and submit

### Binary Analysis Workflow (from `assembly-deep-dive`)

1. **Initial recon**
   ```bash
   file binary
   strings binary | grep -i "key\|pass\|flag"
   objdump -d binary -M intel > disasm.txt
   readelf -h binary
   nm binary
   ```

2. **Find critical functions**
   - Search for success/failure messages
   - Trace backwards to find checks
   - Identify comparison instructions

3. **Understand the logic**
   - Map registers to variables
   - Identify control flow (if/else/loops)
   - Recognize library calls

4. **Bypass or solve**
   - Calculate correct input, OR
   - Patch conditional jumps, OR
   - Use GDB to skip checks

### Code Fusion Workflow (from `frankenstein-fusion`)

1. **Component Inventory**
   - Map each program's functions
   - Identify inputs/outputs
   - Check dependencies

2. **Fusion Techniques**
   - Direct splice (compatible interfaces)
   - Adapter layer (incompatible interfaces)
   - Process pipeline (keep separate)
   - Shared state (communication needed)

3. **Dependency Resolution**
   - Resolve conflicting includes
   - Handle namespace collisions
   - Fix global variable conflicts

4. **Integration Testing**
   - Test components individually
   - Test adapters
   - Test full pipeline

## Tools Reference

### Binary Analysis
- `file` - Identify file type
- `strings` - Extract readable strings
- `objdump` - Disassemble binaries
- `readelf` - Analyze ELF structure
- `nm` - List symbols
- `gdb` - Dynamic debugging
- `ltrace` / `strace` - Trace library/system calls
- `xxd` / `hexdump` - Hex viewer

### Patching
- Python with `bytearray` - Binary patching
- `dd` - Byte-level file manipulation
- Hex editors - Manual patching

### Android/Mobile
- `adb` - Android Debug Bridge
- `frida` - Dynamic instrumentation
- `apktool` - APK decompiler
- `jadx` / `jd-gui` - Java decompiler

### Game Development
- `gdb` - Debugging game engines
- Source code analysis tools
- Build systems (make, cmake)

## Key Insights

1. **Reuse existing systems** - Don't reinvent the wheel
2. **Understand before modifying** - Read the code/disassembly
3. **Test incrementally** - Verify each change
4. **Document everything** - Explain your reasoning
5. **Handle edge cases** - Think about failure modes
6. **Use the right tool** - Static vs dynamic analysis
7. **Pattern recognition** - Many problems are similar
8. **Time management** - Don't get stuck on one approach

## Scoring Optimization

For maximum points:
- **Correctness** - Solution must work
- **Understanding** - Explain what you did and why
- **Quality** - Clean code, good documentation
- **Depth** - Show mastery of the domain
- **Edge cases** - Handle unusual situations
- **Presentation** - Clear writeups, good videos

## Repository Structure

```
.
├── .claude/                    # Skills/agents
│   ├── assembly-deep-dive/
│   ├── frankenstein-fusion/
│   ├── dead-code-resurrection/
│   ├── jailbreak-bypass/
│   └── surprise-challenge/
├── vault_chal/                 # Binary reverse engineering
│   ├── chal
│   ├── README.md
│   └── SOLUTION.md
├── bad_compiler/               # Compiler debugging
│   ├── broken_compiler.exe
│   ├── program.wut
│   ├── expected_output.txt
│   ├── README.md
│   └── SOLUTION.md
├── dooooom/                    # Game engine modification
│   ├── chocolate-doom.zip
│   ├── README.md
│   └── SOLUTION.md
├── ShhhItsSecret.apk          # Android APK
├── XPLOIT Secret Message.md   # APK challenge description
├── XPLOIT_APK_SOLUTION.md     # APK solution guide
└── MASTER_SOLUTION_GUIDE.md   # This file
```

## Next Steps

To complete each challenge:

1. **Vault Challenge**
   - Set up Linux VM or use Wine
   - Run binary and analyze behavior
   - Extract global variables
   - Calculate unlock code OR patch binary
   - Document all steps with screenshots

2. **Bad Compiler**
   - Run compiler with Wine
   - Compare current vs expected output
   - Identify the bug pattern
   - Fix compiler
   - Write team name program
   - Document language specification

3. **DOOM Companion**
   - Extract and build Chocolate DOOM
   - Study p_enemy.c and info.c
   - Implement companion spawn and AI
   - Test in-game
   - Record video
   - Write detailed explanation

4. **APK Challenge**
   - Set up Android device/emulator
   - Install Frida
   - Analyze APK structure
   - Write Frida hook for AudioTrack
   - Identify ghost channel pattern
   - Implement cleaning algorithm
   - Add creative manipulation
   - Record demo

## Conclusion

These challenges demonstrate skills in:
- Binary reverse engineering
- Dynamic instrumentation
- Compiler implementation
- Game engine architecture
- Code analysis and modification
- Problem decomposition
- Creative problem solving

The key to success is understanding existing systems and leveraging them, rather than building everything from scratch. The skills/agents developed provide frameworks for tackling similar problems in the future.
