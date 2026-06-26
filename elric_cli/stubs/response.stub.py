from pydantic import BaseModel, Field


class {{ class_name }}Response(BaseModel):
    """Response schema for {{ class_name }} operations."""

    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the {{ snake_name }}")
