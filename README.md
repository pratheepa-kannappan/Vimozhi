# 🤟 Audio to Indian Sign Language (ISL) Converter

**VIT Chennai | Presented by Abarna P & Pratheepa K**

A real-time system that converts spoken or written English into **Indian Sign Language (ISL) gloss** — with matching sign images for every word, full finger-spelling fallback, and a proper ISL grammar engine.

---

## 📁 Full Project Folder Structure

```
SETCONFERENCE/
│
├── app.py                          ← 🌐 Streamlit web app (main entry point)
├── main.py                         ← Terminal-based pipeline runner
├── model1_pipeline.py              ← Voice-to-ISL pipeline function
├── record_and_run.py               ← Manual audio record + convert script
├── test_full_pipeline.py           ← End-to-end pipeline test
├── test_sign_mapper.py             ← Sign mapper unit test
├── sample.mp3                      ← Sample audio for testing
│
├── image1_hands_birds.jpeg         ← 🖼️ Hero image 1 (place in root)
├── image2_artist_hands.jpeg        ← 🖼️ Hero image 2 (place in root)
├── image3_eyes_hands.jpeg          ← 🖼️ Hero image 3 (place in root)
├── Speech_to_Sign.mp4              ← 🎬 Demo video (place in root)
│
├── nlp/                            ← NLP processing module
│   ├── __init__.py
│   ├── grammar_rules.py            ← ISL grammar restructuring
│   ├── isl_gloss.py                ← English → ISL gloss mapping
│   └── preprocess.py              ← spaCy text preprocessing
│
├── speech/                         ← Speech-to-text module
│   ├── __init__.py
│   ├── voice_to_text.py            ← Whisper transcription
│   └── wish.py                     ← Whisper model loader
│
├── sign/                           ← Sign resolution module
│   ├── __init__.py
│   ├── sentence_to_signs.py        ← Converts ISL words → sign units
│   ├── sign_index.py               ← Indexes available signs from sign_data/
│   ├── sign_mapper.py              ← Maps sign units → image file paths
│   └── sign_resolver.py            ← Resolves word → WORD / ALPHABET / DIGIT
│
├── sign_data/                      ← 📂 Sign image dataset
│   ├── WORD/                       ← One folder per ISL word
│   │   ├── GO/
│   │   │   └── go.jpg
│   │   ├── COLLEGE/
│   │   │   └── college.jpg
│   │   └── TODAY/ ...
│   ├── ALPHABET/                   ← One folder per letter A–Z
│   │   ├── A/
│   │   │   └── a.jpg
│   │   ├── B/ ...
│   │   └── Z/
│   └── DIGIT/                      ← One folder per digit 0–9
│       ├── 0/
│       │   └── zero.jpg
│       └── 1/ ...
│
├── recordings/                     ← 🎙️ Auto-created, stores mic recordings
│   └── recording_YYYY-MM-DD.wav
│
├── output/                         ← 📋 Auto-created by app.py
│   └── isl_gloss_log.txt
│
└── outputs/                        ← 📋 Auto-created by record_and_run.py
    └── isl_gloss_log.txt
```

---

## ❓ Why We Built This

**6.3% of India's population** has significant auditory impairment — yet no real-time, grammar-aware speech-to-ISL tool existed. Existing tools have three key problems:

| Problem | Our Solution |
|---|---|
| Word-for-word translation ignores ISL syntax | Custom ISL grammar engine (Time → Subject → Verb → Negation) |
| No fallback for missing words | Automatic full finger-spelling for unknown words |
| Heavy reliance on Kinect/depth sensors | Works with standard audio input + image dataset |

