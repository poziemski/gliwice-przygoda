# Gliwice: Karta postaci

A simple character creator for a setting inspired by Gliwice. Start at the
title screen, then choose a district and role, write a short backstory, and set
your character's attributes. Characters and their adventure history are saved
in your browser's local storage on this device.

## Audio assets

- `assets/music/title_theme.wav` is the looping title-screen theme.
- Put future sound effects in `assets/sfx/`.

## Run locally

Install the dependencies and start the app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Gemini adventure

The adventure uses the Gemini API to create short scenes and exactly three
clickable action choices per turn. Characters can carry up to three items;
Gemini can award, consume, lose, or hand off items as the story justifies.
Players continue the story by selecting an option button rather than entering
free-form text. If the primary model is unavailable or rate-limited, the app
tries Gemini 2.5 Flash-Lite and then Gemini 2.5 Flash using the same API key.
Fallback models are still subject to Google's free-tier model availability
and quotas. Create an API key in Google AI Studio and provide it using either
a `GEMINI_API_KEY` environment variable or a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-api-key"
```

In PowerShell, you can set the environment variable for the current terminal
before starting Streamlit:

```powershell
$env:GEMINI_API_KEY = "your-api-key"
streamlit run app.py
```

Do not commit the API key. The local secrets file is excluded by `.gitignore`.
The game save remains in this browser and can be cleared by deleting this
site's browser data; it is not synced between devices.
