import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from utils.gemini_adventure import (
    MODEL_NAME,
    AdventureModelError,
    generate_turn,
)
from utils.game_save import (
    MAX_INVENTORY_ITEMS,
    add_adventure_turn,
    add_opening_scene,
    get_character,
    get_messages,
    list_characters,
)


def get_gemini_api_key() -> str | None:
    environment_key = os.environ.get("GEMINI_API_KEY")
    if environment_key:
        return environment_key
    try:
        return st.secrets.get("GEMINI_API_KEY")
    except StreamlitSecretNotFoundError:
        return None


st.title("Przygoda")
st.caption("Wybierz jedną z trzech akcji. Gemini opowie, co dzieje się dalej.")

save_data = st.session_state["browser_save_data"]
characters = list_characters(save_data)
if not characters:
    st.info("Nie ma jeszcze zapisanej postaci. Najpierw stwórz ją w kreatorze.")
    if st.button("Przejdź do kreatora postaci", type="primary", key="go_to_creator"):
        st.switch_page("app_pages/character_creation.py")
    st.stop()

character_ids = {character["character_id"] for character in characters}
selected_id = st.session_state.get("current_character_id")
if selected_id not in character_ids:
    selected_id = None

if selected_id is None:
    character_options = {
        f"{item['name']} — {item['archetype']}, {item['district']}": item["character_id"]
        for item in characters
    }
    selected_label = st.selectbox("Wybierz zapisaną postać", list(character_options))
    if st.button("Wczytaj postać", type="primary", key="load_character"):
        st.session_state["current_character_id"] = character_options[selected_label]
        st.rerun()
    st.stop()

character = get_character(save_data, selected_id)
if character is None:
    st.error("Nie udało się wczytać postaci z zapisu przeglądarki.")
    st.stop()

stats_column, balance_column = st.columns([2, 1])
with stats_column:
    st.subheader(f"{character['name']} · {character['archetype']}")
    st.caption(f"{character['district']} · {character['backstory'] or 'Bez zapisanej historii.'}")
    st.write(
        f"Odwaga **{character['courage']}** · "
        f"Spryt **{character['cleverness']}** · "
        f"Zaradność **{character['resourcefulness']}**"
    )
with balance_column:
    st.metric("Gotówka", f"{character['balance']} zł")

with st.container(border=True):
    inventory = character["inventory"]
    st.subheader(f"Ekwipunek · {len(inventory)}/{MAX_INVENTORY_ITEMS}")
    if inventory:
        for item in inventory:
            st.markdown(f"- {item}")
    else:
        st.caption("Nie masz jeszcze żadnych przedmiotów.")

model_note = st.session_state.get("gemini_model_note")
if model_note:
    st.caption(model_note)

api_key = get_gemini_api_key()
if not api_key:
    st.warning(
        "Dodaj klucz Gemini jako `GEMINI_API_KEY` w zmiennej środowiskowej "
        "albo w `.streamlit/secrets.toml`, żeby uruchomić przygodę."
    )
    st.code(
        'GEMINI_API_KEY = "twój-klucz"\n'
        "# Zapisz te linie w pliku .streamlit/secrets.toml"
    )
    st.stop()

messages = get_messages(save_data, selected_id)
if not messages:
    st.write("Gliwice czekają. Rozpocznij przygodę, by odkryć pierwszą scenę.")
    if st.button("Rozpocznij przygodę", type="primary", key="start_adventure"):
        try:
            opening = generate_turn(
                api_key=api_key,
                character=character,
                messages=[],
                player_action=None,
            )
            if opening.model_name == MODEL_NAME:
                st.session_state.pop("gemini_model_note", None)
            else:
                st.session_state["gemini_model_note"] = (
                    f"Model zapasowy użyty po błędzie: {opening.model_name}"
                )
            add_opening_scene(
                save_data,
                selected_id,
                opening.narration,
                opening.choices,
                opening.item_gain,
                opening.item_loss,
            )
            st.rerun()
        except (AdventureModelError, ValueError) as error:
            st.error(f"Nie udało się rozpocząć przygody: {error}")
    st.stop()

selected_action = None
restore_choices_requested = False

for message_index, message in enumerate(messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if (
            message_index == len(messages) - 1
            and message["role"] == "assistant"
            and message.get("choices")
        ):
            choice_columns = st.columns(3)
            for choice_index, choice in enumerate(message["choices"]):
                if choice_columns[choice_index].button(
                    choice,
                    key=f"adventure_choice_{selected_id}_{message_index}_{choice_index}",
                    width="stretch",
                ):
                    selected_action = choice
        elif (
            message_index == len(messages) - 1
            and message["role"] == "assistant"
        ):
            restore_choices_requested = st.button(
                "Wygeneruj opcje do tej sceny",
                key=f"restore_choices_{selected_id}",
            )

if restore_choices_requested:
    try:
        opening = generate_turn(
            api_key=api_key,
            character=character,
            messages=messages,
            player_action=None,
        )
        if opening.model_name == MODEL_NAME:
            st.session_state.pop("gemini_model_note", None)
        else:
            st.session_state["gemini_model_note"] = (
                f"Model zapasowy użyty po błędzie: {opening.model_name}"
            )
        messages[-1]["choices"] = list(opening.choices)
        st.rerun()
    except (AdventureModelError, ValueError) as error:
        st.error(f"Nie udało się wygenerować opcji: {error}")

if selected_action:
    try:
        turn = generate_turn(
            api_key=api_key,
            character=character,
            messages=messages,
            player_action=selected_action,
        )
        if turn.model_name == MODEL_NAME:
            st.session_state.pop("gemini_model_note", None)
        else:
            st.session_state["gemini_model_note"] = (
                f"Model zapasowy użyty po błędzie: {turn.model_name}"
            )
        balance_change = add_adventure_turn(
            save_data,
            selected_id,
            selected_action,
            turn.narration,
            turn.choices,
            turn.outcome,
            turn.balance_change,
            turn.item_gain,
            turn.item_loss,
        )
        if balance_change != turn.balance_change:
            st.session_state["adventure_balance_note"] = (
                "Wydatek został ograniczony do dostępnej gotówki."
            )
        else:
            st.session_state.pop("adventure_balance_note", None)
        st.rerun()
    except (AdventureModelError, ValueError) as error:
        st.error(f"Nie udało się rozegrać wybranej akcji: {error}")

balance_note = st.session_state.get("adventure_balance_note")
if balance_note:
    st.caption(balance_note)

if st.button("← Wróć do karty postaci", key="back_to_character"):
    st.switch_page("app_pages/character_creation.py")
