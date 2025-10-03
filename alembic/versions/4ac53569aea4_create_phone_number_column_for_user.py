"""create  phone number column for user

Revision ID: 4ac53569aea4
Revises: 
Create Date: 2025-10-03 14:36:39.299664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ac53569aea4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    
