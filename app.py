import streamlit as st
import os
import tempfile
import time
import base64
from pathlib import Path

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ISL Converter | Indian Sign Language",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Fraunces:wght@700;800;900&display=swap');

:root {
    --cream: #FBF8F3;
    --warm-white: #FFFFFF;
    --amber: #E8894A;
    --amber-light: #F4B078;
    --amber-pale: #FFF0E3;
    --teal: #2A7F7F;
    --teal-light: #3D9E9E;
    --teal-pale: #E0F4F4;
    --slate: #1E2D3A;
    --slate-mid: #3D5060;
    --slate-light: #6B8599;
    --border: #E8E0D5;
    --shadow: rgba(30,45,58,0.08);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--slate);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 3rem; max-width: 1280px; }

/* ── HERO ── */
.hero-wrap {
    background: linear-gradient(135deg, #FBF8F3 0%, #FFF0E3 40%, #E0F4F4 100%);
    border-radius: 0 0 32px 32px;
    padding: 3rem 3.5rem 3.5rem;
    margin-bottom: 3rem;
    border-bottom: 2px solid var(--border);
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,137,74,0.12), transparent 70%);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(42,127,127,0.1), transparent 70%);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: var(--amber-pale); color: var(--amber);
    border: 1.5px solid var(--amber-light);
    border-radius: 100px; padding: 0.3em 1em;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 3.2rem; font-weight: 900;
    color: var(--slate); line-height: 1.1;
    margin: 0 0 1rem 0;
}
.hero-title span { color: var(--amber); }
.hero-subtitle {
    font-size: 1.1rem; color: var(--slate-mid);
    max-width: 580px; line-height: 1.75;
    margin: 0 0 2rem 0;
}
.hero-images {
    display: flex; gap: 1.2rem; align-items: center;
    flex-wrap: wrap; margin-top: 1.5rem;
}
.hero-img-card {
    border-radius: 16px; overflow: hidden;
    border: 2px solid var(--border);
    box-shadow: 0 4px 20px var(--shadow);
    flex: 1; min-width: 180px; max-width: 260px;
    aspect-ratio: 4/3; object-fit: cover;
}
.hero-img-card img { width: 100%; height: 100%; object-fit: cover; }

/* ── WHY SECTION ── */
.why-section {
    background: var(--warm-white);
    border-radius: 24px; padding: 2.5rem 3rem;
    border: 1.5px solid var(--border);
    box-shadow: 0 4px 24px var(--shadow);
    margin-bottom: 2.5rem;
}
.section-eyebrow {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--teal);
    margin-bottom: 0.5rem;
}
.section-title {
    font-family: 'Fraunces', serif; font-size: 1.9rem; font-weight: 800;
    color: var(--slate); margin: 0 0 1.5rem 0;
}
.stats-row {
    display: flex; gap: 2rem; flex-wrap: wrap; margin: 1.5rem 0;
}
.stat-block { flex: 1; min-width: 140px; }
.stat-number {
    font-family: 'Fraunces', serif; font-size: 2.8rem; font-weight: 900;
    color: var(--amber); line-height: 1;
}
.stat-label { font-size: 0.88rem; color: var(--slate-light); margin-top: 0.3rem; line-height: 1.4; }
.why-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem; margin-top: 1.5rem;
}
.why-card {
    background: var(--cream); border-radius: 16px;
    padding: 1.3rem 1.5rem; border: 1.5px solid var(--border);
}
.why-card .icon { font-size: 1.6rem; margin-bottom: 0.6rem; }
.why-card h4 {
    font-size: 0.95rem; font-weight: 700; color: var(--slate);
    margin: 0 0 0.4rem 0;
}
.why-card p { font-size: 0.85rem; color: var(--slate-light); margin: 0; line-height: 1.55; }

/* ── VIDEO SECTION ── */
.video-section {
    background: var(--slate);
    border-radius: 24px; padding: 2.5rem 3rem;
    margin-bottom: 2.5rem; overflow: hidden;
    position: relative;
}
.video-section .section-title { color: white; }
.video-section .section-eyebrow { color: var(--amber-light); }
.video-wrap {
    border-radius: 16px; overflow: hidden;
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 40px rgba(0,0,0,0.3);
    margin-top: 1.5rem;
}

