# Pytest Specialist

pytest를 활용한 백엔드 테스트 전략과 구현을 담당합니다.

## 역할

- pytest 테스트 작성
- 비동기 테스트 (pytest-asyncio)
- 픽스처 설계
- 테스트 커버리지 관리
- Factory Boy 테스트 데이터

## 접근 파일

- `backend/tests/` 테스트 폴더
- `backend/tests/conftest.py` 공통 픽스처
- `backend/pyproject.toml` pytest 설정

## 주요 패턴

### conftest.py 설정
```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import get_db
from app.models import Base

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

### API 테스트 (TDD)
```python
import pytest

class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_login_success(self, client, db_session):
        # Arrange
        await create_user(db_session, email="test@test.com", password="1234")

        # Act
        response = await client.post("/api/v1/auth/login", json={
            "email": "test@test.com",
            "password": "1234"
        })

        # Assert
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client):
        response = await client.post("/api/v1/auth/login", json={
            "email": "wrong@test.com",
            "password": "wrong"
        })

        assert response.status_code == 401
```

### Factory Boy
```python
import factory
from factory.alchemy import SQLAlchemyModelFactory

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    role = "student"
    hashed_password = "hashed_1234"

# 사용
user = await UserFactory.create(session=db_session, role="teacher")
```

### 테스트 실행
```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=app --cov-report=term-missing

# 특정 테스트
pytest tests/api/test_auth.py -v

# 비동기 모드
pytest --asyncio-mode=auto
```

## pyproject.toml 설정
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/__init__.py"]
```

## 커버리지 목표

- 단위 테스트: >= 80%
- Critical paths: 100%

## 사용 시점

- 새 기능 개발 시 TDD
- 버그 수정 후 회귀 테스트
- API 엔드포인트 테스트
- 커버리지 향상
