"""add content column to post table

Revision ID: a2af85c89a81
Revises: 0deaa2c4db71
Create Date: 2025-11-16 17:33:21.148584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2af85c89a81"
down_revision: Union[str, Sequence[str], None] = "0deaa2c4db71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
