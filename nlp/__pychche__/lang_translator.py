from googletrans import Translator, LANGUAGES

_translator = Translator()

SUPPORTED_LANGS = {
    "ta": "Tamil",
    "te": "Telugu",
    "fr": "French",
    "hi": "Hindi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "de": "German",
    "es": "Spanish",
    "ar": "Arabic",
    #"zh-cn": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
}

# Unicode ranges for script-based fast detection (avoids an API call)
# Format: (start_codepoint, end_codepoint, lang_code)
UNICODE_RANGES = [
    (0x0B80, 0x0BFF, "ta"),   # Tamil
    (0x0C00, 0x0C7F, "te"),   # Telugu
    (0x0900, 0x097F, "hi"),   # Hindi / Devanagari
    (0x0C80, 0x0CFF, "kn"),   # Kannada
    (0x0D00, 0x0D7F, "ml"),   # Malayalam
    (0x0600, 0x06FF, "ar"),   # Arabic
    (0x4E00, 0x9FFF, "zh-cn"),# Chinese
    (0x3040, 0x30FF, "ja"),   # Japanese (Hiragana + Katakana)
    (0xAC00, 0xD7AF, "ko"),   # Korean
]


def detect_script_language(text: str) -> str | None:
    for ch in text:
        cp = ord(ch)
        for start, end, lang_code in UNICODE_RANGES:
            if start <= cp <= end:
                return lang_code
    return None


def translate_to_english(text: str) -> str:
    if not text or not text.strip():
        return text

    try:
        lang_code = detect_script_language(text)

        if lang_code is None:
            detected = _translator.detect(text)
            lang_code = detected.lang  # e.g. "fr", "en", "de"

        if lang_code == "en":
            return text

        lang_name = SUPPORTED_LANGS.get(lang_code, lang_code.upper())
        result = _translator.translate(text, src=lang_code, dest="en")
        translated = result.text
        print(f"[{lang_name}→English] '{text}' → '{translated}'")
        return translated

    except Exception as e:
        print(f"[WARN] Translation failed for '{text}': {e}. Using original.")
        return text  

def get_supported_languages() -> dict:
    """Returns the SUPPORTED_LANGS dict — useful for UI display."""
    return SUPPORTED_LANGS.copy()