/* ── HOW IT WORKS ── */
.pipeline-section {
    background: linear-gradient(135deg, var(--teal-pale) 0%, var(--amber-pale) 100%);
    border-radius: 24px; padding: 2.5rem 3rem;
    border: 1.5px solid var(--border);
    margin-bottom: 2.5rem;
}
.pipeline-steps {
    display: flex; gap: 0; margin-top: 1.5rem;
    align-items: stretch; flex-wrap: wrap;
}
.pipe-item {
    flex: 1; min-width: 120px;
    background: white; border-radius: 16px;
    padding: 1.2rem 1rem; text-align: center;
    position: relative;
    border: 1.5px solid var(--border);
    box-shadow: 0 2px 12px var(--shadow);
    margin: 0 0.5rem;
}
.pipe-item:first-child { margin-left: 0; }
.pipe-item:last-child { margin-right: 0; }
.pipe-num {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, var(--teal), var(--teal-light));
    color: white; font-weight: 800; font-size: 0.85rem;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 0.7rem;
    box-shadow: 0 3px 10px rgba(42,127,127,0.35);
}
.pipe-item h4 { font-size: 0.88rem; font-weight: 700; color: var(--slate); margin: 0 0 0.25rem 0; }
.pipe-item p { font-size: 0.72rem; color: var(--slate-light); margin: 0; line-height: 1.4; }
.pipe-arrow-outer {
    display: flex; align-items: center;
    color: var(--amber); font-size: 1.4rem; font-weight: 700;
    padding: 0 0.1rem; flex-shrink: 0; align-self: center;
}

