import streamlit as st
import time
from dotenv import load_dotenv

# ── Uncomment these when your modules are ready ──────────────────────────────
# from utils.audio_preprocessor import process_input
# from core.transcriber import transcribe_all
# from core.summarize import summarize, generate_title
# from core.extractor import extract_action_items, extract_key_decisions, extract_questions
# from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightStream AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Glassmorphism CSS ───────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-1: #0d0221;
    --bg-2: #0a1628;
    --bg-3: #0d1f3c;
    --bg-4: #1a0533;
    --glass:        rgba(255, 255, 255, 0.04);
    --glass-hover:  rgba(255, 255, 255, 0.07);
    --glass-border: rgba(255, 255, 255, 0.09);
    --glass-border-hover: rgba(139, 92, 246, 0.35);
    --accent:       #7c3aed;
    --accent-soft:  rgba(139, 92, 246, 0.15);
    --accent-glow:  #a78bfa;
    --cyan:         #06b6d4;
    --cyan-soft:    rgba(6, 182, 212, 0.12);
    --cyan-light:   #67e8f9;
    --green:        #10b981;
    --green-soft:   rgba(16, 185, 129, 0.12);
    --pink:         #ec4899;
    --pink-soft:    rgba(236, 72, 153, 0.12);
    --text:         rgba(255, 255, 255, 0.88);
    --text-muted:   rgba(255, 255, 255, 0.38);
    --text-subtle:  rgba(255, 255, 255, 0.55);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

/* ── App Background with Orbs ── */
.stApp {
    background: linear-gradient(135deg,
        var(--bg-1) 0%,
        var(--bg-2) 30%,
        var(--bg-3) 60%,
        var(--bg-4) 100%
    ) !important;
    min-height: 100vh;
}

/* Orb 1 — top-left purple */
.stApp::before {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.22) 0%, transparent 70%);
    top: -150px; left: -150px;
    pointer-events: none;
    z-index: 0;
    border-radius: 50%;
}

/* Orb 2 — mid-right cyan */
.stApp::after {
    content: '';
    position: fixed;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 70%);
    top: 250px; right: -100px;
    pointer-events: none;
    z-index: 0;
    border-radius: 50%;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.025) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

label {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
}

/* ── Hero Title ── */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1.9rem, 4vw, 2.8rem);
    font-weight: 700;
    line-height: 1.15;
    background: linear-gradient(120deg, #ffffff 0%, #c4b5fd 45%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.hero-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 6px;
    letter-spacing: 0.06em;
}

/* ── Badge Pills ── */
.badge-row {
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.badge {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 11px;
    border-radius: 20px;
    display: inline-block;
}

.badge-purple { background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.25); }
.badge-cyan   { background: rgba(6,182,212,0.12);  color: #67e8f9; border: 1px solid rgba(6,182,212,0.22); }
.badge-green  { background: rgba(16,185,129,0.12); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.22); }
.badge-pink   { background: rgba(236,72,153,0.12); color: #f9a8d4; border: 1px solid rgba(236,72,153,0.22); }

/* ── Glass Card ── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px 22px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    margin-bottom: 0.85rem;
    transition: border-color 0.25s ease, background 0.25s ease;
}

.glass-card:hover {
    border-color: var(--glass-border-hover);
    background: var(--glass-hover);
}

/* shimmer top edge */
.glass-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(139,92,246,0.55) 50%, transparent 100%);
}

.card-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 7px;
}

.card-body {
    font-size: 0.85rem;
    line-height: 1.75;
    color: var(--text-subtle);
}

/* ── Title Banner ── */
.title-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.14) 0%, rgba(6,182,212,0.08) 100%);
    border: 1px solid rgba(139,92,246,0.22);
    border-radius: 14px;
    padding: 18px 22px 18px 26px;
    position: relative;
    overflow: hidden;
    margin-bottom: 0.85rem;
}

.title-banner::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #7c3aed 0%, #06b6d4 100%);
    border-radius: 0 2px 2px 0;
}

.banner-eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 6px;
}

.banner-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1.3;
}

/* ── Pipeline Steps (Sidebar) ── */
.pipeline-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
    margin-top: 4px;
}

.step-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 11px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 9px;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-bottom: 5px;
    transition: all 0.3s ease;
}

.step-row.step-done {
    background: rgba(16,185,129,0.07);
    border-color: rgba(16,185,129,0.2);
    color: rgba(16,185,129,0.9);
}

.step-row.step-active {
    background: rgba(139,92,246,0.09);
    border-color: rgba(139,92,246,0.28);
    color: #a78bfa;
}

