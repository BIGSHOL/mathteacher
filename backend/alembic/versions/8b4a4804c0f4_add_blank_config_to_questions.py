"""add blank_config to questions

Revision ID: 8b4a4804c0f4
Revises: 
Create Date: 2026-02-03 20:29:00.736954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8b4a4804c0f4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add blank_config column to questions table
    op.add_column(
        'questions',
        sa.Column(
            'blank_config',
            postgresql.JSON(astext_type=sa.Text()),
            nullable=True,
            comment='빈칸 채우기 설정: 빈칸 가능 위치, 중요도, 회차별 규칙'
        )
    )

    # Add FILL_IN_BLANK to QuestionType enum if not exists
    op.execute("ALTER TYPE questiontype ADD VALUE IF NOT EXISTS 'FILL_IN_BLANK'")


def downgrade() -> None:
    # Remove blank_config column
    op.drop_column('questions', 'blank_config')

    # Note: Cannot easily remove enum value in PostgreSQL
    # Manual intervention required if downgrading
