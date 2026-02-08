# ID Standardization Completion Report

**Date**: 2026-02-09
**Subject**: Standardization of Concept and Question IDs across All Grade Levels

## 1. 개요 (Overview)
본 보고서는 프로젝트 내 수학 콘텐츠(개념 및 문항)의 ID 체계를 표준화한 결과를 요약합니다. 
기존의 혼재된 ID 포맷(예: `concept-h1-set`, `h1-1-1-lv03`)을 **2022 개정 교육과정**에 맞춘 `Grade-Semester-Chapter-Concept-Type-Number` 형식으로 통일하였습니다.

## 2. 표준 ID 체계 (Standard ID Format)

### 개념 ID (Concept ID)
`[Grade]-[Semester]-[Chapter]-[Concept]`
- 예: `h1-1-1-1` (고1 - 1학기 - 1단원 - 첫 번째 개념)
- 예: `e5-2-1-1` (초5 - 2학기 - 1단원 - 첫 번째 개념)

### 문항 ID (Question ID)
`[Grade]-[Semester]-[Chapter]-[Concept]-[Type]-[Number]`
- 예: `h1-1-1-1-co-001` (연산/computation)
- 예: `h1-1-1-1-cc-001` (개념확인/concept check)
- 예: `h1-1-1-1-fb-001` (빈칸채우기/fill blank)

## 3. 학년별 작업 내역 (Work Logs by Grade)

### 3.1. 고등학교 1학년 (High School 1 - Common Math 1 & 2)
- **공통수학1 (Semester 1)**: `backend/app/seeds/high_1`
    - 다항식, 방정식과 부등식, 경우의 수, 행렬 단원 표준화 완료.
- **공통수학2 (Semester 2)**: `backend/app/seeds/high_2`
    - 도형의 방정식(`/high_2/computation.py`), 집합과 명제, 함수 단원 표준화 완료.
    - 기존 `h2-` 프리픽스를 `h1-2-`로 매핑하여 고1 2학기 과정임을 명확히 함.

### 3.2. 초등학교 5, 6학년 (Elementary 5 & 6)
- **초등 5학년**: `backend/app/seeds/elementary_5`
    - 1학기(`e5-1-x`), 2학기(`e5-2-x`) 단원 구분 및 ID 표준화.
- **초등 6학년**: `backend/app/seeds/elementary_6`
    - `computation.py`: 2학기 개념 ID 학기 코드 수정 (`e6-1-1-2` → `e6-2-1-1`).
    - `concept_questions.py`: 레거시 ID (`concept-e6-spatial` 등) 제거 및 표준화.

### 3.3. 중학교 1, 2, 3학년 (Middle School 1, 2, 3)
- **중등 1학년**: `backend/app/seeds/middle_1`
    - `concept_questions.py`: 레거시 ID (`concept-m1-eq-01` 등) 수정.
    - `__init__.py`: 테스트 시나리오 내 ID 참조 오류 수정.
- **중등 2, 3학년**: 
    - 이전 단계에서 이미 `m2-S-C-K`, `m3-S-C-K` 포맷으로 표준화 완료.

## 4. 결론 (Conclusion)
현재 백엔드 시드 데이터(`backend/app/seeds/`) 내의 모든 학년(초3 ~ 고1) 데이터가 표준 ID 체계를 따르고 있습니다.
이로써 다음과 같은 이점을 확보하였습니다:
1. **데이터 일관성**: 모든 학년이 동일한 ID 구조를 가져 파싱 및 분석 용이.
2. **교육과정 매핑**: ID만으로 몇 학년, 몇 학기, 몇 단원인지 식별 가능.
3. **유지보수 효율성**: 레거시 ID 혼용으로 인한 잠재적 오류 제거.

**다음 단계**: 
- 프론트엔드에서 해당 ID를 사용하는 로직이 있다면 변경된 ID 체계에 맞게 업데이트 필요 (현재는 백엔드 시드 데이터 중심 작업).
