# Coding Convention & AI Collaboration Guide

> 고품질/유지보수/보안을 위한 인간-AI 협업 운영 지침서입니다.

---

## MVP 캡슐

| # | 항목 | 내용 |
|---|------|------|
| 1 | 목표 | 강사 효율 극대화 + 학생 자기주도 학습 환경 구축 |
| 2 | 페르소나 | 초등~고1 학생 (공통수학), 학원 강사/관리자 |
| 3 | 핵심 기능 | FEAT-1: 개념 테스트 (수학 개념 이해도 확인) |
| 4 | 성공 지표 (노스스타) | 강사 개별 확인 시간 50% 절감 |
| 5 | 입력 지표 | 주간 테스트 완료 학생 비율, 평균 정답률 향상 |
| 6 | 비기능 요구 | 응답 시간 < 500ms, 모바일/태블릿 반응형 지원 |
| 7 | Out-of-scope | AI 개인 맞춤 추천, 학부모 앱, 결제 시스템 |
| 8 | Top 리스크 | 학생들이 재미없어서 안 쓸 수 있음 |
| 9 | 완화/실험 | 듀오링고 스타일 게임화 요소 적용 |
| 10 | 다음 단계 | 개념 테스트 문제 DB 설계 |

---

## 1. 핵심 원칙

### 1.1 신뢰하되, 검증하라 (Don't Trust, Verify)

AI가 생성한 코드는 반드시 검증해야 합니다:

- [ ] **코드 리뷰**: 생성된 코드 직접 확인
- [ ] **테스트 실행**: 자동화 테스트 통과 확인
- [ ] **보안 검토**: 민감 정보 노출 여부 확인
- [ ] **동작 확인**: 실제로 실행하여 기대 동작 확인

### 1.2 최종 책임은 인간에게

- AI는 도구이고, 최종 결정과 책임은 개발자에게 있습니다
- 이해하지 못하는 코드는 사용하지 않습니다
- 의심스러운 부분은 반드시 질문합니다

---

## 2. 프로젝트 구조

### 2.1 디렉토리 구조

```
math-test/
├── frontend/
│   ├── src/
│   │   ├── components/        # 재사용 컴포넌트
│   │   │   ├── ui/           # 기본 UI (Button, Card, Input)
│   │   │   ├── test/         # 테스트 관련 (Question, Answer, Feedback)
│   │   │   └── gamification/ # 게임화 (Combo, LevelUp, Streak)
│   │   ├── pages/            # 페이지 컴포넌트
│   │   │   ├── student/      # 학생 페이지
│   │   │   └── teacher/      # 강사 페이지
│   │   ├── hooks/            # 커스텀 훅
│   │   ├── utils/            # 유틸리티 함수
│   │   ├── services/         # API 호출
│   │   ├── stores/           # Zustand 상태 관리
│   │   ├── types/            # TypeScript 타입
│   │   ├── mocks/            # MSW Mock 핸들러
│   │   └── __tests__/        # 단위 테스트
│   ├── e2e/                  # Playwright E2E 테스트
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/              # API 라우터
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── tests.py
│   │   │       ├── students.py
│   │   │       └── stats.py
│   │   ├── models/           # SQLAlchemy 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   ├── services/         # 비즈니스 로직
│   │   ├── core/             # 설정, 보안, DB
│   │   └── utils/            # 유틸리티
│   ├── tests/
│   │   ├── api/              # API 테스트
│   │   └── unit/             # 단위 테스트
│   ├── alembic/              # DB 마이그레이션
│   └── requirements.txt
│
├── contracts/                 # API 계약 (BE/FE 공유)
│   ├── types.ts
│   ├── auth.contract.ts
│   └── test.contract.ts
│
├── docs/
│   └── planning/             # 기획 문서 (소크라테스 산출물)
│       ├── 01-prd.md
│       ├── 02-trd.md
│       ├── 03-user-flow.md
│       ├── 04-database-design.md
│       ├── 05-design-system.md
│       ├── 06-tasks.md
│       └── 07-coding-convention.md
│
├── docker-compose.yml
└── README.md
```

### 2.2 네이밍 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| 파일 (컴포넌트) | PascalCase | `QuestionCard.tsx` |
| 파일 (훅) | camelCase + use 접두사 | `useTestAttempt.ts` |
| 파일 (유틸) | camelCase | `formatScore.ts` |
| 파일 (Python) | snake_case | `test_service.py` |
| 컴포넌트 | PascalCase | `QuestionCard` |
| 함수/변수 | camelCase | `getTestById` |
| Python 함수/변수 | snake_case | `get_test_by_id` |
| 상수 | UPPER_SNAKE | `MAX_COMBO_BONUS` |
| CSS 클래스 | Tailwind (유틸리티) | `bg-primary text-white` |
| 타입/인터페이스 | PascalCase | `TestAttempt` |
| 열거형 | PascalCase | `QuestionType` |

---

## 3. 아키텍처 원칙

### 3.1 뼈대 먼저 (Skeleton First)

1. 전체 구조를 먼저 잡고
2. 빈 함수/컴포넌트로 스켈레톤 생성
3. 하나씩 구현 채워나가기

### 3.2 작은 모듈로 분해

- 한 파일에 200줄 이하 권장
- 한 함수에 50줄 이하 권장
- 한 컴포넌트에 100줄 이하 권장

### 3.3 관심사 분리

**프론트엔드:**
| 레이어 | 역할 | 예시 |
|--------|------|------|
| UI (components) | 화면 표시 | `<QuestionCard />` |
| 상태 (stores) | 데이터 관리 | `useTestStore` |
| 서비스 (services) | API 통신 | `testApi.submit()` |
| 유틸 (utils) | 순수 함수 | `calculateScore()` |

**백엔드:**
| 레이어 | 역할 | 예시 |
|--------|------|------|
| API (routes) | HTTP 엔드포인트 | `@router.post("/submit")` |
| 서비스 (services) | 비즈니스 로직 | `TestService.grade()` |
| 모델 (models) | DB 스키마 | `TestAttempt` |
| 스키마 (schemas) | 요청/응답 검증 | `SubmitAnswerRequest` |

---

## 4. AI 소통 원칙

### 4.1 하나의 채팅 = 하나의 작업

- 한 번에 하나의 명확한 작업만 요청
- 작업 완료 후 다음 작업 진행
- 컨텍스트가 길어지면 새 대화 시작

### 4.2 컨텍스트 명시

**좋은 예:**
> "TASKS 문서의 T1.1을 구현해주세요.
> Database Design의 QUESTION 엔티티를 참조하고,
> TRD의 기술 스택(FastAPI + Pydantic)을 따라주세요."

**나쁜 예:**
> "문제 API 만들어줘"

### 4.3 기존 코드 재사용

- 새로 만들기 전에 기존 코드 확인 요청
- 중복 코드 방지
- 일관성 유지

### 4.4 프롬프트 템플릿

```
## 작업
{{무엇을 해야 하는지}}

## 참조 문서
- {{문서명}} 섹션 {{번호}}

## 제약 조건
- {{지켜야 할 것}}

## 예상 결과
- {{생성될 파일}}
- {{기대 동작}}
```

---

## 5. 코드 스타일

### 5.1 TypeScript (Frontend)

```typescript
// ✅ 좋은 예
interface QuestionCardProps {
  question: Question;
  onAnswer: (answer: string) => void;
  isSubmitting?: boolean;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  onAnswer,
  isSubmitting = false,
}) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);

  const handleSubmit = () => {
    if (selectedAnswer) {
      onAnswer(selectedAnswer);
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">{question.content}</h3>
      {question.options.map((option) => (
        <AnswerOption
          key={option.key}
          option={option}
          isSelected={selectedAnswer === option.key}
          onSelect={() => setSelectedAnswer(option.key)}
        />
      ))}
      <Button
        onClick={handleSubmit}
        disabled={!selectedAnswer || isSubmitting}
        className="mt-4 w-full"
      >
        {isSubmitting ? '제출 중...' : '제출하기'}
      </Button>
    </Card>
  );
};
```

### 5.2 Python (Backend)

