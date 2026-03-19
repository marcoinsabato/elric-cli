---
trigger: glob
globs: ["database/**/*.py", "app/providers/database.py"]
---

# Database — SQLModel, PostgreSQL, Alembic

- IMPORTANT: Activate the `database-development` skill whenever working in `database/` or `app/providers/database.py`.

## SQLModel Models

- Always generate with: `uv run elric make:model ModelName`
- Every model has a UUID `id` as primary key, generated automatically.
- Every model has `created_at` and `updated_at` managed automatically.
- One file per entity in `database/models/`. Never define multiple models in the same file.
- Use `Field()` for all fields with constraints (index, unique, foreign key, default).

```python
# CORRECT — standard model structure
class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    content: str
    is_published: bool = Field(default=False)
    author_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: "User" = Relationship(back_populates="posts")
```

## Queries — Async Session

- Always use `AsyncSession` — never the synchronous session.
- Inject the session via `Depends(get_session)` in controllers.
- Prefer SQLModel's `select()` over raw queries.
- Prevent N+1 queries with `selectinload()` or `joinedload()` for relationships.
- Never use raw DB connections — always go through the ORM.

```python
# CORRECT — async query with eager loading
async def get_posts_with_authors(session: AsyncSession) -> list[Post]:
    statement = (
        select(Post)
        .where(Post.is_published == True)
        .options(selectinload(Post.author))
        .order_by(Post.created_at.desc())
    )
    result = await session.exec(statement)
    return result.all()

# WRONG — N+1
posts = await session.exec(select(Post)).all()
for post in posts:
    print(post.author.name)  # N separate queries!
```

## Migrations — Alembic

- Always generate with: `uv run elric make:migration <description_in_snake_case>`
- Use clear descriptions: `add_is_published_to_posts`, `create_api_keys_table`.
- Before every migration: run `uv run elric migrate:status` to verify current state.
- When modifying a column, include **all** previously defined attributes — Alembic does not preserve them automatically.
- Never modify migration files that have already been run in production. Always create a new migration.
- Every migration must have both `upgrade()` and `downgrade()` fully implemented.

```python
# CORRECT — downgrade always implemented
def upgrade() -> None:
    op.add_column("posts", sa.Column("is_published", sa.Boolean(), nullable=False, server_default="false"))

def downgrade() -> None:
    op.drop_column("posts", "is_published")
```

## Seeders

- Generate with: `uv run elric make:seeder SeederName`
- Run with: `uv run elric db:seed`
- Seeders must be idempotent — use `INSERT ... ON CONFLICT DO NOTHING` or a get-or-create pattern.
- Use seeders for mandatory initial data (e.g. first admin API key), not for test data.
- For tests, use pytest fixtures defined in `tests/conftest.py`.