.step-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: rgba(255,255,255,0.14);
    flex-shrink: 0;
}

.step-done .step-dot {
    background: #10b981;
    box-shadow: 0 0 7px rgba(16,185,129,0.55);
}

.step-active .step-dot {
    background: #7c3aed;
    box-shadow: 0 0 9px rgba(124,58,237,0.7);
    animation: pulseDot 1.3s ease-in-out infinite;
}

@keyframes pulseDot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.35; transform: scale(0.75); }
}

/* ── Sidebar Logo Area ── */
.sb-logo {
    display: flex;
    align-items: center;
    gap: 11px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 4px;
}

.sb-logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.sb-logo-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
}

.sb-logo-tag {
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
}

.sb-section-label {
    font-size: 0.63rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(124,58,237,0.82), rgba(91,33,182,0.82)) !important;
    border: 1px solid rgba(139,92,246,0.38) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.22s ease !important;
    text-transform: none !important;
    backdrop-filter: blur(8px) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(124,58,237,0.38) !important;
    background: linear-gradient(135deg, rgba(139,92,246,0.9), rgba(109,40,217,0.9)) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Secondary button (e.g. Clear Chat) */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: var(--text-subtle) !important;
}

/* ── Text Input & Selectbox ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s, background 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.6) !important;
    background: rgba(139,92,246,0.07) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.22) !important;
}

/* ── Chat Container ── */
.chat-container {
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 18px;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 14px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    backdrop-filter: blur(12px);
}

.chat-msg {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.chat-msg-user { align-items: flex-end; }
.chat-msg-bot  { align-items: flex-start; }

.chat-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.label-user { color: #a78bfa; }
.label-bot  { color: #67e8f9; }

.chat-bubble {
    font-size: 0.84rem;
    line-height: 1.65;
    padding: 10px 15px;
    border-radius: 13px;
    max-width: 88%;
}

.bubble-user {
    background: rgba(124,58,237,0.18);
    border: 1px solid rgba(139,92,246,0.28);
    color: rgba(255,255,255,0.88);
    border-bottom-right-radius: 4px;
}

.bubble-bot {
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.2);
    color: rgba(255,255,255,0.82);
    border-bottom-left-radius: 4px;
}

/* ── Transcript Box ── */
.transcript-box {
    background: rgba(0,0,0,0.22);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.78rem;
    line-height: 1.85;
    max-height: 260px;
    overflow-y: auto;
    color: var(--text-muted);
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'Space Grotesk', monospace;
}

/* ── Action / Decision / Question Items ── */
.action-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.82rem;
    color: var(--text-subtle);
}
.action-item:last-child { border-bottom: none; }

.action-icon-green { color: #6ee7b7; flex-shrink: 0; margin-top: 1px; }
.action-icon-cyan  { color: #67e8f9; flex-shrink: 0; margin-top: 1px; }

.decision-chip {
    padding: 9px 12px;
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.18);
    border-left: 3px solid #7c3aed;
    border-radius: 8px;
    font-size: 0.82rem;
    color: var(--text-subtle);
    margin-bottom: 7px;
    line-height: 1.5;
}
.decision-chip:last-child { margin-bottom: 0; }

.question-chip {
    padding: 9px 12px;
    background: rgba(6,182,212,0.07);
    border: 1px solid rgba(6,182,212,0.16);
    border-left: 3px solid #06b6d4;
    border-radius: 8px;
    font-size: 0.82rem;
    color: var(--text-subtle);
    margin-bottom: 7px;
    line-height: 1.5;
}
.question-chip:last-child { margin-bottom: 0; }

/* ── Section Divider ── */
.gm-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 1.2rem 0;
    border: none;
}

/* ── Section Header ── */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Empty State ── */
.empty-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 70px 20px;
    text-align: center;
    gap: 16px;
}

.empty-ring {
    width: 90px; height: 90px;
    border-radius: 50%;
    background: rgba(139,92,246,0.07);
    border: 1.5px solid rgba(139,92,246,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 36px;
    position: relative;
}

.empty-ring::before {
    content: '';
    position: absolute;
    inset: -10px;
    border-radius: 50%;
    border: 1px solid rgba(139,92,246,0.09);
}

.empty-ring::after {
    content: '';
    position: absolute;
    inset: -20px;
    border-radius: 50%;
    border: 1px solid rgba(139,92,246,0.05);
}

.empty-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: rgba(255,255,255,0.65);
}

.empty-desc {
    font-size: 0.84rem;
    color: var(--text-muted);
    max-width: 340px;
    line-height: 1.75;
}

