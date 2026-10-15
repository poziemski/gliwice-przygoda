from uuid import uuid4

from utils.game_data import ARCHETYPES, DISTRICTS


DEFAULT_SAVE = {"version": 1, "characters": [], "adventures": {}}
VALID_ROLES = {"user", "assistant"}
MAX_MESSAGES_PER_ADVENTURE = 200
MAX_MESSAGE_LENGTH = 5000
MAX_INVENTORY_ITEMS = 3
MAX_ITEM_NAME_LENGTH = 80


def validate_save_data(value: object) -> dict:
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("Zapis z przeglądarki ma nieobsługiwaną wersję.")

    characters = value.get("characters")
    adventures = value.get("adventures")
    if not isinstance(characters, list) or not isinstance(adventures, dict):
        raise ValueError("Zapis z przeglądarki ma nieprawidłową strukturę.")

    validated_characters = []
    character_ids = set()
    for character in characters:
        if not isinstance(character, dict):
            raise ValueError("Zapis zawiera nieprawidłową postać.")
        character_id = character.get("character_id")
        name = character.get("name")
        district = character.get("district")
        archetype = character.get("archetype")
        backstory = character.get("backstory", "")
        stats = {
            key: character.get(key)
            for key in ("courage", "cleverness", "resourcefulness")
        }
        balance = character.get("balance", 0)
        inventory = character.get("inventory", [])
        if (
            not isinstance(character_id, str)
            or not character_id
            or character_id in character_ids
            or not isinstance(name, str)
            or not name.strip()
            or len(name) > 80
            or district not in DISTRICTS
            or archetype not in ARCHETYPES
            or not isinstance(backstory, str)
            or len(backstory) > 240
            or any(
                not isinstance(stat, int)
                or isinstance(stat, bool)
                or not 0 <= stat <= 10
                for stat in stats.values()
            )
            or sum(stats.values()) > 10
            or not isinstance(balance, int)
            or isinstance(balance, bool)
            or balance < 0
            or not isinstance(inventory, list)
            or len(inventory) > MAX_INVENTORY_ITEMS
            or any(
                not isinstance(item, str)
                or not item.strip()
                or len(item.strip()) > MAX_ITEM_NAME_LENGTH
                for item in inventory
            )
            or len({item.strip().casefold() for item in inventory if isinstance(item, str)})
            != len(inventory)
        ):
            raise ValueError("Zapis zawiera nieprawidłowe dane postaci.")
        character_ids.add(character_id)
        validated_characters.append(
            {
                "character_id": character_id,
                "name": name.strip(),
                "district": district,
                "archetype": archetype,
                "backstory": backstory,
                **stats,
                "balance": balance,
                "inventory": [item.strip() for item in inventory],
            }
        )

    validated_adventures = {}
    for character_id, messages in adventures.items():
        if character_id not in character_ids or not isinstance(messages, list):
            raise ValueError("Zapis zawiera nieprawidłowy dziennik przygody.")
        if len(messages) > MAX_MESSAGES_PER_ADVENTURE:
            raise ValueError("Dziennik przygody przekracza maksymalny rozmiar.")
        validated_messages = []
        for message in messages:
            if (
                not isinstance(message, dict)
                or message.get("role") not in VALID_ROLES
                or not isinstance(message.get("content"), str)
                or len(message["content"]) > MAX_MESSAGE_LENGTH
                or (
                    "choices" in message
                    and (
                        not isinstance(message["choices"], list)
                        or len(message["choices"]) != 3
                        or any(
                            not isinstance(choice, str)
                            or not choice.strip()
                            or len(choice) > 80
                            for choice in message["choices"]
                        )
                        or len(
                            {
                                choice.strip().casefold()
                                for choice in message["choices"]
                                if isinstance(choice, str)
                            }
                        )
                        != 3
                    )
                )
            ):
                raise ValueError("Zapis zawiera nieprawidłową wiadomość.")
            validated_message = {
                "role": message["role"],
                "content": message["content"],
            }
            if "choices" in message:
                validated_message["choices"] = message["choices"]
            validated_messages.append(validated_message)
        validated_adventures[character_id] = validated_messages

    return {
        "version": 1,
        "characters": validated_characters,
        "adventures": validated_adventures,
    }


def save_character(
    save_data: dict,
    *,
    name: str,
    district: str,
    archetype: str,
    backstory: str,
    stats: dict[str, int],
) -> str:
    if not name.strip():
        raise ValueError("Postać musi mieć imię lub ksywkę.")
    character_id = str(uuid4())
    character = {
        "character_id": character_id,
        "name": name.strip(),
        "district": district,
        "archetype": archetype,
        "backstory": backstory,
        "courage": stats["courage"],
        "cleverness": stats["cleverness"],
        "resourcefulness": stats["resourcefulness"],
        "balance": 0,
        "inventory": [],
    }
    candidate = {
        **save_data,
        "characters": [*save_data["characters"], character],
        "adventures": {
            **save_data["adventures"],
            character_id: [],
        },
    }
    validate_save_data(candidate)
    save_data["characters"].append(character)
    save_data["adventures"][character_id] = []
    return character_id


