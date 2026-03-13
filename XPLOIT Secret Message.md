Top Secret Message

Our operatives have intercepted a proprietary Android application used for secure, offline communications. Intelligence suggests this APK contains a highly sensitive, encrypted audio transmission stored within its assets.

The app features a built-in player designed to decrypt and play this audio on the fly. However, the original developer implemented an aggressive anti-interception technique known as a "Ghost Channel." While the app successfully decrypts the cryptographic layer, it blindly feeds the entire raw data stream directly to the device's speaker. Pressing play results in an agonizing, corrupted blast of static, though a faint human voice can be heard buried inside the noise.

Your mission is to isolate the clear audio and then weaponize the stream.

#### **Phase 1: The Wiretap (Stabilization)**

You are **not** allowed to decompile, modify the Smali/Java, and recompile the APK. You must fix this app while it is running in memory.

Using dynamic instrumentation (Frida), you must:

1. Reverse engineer the APK to locate the audio playback method.  
2. Intercept the raw PCM audio buffer *just before* it hits the speaker.  
3. Analyze the physical structure of the byte array to identify how the "Ghost Channel" (the static) is woven into the actual voice data.  
4. Write a Frida script that dynamically strips the noise from the buffer in real-time, shrinks the array to the correct size, and recovers the crystal-clear human voice.

*Note: The code itself contains no syntax or mathematical bugs. The secret lies entirely within the structure of the data.*

#### **Phase 2: The DJ (Exploitation)**

Once you have successfully intercepted and cleaned the audio stream, you now have total control over the raw PCM buffer. We want to see what you can do with it.

Modify your Frida script to creatively manipulate the audio in real-time *before* it plays out of the speaker.

* Can you double the speed so it sounds like a chipmunk?  
* Can you drop the pitch?  
* Can you add a synthesized echo or play it in reverse?

**Deliverables:**

1. Your final `.js` Frida script.  
2. A short screen/audio recording of your modified app running Phase 2\.

Link to the APK: [XPLOIT](https://drive.google.com/drive/folders/1B96_-hnLD6s0ZUM0dYgfKyKXOyWTPGeP?usp=sharing)