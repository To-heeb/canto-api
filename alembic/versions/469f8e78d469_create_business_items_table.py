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
    pass


def downgrade() -> None:
    pass
