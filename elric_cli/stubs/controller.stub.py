from typing import Any


class {{ class_name }}:
    """{{ class_name }} controller for business logic."""

    async def index(self) -> dict[str, Any]:
        """List all items."""
        # TODO: Implement list logic
        return {"data": [], "total": 0}

    async def show(self, id: str) -> dict[str, Any]:
        """Get a specific item by ID."""
        # TODO: Implement get logic
        return {"id": id, "data": {}}

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new item."""
        # TODO: Implement create logic
        return {"id": "new_id", "data": data}

    async def update(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Update an item by ID."""
        # TODO: Implement update logic
        return {"id": id, "data": data}

    async def delete(self, id: str) -> dict[str, Any]:
        """Delete an item by ID."""
        # TODO: Implement delete logic
        return {"id": id, "deleted": True}
