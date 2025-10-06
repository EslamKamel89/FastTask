"""Create phone number column in users table

Revision ID: 148f95f3eea6
Revises: 
Create Date: 2025-10-06 06:51:22.711802

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '148f95f3eea6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users' , sa.Column('phone_number' , sa.String(20) , nullable=True ))


def downgrade() -> None:
    op.drop_column('users' , 'phone_number')
