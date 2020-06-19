"""add_file_type_field

Revision ID: 2bce4b7bf8a2
Revises: 97eed6784f4d
Create Date: 2020-06-18 20:19:08.033898

"""
from alembic import op
import sqlalchemy as sa


revision = '2bce4b7bf8a2'
down_revision = '97eed6784f4d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('file', sa.Column('file_type', sa.SmallInteger(), nullable=False))


def downgrade():
    op.drop_column('file', 'file_type')