/* ── MODE BUTTONS ── */
.mode-section {
    margin-bottom: 2rem;
}
.mode-section h2 {
    font-family: 'Fraunces', serif; font-size: 1.8rem;
    color: var(--slate); margin-bottom: 1.2rem;
}
.mode-btn-row {
    display: flex; gap: 1.2rem; flex-wrap: wrap;
}
.mode-btn {
    flex: 1; min-width: 200px; max-width: 340px;
    border-radius: 18px; padding: 1.4rem 2rem;
    border: none; cursor: pointer;
    font-family: 'DM Sans', sans-serif; font-size: 1.05rem; font-weight: 700;
    display: flex; align-items: center; gap: 0.8rem;
    transition: all 0.25s ease;
    text-decoration: none; position: relative; overflow: hidden;
}
.mode-btn-text {
    background: linear-gradient(135deg, #2A7F7F, #3D9E9E);
    color: white; box-shadow: 0 6px 24px rgba(42,127,127,0.35);
}
.mode-btn-text:hover { transform: translateY(-3px); box-shadow: 0 10px 32px rgba(42,127,127,0.45); }
.mode-btn-voice {
    background: linear-gradient(135deg, #E8894A, #F4B078);
    color: white; box-shadow: 0 6px 24px rgba(232,137,74,0.35);
}
.mode-btn-voice:hover { transform: translateY(-3px); box-shadow: 0 10px 32px rgba(232,137,74,0.45); }
.mode-btn-icon { font-size: 1.6rem; }
.mode-btn-label { display: flex; flex-direction: column; text-align: left; }
.mode-btn-label small { font-size: 0.72rem; font-weight: 400; opacity: 0.85; margin-top: 0.1rem; }

/* Streamlit button overrides for conversion buttons */
.stButton > button {
    border-radius: 14px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    padding: 0.75rem 1.5rem !important; border: 2px solid transparent !important;
    transition: all 0.25s ease !important; width: 100% !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #2A7F7F, #3D9E9E) !important;
    color: white !important; box-shadow: 0 4px 16px rgba(42,127,127,0.3) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #E8894A, #F4B078) !important;
    color: white !important; box-shadow: 0 4px 16px rgba(232,137,74,0.3) !important;
}

/* ── PANEL ── */
.panel {
    background: var(--warm-white);
    border-radius: 24px; padding: 2.5rem 3rem;
    border: 1.5px solid var(--border);
    box-shadow: 0 4px 24px var(--shadow);
    margin-bottom: 2rem;
}
.panel h2 {
    font-family: 'Fraunces', serif; font-size: 1.6rem;
    color: var(--slate); margin: 0 0 0.5rem 0;
}

/* ── Result ── */
.result-box {
    background: linear-gradient(135deg, var(--teal-pale), var(--amber-pale));
    border-radius: 18px; padding: 1.6rem 2rem;
    border: 1.5px solid var(--border); margin-top: 1.2rem;
}
.result-box h3 {
    font-size: 0.78rem; font-weight: 700; color: var(--teal);
    text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 0.8rem 0;
}
.pipeline-vis {
    display: flex; align-items: center; gap: 0.3rem;
    flex-wrap: wrap; margin-bottom: 1rem;
}
.pipeline-vis .pvstep {
    background: white; color: var(--slate-mid);
    border-radius: 100px; padding: 0.2em 0.75em;
    font-size: 0.72rem; font-weight: 700;
    border: 1.5px solid var(--border);
}
.pipeline-vis .pvstep.active {
    background: var(--teal); color: white; border-color: var(--teal);
}
.pipeline-vis .pvarrow { color: var(--amber); font-size: 0.85rem; }
.result-original { font-size: 0.98rem; color: var(--slate-mid); line-height: 1.65; margin: 0; }

/* ── Gloss tokens ── */
.gloss-strip { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.6rem 0 1.2rem; }
.gloss-word {
    display: inline-block;
    background: linear-gradient(135deg, var(--teal-pale), #c5eaea);
    color: var(--teal); border-radius: 10px;
    padding: 0.28em 0.8em; font-size: 1rem; font-weight: 700;
    border: 1.5px solid rgba(42,127,127,0.2);
    letter-spacing: 0.03em;
}

/* ── Sign section ── */
.sign-section-title {
    font-family: 'Fraunces', serif; font-size: 1.2rem;
    color: var(--slate); margin: 1.8rem 0 1rem;
    padding-top: 1.2rem; border-top: 2px solid var(--border);
    display: flex; align-items: center; gap: 0.5rem;
}
.sign-card-wrap {
    background: white; border-radius: 14px;
    border: 1.5px solid var(--border);
    overflow: hidden; padding: 0.7rem 0.7rem 0.4rem;
    box-shadow: 0 2px 12px var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.sign-card-wrap:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 24px var(--shadow);
}
.sign-card-label {
    font-size: 0.78rem; font-weight: 800; color: var(--teal);
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-top: 0.5rem; text-align: center; padding-bottom: 0.3rem;
}
.sign-card-label-spell {
    font-size: 0.72rem; font-weight: 800; color: var(--amber);
    text-transform: uppercase; letter-spacing: 0.06em;
    margin-top: 0.5rem; text-align: center; padding-bottom: 0.3rem;
}
.sign-missing {
    background: var(--cream); border-radius: 14px;
    border: 2px dashed var(--border);
    text-align: center; padding: 2rem 0.4rem;
    color: var(--slate-light); font-size: 0.8rem; font-weight: 700;
}

/* ── Fingerspell word strip ── */
.fingerspell-strip {
    display: flex; gap: 0.4rem; flex-wrap: wrap;
    margin: 0.4rem 0; padding: 0.6rem;
    background: var(--amber-pale); border-radius: 12px;
    border: 1.5px solid rgba(232,137,74,0.2);
}
.fingerspell-letter {
    display: flex; flex-direction: column; align-items: center; gap: 0.2rem;
}
.fingerspell-letter img {
    width: 56px; height: 56px; object-fit: cover;
    border-radius: 8px; border: 1.5px solid var(--border);
}
.fingerspell-letter span {
    font-size: 0.65rem; font-weight: 800; color: var(--amber);
    text-transform: uppercase; letter-spacing: 0.05em;
}
.fingerspell-word-label {
    font-size: 0.7rem; font-weight: 700; color: var(--amber);
    margin-bottom: 0.3rem; display: block;
}

/* ── Log ── */
.log-box {
    background: var(--slate); border-radius: 14px;
    padding: 1.2rem 1.5rem; font-family: 'Courier New', monospace;
    font-size: 0.82rem; color: #8EC8C8;
    border: 1.5px solid rgba(255,255,255,0.08);
}
.log-box .log-line { margin: 0.2rem 0; }
.log-box .log-sep { color: rgba(255,255,255,0.15); }

/* ── Chip ── */
.chip {
    display: inline-flex; align-items: center;
    background: var(--teal-pale); color: var(--teal);
    border-radius: 100px; padding: 0.22em 0.9em;
    font-size: 0.75rem; font-weight: 700;
    border: 1.5px solid rgba(42,127,127,0.2);
    margin-bottom: 1.2rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--cream); border-radius: 14px;
    padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; font-family: 'DM Sans', sans-serif;
    font-weight: 600; color: var(--slate-light);
}
.stTabs [aria-selected="true"] {
    background: white !important; color: var(--slate) !important;
    box-shadow: 0 2px 10px var(--shadow);
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'DM Sans', sans-serif !important;
    background: var(--cream) !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(42,127,127,0.12) !important;
}

/* ── Convert button ── */
div[data-testid="stVerticalBlock"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--teal), var(--teal-light)) !important;
    color: white !important; border-radius: 14px !important;
}
button[data-testid*="convert"] {
    background: linear-gradient(135deg, var(--teal), var(--teal-light)) !important;
    color: white !important;
}

