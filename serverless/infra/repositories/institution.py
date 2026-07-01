import json
from uuid import uuid4
from typing import Optional, Any, Tuple
from pynamodb.exceptions import DoesNotExist, PutError
from core.exceptions import InstitutionAlreadyExistsException, InstitutionNotFoundException
from infra.models.institutions import InstitutionModel
from infra.schemas.institutions import CreateInstitution, UpdateInstitution

class PynamoDBInstitutionRepository:
    """Repository implementation using PynamoDB."""

    def save(self, data: CreateInstitution) -> dict[str, Any]:
        institution = InstitutionModel(
            cnpj=data.cnpj,
            id=str(uuid4()),
            token=str(uuid4()),
            name=data.name,
            email=data.email,
            phone_number=data.phone_number,
            cep=data.cep,
            region=data.region,
            state=data.state,
            address=data.address,
            address_number=data.address_number,
            city=data.city,
            neighborhood=data.neighborhood,
            confirmation_audio=data.confirmation_audio,
            image=data.image,
            about=data.about,
            verified=False,
            site=data.site,
        )

        try:
            institution.save(condition=InstitutionModel.cnpj.does_not_exist())
        except PutError:
            raise InstitutionAlreadyExistsException(
                message=f"Institution with cnpj '{data.cnpj}' already exists."
            )
            
        return institution.attribute_values

    def get_all(self, limit: Optional[int] = None, last_evaluated_key: Optional[dict[str, Any]] = None) -> Tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
        scan_kwargs = {}
        if limit is not None:
            scan_kwargs["limit"] = limit
        if last_evaluated_key is not None:
            scan_kwargs["last_evaluated_key"] = last_evaluated_key

        result_iterator = InstitutionModel.scan(**scan_kwargs)
        
        institutions = []
        for _ in range(limit or 1000):
            try:
                institutions.append(next(result_iterator))
            except StopIteration:
                break

        last_key = result_iterator.last_evaluated_key if result_iterator.last_evaluated_key else None
        
        return [inst.attribute_values for inst in institutions], last_key

    def get_by_cnpj(self, cnpj: str) -> dict[str, Any]:
        try:
            institution = InstitutionModel.get(hash_key=cnpj)
            return institution.attribute_values
        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )

    def query(self, region: Optional[str] = None, state: Optional[str] = None, limit: Optional[int] = None, last_evaluated_key: Optional[dict[str, Any]] = None) -> Tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
        query_kwargs = {}
        if limit is not None:
            query_kwargs["limit"] = limit
        if last_evaluated_key is not None:
            query_kwargs["last_evaluated_key"] = last_evaluated_key

        if state and region:
            query_it = InstitutionModel.state_index.query(
                state, filter_condition=(InstitutionModel.region == region), **query_kwargs
            )
        elif state:
            query_it = InstitutionModel.state_index.query(state, **query_kwargs)
        elif region:
            query_it = InstitutionModel.region_index.query(region, **query_kwargs)
        else:
            return self.get_all(limit=limit, last_evaluated_key=last_evaluated_key)

        institutions = []
        for _ in range(limit or 1000):
            try:
                institutions.append(next(query_it))
            except StopIteration:
                break

        last_key = query_it.last_evaluated_key if query_it.last_evaluated_key else None
        return [inst.attribute_values for inst in institutions], last_key

    def update(self, cnpj: str, data: UpdateInstitution) -> dict[str, Any]:
        try:
            institution = InstitutionModel.get(hash_key=cnpj)

            updates = [
                getattr(InstitutionModel, field).set(value)
                for field, value in data.model_dump(exclude_unset=True).items()
            ]
            institution.update(actions=updates)
            
            return institution.attribute_values
            
        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )

    def delete(self, cnpj: str) -> bool:
        try:
            institution = InstitutionModel.get(hash_key=cnpj)
            institution.delete()
            return True
        except DoesNotExist:
            raise InstitutionNotFoundException(
                message=f"Institution with cnpj '{cnpj}' does not exist."
            )
