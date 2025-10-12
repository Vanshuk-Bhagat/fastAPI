"""add content column to post table

Revision ID: b3a62837c304
Revises: f6afa8cd40a6
Create Date: 2025-10-10 16:38:29.574965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3a62837c304'
down_revision: Union[str, Sequence[str], None] = 'f6afa8cd40a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False),)
    pass


def downgrade() :
    op.drop_column('posts', 'content')
    pass
