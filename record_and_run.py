import sounddevice as sd
from scipy.io.wavfile import write
import os
import time
import numpy as np
from model1_pipeline import voice_to_isl

# Folders
RECORDINGS_FOLDER = "recordings"
OUTPUT_FOLDER = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "isl_gloss_log.txt")

os.makedirs(RECORDINGS_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

fs = 44100  # Sample rate

def record_manual():
    print("\nPress Enter to START recording...")
    input()

    print("Recording... Press Enter to STOP.")
    frames = []

    def callback(indata, frames_count, time_info, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        input()

    audio = np.concatenate(frames, axis=0)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"recording_{time.strftime('%Y%m%d_%H%M%S')}.wav"
    filepath = os.path.join(RECORDINGS_FOLDER, filename)

    write(filepath, fs, audio)
    print(f"Saved audio: {filepath}")

    return filepath, timestamp


def save_gloss(timestamp, text, glosses):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\nTime: {timestamp}\n")
        f.write(f"Recognized Text: {text}\n")
        f.write(f"ISL Gloss: {' '.join(glosses)}\n")
        f.write("-" * 50 + "\n")


if __name__ == "__main__":
    while True:
        audio_path, timestamp = record_manual()

        text, glosses = voice_to_isl(audio_path)

        print("\nRecognized Text:", text)
        print("ISL Gloss:", glosses)

        save_gloss(timestamp, text, glosses)

        choice = input("\nRecord another? (y/n): ").lower()
        if choice != "y":
            print("Session ended. All ISL gloss saved.")
            break
