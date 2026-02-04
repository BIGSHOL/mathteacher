"""add_question_reports_table

Revision ID: 8577adedf933
Revises: 308d1236d496
Create Date: 2026-02-05 01:01:03.717758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect as sa_inspect


# revision identifiers, used by Alembic.
revision: str = '8577adedf933'
down_revision: Union[str, None] = '308d1236d496'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa_inspect(bind)
    return table_name in inspector.get_table_names()


def _index_exists(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa_inspect(bind)
    indexes = inspector.get_indexes(table_name)
    return any(idx["name"] == index_name for idx in indexes)


def upgrade() -> None:
    # question_reports 테이블 (create_all로 이미 존재할 수 있음)
    if not _table_exists("question_reports"):
        op.create_table(
            "question_reports",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("question_id", sa.String(36), sa.ForeignKey("questions.id"), nullable=False),
            sa.Column("reporter_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("report_type", sa.Enum("wrong_answer", "wrong_options", "question_error", "other", name="reporttype"), nullable=False),
            sa.Column("comment", sa.Text(), nullable=False),
            sa.Column("status", sa.Enum("pending", "resolved", "dismissed", name="reportstatus"), nullable=False, server_default="pending"),
            sa.Column("admin_response", sa.Text(), nullable=True),
            sa.Column("resolved_by", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
            sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        )
        op.create_index("ix_question_reports_question_id", "question_reports", ["question_id"])
        op.create_index("ix_question_reports_reporter_id", "question_reports", ["reporter_id"])
        op.create_index("ix_question_reports_report_type", "question_reports", ["report_type"])
        op.create_index("ix_question_reports_status", "question_reports", ["status"])

    # 추가 인덱스 (다른 테이블)
    if not _index_exists("concepts", "ix_concept_grade_name"):
        op.create_index("ix_concept_grade_name", "concepts", ["grade", "name"])
    if not _index_exists("daily_test_records", "ix_daily_test_student_date"):
        op.create_index("ix_daily_test_student_date", "daily_test_records", ["student_id", "date"])
    if not _index_exists("questions", "ix_question_active_created"):
        op.create_index("ix_question_active_created", "questions", ["is_active", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_question_active_created", table_name="questions")
    op.drop_index("ix_daily_test_student_date", table_name="daily_test_records")
    op.drop_index("ix_concept_grade_name", table_name="concepts")
    op.drop_table("question_reports")
