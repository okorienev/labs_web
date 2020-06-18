"""Add file table

Revision ID: 97eed6784f4d
Revises: 9e85acdcfe8e
Create Date: 2020-06-18 14:36:39.234873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97eed6784f4d'
down_revision = '9e85acdcfe8e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'file',
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('bucket', sa.String(length=32), nullable=False),
        sa.Column('key', sa.String(length=64), nullable=False),
        sa.Column('file_name', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('file_owner_id_fkey')),
        sa.PrimaryKeyConstraint('file_id', name=op.f('file_pkey'))
    )


def downgrade():
    op.drop_table('file')
