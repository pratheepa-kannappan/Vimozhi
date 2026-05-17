from .sign_resolver import resolve_sign_units
from .sign_mapper import map_sentence_to_signs


def sentence_to_signs(isl_words):
    all_sign_units = []

    for word in isl_words:
        if not word:
            continue

        word = str(word).strip().upper()
        if not word:
            continue

        units = resolve_sign_units(word)
        if not units:
            print(f"[WARN] No sign units found for: {word}")
            continue

        print(f"[INFO] Sign units for {word}: {units}")
        all_sign_units.extend(units)

    sign_frames = map_sentence_to_signs(all_sign_units)
    print(f"[INFO] Sign frames returned: {sign_frames}")
    return sign_frames
