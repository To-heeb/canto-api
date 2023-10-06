"""create_business_items_table

Revision ID: 469f8e78d469
Revises: 9148c662d47b
Create Date: 2023-10-05 12:15:06.428053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '469f8e78d469'
down_revision: Union[str, None] = '9148c662d47b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create business items table with alembic
    """
    op.create_table(
        "business_items",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False,  unique=True),
        sa.Column('status', sa.Integer(), nullable=False,
                  doc="0 for inactive, 1 for active"),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'),
                  server_onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['business_id'], [
            'businesses.id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    """Drop business images with alembic
    """
    op.drop_table('business_items')
