from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from core.config import settings


class StateIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "state-index"
        read_capacity_units = 0
        write_capacity_units = 0
        projection = AllProjection()
    state = UnicodeAttribute(hash_key=True)

class RegionIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "region-index"
        read_capacity_units = 0
        write_capacity_units = 0
        projection = AllProjection()
    region = UnicodeAttribute(hash_key=True)


class InstitutionModel(Model):
    """PynamoDB model definition for the Institutions table"""

    class Meta:
        table_name = settings.TABLE_NAME
        region = settings.REGION_NAME
        billing_mode = settings.BILLING_MODE

    cnpj = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(null=False)
    token = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    phone_number = UnicodeAttribute(null=False)
    cep = UnicodeAttribute(null=False)
    region = UnicodeAttribute(null=False)
    state = UnicodeAttribute(null=False)
    address = UnicodeAttribute(null=False)
    address_number = NumberAttribute(null=False)
    city = UnicodeAttribute(null=False)
    neighborhood = UnicodeAttribute(null=False)
    confirmation_audio = UnicodeAttribute(null=False)
    image = UnicodeAttribute(null=False)
    about = UnicodeAttribute(null=False)
    verified = BooleanAttribute(default=False, null=False)
    site = UnicodeAttribute(null=False)
    
    state_index = StateIndex()
    region_index = RegionIndex()
