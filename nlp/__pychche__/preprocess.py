import spacy
import re

# Load once
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Clean text and return spaCy Doc object
    """

    # Basic cleanup (optional)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    # Convert to spaCy Doc
    doc = nlp(text)

    return doc
