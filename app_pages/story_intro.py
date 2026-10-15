import time

import streamlit as st

from utils.game_data import CAMPAIGN_PREMISE


def stream_story():
    for word in CAMPAIGN_PREMISE.split():
        yield f"{word} "
        time.sleep(0.055)


with st.container(border=True):
    st.title("Sygnał z Radiostacji")
    st.caption("PROLOG · GLIWICE, 02:17")
    if not st.session_state.get("intro_shown", False):
        st.write_stream(stream_story)
        st.session_state["intro_shown"] = True

st.divider()
continue_column, back_column = st.columns([2, 1])
with continue_column:
    if st.button(
        "Stwórz postać i rozpocznij śledztwo",
        type="primary",
        width="stretch",
        key="continue_from_intro",
    ):
        st.switch_page("app_pages/character_creation.py")
with back_column:
    if st.button(
        "← Ekran tytułowy",
        width="stretch",
        key="back_to_title_from_intro",
    ):
        st.session_state["intro_shown"] = False
        st.switch_page("app_pages/title_screen.py")
