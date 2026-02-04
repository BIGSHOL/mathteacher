"""add daily_test_records table

Revision ID: a1b2c3d4e5f6
Revises: df2e75c68cb6
Create Date: 2026-02-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'df2e75c68cb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'daily_test_records',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('student_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('date', sa.String(10), nullable=False, index=True, comment='YYYY-MM-DD (KST)'),
        sa.Column('category', sa.String(20), nullable=False, index=True, comment='concept | computation | fill_in_blank'),
        sa.Column('test_id', sa.String(36), sa.ForeignKey('tests.id'), nullable=False),
        sa.Column('attempt_id', sa.String(36), sa.ForeignKey('test_attempts.id'), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending', comment='pending | in_progress | completed'),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('max_score', sa.Integer(), nullable=True),
        sa.Column('correct_count', sa.Integer(), nullable=True),
        sa.Column('total_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('student_id', 'date', 'category', name='uix_student_date_category'),
    )


def downgrade() -> None:
    op.drop_table('daily_test_records')