```python
# ✅ 좋은 예
from uuid import UUID
from pydantic import BaseModel
from app.models import Question, TestAttempt
from app.schemas.test import SubmitAnswerRequest, AnswerResult


class TestService:
    def __init__(self, db: Session):
        self.db = db

    async def submit_answer(
        self,
        attempt_id: UUID,
        request: SubmitAnswerRequest,
    ) -> AnswerResult:
        """답안을 제출하고 채점 결과를 반환합니다."""
        attempt = await self._get_attempt(attempt_id)
        question = await self._get_question(request.question_id)

        is_correct = self._check_answer(question, request.answer)

        # 답안 기록 저장
        answer_log = AnswerLog(
            attempt_id=attempt_id,
            question_id=request.question_id,
            user_answer=request.answer,
            is_correct=is_correct,
        )
        self.db.add(answer_log)
        await self.db.commit()

        return AnswerResult(
            is_correct=is_correct,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
        )

    def _check_answer(self, question: Question, answer: str) -> bool:
        """정답 여부를 확인합니다."""
        return question.correct_answer.strip().lower() == answer.strip().lower()
```

### 5.3 Tailwind CSS

```tsx
// ✅ 좋은 예: 일관된 Tailwind 클래스 순서
// 1. 레이아웃 (flex, grid)
// 2. 위치 (position, z-index)
// 3. 박스 모델 (w, h, p, m)
// 4. 배경/테두리
// 5. 텍스트
// 6. 상태 (hover, focus)

<button
  className="
    flex items-center justify-center
    w-full h-12 px-6
    bg-primary rounded-xl
    text-white font-semibold
    hover:bg-primary-dark focus:ring-2 focus:ring-primary
    disabled:opacity-50 disabled:cursor-not-allowed
  "
>
  제출하기
</button>
```

---

## 6. 보안 체크리스트

### 6.1 절대 금지

- [ ] 비밀정보 하드코딩 금지 (API 키, 비밀번호, 토큰)
- [ ] .env 파일 커밋 금지
- [ ] SQL 직접 문자열 조합 금지 (SQL Injection)
- [ ] 사용자 입력 그대로 출력 금지 (XSS)
- [ ] JWT 시크릿 노출 금지

### 6.2 필수 적용

- [ ] 모든 사용자 입력 검증 (Pydantic 스키마)
- [ ] 비밀번호 해싱 (bcrypt)
- [ ] HTTPS 사용
- [ ] CORS 설정 (허용 도메인 명시)
- [ ] 인증된 요청만 민감 API 접근 (JWT 검증)
- [ ] 권한 확인 (학생은 본인 데이터만)

### 6.3 환경 변수 관리

```bash
# .env.example (커밋 O)
DATABASE_URL=postgresql://user:password@localhost:5432/mathtest
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# .env (커밋 X)
DATABASE_URL=postgresql://real:real@prod:5432/mathtest
JWT_SECRET=super-secret-key-12345
```

**.gitignore:**
```
.env
.env.local
.env.production
```

---

## 7. 테스트 워크플로우

### 7.1 즉시 실행 검증

코드 작성 후 바로 테스트:

```bash
# 백엔드
cd backend
pytest tests/ -v --cov=app --cov-report=term-missing

# 프론트엔드
cd frontend
npm run test

# E2E
npm run e2e
```

### 7.2 테스트 파일 명명

| 대상 | 패턴 | 예시 |
|------|------|------|
| Python 단위 테스트 | `test_*.py` | `test_test_service.py` |
| Python API 테스트 | `test_*.py` | `test_auth_api.py` |
| TypeScript 테스트 | `*.test.ts(x)` | `QuestionCard.test.tsx` |
| E2E 테스트 | `*.spec.ts` | `test-flow.spec.ts` |

### 7.3 오류 로그 공유 규칙

오류 발생 시 AI에게 전달할 정보:

1. 전체 에러 메시지
2. 관련 코드 스니펫
3. 재현 단계
4. 이미 시도한 해결책

**예시:**
```
## 에러
TypeError: Cannot read property 'id' of undefined

## 코드
const attemptId = currentAttempt.id;  // line 42

## 재현
1. 테스트 시작 버튼 클릭
2. /test/start 페이지 진입

## 시도한 것
- currentAttempt 로그 확인 → undefined
```

