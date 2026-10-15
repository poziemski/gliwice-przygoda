import streamlit as st

from utils.game_data import ARCHETYPES, DISTRICTS
from utils.game_save import save_character
from utils.skills import (
    SKILL_KEYS,
    SKILL_POINT_BUDGET,
    initialize_skill_state,
    validate_skill_budget,
)


initialize_skill_state()

st.title("Karta postaci")
st.caption("Stwórz bohatera miejskich tajemnic — od brukowanych uliczek po industrialne nabrzeża.")

details, sheet = st.columns([1, 1], gap="large")

with details:
    st.subheader("Kim jesteś?")
    name = st.text_input("Imię lub ksywka", placeholder="np. Iskra")
    district = st.selectbox("Twoja część Gliwic", list(DISTRICTS))
    archetype = st.selectbox("Rola", list(ARCHETYPES))
    background = st.text_area(
        "Krótka historia",
        placeholder="Co przydarzyło Ci się w Gliwicach, czego nie potrafisz zapomnieć?",
        max_chars=240,
    )

    st.subheader("Twoje atuty")
    st.caption(
        f"Rozdziel maksymalnie {SKILL_POINT_BUDGET} punktów między atrybuty. "
        "Aby przenieść punkty, najpierw zmniejsz jeden z pozostałych atrybutów."
    )
    courage = st.slider(
        "Odwaga",
        min_value=0,
        max_value=SKILL_POINT_BUDGET,
        key=SKILL_KEYS[0],
        on_change=validate_skill_budget,
        args=(SKILL_KEYS[0],),
    )
    cleverness = st.slider(
        "Spryt",
        min_value=0,
        max_value=SKILL_POINT_BUDGET,
        key=SKILL_KEYS[1],
        on_change=validate_skill_budget,
        args=(SKILL_KEYS[1],),
    )
    resourcefulness = st.slider(
        "Zaradność",
        min_value=0,
        max_value=SKILL_POINT_BUDGET,
        key=SKILL_KEYS[2],
        on_change=validate_skill_budget,
        args=(SKILL_KEYS[2],),
    )
    points_spent = courage + cleverness + resourcefulness
    st.progress(
        points_spent / SKILL_POINT_BUDGET,
        text=f"Wydane punkty: {points_spent}/{SKILL_POINT_BUDGET}",
    )
    if st.session_state.skill_budget_notice:
        st.warning(st.session_state.skill_budget_notice)

with sheet:
    st.subheader("Podgląd postaci")
    character_name = name.strip() or "Nowy bohater"
    st.markdown(f"## {character_name}")
    st.markdown(f"**{archetype} · {district}**")
    st.write(ARCHETYPES[archetype])
    st.info(DISTRICTS[district])

    st.markdown("#### Atrybuty")
    stat_columns = st.columns(3)
    stat_columns[0].metric("Odwaga", courage)
    stat_columns[1].metric("Spryt", cleverness)
    stat_columns[2].metric("Zaradność", resourcefulness)

    st.markdown("#### Historia")
    st.write(background.strip() or "Twoja historia dopiero się zaczyna.")

st.divider()
save_column, back_column = st.columns([2, 1])
with save_column:
    save_and_start = st.button(
        "Zapisz postać i rozpocznij przygodę",
        type="primary",
        width="stretch",
        key="save_character",
    )
with back_column:
    back_to_title = st.button(
        "← Ekran tytułowy",
        width="stretch",
        key="back_to_title",
    )

if save_and_start:
    if not name.strip():
        st.error("Nadaj postaci imię lub ksywkę przed zapisaniem.")
    elif points_spent > SKILL_POINT_BUDGET:
        st.error(f"Postać może wydać maksymalnie {SKILL_POINT_BUDGET} punktów atutów.")
    else:
        save_data = st.session_state["browser_save_data"]
        character_id = save_character(
            save_data,
            name=name.strip(),
            district=district,
            archetype=archetype,
            backstory=background.strip(),
            stats={
                "courage": courage,
                "cleverness": cleverness,
                "resourcefulness": resourcefulness,
            },
        )
        st.session_state["current_character_id"] = character_id
        st.switch_page("app_pages/adventure.py")

if back_to_title:
    st.switch_page("app_pages/title_screen.py")
