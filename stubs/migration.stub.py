"""{{ description }}

Revision ID: {{ revision }}
Revises: {{ down_revision }}
Create Date: {{ create_date }}

"""
from alembic import op
import sqlalchemy as sa
{{ imports }}

# revision identifiers, used by Alembic.
revision = '{{ revision }}'
down_revision = {{ down_revision }}
branch_labels = {{ branch_labels }}
depends_on = {{ depends_on }}


def upgrade() -> None:
    {{ upgrades }}
    pass


def downgrade() -> None:
    {{ downgrades }}
    pass
