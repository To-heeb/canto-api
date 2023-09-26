"""create business table

Revision ID: 91b7ca3853ad
Revises: f32c1b42bb41
Create Date: 2023-09-26 16:51:59.191700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91b7ca3853ad'
down_revision: Union[str, None] = 'f32c1b42bb41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create businesses table with alembic
    """
    op.create_table(
        "businesses",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False,  unique=True),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('business_type_id', sa.Integer(), nullable=False),
        sa.Column('display_image', sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column('views', sa.Integer(), nullable=True, server_default="0"),
        sa.Column("opened_at", sa.TIME, nullable=False),
        sa.Column('closed_at', sa.TIME, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'),
                  server_onupdate=sa.text('now()')),
        sa.orm.relationship("BusinessImage"),
        sa.ForeignKeyConstraint(['business_type_id'], [
                                'business_types.id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    """Drop businesses table with alembic
    """
    op.drop_table('businesses')
