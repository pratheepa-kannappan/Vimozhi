import spacy
import re
from nlp.lang_translator import translate_to_english   # ← UPDATED import

# Load once
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text):
    # ── Translate any supported language → English ───────────────────────
    text = translate_to_english(text)
    # ─────────────────────────────────────────────────────────────────────

    # Basic cleanup (original, unchanged)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    # Convert to spaCy Doc (original, unchanged)
    doc = nlp(text)
    return doc
