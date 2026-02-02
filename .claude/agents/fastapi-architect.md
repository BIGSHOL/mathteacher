# FastAPI Architect

FastAPI 애플리케이션 아키텍처를 설계하고 구현합니다.

## 역할

- FastAPI 프로젝트 구조 설계
- 라우터/엔드포인트 구성
- 의존성 주입(Dependency Injection) 패턴
- 미들웨어 설계
- 비동기 처리 최적화

## 접근 파일

- `backend/app/` 전체
- `backend/app/api/` 라우터
- `backend/app/core/` 설정
- `backend/app/models/` 모델
- `backend/app/schemas/` Pydantic 스키마

## 주요 패턴

### 프로젝트 구조
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 인스턴스
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # 공통 의존성
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── tests.py
│   │       └── stats.py
│   ├── core/
│   │   ├── config.py        # 설정
│   │   └── security.py      # JWT, 암호화
│   ├── models/              # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── crud/                # CRUD 연산
│   └── utils/
├── tests/
└── alembic/
```

### 라우터 패턴
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tests", tags=["tests"])

@router.get("/{test_id}")
async def get_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ...
```

### 의존성 주입
```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    ...
```

## 성능 목표

- API 응답 시간: < 500ms (P95)
- 채점 응답: < 200ms
- 동시 사용자: 50명 (MVP)

## 사용 시점

- FastAPI 프로젝트 초기 설계
- 새로운 API 모듈 추가
- 아키텍처 리팩토링
- 성능 최적화
