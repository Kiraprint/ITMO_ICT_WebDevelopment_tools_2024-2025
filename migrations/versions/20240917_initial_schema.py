"""Initial schema

Revision ID: initial_schema
Revises: 
Create Date: 2023-09-17 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tables for all models
    # This is a placeholder - when you run alembic revision --autogenerate
    # it will generate the actual SQL commands based on your models
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Drop all tables
    # This is a placeholder - when you run alembic revision --autogenerate
    # it will generate the actual SQL commands based on your models
    pass