/* ── Footer ── */
.footer {
    text-align: center; color: var(--slate-light);
    font-size: 0.8rem; margin-top: 4rem;
    padding-top: 2rem; border-top: 1.5px solid var(--border);
    line-height: 1.8;
}
.footer strong { color: var(--teal); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PATHS & DIRS
# ══════════════════════════════════════════════════════════════════════════════
SIGN_DATA_ROOT = "sign_data"
WORD_ROOT      = os.path.join(SIGN_DATA_ROOT, "WORD")
ALPHABET_ROOT  = os.path.join(SIGN_DATA_ROOT, "ALPHABET")
DIGIT_ROOT     = os.path.join(SIGN_DATA_ROOT, "DIGIT")
RECORDINGS_DIR = "recordings"
OUTPUT_DIR     = "output"

os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


# ══════════════════════════════════════════════════════════════════════════════
#  PIPELINE WRAPPERS
# ══════════════════════════════════════════════════════════════════════════════
def demo_convert(text: str):
    """Rule-based fallback when NLP modules are not available."""
    remove   = {"am","is","are","was","were","a","an","the","to","of","for",
                 "in","on","at","be","been","this","that"}
    verb_map = {"going":"GO","eating":"EAT","likes":"LIKE","wants":"WANT",
                "working":"WORK","studying":"STUDY","doing":"DO","drinking":"DRINK"}
    time_w   = {"today","tomorrow","yesterday","morning","evening","night","now"}
    neg      = {"not","don't","dont","didn't","didnt","won't","wont"}

    words = text.lower().replace("\u2019","'").split()
    t_p, c_p, v_p, n_p = [], [], [], []
    for w in words:
        w = w.strip(".,!?")
        if not w or w in remove: continue
        if w in time_w:      t_p.append(w.upper())
        elif w in neg:       n_p.append("NOT")
        elif w in verb_map:  v_p.append(verb_map[w])
        else:                c_p.append(w.upper())
    result = t_p + c_p + v_p + n_p
    seen, out = set(), []
    for g in result:
        if g not in seen:
            out.append(g); seen.add(g)
    return out or [w.upper() for w in words if w.lower() not in remove]


def run_text_pipeline(text: str):
    try:
        from nlp.preprocess    import preprocess_text
        from nlp.grammar_rules import isl_restructure
        from nlp.isl_gloss     import to_isl_gloss
        doc       = preprocess_text(text)
        isl_words = isl_restructure(doc)
        glosses   = to_isl_gloss(isl_words)
        return isl_words, glosses, False
    except ImportError:
        glosses = demo_convert(text)
        return glosses, glosses, True


def run_voice_pipeline(audio_path: str):
    try:
        from speech.voice_to_text  import voice_to_text
        from nlp.preprocess        import preprocess_text
        from nlp.grammar_rules     import isl_restructure
        from nlp.isl_gloss         import to_isl_gloss
        text      = voice_to_text(audio_path)
        doc       = preprocess_text(text)
        isl_words = isl_restructure(doc)
        glosses   = to_isl_gloss(isl_words)
        return text, isl_words, glosses, False
    except ImportError:
        demo_text = "What are you doing? Is this late for you?"
        glosses   = demo_convert(demo_text)
        return demo_text, glosses, glosses, True


# ══════════════════════════════════════════════════════════════════════════════
#  SIGN IMAGE HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _first_image(folder: str):
    if not os.path.isdir(folder):
        return None
    for f in sorted(os.listdir(folder)):
        if Path(f).suffix.lower() in IMG_EXTS:
            return os.path.join(folder, f)
    return None


def _all_images(folder: str):
    """Return all image paths in a folder, sorted."""
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if Path(f).suffix.lower() in IMG_EXTS
    ]


def get_sign_image(token: str):
    """Returns (path, type) for WORD or DIGIT, else (None, None)."""
    token = token.strip().upper()
    img = _first_image(os.path.join(WORD_ROOT, token))
    if img: return img, "WORD"
    if token.isdigit():
        img = _first_image(os.path.join(DIGIT_ROOT, token))
        if img: return img, "DIGIT"
    return None, None


