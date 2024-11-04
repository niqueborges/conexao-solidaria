import re

from utils.responses import LexResponses


def get_slot_value(slots: str, slot_name: str) -> str:
    """Helper function to safely retrieve the interpreted value of a slot."""

    slot = slots.get(slot_name)
    if slot and "value" in slot:
        return slot["value"].get("interpretedValue")
    return None


def validate_slot(slot_value: str, pattern: str):
    """Validates the slot value based on the provided regex pattern."""
    return bool(re.match(pattern, slot_value))


def check_slot_filling(slots: dict, event: dict, validation_rules: dict) -> None:
    """
    Responsible for checking if the slots are properly filled.
    """

    for slot_name, slot_data in slots.items():
        slot_value = (
            slot_data.get("value", {}).get("interpretedValue")
            if slot_data and slot_data.get("value")
            else None
        )
        pattern = validation_rules.get(slot_name)

        if pattern and slot_value is not None:
            is_valid = validate_slot(slot_value, pattern)
            if not is_valid:
                return LexResponses.elicit_slot(event, slot_name)

    return LexResponses.delegate(event)
