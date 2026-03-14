# XPLOIT Secret Message - APK Frida Challenge Solution

## Challenge Overview

**Objective:** Use Frida to dynamically intercept and clean corrupted audio from an Android APK without decompiling/recompiling.

**Phases:**
1. **Phase 1 (Wiretap):** Strip the "Ghost Channel" noise from PCM audio buffer in real-time
2. **Phase 2 (DJ):** Creatively manipulate the cleaned audio (speed up, pitch shift, echo, reverse, etc.)

## Phase 1: The Wiretap (Stabilization)

### Step 1: APK Reconnaissance

```bash
# Download APK from provided link
wget [APK_URL] -O ShhhItsSecret.apk

# Extract APK contents
unzip ShhhItsSecret.apk -d apk_extracted/

# Analyze APK structure
ls -la apk_extracted/
# Look for: assets/, lib/, classes.dex, AndroidManifest.xml

# Check for audio files in assets
find apk_extracted/assets -type f
file apk_extracted/assets/*

# Decompile DEX to understand structure (for analysis only, not modification)
d2j-dex2jar apk_extracted/classes.dex
jd-gui classes-dex2jar.jar

# Or use apktool for better analysis
apktool d ShhhItsSecret.apk -o apk_decompiled/
```

### Step 2: Identify Audio Playback Method

Look for:
- `AudioTrack` class usage (Android's low-level audio API)
- `MediaPlayer` class
- PCM buffer writes
- Methods like `write()`, `play()`, `setDataSource()`

**Key Android Audio APIs:**
```java
// AudioTrack - low level PCM playback
AudioTrack.write(byte[] audioData, int offsetInBytes, int sizeInBytes)
AudioTrack.write(short[] audioData, int offsetInShorts, int sizeInShorts)
AudioTrack.write(float[] audioData, int offsetInFloats, int sizeInFloats)

// MediaPlayer - high level
MediaPlayer.setDataSource()
MediaPlayer.start()
```

### Step 3: Frida Hook Strategy

**Target:** The `write()` method of `AudioTrack` where PCM buffer is sent to speaker.

**Frida Script Template:**
```javascript
Java.perform(function() {
    console.log("[*] Starting Frida hook...");
    
    // Hook AudioTrack.write() method
    var AudioTrack = Java.use("android.media.AudioTrack");
    
    // Hook the byte array version
    AudioTrack.write.overload('[B', 'int', 'int').implementation = function(audioData, offsetInBytes, sizeInBytes) {
        console.log("[*] AudioTrack.write() called");
        console.log("[*] Buffer size: " + sizeInBytes);
        console.log("[*] Offset: " + offsetInBytes);
        
        // Convert Java byte array to JavaScript array
        var buffer = [];
        for (var i = 0; i < sizeInBytes; i++) {
            buffer.push(audioData[offsetInBytes + i] & 0xFF);
        }
        
        console.log("[*] First 20 bytes: " + buffer.slice(0, 20));
        
        // Analyze the buffer structure
        // Look for patterns: alternating channels, interleaved data, etc.
        
        // Call original method (for now)
        return this.write(audioData, offsetInBytes, sizeInBytes);
    };
    
    console.log("[*] Hook installed successfully");
});
```

### Step 4: Analyze the "Ghost Channel" Structure

The challenge states: "The secret lies entirely within the structure of the data."

**Possible structures:**
1. **Interleaved stereo with noise channel:**
   ```
   [Left, Right, Noise, Left, Right, Noise, ...]
   ```
   Solution: Extract every 3rd sample, skip the noise

2. **Alternating good/bad samples:**
   ```
   [Good, Noise, Good, Noise, ...]
   ```
   Solution: Take every other sample

3. **Noise in specific byte positions:**
   ```
   [Good_byte, Noise_byte, Good_byte, Noise_byte, ...]
   ```
   Solution: Filter out noise bytes

4. **Frequency-based separation:**
   - Voice in certain frequency range
   - Noise in another range
   - Solution: Frequency domain filtering (complex)

5. **Bit-level interleaving:**
   - Good data in certain bits
   - Noise in other bits
   - Solution: Bit masking

### Step 5: Clean the Audio Buffer

**Example: Removing every 3rd sample (if it's a 3-channel interleave)**

```javascript
Java.perform(function() {
    var AudioTrack = Java.use("android.media.AudioTrack");
    
    AudioTrack.write.overload('[B', 'int', 'int').implementation = function(audioData, offsetInBytes, sizeInBytes) {
        console.log("[*] Intercepted audio buffer: " + sizeInBytes + " bytes");
        
        // Extract clean audio (assuming every 3rd byte is noise)
        var cleanBuffer = [];
        for (var i = 0; i < sizeInBytes; i++) {
            if (i % 3 !== 2) {  // Skip every 3rd byte (index 2, 5, 8, ...)
                cleanBuffer.push(audioData[offsetInBytes + i]);
            }
        }
        
        console.log("[*] Cleaned buffer size: " + cleanBuffer.length);
        
        // Convert back to Java byte array
        var cleanJavaArray = Java.array('byte', cleanBuffer);
        
        // Write cleaned audio
        return this.write(cleanJavaArray, 0, cleanBuffer.length);
    };
});
```

**Alternative: Stereo to Mono (if one channel is noise)**

```javascript
// Assuming 16-bit PCM stereo (4 bytes per sample: 2 bytes left, 2 bytes right)
var cleanBuffer = [];
for (var i = 0; i < sizeInBytes; i += 4) {
    // Keep only left channel (or right, depending on which is clean)
    cleanBuffer.push(audioData[offsetInBytes + i]);
    cleanBuffer.push(audioData[offsetInBytes + i + 1]);
}
```

### Step 6: Test and Iterate

```bash
# Install APK on device/emulator
adb install ShhhItsSecret.apk

# Run Frida script
frida -U -f com.example.secretmessage -l wiretap.js --no-pause

# Or attach to running process
frida -U com.example.secretmessage -l wiretap.js

# Listen to the output and adjust the cleaning algorithm
```

## Phase 2: The DJ (Exploitation)

Once the audio is clean, manipulate it creatively.

### Technique 1: Double Speed (Chipmunk Effect)

```javascript
// Skip every other sample
var manipulatedBuffer = [];
for (var i = 0; i < cleanBuffer.length; i += 2) {
    manipulatedBuffer.push(cleanBuffer[i]);
}
```

### Technique 2: Half Speed (Slow Motion)

```javascript
// Duplicate each sample
var manipulatedBuffer = [];
for (var i = 0; i < cleanBuffer.length; i++) {
    manipulatedBuffer.push(cleanBuffer[i]);
    manipulatedBuffer.push(cleanBuffer[i]);
}
```

### Technique 3: Reverse Audio

```javascript
var manipulatedBuffer = cleanBuffer.slice().reverse();
```

### Technique 4: Pitch Shift (Simple)

```javascript
// Lower pitch: interpolate samples (add intermediate values)
// Higher pitch: skip samples (similar to speed up)

// Simple pitch down (crude method)
var manipulatedBuffer = [];
for (var i = 0; i < cleanBuffer.length - 1; i++) {
    manipulatedBuffer.push(cleanBuffer[i]);
    // Add interpolated sample
    var avg = Math.floor((cleanBuffer[i] + cleanBuffer[i + 1]) / 2);
    manipulatedBuffer.push(avg);
}
```

### Technique 5: Echo Effect

```javascript
// Add delayed copy of signal
var delayMs = 200;  // 200ms delay
var sampleRate = 44100;  // Typical sample rate
var delaySamples = Math.floor(delayMs * sampleRate / 1000);

var manipulatedBuffer = cleanBuffer.slice();
for (var i = delaySamples; i < cleanBuffer.length; i++) {
    // Mix original with delayed signal (50% each)
    var mixed = Math.floor((cleanBuffer[i] + cleanBuffer[i - delaySamples]) / 2);
    manipulatedBuffer[i] = mixed & 0xFF;
}
```

### Technique 6: Distortion

```javascript
// Amplify and clip
var manipulatedBuffer = [];
for (var i = 0; i < cleanBuffer.length; i++) {
    var amplified = cleanBuffer[i] * 2;
    // Clip to byte range
    manipulatedBuffer.push(Math.min(255, Math.max(0, amplified)));
}
```

### Complete Phase 2 Script Example

```javascript
Java.perform(function() {
    var AudioTrack = Java.use("android.media.AudioTrack");
    
    AudioTrack.write.overload('[B', 'int', 'int').implementation = function(audioData, offsetInBytes, sizeInBytes) {
        // Phase 1: Clean the audio
        var cleanBuffer = [];
        for (var i = 0; i < sizeInBytes; i++) {
            if (i % 3 !== 2) {  // Remove ghost channel
                cleanBuffer.push(audioData[offsetInBytes + i] & 0xFF);
            }
        }
        
        // Phase 2: Apply creative effect (chipmunk voice)
        var manipulatedBuffer = [];
        for (var i = 0; i < cleanBuffer.length; i += 2) {
            manipulatedBuffer.push(cleanBuffer[i]);
        }
        
        console.log("[*] Original: " + sizeInBytes + " -> Clean: " + cleanBuffer.length + " -> Manipulated: " + manipulatedBuffer.length);
        
        // Convert to Java array and play
        var finalArray = Java.array('byte', manipulatedBuffer);
        return this.write(finalArray, 0, manipulatedBuffer.length);
    };
    
    console.log("[+] DJ mode activated!");
});
```

## Running the Solution

### Method 1: Standard Frida

```bash
# Start Frida server on device
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# Run the script
frida -U -f com.example.secretmessage -l solution.js --no-pause
```

### Method 2: Frida Gadget (if standard doesn't work)

```bash
# Extract APK
apktool d ShhhItsSecret.apk

# Add frida-gadget.so to lib folders
# Modify smali to load gadget on startup
# Repackage and sign APK
apktool b ShhhItsSecret -o modified.apk
jarsigner -keystore debug.keystore modified.apk
adb install modified.apk

# Connect Frida
frida -U Gadget -l solution.js
```

## Deliverables

1. **solution.js** - Final Frida script with both phases
2. **Screen recording** - Video showing:
   - Original corrupted audio playing
   - Frida script being loaded
   - Clean audio playing
   - Creative manipulation (chipmunk/echo/reverse)
3. **Documentation** - Explanation of:
   - How the ghost channel was structured
   - The cleaning algorithm used
   - The creative manipulation applied

## Tools Required

- **Frida** - Dynamic instrumentation framework
- **ADB** - Android Debug Bridge
- **apktool** - APK decompiler (for analysis)
- **jd-gui** or **jadx** - Java decompiler
- **Android device/emulator** with USB debugging enabled

## Key Insights

1. The challenge is about **data structure analysis**, not code bugs
2. PCM audio is just raw bytes - easy to manipulate
3. Frida's Java.perform() gives full access to Android APIs
4. The "ghost channel" is likely a simple interleaving pattern
5. Creative audio manipulation is just array operations on the buffer

## Common Pitfalls

- Forgetting to convert between Java and JavaScript arrays
- Not handling byte signedness (Java bytes are signed, need `& 0xFF`)
- Wrong buffer size after manipulation (must match actual data)
- Not considering sample rate and bit depth in calculations
- Frida script syntax errors (use `console.log()` for debugging)
