from typing import Optional

from pydantic import BaseModel, Field


class {{ class_name }}Base(BaseModel):
    """Base schema for {{ class_name }}."""
    
    name: str = Field(..., description="Name of the {{ snake_name }}")
    description: Optional[str] = Field(None, description="Description of the {{ snake_name }}")


class {{ class_name }}Create({{ class_name }}Base):
    """Schema for creating a {{ class_name }}."""
    
    pass


class {{ class_name }}Update(BaseModel):
    """Schema for updating a {{ class_name }}."""
    
    name: Optional[str] = Field(None, description="Name of the {{ snake_name }}")
    description: Optional[str] = Field(None, description="Description of the {{ snake_name }}")


class {{ class_name }}Response({{ class_name }}Base):
    """Schema for {{ class_name }} response."""
    
    id: str = Field(..., description="Unique identifier")
    
    class Config:
        from_attributes = True