/* ── Spinner & Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #06b6d4) !important;
    border-radius: 4px;
}

.stSpinner > div {
    border-top-color: #7c3aed !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 0.85rem !important;
}

.streamlit-expanderContent {
    border: 1px solid var(--glass-border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    background: rgba(255,255,255,0.02) !important;
}

/* ── Alert / Info / Error ── */
.stAlert {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    backdrop-filter: blur(10px) !important;
}

/* ── Markdown container text ── */
[data-testid="stMarkdownContainer"] p {
    color: var(--text) !important;
    font-size: 0.9rem !important;
}

/* ── Scrollbars ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.32); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.55); }
</style>
""",
    unsafe_allow_html=True,
)


# ─── Session State Init ──────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─── Pipeline Step Helpers ───────────────────────────────────────────────────
PIPELINE_STEPS = [
    ("audio", "🔊", "Audio Processing"),
    ("transcript", "📝", "Transcription"),
    ("title", "🏷️", "Title Generation"),
    ("summary", "📋", "Summarisation"),
    ("extract", "🔍", "Extraction"),
    ("rag", "🧠", "RAG Engine"),
]


def get_step_class(key: str) -> str:
    s = st.session_state.pipeline_steps.get(key, "pending")
    return {"active": "step-active", "done": "step-done"}.get(s, "")


def render_pipeline():
    st.markdown(
        '<div class="pipeline-section-label">Pipeline Status</div>',
        unsafe_allow_html=True,
    )
    for key, icon, label in PIPELINE_STEPS:
        cls = get_step_class(key)
        st.markdown(
            f"""
        <div class="step-row {cls}">
            <div class="step-dot"></div>
            <span>{icon}</span>
            <span>{label}</span>
        </div>""",
            unsafe_allow_html=True,
        )


def update_step(key: str, state: str):
    st.session_state.pipeline_steps[key] = state


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown(
        """
    <div class="sb-logo">
        <div class="sb-logo-icon">🎬</div>
        <div>
            <div class="sb-logo-name">InsightStream AI</div>
            <div class="sb-logo-tag">Meeting Intelligence</div>
        </div>
    </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sb-section-label" style="margin-top:18px;">Source</div>',
        unsafe_allow_html=True,
    )
    source = st.text_input(
        "Source",
        placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4",
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sb-section-label" style="margin-top:14px;">Language</div>',
        unsafe_allow_html=True,
    )
    language = st.selectbox(
        "Language", ["english", "hinglish"], label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown("<div class='gm-divider'></div>", unsafe_allow_html=True)
        render_pipeline()


# ─── Main Area ───────────────────────────────────────────────────────────────
# Hero
st.markdown('<div class="hero-title">InsightStream AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="badge-row">
    <span class="badge badge-purple">Transcription</span>
    <span class="badge badge-cyan">Summarisation</span>
    <span class="badge badge-green">RAG Chat</span>
    <span class="badge badge-pink">Multi-language</span>
</div>""",
    unsafe_allow_html=True,
)

st.markdown("<div class='gm-divider'></div>", unsafe_allow_html=True)


# ─── Run Pipeline ────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("⚠️  Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_ph = st.empty()

        try:
            with progress_ph.container():
                st.info("⚙️  Pipeline running — watch the sidebar for live status…")

            update_step("audio", "active")
            # chunks = process_input(source)        # ← uncomment when ready
            time.sleep(0.8)  # ← remove when using real fn
            update_step("audio", "done")

            update_step("transcript", "active")
            # transcript = transcribe_all(chunks, language)
            time.sleep(0.8)
            transcript = "[Sample transcript — replace with real output]"
            update_step("transcript", "done")

            update_step("title", "active")
            # title = generate_title(transcript)
            time.sleep(0.5)
            title = "Sample Meeting Title — Replace with Real Output"
            update_step("title", "done")

            update_step("summary", "active")
            # summary = summarize(transcript)
            time.sleep(0.6)
            summary = (
                "This is a placeholder summary. Replace with output from summarize()."
            )
            update_step("summary", "done")

            update_step("extract", "active")
            # action_items = extract_action_items(transcript)
            # decisions    = extract_key_decisions(transcript)
            # questions    = extract_questions(transcript)
            time.sleep(0.6)
            action_items = "• Action item 1\n• Action item 2\n• Action item 3"
            decisions = "• Key decision 1\n• Key decision 2"
            questions = "• Open question 1\n• Open question 2"
            update_step("extract", "done")

            update_step("rag", "active")
            # rag_chain = build_rag_chain(transcript)
            time.sleep(0.5)
            rag_chain = None  # placeholder
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_ph.success("✅  Analysis complete!")
            time.sleep(0.6)
            progress_ph.empty()
            st.rerun()

        except Exception as e:
            for k, _, _ in PIPELINE_STEPS:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_ph.error(f"❌  Error: {e}")


# ─── Results ─────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # ── Title Banner ──
    st.markdown(
        f"""
    <div class="title-banner">
        <div class="banner-eyebrow">📌 &nbsp; Session Title</div>
        <div class="banner-title">{r['title']}</div>
    </div>""",
        unsafe_allow_html=True,
    )

    # ── Row 1: Summary + Transcript ──
    col_sum, col_tr = st.columns([3, 2], gap="medium")

    with col_sum:
        st.markdown(
            f"""
        <div class="glass-card">
            <div class="card-label">📋 &nbsp; Summary</div>
            <div class="card-body">{r['summary']}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with col_tr:
        with st.expander("📝  Full Transcript", expanded=False):
            st.markdown(
                f'<div class="transcript-box">{r["transcript"]}</div>',
                unsafe_allow_html=True,
            )

    # ── Row 2: Action Items | Key Decisions | Open Questions ──
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        # Build action item rows
        items_html = ""
        for line in r["action_items"].split("\n"):
            line = line.strip().lstrip("•-").strip()
            if line:
                items_html += f"""
                <div class="action-item">
                    <span class="action-icon-green">✓</span>
                    <span>{line}</span>
                </div>"""

        st.markdown(
            f"""
        <div class="glass-card">
            <div class="card-label">✅ &nbsp; Action Items</div>
            <div class="card-body">{items_html}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with c2:
        decisions_html = ""
        for line in r["key_decisions"].split("\n"):
            line = line.strip().lstrip("•-").strip()
            if line:
                decisions_html += f'<div class="decision-chip">{line}</div>'

        st.markdown(
            f"""
        <div class="glass-card">
            <div class="card-label">🔑 &nbsp; Key Decisions</div>
            <div class="card-body">{decisions_html}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with c3:
        questions_html = ""
        for line in r["open_questions"].split("\n"):
            line = line.strip().lstrip("•-").strip()
            if line:
                questions_html += f'<div class="question-chip">{line}</div>'

        st.markdown(
            f"""
        <div class="glass-card">
            <div class="card-label">❓ &nbsp; Open Questions</div>
            <div class="card-body">{questions_html}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='gm-divider'></div>", unsafe_allow_html=True)

    # ── RAG Chat ──
    st.markdown(
        '<div class="section-header">💬 &nbsp; Chat with your Meeting</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg chat-msg-user">
                    <span class="chat-label label-user">You</span>
                    <div class="chat-bubble bubble-user">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg chat-msg-bot">
                    <span class="chat-label label-bot">🤖 &nbsp; Assistant</span>
                    <div class="chat-bubble bubble-bot">{msg['content']}</div>
                </div>"""
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown(
            """
        <div class="glass-card" style="text-align:center; padding:2.5rem 1rem;">
            <div style="font-size:2.2rem; margin-bottom:10px;">💬</div>
            <div style="color:var(--text-muted); font-size:0.85rem; line-height:1.7;">
                Ask anything about your meeting transcript.<br>
                <span style="color:rgba(139,92,246,0.6); font-size:0.75rem;">
                    Try: "What were the main decisions?" or "Who owns each action item?"
                </span>
            </div>
        </div>""",
            unsafe_allow_html=True,
        )

    # Chat input row
    chat_col, send_col = st.columns([6, 1], gap="small")
    with chat_col:
        user_input = st.text_input(
            "Chat input",
            placeholder="What were the main decisions made?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send →", use_container_width=True, key="send_btn")

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            # answer = ask_question(r["rag_chain"], user_input.strip())  # ← uncomment when ready
            answer = f'[RAG answer placeholder for: "{user_input.strip()}"]'
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input.strip()}
        )
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️  Clear Chat", type="secondary", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()

# ─── Empty State ─────────────────────────────────────────────────────────────
else:
    st.markdown(
        """
    <div class="empty-wrap">
        <div class="empty-ring">🎬</div>
        <div class="empty-title">Ready to Analyse</div>
        <div class="empty-desc">
            Paste a YouTube URL or local file path in the sidebar,
            choose your language, and hit <strong style="color:#a78bfa;">Analyse</strong> to begin.
        </div>
        <div class="badge-row" style="justify-content:center; margin-top:6px;">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""",
        unsafe_allow_html=True,
    )
