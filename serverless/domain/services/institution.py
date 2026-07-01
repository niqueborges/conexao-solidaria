from core.exceptions import InstitutionNotFoundException
from domain.interfaces import InstitutionRepository
from infra.schemas.institutions import (
    CreateInstitution,
    InstitutionResponse,
    InstitutionPrivateResponse,
    UpdateInstitution,
    ListInstitutionResponse,
)
from typing import Optional, Dict, Any
import json


class InstitutionService:
    """
    Service class to handle institution operations:
    create, get, retrieve, update, delete.
    """

    def __init__(self, repository: InstitutionRepository):
        self.repository = repository

    def create(self, data: CreateInstitution) -> InstitutionPrivateResponse:
        """Creates a new institution record."""
        institution = self.repository.save(data)
        institution_out = InstitutionPrivateResponse(**institution)
        return institution_out.model_dump()

    def get_all(
        self, limit: Optional[int] = None, last_evaluated_key: Optional[Dict[str, Any]] = None
    ) -> ListInstitutionResponse:
        """Retrieves all institution records from the database."""
        institutions, last_key = self.repository.get_all(limit=limit, last_evaluated_key=last_evaluated_key)

        last_evaluated_key_out = json.dumps(last_key) if last_key else None

        if not institutions:
            raise InstitutionNotFoundException(message="No institutions found.")
            
        institutions_out = [
            InstitutionResponse(**institution).model_dump()
            for institution in institutions
        ]
        return ListInstitutionResponse(
            institutions=institutions_out, last_evaluated_key=last_evaluated_key_out
        ).model_dump()

    def get(self, cnpj: str) -> InstitutionResponse:
        """Retrieves a specific institution by its cnpj."""
        institution = self.repository.get_by_cnpj(cnpj)
        institution_out = InstitutionResponse(**institution)
        return institution_out.model_dump()

    def query(
        self,
        region: Optional[str] = None,
        state: Optional[str] = None,
        limit: Optional[int] = None,
        last_evaluated_key: Optional[Dict[str, Any]] = None,
    ) -> ListInstitutionResponse:
        """Retrieve institutions by region and/or state parameters."""
        institutions, last_key = self.repository.query(
            region=region, state=state, limit=limit, last_evaluated_key=last_evaluated_key
        )

        last_evaluated_key_out = json.dumps(last_key) if last_key else None

        if not institutions:
            raise InstitutionNotFoundException(
                message="No institutions found matching the specified criteria."
            )
            
        institutions_out = [
            InstitutionResponse(**item).model_dump() for item in institutions
        ]
        return ListInstitutionResponse(
            institutions=institutions_out, last_evaluated_key=last_evaluated_key_out
        ).model_dump()

    def update(self, cnpj: str, data: UpdateInstitution) -> InstitutionResponse:
        """Updates an existing institution record by its cnpj."""
        institution = self.repository.update(cnpj, data)
        institution_out = InstitutionResponse(**institution)
        return institution_out.model_dump()

    def delete(self, cnpj: str) -> bool:
        """Deletes an institution by its cnpj."""
        return self.repository.delete(cnpj)
