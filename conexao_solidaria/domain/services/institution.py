from pynamodb.exceptions import DoesNotExist
from core.exceptions import ItemAlreadyExistsException
from infra.models.institutions import InstitutionModel
from infra.schemas.institutions import InstitutionIn, InstitutionOut, UpdateInstitution
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

    @staticmethod
    def get_all() -> list[dict]:
        """Retrieves all institution records from the database."""
        institutions_out = list(InstitutionModel.scan())
        return [
            InstitutionOut(**institution.attribute_values).model_dump()
            for institution in institutions_out
        ]

    @staticmethod
    def get(cnpj: str) -> InstitutionOut:
        """Retrieves a specific institution by its cnpj."""
        try:
            institution = InstitutionModel.get(hash_key=cnpj)
        except DoesNotExist:
            return

        institution_out = InstitutionOut(**institution.attribute_values)
        return institution_out.model_dump()

    @staticmethod
    def update(cnpj: str, data: UpdateInstitution) -> InstitutionOut:
        """Updates an existing institution record by its cnpj."""
        try:
            institution = InstitutionModel.get(hash_key=cnpj)

            # Update field values
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(institution, field, value)
            institution.save()

        except DoesNotExist:
            return

        institution_out = InstitutionOut(**institution.attribute_values)
        return institution_out.model_dump()
