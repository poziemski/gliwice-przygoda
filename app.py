import streamlit as st

from utils.browser_storage import render_browser_save_store
from utils.game_save import DEFAULT_SAVE, validate_save_data
from utils.ui_theme import apply_night_theme


st.set_page_config(page_title="Gliwice: Przygoda", page_icon="🌆", layout="wide")
apply_night_theme()

st.session_state.setdefault("browser_storage_error", "")
store_result = render_browser_save_store(
    st.session_state.get("browser_save_data"),
    ready="browser_save_data" in st.session_state,
)
if store_result.storage_error:
    st.session_state["browser_storage_error"] = store_result.storage_error
elif st.session_state["browser_storage_error"]:
    st.session_state["browser_storage_error"] = ""

if "browser_save_data" not in st.session_state and store_result.save_data is not None:
    st.session_state["browser_save_data"] = validate_save_data(store_result.save_data)

if st.session_state["browser_storage_error"]:
    st.error(st.session_state["browser_storage_error"])
    st.stop()

if "browser_save_data" not in st.session_state:
    st.info("Wczytywanie zapisu z przeglądarki…")
    st.stop()

st.markdown(
    """
    <style>
    [data-testid="stMainMenu"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

page = st.navigation(
    [
        st.Page("app_pages/title_screen.py", title="Start"),
        st.Page("app_pages/story_intro.py", title="Prolog"),
        st.Page("app_pages/character_creation.py", title="Kreator postaci"),
        st.Page("app_pages/adventure.py", title="Przygoda"),
    ],
    position="hidden",
)
page.run()
