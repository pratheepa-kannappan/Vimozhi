from speech.voice_to_text import voice_to_text
from nlp.preprocess import preprocess_text
from nlp.grammar_rules import isl_restructure
from nlp.isl_gloss import to_isl_gloss
from sign.sentence_to_signs import sentence_to_signs


def run_full_pipeline(audio_path):
    print("🔹 STEP 1: Speech → Text")
    text = voice_to_text(audio_path)
    print("Recognized Text:", text)

    print("\n🔹 STEP 2: NLP Preprocessing")
    doc = preprocess_text(text)
    print("Processed Tokens:", [t.text for t in doc])
    #print("Processed Tokens:", doc.split())


    print("\n🔹 STEP 3: ISL Grammar Restructuring")
    isl_words = isl_restructure(doc)
    print("ISL Words:", isl_words)

    print("\n🔹 STEP 4: ISL Gloss Mapping")
    glosses = to_isl_gloss(isl_words)
    print("ISL Glosses:", glosses)

    print("\n🔹 STEP 5: Sentence → Sign Frames")
    sign_frames = sentence_to_signs(glosses)

    print("\n✅ FINAL SIGN FRAME SEQUENCE:")
    for frame in sign_frames:
        print(frame)

    return sign_frames


if __name__ == "__main__":
    audio_file = "sample.mp3"   # place this in project root
    run_full_pipeline(audio_file)
"""from sign.sentence_to_signs import sentence_to_signs

print(sentence_to_signs(["I", "COLLEGE", "GO"]))"""
