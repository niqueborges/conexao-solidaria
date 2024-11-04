import re


def get_slot_value(slots: str, slot_name: str) -> str:
    """Helper function to safely retrieve the interpreted value of a slot."""

    slot = slots.get(slot_name)
    if slot and "value" in slot:
        return slot["value"].get("interpretedValue")
    return None


def validate_slot(slot_value: str, pattern: str):
    """Validates the slot value based on the provided regex pattern."""
    return bool(re.match(pattern, slot_value))
