import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from utils.adventure_prompts import SYSTEM_INSTRUCTION
from utils.game_data import ARCHETYPES, CAMPAIGN_PREMISE, DISTRICTS


MODEL_NAME = "gemini-3.1-flash-lite"
FALLBACK_MODELS = (
    MODEL_NAME,
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
)
MAX_BALANCE_CHANGE = 100
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

Outcome = Literal["scene", "success", "failure", "mixed"]


@dataclass(frozen=True)
class AdventureTurn:
    narration: str
    choices: tuple[str, str, str]
    outcome: Outcome
    balance_change: int
    item_gain: str
    item_loss: str
    model_name: str


class AdventureModelError(RuntimeError):
    """Raised when Gemini cannot return a valid adventure turn."""


RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "narration": {
            "type": "STRING",
            "description": "Natychmiastowa, konkretna narracja po polsku, 1-3 zdania bez filleru.",
        },
        "choices": {
            "type": "ARRAY",
            "items": {
                "type": "STRING",
                "description": "Krótka, jednoznaczna akcja w pierwszej osobie do pokazania jako przycisk.",
            },
            "minItems": 3,
            "maxItems": 3,
        },
        "outcome": {
            "type": "STRING",
            "enum": ["scene", "success", "failure", "mixed"],
        },
        "balance_change": {
            "type": "INTEGER",
            "minimum": -MAX_BALANCE_CHANGE,
            "maximum": MAX_BALANCE_CHANGE,
        },
        "item_gain": {
            "type": "STRING",
            "description": "Nazwa jednego zdobytego przedmiotu albo pusty tekst.",
        },
        "item_loss": {
            "type": "STRING",
            "description": "Dokładna nazwa przedmiotu zużytego, oddanego, zgubionego lub zniszczonego albo pusty tekst.",
        },
    },
    "required": [
        "narration",
        "choices",
        "outcome",
        "balance_change",
        "item_gain",
        "item_loss",
    ],
}


