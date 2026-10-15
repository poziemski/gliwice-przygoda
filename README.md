# Gliwice: Karta postaci

Tekstowa przygoda w klimacie miejskiej tajemnicy, osadzona we współczesnych
Gliwicach. Rozpocznij od prologu o nocnym sygnale z Radiostacji, stwórz postać
i rozwijaj historię, wybierając jedną z trzech akcji w każdej turze. Postać ma
trzy atrybuty oraz ekwipunek z miejscem na maksymalnie trzy przedmioty.

Postacie i przebieg przygody są zapisywane w pamięci lokalnej przeglądarki na
tym urządzeniu. Zapis nie jest synchronizowany między urządzeniami.

## Prezentacja wideo


## Muzyka i efekty dźwiękowe

- `assets/music/title_theme.wav` — zapętlony motyw ekranu tytułowego.
- Przyszłe efekty dźwiękowe umieszczaj w `assets/sfx/`.

## Uruchomienie lokalne

Zainstaluj zależności i uruchom aplikację:

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

## Przygoda z Gemini

Do generowania krótkich scen i trzech klikalnych opcji akcji używane jest API
Gemini. Jeśli główny model jest niedostępny lub osiągnął limit, aplikacja
próbuje kolejno Gemini 2.5 Flash-Lite i Gemini 2.5 Flash, używając tego samego
klucza API. Dostępność modeli i limity darmowego poziomu zależą od Google.

Utwórz klucz API w Google AI Studio i udostępnij go aplikacji przez zmienną
środowiskową `GEMINI_API_KEY` albo plik `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "twój-klucz-api"
```

W PowerShell możesz ustawić zmienną dla bieżącego terminala przed
uruchomieniem Streamlit:

```powershell
$env:GEMINI_API_KEY = "twój-klucz-api"
streamlit run app.py
```

Nie zapisuj klucza API w repozytorium. Lokalny plik secrets jest wykluczony
przez `.gitignore`. Zapis gry można usunąć, kasując dane tej witryny
w przeglądarce.
