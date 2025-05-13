"""create posts table

Revision ID: 6974e4232eef
Revises: 
Create Date: 2025-05-11 12:43:29.924945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6974e4232eef'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',sa.Column('id', sa.Integer, primary_key=True,nullable=False),
                    sa.Column('title', sa.String(100), nullable=False),
                    sa.Column('content', sa.Text, nullable=False),
                    sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
