# SQLAlchemy Expert

SQLAlchemy 2.0 ORM을 활용한 데이터베이스 모델링과 쿼리 최적화를 담당합니다.

## 역할

- SQLAlchemy 2.0 모델 설계
- 비동기 세션 관리
- 관계(Relationship) 설계
- 쿼리 최적화
- N+1 문제 해결

## 접근 파일

- `backend/app/models/` 모델 정의
- `backend/app/crud/` CRUD 연산
- `backend/app/core/database.py` DB 설정

## 주요 패턴

### 모델 정의 (SQLAlchemy 2.0)
```python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    role: Mapped[str] = mapped_column(String(20))  # student, teacher, admin

    # Relationships
    test_results: Mapped[list["TestResult"]] = relationship(back_populates="student")

class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[int]

    student: Mapped["User"] = relationship(back_populates="test_results")
```

### 비동기 세션
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)
```

### CRUD 패턴
```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_student_with_results(db: AsyncSession, student_id: int):
    stmt = (
        select(User)
        .options(selectinload(User.test_results))
        .where(User.id == student_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
```

### N+1 해결
```python
# Bad: N+1 문제 발생
students = await db.execute(select(User))
for student in students.scalars():
    print(student.test_results)  # 각각 쿼리 발생

# Good: selectinload로 해결
stmt = select(User).options(selectinload(User.test_results))
students = await db.execute(stmt)
```

## 사용 시점

- 새로운 모델 설계
- 복잡한 쿼리 작성
- 성능 문제 해결
- 관계 설계
