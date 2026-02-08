"""과제 스키마."""

from datetime import datetime

from pydantic import BaseModel, Field


class AssignmentBase(BaseModel):
    """과제 기본 스키마."""
    
    assignment_type: str = Field(..., description="chapter, review, custom")
    reference_id: str | None = None
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    due_date: datetime | None = None


class AssignmentCreate(AssignmentBase):
    """과제 생성 스키마."""
    
    student_id: str


class AssignmentUpdate(BaseModel):
    """과제 수정 스키마."""
    
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None


class AssignmentResponse(AssignmentBase):
    """과제 응답 스키마."""
    
    id: str
    student_id: str
    is_completed: bool
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
