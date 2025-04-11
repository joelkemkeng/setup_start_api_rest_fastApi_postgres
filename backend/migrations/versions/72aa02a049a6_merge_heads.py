"""merge heads

Revision ID: 72aa02a049a6
Revises: d5ecf7a4b210, fa84683ee8bb
Create Date: 2025-04-11 00:26:12.638711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72aa02a049a6'
down_revision: Union[str, None] = ('d5ecf7a4b210', 'fa84683ee8bb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
