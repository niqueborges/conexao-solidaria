def get_slot_value(slots: str, slot_name: str) -> str:
    """Helper function to safely retrieve the interpreted value of a slot."""

    slot = slots.get(slot_name)
    if slot and "value" in slot:
        return slot["value"].get("interpretedValue")
    return None
