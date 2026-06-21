from typing import Dict, Any
from domain.schemas import RegistrationRequest, ListInstitutionRequest

class LexMapper:
    @staticmethod
    def extract_flat_slots(slots: dict) -> Dict[str, Any]:
        """
        Converte o dicionário complexo de slots do Lex em um dicionário plano.
        Ex: {"CNPJ": {"value": {"interpretedValue": "123"}}} -> {"CNPJ": "123"}
        """
        flat_slots = {}
        if not slots:
            return flat_slots

        for slot_name, slot_data in slots.items():
            if slot_data and slot_data.get("value"):
                flat_slots[slot_name] = slot_data["value"].get("interpretedValue")
            else:
                flat_slots[slot_name] = None
        return flat_slots

    @staticmethod
    def to_registration_request(slots: dict) -> RegistrationRequest:
        flat_slots = LexMapper.extract_flat_slots(slots)
        return RegistrationRequest(
            cnpj=flat_slots.get("CNPJ"),
            name=flat_slots.get("InstitutionName"),
            email=flat_slots.get("InstitutionEmail"),
            phone_number=flat_slots.get("InstitutionPhone"),
            region=flat_slots.get("InstitutionRegion"),
            state=flat_slots.get("InstitutionState"),
            address=flat_slots.get("InstitutionAddress"),
            city=flat_slots.get("InstitutionCity"),
            neighborhood=flat_slots.get("InstitutionNeighborhood"),
            cep=flat_slots.get("InstitutionCep"),
            address_number=flat_slots.get("InstitutionAddressNumber"),
            description=flat_slots.get("InstitutionDescription"),
            site=flat_slots.get("InstitutionSite"),
            image_path=flat_slots.get("ImagePath"),
        )

    @staticmethod
    def to_list_request(slots: dict) -> ListInstitutionRequest:
        flat_slots = LexMapper.extract_flat_slots(slots)
        return ListInstitutionRequest(
            filter_boolean=flat_slots.get("FilterBoolean"),
            filter_type=flat_slots.get("FilterType"),
            region=flat_slots.get("Region"),
            state=flat_slots.get("States"),
        )
