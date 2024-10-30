from pydantic import BaseModel, Field


class SuggestionIn(BaseModel):
    """Input model for generating suggestions based on a specified topic."""

    topic: str = Field(
        description="The topic for which the suggestion should be generated.",
        example="Artificial Intelligence",
    )
