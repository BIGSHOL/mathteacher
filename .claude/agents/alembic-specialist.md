# Alembic Specialist

Alembic을 활용한 데이터베이스 마이그레이션을 관리합니다.

## 역할

- 마이그레이션 스크립트 생성
- 스키마 버전 관리
- 안전한 마이그레이션 전략
- 롤백 계획 수립
- 데이터 마이그레이션

## 접근 파일

- `backend/alembic/` 마이그레이션 폴더
- `backend/alembic.ini` 설정
- `backend/alembic/env.py` 환경 설정
- `backend/alembic/versions/` 마이그레이션 스크립트

## 주요 명령어

```bash
# 마이그레이션 생성 (자동)
alembic revision --autogenerate -m "add_test_results_table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1

# 현재 버전 확인
alembic current

# 마이그레이션 히스토리
alembic history
```

## 주요 패턴

### 비동기 env.py 설정
```python
from sqlalchemy.ext.asyncio import async_engine_from_config

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
```

### 안전한 마이그레이션 스크립트
```python
def upgrade() -> None:
    # 1. 새 컬럼 추가 (nullable)
    op.add_column('users', sa.Column('grade', sa.Integer(), nullable=True))

    # 2. 기존 데이터 업데이트
    op.execute("UPDATE users SET grade = 1 WHERE grade IS NULL")

    # 3. NOT NULL 제약 추가
    op.alter_column('users', 'grade', nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'grade')
```

### 데이터 마이그레이션
```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # 테이블 생성
    op.create_table(
        'concepts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('grade_level', sa.Integer(), nullable=False),
    )

    # 초기 데이터 삽입
    op.bulk_insert(
        sa.table('concepts',
            sa.column('name', sa.String),
            sa.column('grade_level', sa.Integer),
        ),
        [
            {'name': '분수', 'grade_level': 5},
            {'name': '방정식', 'grade_level': 7},
        ]
    )
```

## 마이그레이션 체크리스트

- [ ] 마이그레이션 전 백업 확인
- [ ] downgrade 함수 테스트
- [ ] 스테이징 환경에서 먼저 실행
- [ ] 롤백 계획 수립
- [ ] 데이터 무결성 검증

## 사용 시점

- 스키마 변경 필요 시
- 새 테이블/컬럼 추가
- 인덱스 추가/변경
- 데이터 마이그레이션
