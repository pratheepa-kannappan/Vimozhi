from sign.sign_mapper import map_sentence_to_signs

test_units = [
    ("WORD", "GO"),
    ("WORD", "COLLEGE"),
    ("ALPHABET", "A"),
    ("DIGIT", "5")
]

frames = map_sentence_to_signs(test_units)

for f in frames:
    print(f)
