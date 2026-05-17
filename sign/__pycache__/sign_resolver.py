from .sign_index import (
    is_word_sign,
    is_letter_sign,
    is_digit_sign
)

def resolve_sign_units(token):
    """
    Returns a list of sign units to display
    """

    token = token.upper()
    sign_units = []

    # 1️⃣ WORD sign
    if is_word_sign(token):
        sign_units.append(("WORD", token))
        return sign_units

    # 2️⃣ DIGIT sign
    if token.isdigit() and is_digit_sign(token):
        sign_units.append(("DIGIT", token))
        return sign_units

    # 3️⃣ LETTER fallback (spell it)
    for char in token:
        if char.isalpha() and is_letter_sign(char):
            sign_units.append(("ALPHABET", char))
        elif char.isdigit() and is_digit_sign(char):
            sign_units.append(("DIGIT", char))
        else:
            # Unknown character
            print(f"[WARN] No sign found for: {char}")

    return sign_units


print(resolve_sign_units("GO"))
print(resolve_sign_units("HELLO"))
print(resolve_sign_units("123"))
print(resolve_sign_units("MEET@"))