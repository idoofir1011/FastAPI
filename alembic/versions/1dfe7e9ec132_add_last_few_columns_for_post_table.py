"""add last few columns for post table

Revision ID: 1dfe7e9ec132
Revises: 0181873cfbaa
Create Date: 2025-11-16 20:23:13.967084

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1dfe7e9ec132"
down_revision: Union[str, Sequence[str], None] = "0181873cfbaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "published", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")
        ),
    )

    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
