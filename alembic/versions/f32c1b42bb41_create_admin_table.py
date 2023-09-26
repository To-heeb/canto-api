"""create admin table

Revision ID: f32c1b42bb41
Revises: 068053292dc7
Create Date: 2023-09-26 16:51:39.566082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f32c1b42bb41'
down_revision: Union[str, None] = '068053292dc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create admin table with alembic
    """
    op.create_table(
        "admins",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column('display_image', sa.String(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    """Drop admin table with alembic
    """
    op.drop_table('admins')
