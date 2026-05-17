import os

# ===============================
# PATH SETUP (DO NOT CHANGE)
# ===============================

# Path of this file → signs/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root → setconference/
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Main sign dataset folder
SIGN_ROOT = os.path.join(PROJECT_ROOT, "sign_data")

# Sub-folders
WORD_ROOT = os.path.join(SIGN_ROOT, "WORD")
ALPHABET_ROOT = os.path.join(SIGN_ROOT, "ALPHABET")
DIGIT_ROOT = os.path.join(SIGN_ROOT, "DIGIT")


# ===============================
# LOAD AVAILABLE SIGNS
# ===============================

def load_signs(folder_path):
    """
    Returns a set of all folder names inside the given directory
    """
    if not os.path.exists(folder_path):
        return set()

    return set(
        name for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    )


AVAILABLE_WORD_SIGNS = load_signs(WORD_ROOT)
AVAILABLE_ALPHABET_SIGNS = load_signs(ALPHABET_ROOT)
AVAILABLE_DIGIT_SIGNS = load_signs(DIGIT_ROOT)


# ===============================
# SIGN TYPE CHECK FUNCTIONS
# ===============================

def is_word_sign(word):
    """
    Check if a full WORD sign exists
    Example: GO, COLLEGE, TODAY
    """
    return word.upper() in AVAILABLE_WORD_SIGNS


def is_letter_sign(letter):
    """
    Check if an ALPHABET sign exists
    Example: A, B, C
    """
    return letter.upper() in AVAILABLE_ALPHABET_SIGNS


def is_digit_sign(digit):
    """
    Check if a DIGIT sign exists
    Example: 0, 1, 2
    """
    return str(digit) in AVAILABLE_DIGIT_SIGNS
