"""add user table

Revision ID: 97f6bbfa19d2
Revises: a2af85c89a81
Create Date: 2025-11-16 17:43:59.240011

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97f6bbfa19d2"
down_revision: Union[str, Sequence[str], None] = "a2af85c89a81"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")


pass
