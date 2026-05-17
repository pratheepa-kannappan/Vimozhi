from .sign_index import WORD_ROOT, ALPHABET_ROOT, DIGIT_ROOT

import os

# =========================
# ROOT DECLARATION
# =========================
SIGN_ROOT = "sign_data"

WORD_ROOT = os.path.join(SIGN_ROOT, "WORD")
ALPHABET_ROOT = os.path.join(SIGN_ROOT, "ALPHABET")
DIGIT_ROOT = os.path.join(SIGN_ROOT, "DIGIT")


# =========================
# CORE SIGN MAPPING
# =========================
def get_sign_path(sign_type, value):
    """
    Returns folder path for a sign unit
    sign_type: WORD | ALPHABET | DIGIT
    value: GO / A / 5
    """

    value = value.upper()

    if sign_type == "WORD":
        path = os.path.join(WORD_ROOT, value)

    elif sign_type == "ALPHABET":
        path = os.path.join(ALPHABET_ROOT, value)

    elif sign_type == "DIGIT":
        path = os.path.join(DIGIT_ROOT, value)

    else:
        return None

    return path if os.path.exists(path) else None


# =========================
# LOAD IMAGE / VIDEO FILES
# =========================
def load_sign_frames(sign_type, value):
    """
    Returns ordered list of sign frame paths
    """

    folder = get_sign_path(sign_type, value)
    if not folder:
        return []

    files = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".png", ".mp4"))
    ])

    return files


# =========================
# FULL SENTENCE MAPPING
# =========================
def map_sentence_to_signs(sign_units):
    """
    sign_units: [('WORD','GO'), ('ALPHABET','H')]
    """

    sign_sequence = []

    for sign_type, value in sign_units:
        frames = load_sign_frames(sign_type, value)

        if frames:
            sign_sequence.extend(frames)
        else:
            print(f"[WARN] Missing sign data: {sign_type} -> {value}")

    return sign_sequence