def _parse_turn(
    response_data: dict,
    *,
    player_action: str | None = None,
) -> AdventureTurn:
    try:
        candidates = response_data["candidates"]
        response_text = candidates[0]["content"]["parts"][0]["text"]
        turn_data = json.loads(response_text)
        narration = turn_data["narration"]
        choices = turn_data["choices"]
        outcome = turn_data["outcome"]
        balance_change = turn_data["balance_change"]
        item_gain = turn_data["item_gain"]
        item_loss = turn_data["item_loss"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        raise AdventureModelError(
            "Gemini zwróciło odpowiedź w nieoczekiwanym formacie."
        ) from error

    if not isinstance(narration, str) or not narration.strip():
        raise AdventureModelError("Gemini zwróciło pustą narrację.")
    if (
        not isinstance(item_gain, str)
        or len(item_gain.strip()) > 80
        or not isinstance(item_loss, str)
        or len(item_loss.strip()) > 80
    ):
        raise AdventureModelError("Gemini zwróciło nieprawidłową zmianę ekwipunku.")
    if (
        not isinstance(choices, list)
        or len(choices) != 3
        or any(
            not isinstance(choice, str)
            or not choice.strip()
            or len(choice.strip()) > 80
            for choice in choices
        )
        or len({choice.strip().casefold() for choice in choices}) != 3
    ):
        raise AdventureModelError(
            "Gemini musi zwrócić dokładnie trzy różne, krótkie opcje działań."
        )
    normalized_outcome = _normalize_outcome(outcome)
    if (
        not isinstance(balance_change, int)
        or isinstance(balance_change, bool)
        or not -MAX_BALANCE_CHANGE <= balance_change <= MAX_BALANCE_CHANGE
    ):
        raise AdventureModelError("Gemini zwróciło nieprawidłową zmianę salda.")
    if player_action is not None and normalized_outcome == "scene":
        normalized_outcome = "mixed"
    return AdventureTurn(
        narration.strip(),
        tuple(choice.strip() for choice in choices),
        normalized_outcome,
        balance_change,
        item_gain.strip(),
        item_loss.strip(),
        "",
    )


def _normalize_outcome(value: object) -> Outcome:
    if not isinstance(value, str):
        raise AdventureModelError("Gemini nie zwróciło tekstowego wyniku działania.")

    plain_ascii = (
        unicodedata.normalize("NFKD", value.strip().casefold())
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    normalized = re.sub(r"[^a-z0-9]+", "_", plain_ascii).strip("_")
    aliases: dict[str, Outcome] = {
        "success": "success",
        "successful": "success",
        "sukces": "success",
        "udalo_sie": "success",
        "failure": "failure",
        "fail": "failure",
        "failed": "failure",
        "porazka": "failure",
        "nie_udalo_sie": "failure",
        "mixed": "mixed",
        "partial": "mixed",
        "partial_success": "mixed",
        "mixed_success": "mixed",
        "czesciowy_sukces": "mixed",
        "scene": "scene",
        "situation": "scene",
        "scena": "scene",
    }
    outcome = aliases.get(normalized)
    if outcome is None:
        if "partial" in normalized or "complication" in normalized:
            outcome = "mixed"
        elif normalized.startswith(("success_", "successful_", "succeeded_")):
            outcome = "success"
        elif normalized.startswith(("failure_", "failed_", "unsuccessful_")):
            outcome = "failure"
    if outcome is None:
        raise AdventureModelError(
            f"Gemini zwróciło nieznany wynik {value!r}; "
            "oczekiwano success, failure, mixed albo scene."
        )
    return outcome


def generate_turn(
    *,
    api_key: str,
    character: dict,
    messages: list[dict],
    player_action: str | None,
) -> AdventureTurn:
    character_context = {
        "name": character["name"],
        "district": character["district"],
        "district_lore": DISTRICTS.get(character["district"], ""),
        "campaign_premise": CAMPAIGN_PREMISE,
        "archetype": character["archetype"],
        "archetype_description": ARCHETYPES.get(character["archetype"], ""),
        "backstory": character["backstory"],
        "stats": {
            "courage": character["courage"],
            "cleverness": character["cleverness"],
            "resourcefulness": character["resourcefulness"],
        },
        "balance_pln": character["balance"],
        "inventory": character.get("inventory", []),
        "player_action": player_action,
        "recent_conversation": [
            {
                "role": message["role"],
                "content": message["content"],
                **({"choices": message["choices"]} if message.get("choices") else {}),
            }
            for message in messages[-20:]
        ],
    }
    request_body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": json.dumps(character_context, ensure_ascii=False)}
                ],
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
            "temperature": 0.8,
        },
    }
    errors = []
    for model_name in FALLBACK_MODELS:
        request = Request(
            f"{GEMINI_API_URL}/{model_name}:generateContent?key={api_key}",
            data=json.dumps(request_body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=30) as response:
                response_data = json.loads(response.read())
            turn = _parse_turn(response_data, player_action=player_action)
            return AdventureTurn(
                turn.narration,
                turn.choices,
                turn.outcome,
                turn.balance_change,
                turn.item_gain,
                turn.item_loss,
                model_name,
            )
        except HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            try:
                error_data = json.loads(error_body)
            except json.JSONDecodeError:
                error_data = {}
            api_message = error_data.get("error", {}).get("message")
            detail = (
                f": {api_message}"
                if isinstance(api_message, str)
                else ""
            )
            errors.append(f"{model_name}: HTTP {error.code}{detail}")
            if error.code not in {404, 408, 429, 500, 502, 503, 504}:
                break
        except URLError as error:
            errors.append(f"{model_name}: połączenie — {error.reason}")
        except TimeoutError:
            errors.append(f"{model_name}: przekroczono limit czasu")
        except json.JSONDecodeError:
            errors.append(f"{model_name}: API zwróciło nieprawidłowy JSON")
        except AdventureModelError as error:
            errors.append(f"{model_name}: {error}")

    raise AdventureModelError(
        "Nie udało się uzyskać odpowiedzi z Gemini. Próby modeli: "
        + " | ".join(errors)
    )
