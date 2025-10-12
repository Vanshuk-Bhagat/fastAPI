"""create post table

Revision ID: f6afa8cd40a6
Revises: 
Create Date: 2025-10-10 16:14:43.647048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6afa8cd40a6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts", sa.Column("id",sa.Integer, primary_key=True, nullable=False), sa.Column("title",sa.String(),nullable=False) )

    pass


def downgrade() :
    op.drop_table("posts")
    pass
