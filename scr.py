import wave
import numpy as np

input_file = "raw.wav"
output_file = "clean.wav"

# read wav
with wave.open(input_file, 'rb') as wf:
    n_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()

    audio_data = wf.readframes(n_frames)

# convert to numpy
samples = np.frombuffer(audio_data, dtype=np.int16)

# remove ghost samples (keep every second sample)
clean = samples[::2]

# write cleaned audio
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(framerate)
    wf.writeframes(clean.tobytes())

print("Clean audio saved to:", output_file)
