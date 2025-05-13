"""add foreign-key to posts table

Revision ID: 88163ececc7a
Revises: 4ad4b6932857
Create Date: 2025-05-11 15:04:09.870158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88163ececc7a'
down_revision: Union[str, None] = '4ad4b6932857'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'posts_users_fk',  # name of the constraint
        source_table='posts',  # name of the source table
        referent_table='users',  # name of the target table
        local_cols=['owner_id'],  # name of the local column
        remote_cols=['id'],  # name of the remote column
        ondelete='CASCADE')  # action on delete


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'posts_users_fk',  # name of the constraint
        table_name='posts'  # name of the table
    )
    op.drop_column('posts', 'owner_id')  # name of the column
    pass
