# Claude Code Agent System

> **Project**: math-test (수학 테스트 앱)
> **Updated**: 2026-02-02
> **Structure**: 11 Teams, 62 Agents + 1 Director Command

---

## Architecture

```
refactor (Director Command, opus model)
|
|-- Frontend Team (frontend-lead) .......... 6 agents
|-- Backend Team (backend-lead) ............ 7 agents
|-- Database Team (database-lead) .......... 6 agents
|-- Test Team (test-lead) .................. 7 agents
|-- Review Team (review-lead) .............. 6 agents
|-- Security Team (security-lead) .......... 4 agents
|-- Cost Optimization Team (cost-lead) ..... 5 agents
|-- Design Team (design-lead) .............. 7 agents
|-- Debug Team (debug-lead) ................ 4 agents
|-- Content Team (content-lead) ............ 4 agents
|-- Migration Team (migration-lead) ........ 5 agents
```

Director: `.claude/commands/refactor.md` (opus model, Task tool access)
Agents: `.claude/agents/*.md` (sonnet model, subagent_type for Task)

---

## Tech Stack

- **Frontend**: React 18 + Vite + TypeScript + TailwindCSS + Framer Motion
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ + SQLAlchemy 2.0 + Alembic
- **Auth**: JWT (자체 인증)
- **Deploy**: Vercel/Netlify (frontend) + Railway/Render (backend)
- **Test**: pytest + Vitest + Playwright

---

## Team Details

### 1. Frontend Team (frontend-lead)

| Agent | Role |
|-------|------|
| frontend-lead | Team lead. React 컴포넌트 아키텍처 |
| component-refactorer | 컴포넌트 분리/병합/최적화 |
| state-optimizer | 상태 관리 최적화 (Zustand) |
| ui-consistency | UI 디자인 일관성 |
| performance-optimizer | React 렌더링 성능 |
| accessibility-specialist | 접근성, 반응형 디자인 |

Access: `frontend/src/`

### 2. Backend Team (backend-lead)

| Agent | Role |
|-------|------|
| backend-lead | Team lead. FastAPI 아키텍처 |
| fastapi-architect | FastAPI 프로젝트 구조 설계 |
| api-designer | RESTful API 표준화 |
| sqlalchemy-expert | SQLAlchemy ORM/쿼리 최적화 |
| pydantic-validator | Pydantic 스키마 검증 |
| error-handler | 에러 핸들링/로깅 |
| caching-specialist | 캐싱 전략 (Redis, 메모리) |

Access: `backend/app/`, `backend/tests/`

### 3. Database Team (database-lead)

| Agent | Role |
|-------|------|
| database-lead | Team lead. PostgreSQL 스키마 설계 |
| schema-designer | DB 스키마 설계 |
| query-optimizer | 쿼리/인덱스 최적화 |
| alembic-specialist | Alembic 마이그레이션 관리 |
| data-validator | 데이터 무결성 검증 |
| migration-helper | 마이그레이션 스크립트 |

Access: `backend/app/models/`, `backend/alembic/`

### 4. Test Team (test-lead)

| Agent | Role |
|-------|------|
| test-lead | Team lead. 테스트 전략 |
| test-writer | Unit/Integration 테스트 작성 |
| pytest-specialist | pytest 비동기 테스트 |
| tdd-expert | TDD 워크플로우 |
| e2e-tester | Playwright E2E 테스트 |
| bug-hunter | 버그 탐지/수정 |
| test-infra-specialist | 테스트 인프라 |

Access: `backend/tests/`, `frontend/src/__tests__/`, `e2e/`

### 5. Review Team (review-lead)

| Agent | Role |
|-------|------|
| review-lead | Team lead. 코드 품질 기준 |
| code-reviewer | 코드 리뷰 |
| refactor-expert | 리팩토링 패턴 |
| doc-writer | 문서화 |
| report-analyst | 보고서 분석 |
| architecture-reviewer | 아키텍처 검토 |
| report-summarizer | 보고서 요약/브리핑 |

Access: All files (read-only)

### 6. Security Team (security-lead)

| Agent | Role |
|-------|------|
| security-lead | Team lead. 보안 정책 |
| security-auditor | 보안 감사 |
| auth-specialist | 인증/인가 (JWT) |
| dependency-scanner | 의존성 취약점 스캔 |

Access: `backend/app/core/security.py`, `.env`

### 7. Cost Optimization Team (cost-lead)

| Agent | Role |
|-------|------|
| cost-lead | Team lead. 비용 절감 전략 |
| bundle-optimizer | 번들 사이즈 최적화 |
| network-optimizer | 네트워크 최적화 |
| resource-monitor | 리소스 모니터링 |
| token-optimizer | Claude Code 토큰 비용 최적화 |

Access: All files (read-only) + `package.json`

### 8. Design Team (design-lead)

| Agent | Role |
|-------|------|
| design-lead | Team lead. 디자인 시스템 |
| gamification-designer | 듀오링고 스타일 게임화 |
| ux-researcher | UX 리서치/분석 |
| ui-designer | UI 컴포넌트 디자인 |
| interaction-designer | 인터랙션 디자인 |
| responsive-specialist | 반응형 디자인 |
| design-system-guardian | 디자인 시스템 일관성 |

