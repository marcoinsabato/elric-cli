from datetime import datetime
from typing import Any


class {{ class_name }}:
    """{{ class_name }} event."""

    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event": "{{ snake_name }}",
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }
