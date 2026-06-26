# Logging and Validation

## Logging

Use structured logs and meaningful event names.

Example style:

```python
log.info("chat.request.received", route="/api/v1/chat")
```

## Validation

Validate request payloads with Pydantic schemas in `app/schemas`.

```python
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    email: str
    age: int = Field(ge=18)
```

