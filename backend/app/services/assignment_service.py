"""과제 서비스."""

from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate


class AssignmentService:
    """과제 관리 서비스."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_assignments(
        self,
        student_id: str,
        include_completed: bool = True,
        limit: int = 50,
    ) -> list[Assignment]:
        """학생의 과제 목록 조회."""
        stmt = select(Assignment).where(Assignment.student_id == student_id)
        
        if not include_completed:
            stmt = stmt.where(Assignment.is_completed == False)  # noqa: E712
            
        stmt = stmt.order_by(Assignment.created_at.desc()).limit(limit)
        return list((await self.db.scalars(stmt)).all())

    async def create_assignment(self, data: AssignmentCreate) -> Assignment:
        """과제 생성."""
        assignment = Assignment(
            student_id=data.student_id,
            assignment_type=data.assignment_type,
            reference_id=data.reference_id,
            title=data.title,
            description=data.description,
            due_date=data.due_date,
        )
        self.db.add(assignment)
        await self.db.commit()
        await self.db.refresh(assignment)
        return assignment

    async def update_assignment(
        self, assignment_id: str, data: AssignmentUpdate
    ) -> Assignment | None:
        """과제 수정."""
        assignment = await self.db.get(Assignment, assignment_id)
        if not assignment:
            return None

        update_dict = data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(assignment, field, value)
            
        if data.is_completed is not None:
             if data.is_completed and not assignment.completed_at:
                 assignment.completed_at = datetime.now(timezone.utc)
             elif not data.is_completed:
                 assignment.completed_at = None

        await self.db.commit()
        await self.db.refresh(assignment)
        return assignment

    async def delete_assignment(self, assignment_id: str) -> bool:
        """과제 삭제."""
        assignment = await self.db.get(Assignment, assignment_id)
        if not assignment:
            return False

        await self.db.delete(assignment)
        await self.db.commit()
        return True
