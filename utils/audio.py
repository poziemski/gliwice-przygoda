import base64
import html
from pathlib import Path

import streamlit as st


def render_hidden_looping_audio(audio_path: Path, label: str) -> None:
    if not audio_path.is_file():
        st.error(f"Nie znaleziono pliku muzycznego: {audio_path}")
        return

    audio_data = base64.b64encode(audio_path.read_bytes()).decode("ascii")
    accessible_label = html.escape(label, quote=True)
    st.html(
        f"""
        <audio
            id="title-screen-music"
            src="data:audio/wav;base64,{audio_data}"
            autoplay
            loop
            preload="auto"
            aria-label="{accessible_label}"
            style="display: none;"
        ></audio>
        <button id="enable-title-music" type="button" hidden>
            🔊 Włącz muzykę
        </button>
        <style>
            #enable-title-music {{
                position: fixed;
                left: 1.5rem;
                bottom: 1rem;
                z-index: 1000;
                padding: 0.5rem 0.8rem;
                border: 1px solid #777;
                border-radius: 0.5rem;
                color: inherit;
                background: var(--background-color, #222);
                cursor: pointer;
            }}
        </style>
        <script>
            (() => {{
                const audio = document.getElementById("title-screen-music");
                const enableButton = document.getElementById("enable-title-music");

                audio.play().catch(() => {{
                    enableButton.hidden = false;
                }});

                enableButton.addEventListener("click", () => {{
                    audio.play().then(() => {{
                        enableButton.hidden = true;
                    }}).catch(() => {{
                        enableButton.textContent = "Nie udało się uruchomić muzyki";
                    }});
                }});
            }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )
