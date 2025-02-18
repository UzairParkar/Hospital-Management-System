"""adding columns

Revision ID: d14289d64300
Revises: 2756ab89d81b
Create Date: 2025-02-18 11:57:38.761365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd14289d64300'
down_revision: Union[str, None] = '2756ab89d81b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('appointments', sa.Column('doctor_first_name', sa.String(length=100), nullable=False))
    op.add_column('appointments', sa.Column('doctor_last_name', sa.String(length=100), nullable=False))
    op.add_column('appointments', sa.Column('patient_first_name', sa.String(length=100), nullable=False))
    op.add_column('appointments', sa.Column('patient_last_name', sa.String(length=100), nullable=False))

def downgrade():
    op.drop_column('appointments', 'doctor_first_name')
    op.drop_column('appointments', 'doctor_last_name')
    op.drop_column('appointments', 'patient_first_name')
    op.drop_column('appointments', 'patient_last_name')
