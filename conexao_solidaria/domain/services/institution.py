from pynamodb.exceptions import DoesNotExist
from core.exceptions import ItemAlreadyExistsException
from infra.models.institutions import InstitutionModel
from infra.schemas.institutions import InstitutionIn, InstitutionOut
from uuid import uuid4


class InstitutionService:
    """
    Service class to handle institution operations:
    create, get, retrieve, update, delete.
    """

    @staticmethod
    def create(data: InstitutionIn) -> InstitutionOut:
        """Creates a new institution record."""
        try:
            InstitutionModel.get(hash_key=data.cnpj)
            raise ItemAlreadyExistsException(
                message=f"Institution with cnpj '{data.cnpj}' already exists."
            )
        except DoesNotExist:
            # The institution does not exist, proceed with creation
            pass

        # Creates the institution record in DynamoDB
        institution = InstitutionModel(
            cnpj=data.cnpj,
            id=str(uuid4()),  # Generates a new UUID
            token=str(uuid4()),  # Generates a new token
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            cep=data.cep,
            region=data.region,
            state=data.state,
            address_number=data.address_number,
            confirmation_audio=data.confirmation_audio,
            image=data.image,
            about=data.about,
            verified=False,
            site=data.site,
        )
        institution.save()

        institution_out = InstitutionOut(**institution.attribute_values)
        return institution_out.model_dump()
