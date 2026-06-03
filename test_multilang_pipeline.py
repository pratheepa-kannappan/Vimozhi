
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.preprocess import preprocess_text
from nlp.grammar_rules import isl_restructure
from nlp.isl_gloss import to_isl_gloss

TEST_SENTENCES = [
    # ── Tamil ──────────────────────────────────────────────────────────────
    ("Tamil",   "நான் நாளை கல்லூரிக்கு போகிறேன்"),     # I am going to college tomorrow
    ("Tamil",   "என் பெயர் என்ன?"),                      # What is my name?
    ("Tamil",   "அவள் சாப்பிட விரும்பவில்லை"),           # She does not want to eat
    ("Tamil",   "நீங்கள் எங்கே போகிறீர்கள்?"),            # Where are you going?

    # ── Telugu ─────────────────────────────────────────────────────────────
    ("Telugu",  "నేను రేపు కళాశాలకు వెళ్తున్నాను"),      # I am going to college tomorrow
    ("Telugu",  "నీ పేరు ఏమిటి?"),                        # What is your name?
    ("Telugu",  "అతను నీళ్ళు తాగాలనుకుంటున్నాడు"),        # He wants to drink water
    ("Telugu",  "ఆమె తినాలనుకోవడం లేదు"),                 # She does not want to eat

    # ── French ─────────────────────────────────────────────────────────────
    ("French",  "Je vais à l'université demain"),          # I am going to college tomorrow
    ("French",  "Quel est ton nom?"),                      # What is your name?
    ("French",  "Elle ne veut pas manger"),                # She does not want to eat
    ("French",  "Où vas-tu?"),                             # Where are you going?

    # ── English passthrough (must be unchanged) ────────────────────────────
    ("English", "I am going to college tomorrow"),
    ("English", "She does not want to eat"),
    ("English", "What is your name?"),
]

DIVIDER = "─" * 60

def run_test(label, text):
    print(f"\n{DIVIDER}")
    print(f"[{label:7s}] Input:     {text}")
    try:
        doc = preprocess_text(text)
        isl_words = isl_restructure(doc)
        gloss = to_isl_gloss(isl_words)
        print(f"           English:   {doc.text}")
        print(f"           ISL words: {isl_words}")
        print(f"           ISL gloss: {gloss}")
    except Exception as e:
        print(f"           ERROR: {e}")

if __name__ == "__main__":
    print("Multi-language → ISL pipeline test")
    print("Languages: Tamil | Telugu | French | English\n")
    for label, sentence in TEST_SENTENCES:
        run_test(label, sentence)
    print(f"\n{DIVIDER}")
    print("Done.")