---

## 8. Git 워크플로우

### 8.1 브랜치 전략

```
main              # 프로덕션 배포
├── develop       # 개발 통합 (선택)
│   ├── feature/feat-0-auth
│   ├── feature/feat-1-test
│   ├── feature/feat-1-gamification
│   └── fix/login-error
```

### 8.2 커밋 메시지

```
<type>(<scope>): <subject>

<body>
```

**타입:**
| 타입 | 용도 |
|------|------|
| feat | 새 기능 |
| fix | 버그 수정 |
| refactor | 리팩토링 |
| docs | 문서 |
| test | 테스트 |
| style | 포맷팅 (세미콜론 등) |
| chore | 빌드, 설정 |

**예시:**
```
feat(test): 개념 테스트 채점 API 구현

- POST /api/v1/tests/{id}/submit 엔드포인트 추가
- 정답 체크 로직 구현
- AnswerLog 저장 기능 추가

TRD 섹션 8.2 구현 완료
```

### 8.3 PR 규칙

```markdown
## 변경 사항
- 개념 테스트 채점 API 구현

## 관련 문서
- TRD 섹션 8.2
- Database Design 2.4

## 테스트
- [x] pytest 통과
- [x] 커버리지 80% 이상

## 스크린샷 (UI 변경 시)
![screenshot](...)
```

---

## 9. 코드 품질 도구

### 9.1 프론트엔드

| 도구 | 용도 | 설정 파일 |
|------|------|----------|
| ESLint | 린팅 | `.eslintrc.cjs` |
| Prettier | 포맷팅 | `.prettierrc` |
| TypeScript | 타입 체크 | `tsconfig.json` |

**ESLint 설정:**
```javascript
// .eslintrc.cjs
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
  },
};
```

### 9.2 백엔드

| 도구 | 용도 | 설정 파일 |
|------|------|----------|
| Ruff | 린팅 + 포맷팅 | `ruff.toml` |
| mypy | 타입 체크 | `mypy.ini` |

**Ruff 설정:**
```toml
# ruff.toml
[lint]
select = ["E", "F", "W", "I", "N", "UP"]
ignore = ["E501"]  # line too long

[format]
quote-style = "double"
indent-style = "space"
```

### 9.3 Pre-commit 훅

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: frontend-lint
        name: Frontend Lint
        entry: npm run lint --prefix frontend
        language: system
        types: [typescript, tsx]

      - id: backend-lint
        name: Backend Lint
        entry: ruff check backend/
        language: system
        types: [python]

      - id: backend-format
        name: Backend Format
        entry: ruff format --check backend/
        language: system
        types: [python]
```

---

## 10. 명령어 치트시트

### 10.1 개발 서버

```bash
# 전체 실행 (Docker)
docker-compose up

# 프론트엔드만
cd frontend && npm run dev

# 백엔드만
cd backend && uvicorn app.main:app --reload
```

### 10.2 테스트

```bash
# 백엔드 전체 테스트
pytest

# 백엔드 특정 테스트
pytest tests/api/test_auth.py -v

# 프론트엔드 전체 테스트
npm run test

# 프론트엔드 워치 모드
npm run test -- --watch

# E2E 테스트
npm run e2e

# E2E 디버그 모드
npm run e2e -- --debug
```

### 10.3 품질 검사

```bash
# 프론트엔드
npm run lint
npm run lint:fix
npm run type-check

# 백엔드
ruff check .
ruff format .
mypy app/
```

### 10.4 DB 마이그레이션

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "Add question table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

---

## Decision Log 참조

| ID | 항목 | 선택 | 근거 | 영향 |
|----|------|------|------|------|
| D-20 | 상태관리 | Zustand | 가벼움, 보일러플레이트 적음 | Redux 대신 사용 |
| D-21 | 린터 | Ruff | 빠름, all-in-one | Flake8+Black 대체 |
| D-22 | E2E | Playwright | 크로스 브라우저, 안정성 | Cypress 대신 사용 |
| D-23 | Mock | MSW | 네트워크 레벨 모킹 | jest.mock 대신 사용 |
