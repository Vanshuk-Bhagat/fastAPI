"""add user table

Revision ID: dead1e9edf34
Revises: b3a62837c304
Create Date: 2025-10-10 16:56:35.997944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dead1e9edf34'
down_revision: Union[str, Sequence[str], None] = 'b3a62837c304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table("users", sa.Column("id",sa.Integer, primary_key=True, nullable=False), 
                    sa.Column("email",sa.String(), nullable=False, unique=True), 
                    sa.Column("password",sa.String(), nullable=False), 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() :
    op.drop_table("users")

    pass
