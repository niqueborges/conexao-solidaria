from typing import Protocol, Optional, Any, Tuple
from infra.schemas.institutions import CreateInstitution, UpdateInstitution

class InstitutionRepository(Protocol):
    def save(self, data: CreateInstitution) -> dict[str, Any]:
        """Saves a new institution and returns the created record."""
        ...
        
    def get_all(self, limit: Optional[int] = None, last_evaluated_key: Optional[dict[str, Any]] = None) -> Tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
        """Retrieves all institutions with pagination."""
        ...

    def get_by_cnpj(self, cnpj: str) -> dict[str, Any]:
        """Retrieves an institution by its CNPJ."""
        ...

    def query(self, region: Optional[str] = None, state: Optional[str] = None, limit: Optional[int] = None, last_evaluated_key: Optional[dict[str, Any]] = None) -> Tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
        """Queries institutions by region and/or state."""
        ...

    def update(self, cnpj: str, data: UpdateInstitution) -> dict[str, Any]:
        """Updates an existing institution."""
        ...

    def delete(self, cnpj: str) -> bool:
        """Deletes an institution."""
        ...
