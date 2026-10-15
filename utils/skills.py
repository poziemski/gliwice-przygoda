import streamlit as st


SKILL_POINT_BUDGET = 10
SKILL_KEYS = ("skill_courage", "skill_cleverness", "skill_resourcefulness")
DEFAULT_SKILLS = dict(zip(SKILL_KEYS, (3, 3, 2)))
CHARACTER_SKILLS_KEY = "character_skills"


def initialize_skill_state():
    st.session_state.setdefault(CHARACTER_SKILLS_KEY, DEFAULT_SKILLS.copy())
    for skill_key, default_value in DEFAULT_SKILLS.items():
        st.session_state.setdefault(
            skill_key,
            st.session_state[CHARACTER_SKILLS_KEY].get(skill_key, default_value),
        )

    st.session_state.setdefault(
        "accepted_skill_values",
        st.session_state[CHARACTER_SKILLS_KEY].copy(),
    )
    st.session_state.setdefault("skill_budget_notice", "")


def validate_skill_budget(changed_skill):
    current_total = sum(st.session_state[key] for key in SKILL_KEYS)
    accepted_values = st.session_state.accepted_skill_values

    if current_total > SKILL_POINT_BUDGET:
        st.session_state[changed_skill] = accepted_values[changed_skill]
        st.session_state.skill_budget_notice = (
            "Brakuje punktów w puli. Zmniejsz najpierw inny atrybut, "
            "aby przydzielić punkty tutaj."
        )
        return

    accepted_values.update({key: st.session_state[key] for key in SKILL_KEYS})
    st.session_state[CHARACTER_SKILLS_KEY].update(accepted_values)
    st.session_state.skill_budget_notice = ""
