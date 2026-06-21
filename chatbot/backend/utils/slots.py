def get_slot_value(slots: dict, slot_name: str) -> str:
    """Helper function to safely retrieve the interpreted value of a slot."""
    slot = slots.get(slot_name)
    if slot and "value" in slot:
        return slot["value"].get("interpretedValue")
    return None

def update_multiple_slot_values(event: dict, slots_values: dict) -> None:
    """
    Updates multiple slot values in the event with the required format.
    """
    for slot_name, value in slots_values.items():
        event["sessionState"]["intent"]["slots"][slot_name] = {
            "shape": "Scalar",
            "value": {"interpretedValue": value},
        }
