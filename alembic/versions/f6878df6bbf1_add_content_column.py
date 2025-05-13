"""add content column

Revision ID: f6878df6bbf1
Revises: 6974e4232eef
Create Date: 2025-05-11 12:57:36.235711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6878df6bbf1'
down_revision: Union[str, None] = '6974e4232eef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content2', sa.Text, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content2')
    pass
