"""create business working hours table

Revision ID: 9148c662d47b
Revises: 878f0202a314
Create Date: 2023-09-27 11:28:18.243583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9148c662d47b'
down_revision: Union[str, None] = '878f0202a314'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create business working hours table with alembic
    """
    op.create_table(
        "business_working_hours",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('weekday', sa.Integer(), ),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column("opened_at", sa.TIME, nullable=False),
        sa.Column('closed_at', sa.TIME, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'),
                  server_onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['business_id'],
                                ['businesses.id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    """Drop business working hours table with alembic
    """
    op.drop_table('business_working_hours')
