from pydantic import BaseModel, Field


class {{ class_name }}Request(BaseModel):
    """Request schema for {{ class_name }} operations."""

    name: str = Field(..., description="Name of the {{ snake_name }}")
