# Math Test - 수학 개념 및 연산 테스트 프로그램

선생님 업무를 대신해 학생들이 랩실 등의 강의실에서 스스로 개념테스트와 연산테스트를 할 수 있는 학습 도구입니다.

## Features

- **개념 테스트**: 수학 개념 이해도 확인
- **즉시 채점**: 문제 풀이 후 바로 정답/오답 확인
- **게임화**: 듀오링고 스타일 (레벨업, 콤보, 스트릭)
- **학습 통계**: 학생별 취약점 파악 및 수준별 맞춤 학습

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React + Vite, TypeScript, TailwindCSS, Zustand
- **Testing**: pytest, Vitest, Playwright

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Quick Start (Docker)

```bash
# 1. Clone and setup
cp .env.example .env

# 2. Start all services
docker-compose up -d

# 3. Access
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
math-test/
├── frontend/           # React + Vite
│   ├── src/
│   │   ├── components/ # UI Components
│   │   ├── pages/      # Page Components
│   │   ├── hooks/      # Custom Hooks
│   │   ├── services/   # API Calls
│   │   ├── stores/     # Zustand Stores
│   │   └── mocks/      # MSW Mocks
│   └── e2e/            # Playwright Tests
├── backend/            # FastAPI
│   ├── app/
│   │   ├── api/        # API Routes
│   │   ├── models/     # SQLAlchemy Models
│   │   ├── schemas/    # Pydantic Schemas
│   │   └── services/   # Business Logic
│   └── tests/          # pytest Tests
├── contracts/          # API Contracts (shared types)
└── docs/planning/      # Planning Documents
```

## Documentation

- [PRD](docs/planning/01-prd.md) - 제품 요구사항
- [TRD](docs/planning/02-trd.md) - 기술 요구사항
- [User Flow](docs/planning/03-user-flow.md) - 사용자 흐름도
- [Database Design](docs/planning/04-database-design.md) - DB 설계
- [Design System](docs/planning/05-design-system.md) - 디자인 시스템
- [Tasks](docs/planning/06-tasks.md) - 개발 태스크
- [Coding Convention](docs/planning/07-coding-convention.md) - 코딩 컨벤션

## Testing

```bash
# Backend
cd backend
pytest --cov=app

# Frontend
cd frontend
npm run test

# E2E
npm run e2e
```

## License

Private - 학원 내부 전용
