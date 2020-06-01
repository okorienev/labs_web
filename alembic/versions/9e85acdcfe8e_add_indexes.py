"""add_indexes

Revision ID: 9e85acdcfe8e
Revises: 5c079ddca377
Create Date: 2020-06-01 17:18:33.532370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e85acdcfe8e'
down_revision = '5c079ddca377'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('course_course_tutor_idx'), 'course', ['course_tutor'], unique=False)
    op.create_index(op.f('report_report_course_idx'), 'report', ['report_course'], unique=False)
    op.create_index(op.f('report_report_student_idx'), 'report', ['report_student'], unique=False)
    op.drop_constraint('user_email_key', 'user', type_='unique')


def downgrade():
    op.drop_index(op.f('user_email_idx'), table_name='user')
    op.drop_index(op.f('report_report_student_idx'), table_name='report')
    op.drop_index(op.f('report_report_course_idx'), table_name='report')
    op.drop_index(op.f('course_course_tutor_idx'), table_name='course')
