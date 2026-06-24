from typing import Any, Optional

from app.exceptions.base import ElricException


class {{ class_name }}(ElricException):
    """{{ class_name }} exception."""

    def __init__(
        self,
        message: str = "{{ class_name }} error occurred",
        error_code: str = "{{ snake_name }}_error",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            details=details,
        )
