import re

class DomainValidators:
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        return bool(re.match(r"^\d{14}$", cnpj))

    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.match(r"^[\w\s.,&-]{2,}$", name))

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return bool(re.match(r"^\d{11}$", phone))

    @staticmethod
    def validate_address_number(number: str) -> bool:
        return bool(re.match(r"^\d+$", number))

    @staticmethod
    def validate_site(site: str) -> bool:
        # Permissivo para aceitar IDNs, omitir http e suportar TLDs variados
        return bool(re.match(r"^(https?://)?(www\.)?([a-zA-Z0-9-\u00C0-\u024F]+(\.[a-zA-Z]{2,})+)(/[^\s]*)?$", site))

    @staticmethod
    def validate_cep(cep: str) -> bool:
        return bool(re.match(r"^\d{8}$", cep))

    @staticmethod
    def validate_description(desc: str) -> bool:
        return bool(re.match(r"^[A-Za-z0-9\w\s.,&-]{10,150}$", desc))

    @staticmethod
    def validate_boolean_sim_nao(val: str) -> bool:
        return bool(re.match(r"^(sim|não)$", val, re.IGNORECASE))

    @staticmethod
    def validate_filter_type(val: str) -> bool:
        return bool(re.match(r"^(estado|região)$", val, re.IGNORECASE))

    @staticmethod
    def validate_region(region: str) -> bool:
        return bool(re.match(r"^(Norte|Nordeste|Centro-Oeste|Sudeste|Sul)$", region, re.IGNORECASE))

    @staticmethod
    def validate_state(state: str) -> bool:
        return bool(re.match(r"^[a-zA-Z]{2}$", state))

    @staticmethod
    def validate_intent_choice(choice: str) -> bool:
        return bool(re.match(r"^[1-3]$", choice))
