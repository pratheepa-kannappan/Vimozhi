def remove_duplicates(words):
    seen = set()
    result = []
    for w in words:
        if w not in seen:
            result.append(w)
            seen.add(w)
    return result


def isl_restructure(doc):
    """
    MODEL-2 Grammar Rules (FINAL - spaCy compatible):
    - QUESTION word first
    - TIME first
    - Remove auxiliary words
    - Subject/Object next
    - Verb at the end
    - NEGATION at the end
    """

    time_words = {"today", "tomorrow", "yesterday"}
    question_words = {"what", "where", "when", "why", "how"}
    aux_words = {"am", "is", "are", "was", "were", "to", "the", "a", "an"}

    verbs_map = {
        "going": "go",
        "eating": "eat",
        "likes": "like",
        "liked": "like",
        "wants": "want",
        "wanted": "want"
    }

    time = []
    content = []
    verbs = []
    negation = []
    question = None

    for token in doc:
        word = token.text.lower()

        # Skip punctuation
        if token.is_punct:
            continue

        # Question
        if word in question_words:
            question = word

        # Time
        elif word in time_words:
            time.append(word)

        # Negation
        elif word in {"not", "dont", "don't", "didnt", "didn't", "wont", "won't"}:
            negation.append("not")

        # Remove auxiliaries
        elif word in aux_words:
            continue

        # Verb normalization
        elif word in verbs_map:
            verbs.append(verbs_map[word])

        elif token.pos_ == "VERB":
            verbs.append(word)

        else:
            content.append(word)

    # ISL word order
    isl_sentence = []

    if question:
        isl_sentence.append(question.upper())

    isl_sentence += [w.upper() for w in time]
    isl_sentence += [w.upper() for w in content]
    isl_sentence += [w.upper() for w in verbs]
    isl_sentence += [w.upper() for w in negation]

    # Remove duplicates
    isl_sentence = remove_duplicates(isl_sentence)

    return isl_sentence
