# Math Test - 명령어 레퍼런스

> 백엔드(FastAPI/Python) 및 프론트엔드(React/Vite) 전체 명령어 가이드

---

## 목차

1. [빠른 시작](#빠른-시작)
2. [Docker 명령어](#docker-명령어)
3. [프론트엔드 명령어](#프론트엔드-명령어)
4. [백엔드 명령어](#백엔드-명령어)
5. [데이터베이스 명령어](#데이터베이스-명령어)
6. [환경 변수](#환경-변수)
7. [배포](#배포)

---

## 빠른 시작

### Docker로 한 번에 실행 (권장)

```bash
cp .env.example .env          # 환경변수 파일 복사 후 편집
docker-compose up -d           # 전체 서비스 백그라운드 실행
```

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | http://localhost:5173 |
| 백엔드 API | http://localhost:8000 |
| API 문서 (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

### 로컬 개발 (수동 실행)

```powershell
# 터미널 1: 백엔드
cd backend
python -m venv venv              # 가상환경 생성 (최초 1회)
.\venv\Scripts\Activate.ps1      # 가상환경 활성화 (PowerShell)
pip install -r requirements.txt  # 패키지 설치 (최초 1회)
uvicorn app.main:app --reload    # 서버 실행
```

```bash
# 터미널 2: 프론트엔드
cd frontend
npm install                      # 패키지 설치 (최초 1회)
npm run dev                      # 서버 실행
```

> **PowerShell 보안 오류 시:** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 실행 후 재시도
>
> **CMD 사용 시:** `.\venv\Scripts\Activate.ps1` 대신 `venv\Scripts\activate.bat` 사용

---

## Docker 명령어

### 서비스 실행/중지

| 명령어 | 설명 |
|--------|------|
| `docker-compose up` | 전체 서비스 실행 (로그 표시) |
| `docker-compose up -d` | 전체 서비스 백그라운드 실행 |
| `docker-compose down` | 전체 서비스 중지 |
| `docker-compose down -v` | 전체 서비스 중지 + 볼륨 삭제 (DB 초기화) |

### 개별 서비스 관리

| 명령어 | 설명 |
|--------|------|
| `docker-compose up db` | DB만 실행 |
| `docker-compose up backend` | 백엔드만 실행 (DB 자동 포함) |
| `docker-compose up frontend` | 프론트엔드만 실행 (백엔드 자동 포함) |
| `docker-compose restart backend` | 백엔드 재시작 |

### 로그 확인

| 명령어 | 설명 |
|--------|------|
| `docker-compose logs -f` | 전체 로그 실시간 확인 |
| `docker-compose logs -f backend` | 백엔드 로그만 확인 |
| `docker-compose logs -f frontend` | 프론트엔드 로그만 확인 |
| `docker-compose logs -f db` | DB 로그만 확인 |

---

## 프론트엔드 명령어

> 실행 위치: `frontend/`

### 개발 & 빌드

| 명령어 | 설명 |
|--------|------|
| `npm run dev` | 개발 서버 실행 (http://localhost:5173) |
| `npm run build` | 프로덕션 빌드 (TypeScript 컴파일 + Vite 번들링) |
| `npm run preview` | 프로덕션 빌드 미리보기 |

### 코드 품질

| 명령어 | 설명 |
|--------|------|
| `npm run lint` | ESLint 코드 검사 |
| `npm run lint:fix` | ESLint 자동 수정 |
| `npm run format` | Prettier 코드 포맷팅 (`src/**/*.{ts,tsx,css,json}`) |

### 테스트

| 명령어 | 설명 |
|--------|------|
| `npm run test` | Vitest 단위 테스트 실행 (watch 모드) |
| `npm run test:ui` | Vitest UI 대시보드로 테스트 실행 |
| `npm run test:coverage` | 테스트 커버리지 리포트 생성 |

### 의존성 관리

| 명령어 | 설명 |
|--------|------|
| `npm install` | 전체 패키지 설치 |
| `npm install <패키지명>` | 프로덕션 패키지 추가 |
| `npm install -D <패키지명>` | 개발 패키지 추가 |
| `npm update` | 패키지 업데이트 |
| `npm outdated` | 업데이트 가능한 패키지 확인 |

### 주요 기술 스택

| 패키지 | 버전 | 용도 |
|--------|------|------|
| React | 18.3.1 | UI 프레임워크 |
| Vite | 5.4.10 | 빌드 도구 |
| TypeScript | 5.6.2 | 타입 시스템 |
| TailwindCSS | 3.4.14 | 스타일링 |
| Zustand | 5.0.0 | 상태 관리 |
| Axios | 1.7.7 | HTTP 클라이언트 |
| React Router | 6.28.0 | 라우팅 |
| Framer Motion | 11.11.0 | 애니메이션 |

---

## 백엔드 명령어

> 실행 위치: `backend/`
> Python 3.11 이상 필요
> **모든 명령어는 가상환경 활성화 후 실행**

### 가상환경 설정 (최초 1회)

```powershell
python -m venv venv              # 가상환경 생성
.\venv\Scripts\Activate.ps1      # 활성화 (PowerShell)
pip install -r requirements.txt  # 패키지 설치
```

| 셸 | 활성화 명령어 |
|----|--------------|
| PowerShell | `.\venv\Scripts\Activate.ps1` |
| CMD | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

> 터미널을 새로 열 때마다 가상환경 활성화가 필요합니다.
> 활성화되면 프롬프트 앞에 `(venv)`가 표시됩니다.

### 서버 실행

| 명령어 | 설명 |
|--------|------|
| `uvicorn app.main:app --reload` | 개발 서버 실행 (핫 리로드, http://localhost:8000) |
| `uvicorn app.main:app --host 0.0.0.0 --port 8000` | 프로덕션 서버 실행 |

### 코드 품질

| 명령어 | 설명 |
|--------|------|
| `ruff check .` | Ruff 린트 검사 |
| `ruff check . --fix` | Ruff 린트 자동 수정 |
| `ruff format .` | Ruff 코드 포맷팅 |
| `mypy app/` | 타입 체크 (Pydantic 플러그인 포함) |

### 테스트

| 명령어 | 설명 |
|--------|------|
| `pytest` | 전체 테스트 실행 (커버리지 포함) |
| `pytest tests/` | tests 디렉토리 테스트 실행 |
| `pytest tests/test_health.py` | 특정 파일 테스트 실행 |
| `pytest -k "test_login"` | 이름으로 테스트 필터링 |
| `pytest --cov=app --cov-report=html` | HTML 커버리지 리포트 생성 |

> pytest 기본 설정 (`pyproject.toml`): `-v --cov=app --cov-report=term-missing`, asyncio_mode=auto

### 시드 데이터

| 명령어 | 설명 |
|--------|------|
| `python -m app.scripts.seed_all` | 전체 시드 데이터 삽입 |
| `python -m app.scripts.seed_all --clear` | 기존 데이터 삭제 후 재삽입 |
| `python -m app.scripts.seed_all --dry-run` | 삽입 없이 유효성 검증만 실행 |
| `python -m app.scripts.seed_all --grade elementary_5` | 특정 학년만 시드 |

### AI 시드 생성

| 명령어 | 설명 |
|--------|------|
| `python -m app.scripts.generate_seeds --guide <가이드파일> --grade <학년> --output <출력경로>` | Gemini API로 시드 데이터 자동 생성 |

> `GEMINI_API_KEY` 환경변수 필요

### 의존성 관리

| 명령어 | 설명 |
|--------|------|
| `pip install -r requirements.txt` | 전체 패키지 설치 |
| `pip install <패키지명>` | 패키지 추가 |
| `pip freeze > requirements.txt` | requirements.txt 갱신 |

### 주요 기술 스택

| 패키지 | 용도 |
|--------|------|
| FastAPI | API 프레임워크 |
| SQLAlchemy (async) | ORM |
| PostgreSQL (asyncpg) | 데이터베이스 |
| Pydantic | 데이터 검증 |
| python-jose | JWT 인증 |
| Alembic | DB 마이그레이션 |
| google-genai | AI 문제 생성 |
| slowapi | Rate Limiting |

---

## 데이터베이스 명령어

### Alembic 마이그레이션

| 명령어 | 설명 |
|--------|------|
| `alembic current` | 현재 마이그레이션 상태 확인 |
| `alembic upgrade head` | 최신 마이그레이션까지 적용 |
| `alembic downgrade -1` | 마이그레이션 1단계 롤백 |
| `alembic downgrade base` | 전체 마이그레이션 롤백 |
| `alembic revision --autogenerate -m "설명"` | 새 마이그레이션 자동 생성 |
| `alembic history` | 마이그레이션 이력 확인 |

### PostgreSQL 직접 접속 (Docker)

```bash
docker exec -it mathtest-db psql -U postgres -d mathtest
```

### 기본 계정 (자동 생성)

앱 최초 실행 시 아래 테스트 계정이 자동 생성됩니다:

| 역할 | 로그인 ID | 비고 |
|------|-----------|------|
| 마스터 관리자 | `master01` | 최고 권한 |
| 관리자 | `admin01` | 관리 권한 |
| 교사 | `teacher01` | 교사 권한 |
| 학생 | `student01` | 학생 권한 |

---

## 환경 변수

### 루트 `.env`

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mathtest
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mathtest
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
VITE_API_URL=http://localhost:8000/api/v1
```

### 백엔드 `backend/.env`

| 변수 | 필수 | 설명 |
|------|------|------|
| `ENV` | O | 환경 (`development` / `production`) |
| `DATABASE_URL` | O | PostgreSQL 연결 문자열 |
| `JWT_SECRET` | O | JWT 서명 키 (32자 이상) |
| `BACKEND_CORS_ORIGINS` | O | CORS 허용 도메인 (JSON 배열) |
| `GEMINI_API_KEY` | - | AI 기능 사용 시 필요 |

### 프론트엔드 `frontend/.env`

| 변수 | 필수 | 설명 |
|------|------|------|
| `VITE_API_URL` | O | 백엔드 API 기본 URL |

---

## 배포

### 백엔드 - Railway

```bash
# Railway CLI 사용 시
railway login
railway link
railway up
```

필수 환경변수 설정:
- `ENV=production`
- `DATABASE_URL` (Supabase 연결 문자열)
- `JWT_SECRET` (`openssl rand -hex 32`로 생성)
- `BACKEND_CORS_ORIGINS` (Vercel 도메인 포함)

### 프론트엔드 - Vercel

1. GitHub 레포 연결
2. Root Directory: `frontend` 지정
3. 환경변수 추가: `VITE_API_URL` = Railway 백엔드 URL
4. 배포

---

## Git 명령어 참고

| 명령어 | 설명 |
|--------|------|
| `git status` | 변경사항 확인 |
| `git add .` | 전체 스테이징 |
| `git commit -m "메시지"` | 커밋 |
| `git push origin master` | 원격 푸시 |
| `git pull origin master` | 원격 변경사항 가져오기 |