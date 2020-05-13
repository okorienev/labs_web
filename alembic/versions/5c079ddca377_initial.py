"""initial

Revision ID: 5c079ddca377
Revises: 
Create Date: 2020-05-11 16:26:42.524834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c079ddca377'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'group',
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('group_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'role',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=40), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('password', sa.String(length=100), nullable=True),
        sa.Column('role', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role'], ['role.role_id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'course',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('course_name', sa.String(length=50), nullable=False),
        sa.Column('course_shortened', sa.String(length=10), nullable=False),
        sa.Column('course_tutor', sa.Integer(), nullable=True),
        sa.Column('labs_amount', sa.Integer(), nullable=False),
        sa.Column('lab_max_score', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['course_tutor'], ['user.id'], ),
        sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table(
        'user_groups',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table(
        'group_courses',
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
        sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], )
    )
    op.create_table(
        'report',
        sa.Column('report_id', sa.Integer(), nullable=False),
        sa.Column('report_course', sa.Integer(), nullable=True),
        sa.Column('report_student', sa.Integer(), nullable=True),
        sa.Column('report_num', sa.Integer(), nullable=False),
        sa.Column('report_mark', sa.Integer(), nullable=True),
        sa.Column('report_uploaded', sa.DateTime(), nullable=False),
        sa.Column('report_checked', sa.DateTime(), nullable=True),
        sa.Column('report_stu_comment', sa.Text(), nullable=True),
        sa.Column('report_tut_comment', sa.Text(), nullable=True),
        sa.Column('report_hash', sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(['report_course'], ['course.course_id'], ),
        sa.ForeignKeyConstraint(['report_student'], ['user.id'], ),
        sa.PrimaryKeyConstraint('report_id')
    )


def downgrade():
    op.drop_table('report')
    op.drop_table('group_courses')
    op.drop_table('user_roles')
    op.drop_table('user_groups')
    op.drop_table('course')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('group')
