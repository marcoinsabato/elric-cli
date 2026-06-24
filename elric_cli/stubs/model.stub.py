import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class {{ class_name }}(SQLModel, table=True):
    """{{ class_name }} database model."""
    
    __tablename__ = "{{ snake_name }}s"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