Access: `frontend/src/components/`, `tailwind.config.js`

### 9. Debug Team (debug-lead)

| Agent | Role |
|-------|------|
| debug-lead | Team lead. RADAR 프로세스 |
| error-tracer | 에러 추적/스택 분석 |
| regression-tester | 회귀 테스트 |
| performance-debugger | 성능 이슈 디버깅 |

Access: All files (full access)
Process: Reproduce -> Analyze -> Diagnose -> Act -> Regression (RADAR)

### 10. Content Team (content-lead)

| Agent | Role |
|-------|------|
| content-lead | Team lead. 학생 중심 콘텐츠 |
| ui-text-specialist | UI 텍스트/라벨 |
| data-display-specialist | 데이터 표시 형식 |
| help-content-specialist | 도움말/가이드/온보딩 |

Access: `frontend/src/components/` (text)

### 11. Migration Team (migration-lead)

| Agent | Role |
|-------|------|
| migration-lead | Team lead. SAFE 프로세스 |
| schema-migrator | 스키마 변경 영향 분석 |
| data-integrity-checker | 데이터 무결성 검증 |
| code-sync-specialist | 코드 참조 동기화 |
| rollback-specialist | 롤백/긴급 복구 |

Access: All files (full access)
Process: Survey -> Architect -> Fulfill -> Evaluate (SAFE)

---

## Shared Agents

Some agents serve on multiple teams:

| Agent | Primary Team | Shared With |
|-------|-------------|-------------|
| migration-helper | Database | Migration |
| bug-hunter | Test | Debug |

---

## Access Rights

| Level | Teams | Scope |
|-------|-------|-------|
| Full access (R/W) | Director, Debug, Migration | All project files |
| Domain access (R/W) | Frontend, Backend, Database, Security, Design, Content, Test | Own domain files |
| Read-only | Review, Cost Optimization | All files (analysis/review) |

---

## Dispatch Priority

| Priority | Situation | Teams Dispatched |
|----------|-----------|-----------------|
| P0 (immediate) | Error/Bug | Debug + related teams |
| P0 (immediate) | Security vulnerability | Security (can halt all) |
| P1 (high) | New feature | Frontend + Backend + DB |
| P1 (high) | Performance issue | Cost Optimization + Debug |
| P1 (high) | Data migration | Migration + DB |
| P2 (medium) | UI/UX improvement | Design + Frontend |
| P2 (medium) | Refactoring | Review + related teams |
| P2 (medium) | Content update | Content |
| P2 (medium) | Test writing | Test |
| P3 (low) | Documentation | Review (doc-writer) |

---

## Usage

### Via Director (recommended for complex tasks)
```
/refactor [description of work]
```
The Director analyzes the situation, dispatches appropriate teams in parallel/sequence, and reports results.

### Via Individual Agent (for specific tasks)
Use Task tool with `subagent_type` matching the agent name:
```
Task(subagent_type="code-reviewer", prompt="Review main.py")
Task(subagent_type="bug-hunter", prompt="Fix login error")
Task(subagent_type="gamification-designer", prompt="Design level-up animation")
```

### Quick Reference

| Situation | Agent/Team |
|-----------|-----------|
| Code review | code-reviewer |
| Bug fix | bug-hunter / debug-lead |
| New API endpoint | api-designer / fastapi-architect |
| DB schema change | schema-designer / alembic-specialist |
| Refactoring | refactor-expert |
| Documentation | doc-writer |
| Security audit | security-auditor |
| Performance issue | performance-debugger |
| UI consistency | design-system-guardian |
| Data migration | migration-lead |
| Report summary | report-summarizer |
| Test writing | test-writer / pytest-specialist |
| Game UI design | gamification-designer |

---

## Changelog

### v2.1 (2026-02-02) - Current
- **Migrated from Firebase to FastAPI + PostgreSQL**
- Removed 11 Firebase-specific agents:
  - firebase-cost-optimizer, firebase-debugger, firestore-rules-specialist
  - cloud-function-architect, function-cost-optimizer, backup-specialist
  - academy-domain-expert, analytics-expert
  - notification-designer, i18n-specialist, data-privacy-specialist
- Added 6 new agents:
  - fastapi-architect, sqlalchemy-expert, alembic-specialist
  - pydantic-validator, pytest-specialist, gamification-designer
- Updated 4 agents for FastAPI:
  - backend-lead, api-designer, error-handler, caching-specialist
- Total: 62 agents (from 67)

### v2.0 (2026-01-31)
- Complete restructure: flat 17-agent system -> 11-team hierarchy
- Added Director command (opus model) for orchestration
- Created 6 new teams: Frontend, Backend, Database, Design, Debug, Content
- Added Migration team (SAFE process)
- Expanded to 67 agents with team leads
- Access rights distribution policy
- Autonomous dispatch system (P0-P3)

### v1.4 (2026-01-09)
- Added report-summarizer, design-system-guardian, agent-orchestrator, token-optimizer
- 17 agents total

---

**Maintainer**: math-test dev team
**Last updated**: 2026-02-02