def render_sign_images(glosses: list):
    """
    Show sign card per gloss word.
    FIX: For finger-spelling, show ALL letters of the word (not just the first).
    """
    if not glosses:
        return
    st.markdown('<div class="sign-section-title">🖼️ Sign Images</div>', unsafe_allow_html=True)

    COLS = min(len(glosses), 6)
    for row_start in range(0, len(glosses), COLS):
        row = glosses[row_start: row_start + COLS]
        cols = st.columns(len(row))
        for col, word in zip(cols, row):
            img_path, sign_type = get_sign_image(word)
            with col:
                if img_path:
                    # Word / digit sign exists — show it
                    st.markdown('<div class="sign-card-wrap">', unsafe_allow_html=True)
                    st.image(img_path, use_container_width=True)
                    st.markdown(
                        f'<div class="sign-card-label">{word}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # ── Finger-spell ALL letters of the word ──────────────
                    letter_data = []
                    for ch in word:
                        if ch.isalpha():
                            lp = _first_image(os.path.join(ALPHABET_ROOT, ch.upper()))
                            letter_data.append((ch.upper(), lp))
                        elif ch.isdigit():
                            lp = _first_image(os.path.join(DIGIT_ROOT, ch))
                            letter_data.append((ch, lp))

                    if letter_data:
                        # Build inline HTML strip with all letter images
                        letters_html = ""
                        for ch, lp in letter_data:
                            if lp:
                                try:
                                    with open(lp, "rb") as f:
                                        b64 = base64.b64encode(f.read()).decode()
                                    ext = Path(lp).suffix.lower().replace('.', '')
                                    mime = "jpeg" if ext in ("jpg","jpeg") else ext
                                    letters_html += (
                                        f'<div class="fingerspell-letter">'
                                        f'<img src="data:image/{mime};base64,{b64}" />'
                                        f'<span>{ch}</span></div>'
                                    )
                                except Exception:
                                    letters_html += f'<div class="fingerspell-letter"><span style="font-size:1.2rem">❓</span><span>{ch}</span></div>'
                            else:
                                letters_html += f'<div class="fingerspell-letter"><span style="font-size:1.2rem">❓</span><span>{ch}</span></div>'

                        st.markdown(
                            f'<span class="fingerspell-word-label">✋ {word} — finger-spell</span>'
                            f'<div class="fingerspell-strip">{letters_html}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="sign-missing">❓<br>{word}</div>',
                            unsafe_allow_html=True
                        )


def render_gloss_tokens(glosses: list):
    html = "".join(f'<span class="gloss-word">{g}</span>' for g in glosses)
    st.markdown(f'<div class="gloss-strip">{html}</div>', unsafe_allow_html=True)


def save_and_show_log(text: str, glosses: list) -> str:
    import datetime
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sep = "─" * 50
    log = f"{sep}\nTime: {ts}\nRecognized Text:  {text}\nISL Gloss: {' '.join(glosses)}\n{sep}\n"
    with open(os.path.join(OUTPUT_DIR, "isl_gloss_log.txt"), "a", encoding="utf-8") as f:
        f.write(log)
    with st.expander("📋 Session log"):
        st.markdown(
            f'<div class="log-box">'
            f'<div class="log-sep">{sep}</div>'
            f'<div class="log-line">🕐 Time: {ts}</div>'
            f'<div class="log-line">📝 Text:  {text}</div>'
            f'<div class="log-line">🤟 Gloss: {" ".join(glosses)}</div>'
            f'<div class="log-sep">{sep}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    return ts


def show_result(original_text: str, glosses: list, is_demo: bool, source_label: str = "Text"):
    st.markdown(f"""
    <div class="result-box">
        <h3>✅ Conversion Result</h3>
        <div class="pipeline-vis">
            <span class="pvstep">{source_label}</span>
            <span class="pvarrow">→</span>
            <span class="pvstep">Preprocess</span>
            <span class="pvarrow">→</span>
            <span class="pvstep">ISL Grammar</span>
            <span class="pvarrow">→</span>
            <span class="pvstep">Gloss Map</span>
            <span class="pvarrow">→</span>
            <span class="pvstep active">ISL Gloss ✓</span>
        </div>
        <p class="result-original"><strong>Original:</strong> {original_text}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**ISL Gloss tokens:**")
    render_gloss_tokens(glosses)
    render_sign_images(glosses)
    save_and_show_log(original_text, glosses)

    if is_demo:
        st.info(
            "ℹ️ **Demo mode** — NLP/speech modules not found. "
            "Place `app.py` in your project root folder to use the full pipeline."
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "mode" not in st.session_state:
    st.session_state.mode = None


# ══════════════════════════════════════════════════════════════════════════════
#  HOME PAGE  (shown when no mode is selected)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode is None:

    # ── HERO ────────────────────────────────────────────────────────────────
    def img_to_b64(path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except FileNotFoundError:
            return ""

    img1 = img_to_b64("image3_eyes_hands.jpeg")
    img2 = img_to_b64("image2_artist_hands.jpeg")
    img3 = img_to_b64("image1_hands_birds.jpeg")

    img1_tag = f'<img src="data:image/jpeg;base64,{img1}" />' if img1 else '<div style="padding:2rem;text-align:center;color:#aaa;">Image not found</div>'
    img2_tag = f'<img src="data:image/jpeg;base64,{img2}" />' if img2 else '<div style="padding:2rem;text-align:center;color:#aaa;">Image not found</div>'
    img3_tag = f'<img src="data:image/jpeg;base64,{img3}" />' if img3 else '<div style="padding:2rem;text-align:center;color:#aaa;">Image not found</div>'

    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-badge">🤟 VIT Chennai · Accessibility Tech</div>
        <h1 class="hero-title">Vimozhi</h1>
        <p class="hero-subtitle">
            Freedom of expression through sign. Real-time conversion of spoken or written English into Indian Sign Language (ISL) gloss —
            with full sign images and smart grammar restructuring for India's 6.3 crore Deaf community.
        </p>
        <div class="hero-images">
            <div class="hero-img-card">{img1_tag}</div>
            <div class="hero-img-card">{img2_tag}</div>
            <div class="hero-img-card">{img3_tag}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WHY WE BUILT THIS ────────────────────────────────────────────────────
    st.markdown("""
    <div class="why-section">
        <div class="section-eyebrow">Our Mission</div>
        <div class="section-title">Why We Built This</div>
        <p style="color: var(--slate-mid); max-width: 700px; line-height: 1.75; font-size: 0.98rem; margin-bottom: 1.5rem;">
            Indian Sign Language is the primary language of India's Deaf and hard-of-hearing community.
            Yet most translation technology ignores ISL's unique grammar — a double-hand system with
            <strong>Time → Subject/Object → Verb → Negation</strong> word order, distinct from English.
            Existing tools either do word-for-word translation (wrong grammar), rely on expensive hardware,
            or only work for American Sign Language. We bridge that gap.
        </p>
        <div class="stats-row">
            <div class="stat-block">
                <div class="stat-number">6.3%</div>
                <div class="stat-label">of India's population has significant auditory impairment</div>
            </div>
            <div class="stat-block">
                <div class="stat-number">ISL</div>
                <div class="stat-label">uses a double-hand system — higher engineering complexity than ASL</div>
            </div>
            <div class="stat-block">
                <div class="stat-number">0→1</div>
                <div class="stat-label">First open speech-to-ISL pipeline with proper grammar rules</div>
            </div>
        </div>
        <div class="why-grid">
            <div class="why-card">
                <div class="icon">🏫</div>
                <h4>Schools &amp; Workplaces</h4>
                <p>Deaf students and employees face social isolation due to lack of real-time translation tools in everyday environments.</p>
            </div>
            <div class="why-card">
                <div class="icon">🧠</div>
                <h4>Grammar-Aware NLP</h4>
                <p>spaCy POS tagging + custom ISL grammar rules reorder English sentences correctly before gloss mapping.</p>
            </div>
            <div class="why-card">
                <div class="icon">🎙️</div>
                <h4>Whisper AI Speech</h4>
                <p>OpenAI Whisper transcribes spoken audio — bypassing Hidden Markov Model limitations to handle Indian accents and noise.</p>
            </div>
            <div class="why-card">
                <div class="icon">✋</div>
                <h4>Full Finger-Spelling</h4>
                <p>Words not in the sign vocabulary are automatically broken into individual letter signs — no vocabulary crash.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── VIDEO ────────────────────────────────────────────────────────────────
    video_path = "Speech_to_Sign.mp4"
    if os.path.exists(video_path):
        st.markdown("""
        <div class="video-section">
            <div class="section-eyebrow">See It In Action</div>
            <div class="section-title">Why Vimozhi</div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="video-wrap">', unsafe_allow_html=True)
        st.video(video_path)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="video-section">
            <div class="section-eyebrow">See It In Action</div>
            <div class="section-title">Live Demo</div>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.92rem; margin-top: 1rem;">
                Place <code>Speech_to_Sign.mp4</code> in the project root to display the demo video here.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── PIPELINE ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="pipeline-section">
        <div class="section-eyebrow">Under the Hood</div>
        <div class="section-title">How It Works</div>
        <div class="pipeline-steps">
            <div class="pipe-item">
                <div class="pipe-num">1</div>
                <h4>Input</h4>
                <p>Type text or record / upload audio</p>
            </div>
            <div class="pipe-arrow-outer">→</div>
            <div class="pipe-item">
                <div class="pipe-num">2</div>
                <h4>Whisper STT</h4>
                <p>Transformer model transcribes audio to English</p>
            </div>
            <div class="pipe-arrow-outer">→</div>
            <div class="pipe-item">
                <div class="pipe-num">3</div>
                <h4>NLP Engine</h4>
                <p>spaCy tokenises & POS-tags words</p>
            </div>
            <div class="pipe-arrow-outer">→</div>
            <div class="pipe-item">
                <div class="pipe-num">4</div>
                <h4>ISL Grammar</h4>
                <p>Time → Subject → Verb → Negation reordering</p>
            </div>
            <div class="pipe-arrow-outer">→</div>
            <div class="pipe-item">
                <div class="pipe-num">5</div>
                <h4>Gloss Mapper</h4>
                <p>Multi-word signs & vocabulary lookup</p>
            </div>
            <div class="pipe-arrow-outer">→</div>
            <div class="pipe-item">
                <div class="pipe-num">6</div>
                <h4>Sign Renderer</h4>
                <p>Sign cards + full finger-spelling shown</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODE SELECTION ────────────────────────────────────────────────────────
    st.markdown('<div class="section-eyebrow" style="margin-bottom:0.5rem;">Get Started</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:\'Fraunces\',serif;font-size:1.8rem;color:var(--slate);margin-bottom:1.5rem;">Choose Conversion Mode</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📝  Text → ISL Conversion\nType English text and convert"):
            st.session_state.mode = "text"
            st.rerun()
    with col2:
        if st.button("🎙️  Voice → ISL Conversion\nSpeak or upload audio"):
            st.session_state.mode = "voice"
            st.rerun()

    st.markdown("""
    <div style="margin-top:2rem; padding:1.5rem 2rem; background: var(--cream);
    border-radius:16px; border:1.5px solid var(--border); display:flex; gap:2rem; flex-wrap:wrap;">
        <div style="flex:1; min-width:200px;">
            <div style="font-size:0.75rem; font-weight:700; color:var(--amber); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">Presented by</div>
            <div style="font-weight:700; color:var(--slate);">Abarna P &amp; Pratheepa K</div>
            <div style="font-size:0.85rem; color:var(--slate-light); margin-top:0.2rem;">VIT Chennai</div>
        </div>
        <div style="flex:1; min-width:200px;">
            <div style="font-size:0.75rem; font-weight:700; color:var(--teal); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">Tech Stack</div>
            <div style="font-size:0.85rem; color:var(--slate-mid); line-height:1.6;">Streamlit · spaCy · OpenAI Whisper · Python</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TEXT PANEL PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "text":
    if st.button("← Back to Home"):
        st.session_state.mode = None
        st.rerun()

    st.markdown("""
    <div style="margin: 1.5rem 0 1rem;">
        <div class="section-eyebrow">Text to ISL</div>
        <h1 style="font-family:'Fraunces',serif; font-size:2.4rem; color:var(--slate); margin:0;">
            📝 Text → Sign Language
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="chip">Preprocessing → ISL Grammar Restructure → Gloss Mapping → Sign Images</span>', unsafe_allow_html=True)

    user_text = st.text_area(
        "English text",
        placeholder="e.g. What are you doing? Is this late for you?",
        height=130,
        label_visibility="collapsed",
    )

    st.caption("💡 Try an example:")
    ex_cols = st.columns(4)
    examples = [
        "What are you doing? Is this late for you?",
        "I am going to college tomorrow",
        "She does not want to eat",
        "Today I will study computer science",
    ]
    for i, ex in enumerate(examples):
        with ex_cols[i]:
            if st.button(ex, key=f"ex_{i}"):
                user_text = ex

    if st.button("Convert to ISL Gloss ➜", key="convert_text"):
        if not user_text.strip():
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Running ISL pipeline…"):
                time.sleep(0.3)
                _, glosses, is_demo = run_text_pipeline(user_text.strip())
            show_result(user_text.strip(), glosses, is_demo, source_label="English Text")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  VOICE PANEL PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "voice":
    if st.button("← Back to Home"):
        st.session_state.mode = None
        st.rerun()

    st.markdown("""
    <div style="margin: 1.5rem 0 1rem;">
        <div class="section-eyebrow">Voice to ISL</div>
        <h1 style="font-family:'Fraunces',serif; font-size:2.4rem; color:var(--slate); margin:0;">
            🎙️ Voice → Sign Language
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<span class="chip">Whisper STT → Preprocessing → ISL Grammar → Gloss → Sign Images</span>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🎤 Record in Browser", "📁 Upload Audio File"])

    # ── TAB 1: In-browser mic recording ─────────────────────────────────────
    with tab1:
        st.markdown(
            "Click the **microphone icon** below, speak your sentence clearly, "
            "then click stop. Whisper will transcribe it automatically."
        )

        audio_value = None
        try:
            audio_value = st.audio_input(
                "🎙️ Record your voice",
                label_visibility="collapsed"
            )
        except AttributeError:
            st.warning(
                "⚠️ In-browser recording requires **Streamlit ≥ 1.33**. "
                "Run `pip install --upgrade streamlit` then restart."
            )

        if audio_value is not None:
            st.audio(audio_value, format="audio/wav")
            st.success("✅ Recording captured — click below to convert.")

            if st.button("Transcribe & Convert ➜", key="convert_mic"):
                with st.spinner("Transcribing with Whisper…"):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(audio_value.getvalue())
                        tmp_path = tmp.name

                    import datetime
                    ts_str   = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    rec_path = os.path.join(RECORDINGS_DIR, f"recording_{ts_str}.wav")
                    with open(rec_path, "wb") as rf:
                        rf.write(audio_value.getvalue())

                    recognized_text, _, glosses, is_demo = run_voice_pipeline(tmp_path)
                    os.unlink(tmp_path)

                show_result(recognized_text, glosses, is_demo, source_label="Microphone")
                st.caption(f"Recording saved → `{rec_path}`")

    # ── TAB 2: Upload audio ──────────────────────────────────────────────────
    with tab2:
        st.markdown("Upload a **WAV, MP3, or M4A** file to convert.")
        audio_file = st.file_uploader(
            "Audio file", type=["wav","mp3","m4a","ogg"],
            label_visibility="collapsed",
        )

        if audio_file:
            st.audio(audio_file, format=audio_file.type)
            st.caption(f"`{audio_file.name}` · {audio_file.size // 1024} KB")

            if st.button("Transcribe & Convert ➜", key="convert_upload"):
                with st.spinner("Transcribing with Whisper…"):
                    ext = os.path.splitext(audio_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                        tmp.write(audio_file.read())
                        tmp_path = tmp.name
                    recognized_text, _, glosses, is_demo = run_voice_pipeline(tmp_path)
                    os.unlink(tmp_path)
                show_result(recognized_text, glosses, is_demo, source_label="Uploaded Audio")

        st.markdown("---")
        st.markdown("##### Or convert a previously saved recording")
        rec_files = []
        if os.path.exists(RECORDINGS_DIR):
            rec_files = sorted(
                [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".wav")],
                reverse=True
            )
        if rec_files:
            selected = st.selectbox("Select recording", rec_files)
            if st.button("Convert Selected ➜", key="convert_saved"):
                audio_path = os.path.join(RECORDINGS_DIR, selected)
                with st.spinner("Processing…"):
                    recognized_text, _, glosses, is_demo = run_voice_pipeline(audio_path)
                show_result(recognized_text, glosses, is_demo, source_label=selected)
        else:
            st.caption("No `.wav` files in `recordings/` yet — use the Record tab above.")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    🤟 <strong>ISL Converter</strong> · Streamlit + spaCy + OpenAI Whisper<br>
    Built at <strong>VIT Chennai</strong> by Abarna P & Pratheepa K<br>
    Supporting the Deaf community through accessible technology
</div>
""", unsafe_allow_html=True)
