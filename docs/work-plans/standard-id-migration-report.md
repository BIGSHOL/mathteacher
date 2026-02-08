# 초등 3·4·5학년 시드 데이터 ID 표준화 완료 보고서

## 1. 개요
데이터의 일관성과 확장성을 확보하기 위해 초등 3, 4, 5학년 백엔드 시드 데이터의 모든 개념(Concept) 및 문항(Question) ID 체계를 새로운 표준 규격으로 전면 개편하였습니다.

## 2. 표준 ID 규격
- **개념 ID**: `Grade-Semester-Chapter-Concept` (예: `e5-1-1-1`)
- **문항 ID**: `Grade-Semester-Chapter-Concept-Type-Number` (예: `e5-1-1-1-co-001`)
    - `co`: Computation (연산)
    - `cc`: Concept Question (개념 문제)
    - `fb`: Fill in the Blank (빈칸 채우기)

## 3. 작업 내용
### 대상 학년 및 파일
- **초등 3학년**: `computation.py`, `concept_questions.py`, `fill_blank.py`, `__init__.py`
- **초등 4학년**: `computation.py`, `concept_questions.py`, `fill_blank.py`, `__init__.py`
- **초등 5학년**: `computation.py`, `concept_questions.py`, `fill_blank.py`, `__init__.py`

### 주요 변경 사항
- **레거시 제거**: 기존 `concept-eX-...` 접두사와 ID 내부에 포함되어 있던 난이도 정보(`-lvXX`)를 모두 제거하였습니다.
- **매핑 최적화**: 문항 ID가 소속 개념 ID를 직관적으로 추론할 수 있도록 구조화하였습니다.
- **테스트 정합성**: 모든 시드 파일 내의 테스트 정의(`tests`)와 통합 데이터 반환 함수(`get_all_data`)를 표준 ID 시스템에 맞춰 업데이트하였습니다.

## 4. 검증 결과
- **정적 분석**: `findstr` 검색을 통해 시드 데이터 폴더 내에서 `concept-e` 및 `-lv` 등 구형 ID 패턴이 완전히 제거되었음을 확인하였습니다.
- **중복 검사**: 각 학년별 파일 내 문항 ID의 고유성을 검증하였습니다.
- **연속성 확인**: 문항 번호(`001`, `002`...)가 누락 없이 순차적으로 부여되었음을 확인하였습니다.

## 5. 결론 및 향후 계획
백엔드 시드 데이터의 ID 표준화 1단계(초3~초5)가 완료되었습니다. 이로써 데이터 관리 아키텍처가 통일되었으며, 향후 프론트엔드 룰 베이스 템플릿과의 연계 및 관리자 UI 최적화 작업의 기반을 마련하였습니다. 

이후 단계에서는 프론트엔드 템플릿 ID 개편 및 전체 데이터 시스템의 무결성 검증을 진행할 예정입니다.
