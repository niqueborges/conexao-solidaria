from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from conexao_solidaria.core.config import settings


class InstitutionModel(Model):
    """
    Definição do modelo PynamoDB para a tabela de Instituições
    """

    class Meta:
        table_name = settings.TABLE_NAME
        region = settings.REGION_NAME
        billing_mode = "PAY_PER_REQUEST"  # Modo de pagamento sob demanda

    cnpj = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute()
    token = UnicodeAttribute()
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone_number = UnicodeAttribute()
    cep = UnicodeAttribute()
    address_number = NumberAttribute()
    image_path = UnicodeAttribute()
    about = UnicodeAttribute()
    verified = BooleanAttribute()
