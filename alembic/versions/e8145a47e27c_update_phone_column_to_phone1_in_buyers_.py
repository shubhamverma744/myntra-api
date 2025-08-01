"""Update phone column to phone1 in buyers table

Revision ID: e8145a47e27c
Revises: 72a4749c2c70
Create Date: 2025-07-31 17:41:29.988986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8145a47e27c'
down_revision: Union[str, Sequence[str], None] = '72a4749c2c70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('buyers', 'phone', new_column_name='phone1')


def downgrade() -> None:
    op.alter_column('buyers', 'phone1', new_column_name='phone')
