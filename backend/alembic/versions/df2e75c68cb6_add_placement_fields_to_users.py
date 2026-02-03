"""add placement fields to users

Revision ID: df2e75c68cb6
Revises: 8b4a4804c0f4
Create Date: 2026-02-03 20:46:20.898235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'df2e75c68cb6'
down_revision: Union[str, None] = '8b4a4804c0f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add placement-related fields to users table
    op.add_column(
        'users',
        sa.Column(
            'has_completed_placement',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment='진단 평가 완료 여부'
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'placement_test_id',
            sa.String(36),
            nullable=True,
            comment='완료한 진단 평가 시도 ID'
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'placement_result',
            postgresql.JSON(astext_type=sa.Text()),
            nullable=True,
            comment='진단 평가 결과 (시작 단원, 레벨 등)'
        )
    )


def downgrade() -> None:
    # Remove placement fields
    op.drop_column('users', 'placement_result')
    op.drop_column('users', 'placement_test_id')
    op.drop_column('users', 'has_completed_placement')
