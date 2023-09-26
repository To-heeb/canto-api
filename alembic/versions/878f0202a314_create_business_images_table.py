"""create business images table

Revision ID: 878f0202a314
Revises: 91b7ca3853ad
Create Date: 2023-09-26 16:52:06.469234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '878f0202a314'
down_revision: Union[str, None] = '91b7ca3853ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create business images table with alembic
    """
    op.create_table(
        "business_images",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('image_name', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('image_type', sa.String(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['business_id'], [
            'businesses.id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    """Drop business images with alembic
    """
    op.drop_table('business_images')
