import base64
import html
import mimetypes
from pathlib import Path

import streamlit as st


def render_hidden_looping_audio(
    audio_path: Path,
    label: str,
    *,
    audio_id: str,
) -> None:
    if not audio_path.is_file():
        st.error(f"Nie znaleziono pliku muzycznego: {audio_path}")
        return

    audio_data = base64.b64encode(audio_path.read_bytes()).decode("ascii")
    accessible_label = html.escape(label, quote=True)
    safe_audio_id = html.escape(audio_id, quote=True)
    safe_button_id = html.escape(f"enable-{audio_id}", quote=True)
    mime_type, _ = mimetypes.guess_type(audio_path.name)
    if mime_type is None or not mime_type.startswith("audio/"):
        st.error(f"Nieznany format pliku muzycznego: {audio_path.name}")
        return
    st.html(
        f"""
        <audio
            id="{safe_audio_id}"
            src="data:{mime_type};base64,{audio_data}"
            autoplay
            loop
            preload="auto"
            aria-label="{accessible_label}"
            style="display: none;"
        ></audio>
        <button id="{safe_button_id}" type="button" hidden>
            🔊 Włącz muzykę
        </button>
        <style>
            #{safe_button_id} {{
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
                const audio = document.getElementById("{safe_audio_id}");
                const enableButton = document.getElementById("{safe_button_id}");

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
