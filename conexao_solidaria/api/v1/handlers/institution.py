import json
from typing import Any
from core.exceptions import ItemAlreadyExistsException
from domain.services.institution import InstitutionService
from infra.schemas.institutions import InstitutionIn
from aws_lambda_powertools.utilities.parser import parse, ValidationError
from aws_lambda_powertools.utilities.typing import LambdaContext
from utils.build import build_http_response


def create(event: dict, context: LambdaContext) -> dict[str, Any]:
    """Registers a new Institution in Dynamo."""
    try:
        # Validates the body by parsing to InstitutionIn
        data = parse(event=json.loads(event.get("body")), model=InstitutionIn)
    except ValidationError as exc:
        return build_http_response(
            status_code=400, body={"ValidationError": exc.errors(include_url=False)}
        )
    try:
        institution = InstitutionService.create(data=data)
    except ItemAlreadyExistsException as exc:
        return build_http_response(status_code=409, body={"detail": exc.message})

    return build_http_response(status_code=201, body=institution)