def list_characters(save_data: dict) -> list[dict]:
    return list(save_data["characters"])


def get_character(save_data: dict, character_id: str) -> dict | None:
    return next(
        (
            character
            for character in save_data["characters"]
            if character["character_id"] == character_id
        ),
        None,
    )


def get_messages(save_data: dict, character_id: str) -> list[dict]:
    return list(save_data["adventures"].get(character_id, []))


def _apply_inventory_change(
    character: dict,
    *,
    item_gain: str,
    item_loss: str,
) -> list[str]:
    if (
        not isinstance(item_gain, str)
        or len(item_gain.strip()) > MAX_ITEM_NAME_LENGTH
        or not isinstance(item_loss, str)
        or len(item_loss.strip()) > MAX_ITEM_NAME_LENGTH
    ):
        raise ValueError("Zmiana ekwipunku jest nieprawidłowa.")

    inventory = character["inventory"]
    notices = []
    normalized_loss = item_loss.strip().casefold()
    removed_item = next(
        (item for item in inventory if item.casefold() == normalized_loss),
        None,
    )
    if removed_item is not None:
        inventory.remove(removed_item)
        notices.append(f"🎒 Oddano lub zużyto: {removed_item}")

    normalized_gain = item_gain.strip()
    if normalized_gain:
        if any(item.casefold() == normalized_gain.casefold() for item in inventory):
            notices.append(f"🎒 Masz już przedmiot: {normalized_gain}")
        elif len(inventory) >= MAX_INVENTORY_ITEMS:
            notices.append("🎒 Ekwipunek pełny — przedmiot nie został dodany.")
        else:
            inventory.append(normalized_gain)
            notices.append(f"🎒 Zdobyto: {normalized_gain}")
    return notices


def add_opening_scene(
    save_data: dict,
    character_id: str,
    narration: str,
    choices: tuple[str, str, str],
    item_gain: str = "",
    item_loss: str = "",
) -> None:
    character = get_character(save_data, character_id)
    if character is None:
        raise ValueError("Nie znaleziono zapisanej postaci.")
    inventory_notices = _apply_inventory_change(
        character,
        item_gain=item_gain,
        item_loss=item_loss,
    )
    content = narration
    if inventory_notices:
        content += "\n\n" + "\n\n".join(inventory_notices)
    save_data["adventures"].setdefault(character_id, []).append(
        {"role": "assistant", "content": content, "choices": list(choices)}
    )


def add_adventure_turn(
    save_data: dict,
    character_id: str,
    player_action: str,
    narration: str,
    choices: tuple[str, str, str],
    outcome: str,
    balance_change: int,
    item_gain: str,
    item_loss: str,
) -> int:
    character = get_character(save_data, character_id)
    if character is None:
        raise ValueError("Nie znaleziono zapisanej postaci.")
    if outcome not in {"scene", "success", "failure", "mixed"}:
        raise ValueError("Nieprawidłowy wynik tury.")
    if not isinstance(balance_change, int) or not -100 <= balance_change <= 100:
        raise ValueError("Zmiana salda musi mieścić się w zakresie od -100 do 100.")
    if (
        len(player_action) > MAX_MESSAGE_LENGTH
        or len(narration) > MAX_MESSAGE_LENGTH
        or len(choices) != 3
        or any(not choice.strip() or len(choice) > 80 for choice in choices)
    ):
        raise ValueError("Wiadomość przekracza maksymalną długość.")

    applied_change = max(-character["balance"], balance_change)
    outcome_labels = {
        "scene": "📖 Sytuacja się rozwija",
        "success": "✅ Udało się",
        "failure": "❌ Nie udało się",
        "mixed": "⚖️ Częściowy sukces",
    }
    response_content = f"**{outcome_labels[outcome]}**\n\n{narration}"
    if applied_change:
        response_content += f"\n\n💰 Saldo: {applied_change:+d} zł"
    inventory_notices = _apply_inventory_change(
        character,
        item_gain=item_gain,
        item_loss=item_loss,
    )
    if inventory_notices:
        response_content += "\n\n" + "\n\n".join(inventory_notices)
    messages = save_data["adventures"].setdefault(character_id, [])
    messages.extend(
        [
            {"role": "user", "content": player_action},
            {
                "role": "assistant",
                "content": response_content,
                "choices": list(choices),
            },
        ]
    )
    character["balance"] += applied_change
    if len(messages) > MAX_MESSAGES_PER_ADVENTURE:
        del messages[:-MAX_MESSAGES_PER_ADVENTURE]
    return applied_change
