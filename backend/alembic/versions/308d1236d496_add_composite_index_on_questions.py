"""add composite index on questions

Revision ID: 308d1236d496
Revises: a1b2c3d4e5f6
Create Date: 2026-02-04 23:38:22.333481

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '308d1236d496'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_questions_is_active', 'questions', ['is_active'])
    op.create_index(
        'ix_question_concept_type_diff_active',
        'questions',
        ['concept_id', 'question_type', 'difficulty', 'is_active'],
    )


def downgrade() -> None:
    op.drop_index('ix_question_concept_type_diff_active', table_name='questions')
    op.drop_index('ix_questions_is_active', table_name='questions')
