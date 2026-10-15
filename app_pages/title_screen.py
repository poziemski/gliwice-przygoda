import base64
from pathlib import Path

import streamlit as st

from utils.audio import render_hidden_looping_audio


MUSIC_FILE = Path(__file__).resolve().parents[1] / "assets" / "music" / "title_theme.wav"
BACKGROUND_FILE = Path(__file__).resolve().parents[1] / "assets" / "img" / "title-screen.gif"
background_data = base64.b64encode(BACKGROUND_FILE.read_bytes()).decode("ascii")

st.markdown(
    """
    <style>
    .stApp {
        background:
            linear-gradient(rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.62)),
            url("data:image/gif;base64,BACKGROUND_DATA") center / cover no-repeat fixed;
    }
    [data-testid="stHeader"],
    [data-testid="stMain"] {
        background: transparent;
    }
    .block-container {
        min-height: 88vh;
        padding-top: 3rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .block-container h1 {
        width: 100%;
        margin-top: 2rem;
        text-align: center;
        font-size: clamp(3rem, 9vw, 6rem);
        letter-spacing: 0.12em;
    }
    .block-container [data-testid="stHorizontalBlock"] {
        width: 100%;
    }
    .block-container [data-testid="stButton"] {
        margin-top: 1rem;
        text-align: center;
    }
    .block-container [data-testid="stButton"] button {
        min-width: 12rem;
        min-height: 3.25rem;
        font-size: 1.2rem;
    }
    .game-version {
        position: fixed;
        right: 1.5rem;
        bottom: 1rem;
        color: #888;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
    }
    </style>
    """.replace("BACKGROUND_DATA", background_data),
    unsafe_allow_html=True,
)

st.title("GLIWICE")
render_hidden_looping_audio(
    MUSIC_FILE,
    "Ambientowy motyw muzyczny ekranu tytułowego",
)

_, start_column, _ = st.columns([1, 1, 1])
with start_column:
    start_game = st.button("Zacznij!", type="primary", use_container_width=True)

st.markdown('<div class="game-version">WERSJA 0.1.0 · PROLOG</div>', unsafe_allow_html=True)

if start_game:
    st.switch_page("app_pages/character_creation.py")
