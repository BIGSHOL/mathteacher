# 에이전트 분석 보고서

> **프로젝트**: math_test (수학 테스트 앱)
> **분석일**: 2026-02-02
> **총 에이전트 수**: 67개

---

## 1. 프로젝트 기술 스택 비교

| 항목 | math_test (현재) | ijw-calander (에이전트 설계 기준) |
|------|-----------------|--------------------------------|
| 백엔드 | **FastAPI (Python)** | Firebase Cloud Functions (Node.js) |
| 데이터베이스 | **PostgreSQL + Alembic** | Cloud Firestore |
| 프론트엔드 | React + Vite + TypeScript | React + Vite + TypeScript |
| 인증 | **JWT 자체 인증** | Firebase Authentication |
| 배포 (BE) | **Railway / Render** | Firebase |
| 배포 (FE) | Vercel / Netlify | Vercel |

**핵심 차이점**: 현재 프로젝트는 Firebase를 전혀 사용하지 않습니다.

---

## 2. 불필요한 에이전트 분류

### 2.1 Firebase/Firestore 특화 에이전트 (6개) - **완전히 불필요**

| 에이전트 | 역할 | 불필요 사유 |
|---------|------|-----------|
| `firebase-cost-optimizer` | Firebase 비용 최적화 | PostgreSQL 사용, Firebase 미사용 |
| `firebase-debugger` | Firebase 디버깅 | PostgreSQL 사용, Firebase 미사용 |
| `firestore-rules-specialist` | Firestore 보안 규칙 | PostgreSQL 사용, Firestore 미사용 |
| `cloud-function-architect` | Cloud Functions 아키텍처 | FastAPI 사용, Cloud Functions 미사용 |
| `function-cost-optimizer` | Cloud Functions 비용 최적화 | FastAPI 사용, Cloud Functions 미사용 |
| `backup-specialist` | Firestore 백업/복구 | PostgreSQL 네이티브 백업 사용 |

### 2.2 학원 관리 도메인 특화 에이전트 (2개) - **도메인 불일치**

| 에이전트 | 역할 | 불필요 사유 |
|---------|------|-----------|
| `academy-domain-expert` | 학원 관리 비즈니스 로직 | 현재 프로젝트는 단순 수학 테스트 앱 (학원 관리 기능 없음) |
| `analytics-expert` | 학원 운영 데이터 분석 | 출석률, 수강생 추이 등 학원 특화 지표 불필요 |

### 2.3 MVP 단계에서 불필요한 에이전트 (3개) - **Out-of-scope**

| 에이전트 | 역할 | 불필요 사유 |
|---------|------|-----------|
| `notification-designer` | 푸시 알림 설계 | PRD에서 v2 이후로 명시 (Out-of-scope) |
| `i18n-specialist` | 다국어 지원 | MVP는 한국어 단일 언어 |
| `data-privacy-specialist` | 개인정보 보호 | 최소 정보만 수집 (이름, 학년), 복잡한 보호 불필요 |

---

## 3. 필요한 에이전트 분류

### 3.1 필수 에이전트 (핵심 개발)

