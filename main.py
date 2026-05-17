import sounddevice as sd
from scipy.io.wavfile import write
import datetime
import os
import cv2
import numpy as np

from speech.voice_to_text import voice_to_text
from nlp.preprocess import preprocess_text
from nlp.grammar_rules import isl_restructure
from nlp.isl_gloss import to_isl_gloss
from sign.sentence_to_signs import sentence_to_signs


SAMPLE_RATE = 16000
CHANNELS = 1

# =========================
# MANUAL AUDIO RECORDING
# =========================
def record_audio_manual():
    input("\n🎙️ Press ENTER to START recording...")
    print("🔴 Recording... Press ENTER to STOP")

    recording = []
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    stream.start()

    try:
        input()
    finally:
        stream.stop()
        stream.close()

    audio = np.concatenate(recording) if recording else sd.rec(1, SAMPLE_RATE, CHANNELS)
    return audio


def record_audio_to_file():
    os.makedirs("recordings", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recordings/recording_{timestamp}.wav"

    print("\n🎙️ Press ENTER to START recording")
    input()
    print("🔴 Recording... Press ENTER to STOP")

    frames = []

    def callback(indata, frames_count, time, status):
        frames.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=callback
    ):
        input()

    audio = np.concatenate(frames, axis=0)
    write(filename, SAMPLE_RATE, audio)

    print("✅ Audio saved:", filename)
    return filename


# =========================
# DISPLAY SIGN IMAGES
# =========================
def display_signs(sign_frames, delay=900):
    print("\n✋ Showing ISL signs (Press Q to quit)")

    for frame_path in sign_frames:
        if not os.path.exists(frame_path):
            continue

        img = cv2.imread(frame_path)
        if img is None:
            continue

        cv2.imshow("ISL Output", img)
        key = cv2.waitKey(delay) & 0xFF

        if key == ord('q'):
            break

    cv2.destroyAllWindows()


# =========================
# MAIN PIPELINE
# =========================
def main():
    # Step 1: Record audio
    audio_path = record_audio_to_file()

    # Step 2: Speech → Text
    text = voice_to_text(audio_path)

    # Step 3: NLP
    tokens = preprocess_text(text)
    isl_words = isl_restructure(tokens)
    isl_gloss = to_isl_gloss(isl_words)

    # Step 4: LOG OUTPUT
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = (
        "-" * 50 + "\n" +
        f"Time: {timestamp}\n" +
        f"Recognized Text: {text}\n" +
        f"ISL Gloss: {' '.join(isl_gloss)}\n" +
        "-" * 50 + "\n"
    )
    print(log_text)

    # Save to file
    os.makedirs("output", exist_ok=True)
    with open("output/isl_gloss_log.txt", "a", encoding="utf-8") as f:
        f.write(log_text)

    

    # Step 5: Convert to signs
    sign_frames = sentence_to_signs(isl_gloss)

    if not sign_frames:
        print("❌ No sign images found")
        return

    # Step 6: Show signs
    def display_signs(sign_frames, delay=1500):
        print("\n✋ Showing ISL signs (Press Q to quit)")

        for frame_path in sign_frames:
            if not os.path.exists(frame_path):
                print("❌ Image not found:", frame_path)
                continue

            img = cv2.imread(frame_path)
            if img is None:
                print("❌ Failed to read:", frame_path)
                continue

            # Optional: resize to fit screen
            img = cv2.resize(img, (640, 480))
            cv2.imshow("ISL Output", img)
            key = cv2.waitKey(delay) & 0xFF

            if key == ord('q'):
                break
        cv2.destroyAllWindows()



# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()


