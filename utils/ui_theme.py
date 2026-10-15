import streamlit as st


def apply_night_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --night: #101522;
            --navy: #202B48;
            --violet: #6556A8;
            --neon: #54C6C0;
            --paper: #E4D9C5;
        }
        .stApp {
            background:
                radial-gradient(ellipse at 50% -20%, rgba(101, 86, 168, 0.20), transparent 55%),
                var(--night);
            color: var(--paper);
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        [data-testid="stMain"] > div {
            background: transparent;
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2.5rem;
            padding-bottom: 3.5rem;
        }
        h1, h2, h3, h4 {
            color: var(--paper);
            letter-spacing: -0.025em;
        }
        h1 {
            font-weight: 750;
        }
        h2, h3 {
            font-weight: 650;
        }
        [data-testid="stCaptionContainer"] {
            color: rgba(228, 217, 197, 0.72);
        }
        a {
            color: var(--neon);
        }
        a:hover {
            color: #8be2dc;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: rgba(101, 86, 168, 0.45);
            border-radius: 16px;
            background: linear-gradient(145deg, rgba(32, 43, 72, 0.8), rgba(16, 21, 34, 0.5));
        }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            border-color: rgba(101, 86, 168, 0.55);
            border-radius: 10px;
            background-color: rgba(32, 43, 72, 0.72);
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: var(--neon);
            box-shadow: 0 0 0 1px var(--neon);
        }
        [data-testid="stButton"] button {
            border-radius: 10px;
            border-color: rgba(101, 86, 168, 0.72);
            background: rgba(32, 43, 72, 0.78);
            color: var(--paper);
            transition: border-color 140ms ease, background 140ms ease, transform 140ms ease;
        }
        [data-testid="stButton"] button:hover {
            border-color: var(--neon);
            background: rgba(101, 86, 168, 0.35);
            color: #fff;
            transform: translateY(-1px);
        }
        [data-testid="stButton"] button[kind="primary"] {
            border-color: var(--neon);
            background: var(--neon);
            color: var(--night);
            font-weight: 700;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            border-color: #7be0d8;
            background: #7be0d8;
            color: var(--night);
        }
        [data-testid="stSlider"] [role="slider"] {
            border-color: var(--neon);
            background-color: var(--neon);
            box-shadow: 0 0 12px rgba(84, 198, 192, 0.45);
        }
        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, var(--violet), var(--neon));
        }
        [data-testid="stMetric"] {
            padding: 0.85rem 1rem;
            border: 1px solid rgba(101, 86, 168, 0.4);
            border-radius: 12px;
            background: rgba(32, 43, 72, 0.56);
        }
        [data-testid="stMetricValue"] {
            color: var(--neon);
        }
        [data-testid="stAlert"] {
            border: 1px solid rgba(101, 86, 168, 0.5);
            border-left: 3px solid var(--violet);
            border-radius: 12px;
            background: rgba(32, 43, 72, 0.82);
            color: var(--paper);
        }
        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
            color: var(--paper);
        }
        [data-testid="stChatMessage"] {
            border: 1px solid rgba(101, 86, 168, 0.3);
            border-radius: 14px;
            background: rgba(32, 43, 72, 0.42);
        }
        hr {
            border-color: rgba(101, 86, 168, 0.4);
        }
        [data-testid="stCode"] {
            border: 1px solid rgba(101, 86, 168, 0.38);
            border-radius: 12px;
        }
        @media (max-width: 700px) {
            .block-container {
                padding-top: 1.4rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            [data-testid="stButton"] button {
                transition: none;
            }
            [data-testid="stButton"] button:hover {
                transform: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
