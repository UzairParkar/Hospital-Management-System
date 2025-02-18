"""Creating the necessary Tables

Revision ID: 2756ab89d81b
Revises: 
Create Date: 2025-02-17 18:21:30.420261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2756ab89d81b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table(
        'staff',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), unique=True, nullable=False),
        sa.Column('_password', sa.String(length=300), nullable=False),
        sa.Column('role', sa.String(length=60), nullable=False, default='staff'),
    )

    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=30), nullable=True),
        sa.Column('contact', sa.String(length=11), nullable=False),
        sa.Column('email', sa.String(length=29), unique=True, nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=30), nullable=False),
        sa.Column('blood_group', sa.String(length=12), nullable=True),
        sa.Column('medical_history', sa.Text(), nullable=True),
    )


    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=30), nullable=True),
        sa.Column('specs', sa.String(length=100), nullable=True),
        sa.Column('contact', sa.String(length=100), nullable=True),
        sa.Column('from_time', sa.Time(), nullable=False),
        sa.Column('to_time', sa.Time(), nullable=False),
    )


    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patients.id'), nullable=False),
        sa.Column('doctor_id', sa.Integer(), sa.ForeignKey('doctors.id'), nullable=False),
        sa.Column('a_date', sa.Date(), nullable=False),
        sa.Column('a_time', sa.Time(), nullable=False),
    )

def downgrade():
    op.drop_table('appointments')
    op.drop_table('doctors')
    op.drop_table('patients')
    op.drop_table('staff')