ISL uses a **double-hand system** (unlike ASL's single-hand), making it significantly more complex to model. We bridge that gap with a pure software pipeline.

---

## ⚙️ Pipeline — How It Works

```
Audio / Text Input
        ↓
[1] Whisper AI  →  Transcribes speech to English text
        ↓
[2] preprocess.py  →  spaCy tokenization + POS tagging
        ↓
[3] grammar_rules.py  →  ISL word-order restructuring
                          (Time → Subject/Object → Verb → Negation)
        ↓
[4] isl_gloss.py  →  Multi-word sign lookup + single-word mapping
        ↓
[5] sign_resolver.py  →  WORD sign? → DIGIT sign? → Finger-spell?
        ↓
[6] sign_mapper.py  →  Loads image file paths for each sign unit
        ↓
Sign images displayed in Streamlit UI
```

### ISL Grammar Rules (`nlp/grammar_rules.py`)

ISL word order is **completely different** from English:

| English | ISL Gloss |
|---|---|
| I am going to college tomorrow | TOMORROW COLLEGE GO |
| She does not want to eat | SHE EAT WANT NOT |
| What are you doing? | WHAT YOU DO |

Rules applied:
- **Question words** → placed first
- **Time words** (today, tomorrow, yesterday) → placed second
- **Auxiliaries removed** (am, is, are, was, were, to, the, a, an)
- **Verbs normalized** (going → GO, eating → EAT, liked → LIKE)
- **Negation** (not, don't, didn't) → placed last as NOT
- **Duplicates removed**

### ISL Gloss Mapping (`nlp/isl_gloss.py`)

Supports **multi-word signs** checked in order: 4-word → 3-word → 2-word → single.

Example multi-word signs supported:

| English Phrase | ISL Sign |
|---|---|
| computer science | COMPUTER_SCIENCE |
| sign language | SIGN_LANGUAGE |
| how are you | HOW_ARE_YOU |
| artificial intelligence | ARTIFICIAL_INTELLIGENCE |
| thank you very much | THANK_YOU_VERY_MUCH |
| bus stand | BUS_STAND |
| police station | POLICE_STATION |

### Sign Resolution (`sign/sign_resolver.py`)

For each ISL gloss word, resolution happens in this order:

1. ✅ **WORD sign exists** → use `sign_data/WORD/WORDNAME/`
2. ✅ **DIGIT** → use `sign_data/DIGIT/N/`
3. ✅ **Unknown word** → **finger-spell every letter** using `sign_data/ALPHABET/`

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- pip

### Step 1 — Install dependencies

```bash
pip install streamlit spacy openai-whisper sounddevice scipy numpy opencv-python
```

### Step 2 — Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### Step 3 — Add your sign images

Place sign images inside `sign_data/` following the folder structure above.
- Folder name = the sign word (e.g. `WORD/GO/`, `ALPHABET/A/`, `DIGIT/5/`)
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- File names inside don't matter — only the **folder name** is matched

### Step 4 — Add hero images & demo video (for web app)

Place these files in the **root folder** (same folder as `app.py`):

```
image1_hands_birds.jpeg
image2_artist_hands.jpeg
image3_eyes_hands.jpeg
Speech_to_Sign.mp4
```

### Step 5 — Run the web app

```bash
streamlit run app.py
```

---

## 🖥️ Running Other Scripts

### Terminal pipeline (no UI)

```bash
python main.py
# Press ENTER to start recording, ENTER again to stop
```

### Record and convert loop

```bash
python record_and_run.py
# Records audio, converts to ISL gloss, repeats until you say n
```

### Test the full pipeline with an audio file

```bash
# Place a sample.mp3 in the root folder first
python test_full_pipeline.py
```

### Test sign mapper only

```bash
python test_sign_mapper.py
```

---

## 📂 Module Reference

### `nlp/preprocess.py`
- Loads spaCy `en_core_web_sm` model once
- Cleans text (lowercase, removes punctuation)
- Returns a spaCy `Doc` object with POS tags

### `nlp/grammar_rules.py`
- `isl_restructure(doc)` — applies ISL word-order rules
- `remove_duplicates(words)` — removes repeated gloss tokens

### `nlp/isl_gloss.py`
- `to_isl_gloss(words)` — maps reordered words to ISL gloss tokens
- `MULTI_WORD_SIGNS` — dictionary of phrase → ISL sign
- `ENGLISH_TO_ISL` — dictionary of single word → ISL token

### `speech/wish.py`
- Loads Whisper `base` model once at startup

### `speech/voice_to_text.py`
- `voice_to_text(audio_path)` — transcribes audio file to English string

### `sign/sign_index.py`
- Indexes all available signs from `sign_data/` subfolders
- Provides `is_word_sign()`, `is_letter_sign()`, `is_digit_sign()`

### `sign/sign_resolver.py`
- `resolve_sign_units(token)` — returns list of `(type, value)` tuples
- Falls back to finger-spelling if no word/digit sign found

### `sign/sign_mapper.py`
- `get_sign_path(sign_type, value)` — returns folder path for a sign
- `load_sign_frames(sign_type, value)` — returns sorted image file list
- `map_sentence_to_signs(sign_units)` — returns full image path sequence

### `sign/sentence_to_signs.py`
- `sentence_to_signs(isl_words)` — orchestrates resolve + map for a full sentence

---

## 🌐 Web App Pages

### Home Page
- Project overview, mission, statistics
- "Why We Built This" section
- Pipeline diagram (6 steps)
- Demo video player
- Hero images

### Text → ISL Page
- Text input area
- 4 example sentence buttons
- Converts to ISL gloss + displays sign images

### Voice → ISL Page
- **Tab 1:** Browser microphone recording (requires Streamlit ≥ 1.33)
- **Tab 2:** Upload WAV / MP3 / M4A file
- Previously saved recordings picker

---

## 📝 Output Logs

Every conversion is saved automatically:

```
output/isl_gloss_log.txt        ← from app.py (web UI)
outputs/isl_gloss_log.txt       ← from record_and_run.py (terminal)
```

Log format:
```
──────────────────────────────────────────────────
Time: 2026-01-09 22:22:02
Recognized Text:  I am going to college tomorrow
ISL Gloss: TOMORROW COLLEGE GO
──────────────────────────────────────────────────
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: spacy` | Run `pip install spacy` and `python -m spacy download en_core_web_sm` |
| `ModuleNotFoundError: whisper` | Run `pip install openai-whisper` |
| Images show "not found" | Check image files are in root folder; check filename matches exactly |
| Sign images not showing | Check `sign_data/WORD/WORDNAME/` folder exists with images inside |
| Finger-spelling shows only 1 letter | Update to latest `app.py` — old bug fixed |
| Video not showing | Place `Speech_to_Sign.mp4` in root folder (same as `app.py`) |
| Audio recording doesn't work in browser | Upgrade Streamlit: `pip install --upgrade streamlit` (needs ≥ 1.33) |

---

## 🏗️ Tech Stack

| Component | Technology |
|---|---|
| Web UI | Streamlit |
| Speech-to-Text | OpenAI Whisper (base model) |
| NLP / POS Tagging | spaCy `en_core_web_sm` |
| ISL Grammar | Custom rule-based engine |
| Sign Image Display | Python + base64 + HTML |
| Audio Recording | sounddevice + scipy |
| Sign Visualization | OpenCV (terminal) / Streamlit (web) |

---

*Built at VIT Chennai · Supporting the Deaf community through accessible technology* 🤟
