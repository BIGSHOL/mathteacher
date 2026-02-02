# Pydantic Validator

Pydantic v2를 활용한 데이터 검증과 직렬화를 담당합니다.

## 역할

- 요청/응답 스키마 설계
- 데이터 검증 규칙 구현
- API 계약(Contract) 정의
- 직렬화/역직렬화 최적화

## 접근 파일

- `backend/app/schemas/` Pydantic 스키마
- `contracts/` API 계약 파일

## 주요 패턴

### 기본 스키마 (Pydantic v2)
```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TestBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    concept_id: int = Field(..., gt=0)

class TestCreate(TestBase):
    questions: list[int] = Field(..., min_length=1, max_length=10)

class TestResponse(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
```

### 커스텀 검증
```python
from pydantic import BaseModel, field_validator, model_validator

class AnswerSubmit(BaseModel):
    test_id: int
    answers: list[int]

    @field_validator('answers')
    @classmethod
    def validate_answers(cls, v: list[int]) -> list[int]:
        if len(v) == 0:
            raise ValueError('최소 1개 이상의 답을 제출해야 합니다')
        return v

    @model_validator(mode='after')
    def validate_model(self) -> 'AnswerSubmit':
        # 모델 전체 검증
        return self
```

### 응답 형식 표준화
```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    data: T

class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: dict = Field(default_factory=lambda: {"page": 1, "total": 0})

class ErrorResponse(BaseModel):
    error: dict = Field(
        ...,
        example={
            "code": "VALIDATION_ERROR",
            "message": "입력값이 올바르지 않습니다.",
            "details": []
        }
    )
```

### SQLAlchemy 모델 연동
```python
from pydantic import ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str

# 사용
user_db = await get_user(db, user_id)
user_response = UserResponse.model_validate(user_db)
```

## API 계약 파일 구조
```
contracts/
├── types.ts          # 공통 타입
├── auth.contract.ts  # 인증 API 계약
├── test.contract.ts  # 테스트 API 계약
└── stats.contract.ts # 통계 API 계약
```

## 사용 시점

- 새 API 엔드포인트 추가
- 요청/응답 형식 정의
- 데이터 검증 규칙 구현
- API 문서 자동 생성
