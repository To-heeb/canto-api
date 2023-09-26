"""create business types table

Revision ID: 068053292dc7
Revises: 
Create Date: 2023-09-26 16:51:27.869749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '068053292dc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create business types table with alembic
    """
    op.create_table(
        "business_types",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False,  unique=True),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'),
                  server_onupdate=sa.text('now()'))
    )


def downgrade() -> None:
    """Drop business types table with alembic
    """
    op.drop_table('business_types')