| 팀 | 에이전트 | 역할 | 필요성 |
|----|---------|------|--------|
| Frontend | `frontend-lead` | React 컴포넌트 아키텍처 | 게임화 UI 개발 |
| Frontend | `component-refactorer` | 컴포넌트 최적화 | 재사용 가능한 컴포넌트 설계 |
| Frontend | `state-optimizer` | 상태 관리 최적화 | Zustand 상태 관리 |
| Frontend | `ui-consistency` | UI 일관성 | 디자인 시스템 유지 |
| Frontend | `performance-optimizer` | React 렌더링 성능 | < 500ms 응답 목표 |
| Frontend | `accessibility-specialist` | 접근성, 반응형 | 모바일/태블릿 지원 필수 |
| Database | `database-lead` | DB 스키마 설계 | PostgreSQL 스키마 설계 |
| Database | `schema-designer` | 스키마 설계 | 문제 뱅크, 학습 기록 설계 |
| Database | `query-optimizer` | 쿼리 최적화 | 통계 쿼리 성능 |
| Database | `data-validator` | 데이터 무결성 | 테스트 결과 정합성 |
| Test | `test-lead` | 테스트 전략 | Contract-First TDD |
| Test | `test-writer` | 테스트 코드 작성 | pytest, Vitest |
| Test | `tdd-expert` | TDD 워크플로우 | RED-GREEN-REFACTOR |
| Test | `e2e-tester` | E2E 테스트 | Playwright |
| Test | `bug-hunter` | 버그 탐지 | 품질 보증 |
| Test | `test-infra-specialist` | 테스트 인프라 | CI/CD 통합 |
| Review | `review-lead` | 코드 품질 | 품질 게이트 |
| Review | `code-reviewer` | 코드 리뷰 | PR 검토 |
| Review | `refactor-expert` | 리팩토링 | 코드 개선 |
| Review | `doc-writer` | 문서화 | API 문서 |
| Review | `architecture-reviewer` | 아키텍처 검토 | 설계 검증 |
| Review | `report-analyst` | 보고서 분석 | 진행 상황 분석 |
| Review | `report-summarizer` | 보고서 요약 | 브리핑 |
| Security | `security-lead` | 보안 정책 | 인증/인가 |
| Security | `security-auditor` | 보안 감사 | OWASP 체크 |
| Security | `auth-specialist` | 인증/인가 | JWT 구현 |
| Security | `dependency-scanner` | 의존성 취약점 | npm/pip 보안 |
| Design | `design-lead` | 디자인 시스템 | 듀오링고 스타일 |
| Design | `ux-researcher` | UX 연구 | 학생 사용성 |
| Design | `ui-designer` | UI 컴포넌트 | 게임화 피드백 UI |
| Design | `interaction-designer` | 인터랙션 | 레벨업, 콤보 애니메이션 |
| Design | `responsive-specialist` | 반응형 | 모바일 퍼스트 |
| Design | `design-system-guardian` | 디자인 일관성 | 브랜드 유지 |
| Debug | `debug-lead` | 디버깅 총괄 | RADAR 프로세스 |
| Debug | `error-tracer` | 에러 추적 | 스택 분석 |
| Debug | `regression-tester` | 회귀 테스트 | 버그 재발 방지 |
| Debug | `performance-debugger` | 성능 디버깅 | < 500ms 보장 |
| Migration | `migration-lead` | 마이그레이션 총괄 | Alembic 관리 |
| Migration | `schema-migrator` | 스키마 변경 | DB 마이그레이션 |
| Migration | `data-integrity-checker` | 데이터 무결성 | 마이그레이션 검증 |
| Migration | `migration-helper` | 마이그레이션 지원 | 스크립트 작성 |
| Migration | `code-sync-specialist` | 코드 동기화 | 스키마-코드 일치 |
| Migration | `rollback-specialist` | 롤백 | 긴급 복구 |
| Cost | `cost-lead` | 비용 전략 | 인프라 비용 관리 |
| Cost | `bundle-optimizer` | 번들 최적화 | FE 빌드 크기 |
| Cost | `network-optimizer` | 네트워크 최적화 | API 호출 최적화 |
| Cost | `resource-monitor` | 리소스 모니터링 | 서버 자원 관리 |
| Cost | `token-optimizer` | 토큰 최적화 | Claude Code 비용 |
| Content | `content-lead` | 콘텐츠 총괄 | 학생 중심 콘텐츠 |
| Content | `ui-text-specialist` | UI 텍스트 | 라벨, 메시지 |
| Content | `data-display-specialist` | 데이터 표시 | 통계 표시 형식 |
| Content | `help-content-specialist` | 도움말 | 온보딩 콘텐츠 |

---

## 4. 수정 필요 에이전트

다음 에이전트들은 역할은 유효하나, **Firebase 특화 내용을 FastAPI/PostgreSQL로 수정 필요**:

| 에이전트 | 현재 내용 | 수정 방향 |
|---------|----------|----------|
| `backend-lead` | Firebase Cloud Functions | FastAPI 아키텍처 |
| `api-designer` | Firebase API | RESTful API (FastAPI) |
| `error-handler` | Firebase 에러 | FastAPI 에러 핸들링 |
| `caching-specialist` | Firebase 캐싱 | Redis 캐싱 (v2) |

---

## 5. 요약

| 분류 | 개수 | 조치 |
|------|-----|------|
| **완전히 불필요** (Firebase 특화) | 6개 | 삭제 권장 |
| **도메인 불일치** (학원 관리 특화) | 2개 | 삭제 권장 |
| **Out-of-scope** (MVP 이후) | 3개 | 보류 또는 삭제 |
| **수정 필요** (기술 스택 변경) | 4개 | 내용 수정 |
| **그대로 사용 가능** | 52개 | 유지 |

### 삭제 권장 에이전트 목록 (11개)

```
.claude/agents/firebase-cost-optimizer.md
.claude/agents/firebase-debugger.md
.claude/agents/firestore-rules-specialist.md
.claude/agents/cloud-function-architect.md
.claude/agents/function-cost-optimizer.md
.claude/agents/backup-specialist.md
.claude/agents/academy-domain-expert.md
.claude/agents/analytics-expert.md
.claude/agents/notification-designer.md
.claude/agents/i18n-specialist.md
.claude/agents/data-privacy-specialist.md
```

---

## 6. 권장 조치

1. **즉시 삭제**: Firebase/Firestore 특화 에이전트 6개
2. **삭제 검토**: 학원 도메인 특화 에이전트 2개
3. **보류**: Out-of-scope 에이전트 3개 (v2에서 필요할 수 있음)
4. **수정**: backend-lead, api-designer, error-handler, caching-specialist 내용 업데이트
5. **신규 추가 고려**: FastAPI 특화 에이전트 (sqlalchemy-expert, alembic-specialist 등)

---

**분석 완료**: 67개 에이전트 중 11개가 현재 프로젝트에 불필요합니다.
