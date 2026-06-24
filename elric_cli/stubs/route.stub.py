from fastapi import APIRouter

router = APIRouter(prefix="/{{ kebab_name }}", tags=["{{ snake_name }}"])


@router.get("/")
async def list_{{ snake_name }}():
    """List all {{ snake_name }} items."""
    return {"message": "List {{ snake_name }}"}


@router.get("/{id}")
async def get_{{ snake_name }}(id: str):
    """Get a specific {{ snake_name }} by ID."""
    return {"message": f"Get {{ snake_name }} {id}"}


@router.post("/")
async def create_{{ snake_name }}():
    """Create a new {{ snake_name }}."""
    return {"message": "Create {{ snake_name }}"}


@router.put("/{id}")
async def update_{{ snake_name }}(id: str):
    """Update a {{ snake_name }} by ID."""
    return {"message": f"Update {{ snake_name }} {id}"}


@router.delete("/{id}")
async def delete_{{ snake_name }}(id: str):
    """Delete a {{ snake_name }} by ID."""
    return {"message": f"Delete {{ snake_name }} {id}"}
