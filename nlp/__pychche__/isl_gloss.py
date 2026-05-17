MULTI_WORD_SIGNS = {
    #SENTANCES
    ("how", "are", "you"): "HOW_ARE_YOU",
    ("meet","you","soon"): "MEET_YOU_SOON",
    ("thank","you","very","much"): "THANK_YOU_VERY_MUCH",
    ("sign", "language"): "SIGN_LANGUAGE",
    # 🚌 Transport
    ("bus", "stand"): "BUS_STAND",
    ("bus", "stop"): "BUS_STOP",
    ("train", "station"): "TRAIN_STATION",
    ("railway", "station"): "RAILWAY_STATION",
    ("metro", "station"): "METRO_STATION",
    ("auto", "stand"): "AUTO_STAND",
    ("taxi", "stand"): "TAXI_STAND",
    ("flight", "ticket"): "FLIGHT_TICKET",
    ("train", "ticket"): "TRAIN_TICKET",

    # 🏫 Education
    ("college", "campus"): "COLLEGE_CAMPUS",
    ("engineering", "college"): "ENGINEERING_COLLEGE",
    ("arts", "college"): "ARTS_COLLEGE",
    ("computer", "science"): "COMPUTER_SCIENCE",
    ("data", "science"): "DATA_SCIENCE",
    ("information", "technology"): "INFORMATION_TECHNOLOGY",

    # 🏥 Health
    ("government", "hospital"): "GOVT_HOSPITAL",
    ("private", "hospital"): "PRIVATE_HOSPITAL",
    ("primary", "health"): "PRIMARY_HEALTH",
    ("health", "center"): "HEALTH_CENTER",
    ("medical", "college"): "MEDICAL_COLLEGE",

    # 🏛 Government / Services
    ("post", "office"): "POST_OFFICE",
    ("police", "station"): "POLICE_STATION",
    ("passport", "office"): "PASSPORT_OFFICE",
    ("ration", "shop"): "RATION_SHOP",
    ("electricity", "office"): "ELECTRICITY_OFFICE",

    # 🏠 Daily Life
    ("bus", "fare"): "BUS_FARE",
    ("room", "rent"): "ROOM_RENT",
    ("house", "rent"): "HOUSE_RENT",
    ("water", "bottle"): "WATER_BOTTLE",
    ("mobile", "phone"): "MOBILE_PHONE",
    ("cell", "phone"): "MOBILE_PHONE",

    # 🍽 Food
    ("street", "food"): "STREET_FOOD",
    ("fast", "food"): "FAST_FOOD",
    ("fruit", "shop"): "FRUIT_SHOP",
    ("tea", "shop"): "TEA_SHOP",
    ("coffee", "shop"): "COFFEE_SHOP",

    # 💻 Technology
    ("machine", "learning"): "MACHINE_LEARNING",
    ("artificial", "intelligence"): "ARTIFICIAL_INTELLIGENCE",
    ("deep", "learning"): "DEEP_LEARNING",
    ("cloud", "computing"): "CLOUD_COMPUTING",

    # 🕒 Time Expressions
    ("day", "after"): "DAY_AFTER",
    ("day", "before"): "DAY_BEFORE",
    ("next", "week"): "NEXT_WEEK",
    ("last", "week"): "LAST_WEEK",
    ("this", "morning"): "THIS_MORNING",
    ("this", "evening"): "THIS_EVENING"
}

ENGLISH_TO_ISL = {

    # Pronouns (form changes)
    "i": "ME", "me": "ME",
    "my": "MY", "mine": "MINE",

    "you": "YOU", "your": "YOUR",

    "he": "HE", "him": "HE", "his": "HIS",
    "she": "SHE", "her": "SHE", "hers": "HERS",

    "we": "WE", "us": "WE", "our": "OUR",
    "they": "THEY", "them": "THEY", "their": "THEIR",

    # Auxiliary verbs (removed in ISL)
    "am": "", "is": "", "are": "",
    "was": "", "were": "",
    "be": "", "been": "",

    # Articles & prepositions (mostly removed)
    "a": "", "an": "", "the": "",
    "to": "", "of": "", "for": "",
    "in": "", "on": "", "at": "",

    # Verb normalization (tense → base sign)
    "going": "GO", "goes": "GO", "went": "GO",
    "eating": "EAT", "ate": "EAT",
    "drinking": "DRINK", "drank": "DRINK",
    "studying": "STUDY", "studied": "STUDY",
    "working": "WORK", "worked": "WORK",
    "wanting": "WANT", "wanted": "WANT",

    # Negation
    "not": "NOT",
    "no": "NO",

    # Modals (simplified)
    "can": "CAN",
    "cannot": "CANNOT",
    "cant": "CANNOT",
    "will": "WILL",
    "would": "WILL",
    "should": "SHOULD",
    "must": "MUST",

    # Time words (important in ISL order)
    "today": "TODAY",
    "tomorrow": "TOMORROW",
    "yesterday": "YESTERDAY",
    "now": "NOW",
    "morning": "MORNING",
    "evening": "EVENING",
    "night": "NIGHT"
}
"""
    Convert reordered English words into ISL gloss
    - Supports multi-word signs
    - Removes empty tokens
    - Normalizes to UPPERCASE
"""

"""def to_isl_gloss(words):
    

    glosses = []
    i = 0

    # Normalize input (remove empty, lowercase → uppercase)
    words = [w.strip().lower() for w in words if w and str(w).strip()]

    while i < len(words):

        # 🔹 Multi-word sign check
        if i + 1 < len(words):
            pair = (words[i], words[i + 1])
            if pair in MULTI_WORD_SIGNS:
                glosses.append(MULTI_WORD_SIGNS[pair].upper())
                i += 2
                continue

        # 🔹 Single-word mapping
        word = words[i]

        gloss = ENGLISH_TO_ISL.get(word, word).upper()

        if gloss.strip():   # safety check
            glosses.append(gloss)

        i += 1

    return glosses
"""
def to_isl_gloss(words):
    glosses = []
    i = 0

    words = [w.lower().strip() for w in words if w.strip()]

    while i < len(words):

        # 🔴 4-word phrases
        if i + 3 < len(words):
            quad = tuple(words[i:i+4])
            if quad in MULTI_WORD_SIGNS:
                glosses.append(MULTI_WORD_SIGNS[quad])
                i += 4
                continue

        # 🔴 3-word phrases
        if i + 2 < len(words):
            tri = tuple(words[i:i+3])
            if tri in MULTI_WORD_SIGNS:
                glosses.append(MULTI_WORD_SIGNS[tri])
                i += 3
                continue

        # 🔴 2-word phrases
        if i + 1 < len(words):
            pair = tuple(words[i:i+2])
            if pair in MULTI_WORD_SIGNS:
                glosses.append(MULTI_WORD_SIGNS[pair])
                i += 2
                continue

        # 🔹 Single word
        word = words[i]
        gloss = ENGLISH_TO_ISL.get(word, word)
        if gloss:
            glosses.append(gloss.upper())
        i += 1

    return glosses
