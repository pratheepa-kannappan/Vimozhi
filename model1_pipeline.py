from speech.voice_to_text import voice_to_text
# Make sure you have these modules in an nlp/ folder if using them
from nlp.preprocess import preprocess_text
from nlp.grammar_rules import isl_restructure
from nlp.isl_gloss import to_isl_gloss
"here is a example usage how it converted from audio to isl gloss"
"""text = "I am going to college tomorrow"
words = preprocess_text(text)
isl_words = isl_restructure(words)
glosses = to_isl_gloss(isl_words)

print("Words:", words)
print("ISL Words:", isl_words)
print("ISL Gloss:", glosses)"""

def voice_to_isl(audio_path):
    text = voice_to_text(audio_path)
    doc = preprocess_text(text)
    isl_words = isl_restructure(doc)
    glosses = to_isl_gloss(isl_words)
    return text,glosses

if __name__ == "__main__":
    audio_file = "record.mp3"  # or "sample.wav" if you have
    text,glosses = voice_to_isl(audio_file)
    print("Recognized Text:", text)
    print("ISL Gloss:", glosses)
