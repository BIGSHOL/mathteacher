# Debugging Category Reset

Question `e3-comp-002` (또는 신규 ID `e3-1-1-2-lv04-co-001`) 등 일부 개념형 문항이 서버 시작 시마다 `computation`으로 초기화된 후 `audit_question_categories`에 의해 다시 `concept`으로 수정되는 현상을 분석하고 해결 방안을 수립합니다.

## 원인 분석 (Root Cause)

1. **시드 데이터 불일치**:
    - `backend/app/seeds/elementary_3/computation.py` 파일 내에 "의미", "이유", "틀린 이유" 등을 묻는 명백한 개념형 문항들이 `category="computation"`으로 설정되어 있습니다.
    - 특히 `e3-1-1-2-lv04-co-001` (기존 `e3-comp-002`와 동일 내용)이 연산 시드 파일에 포함되어 있어 발생한 문제입니다.

2. **반복적인 초기화 (Reset) 원인**:
    - 서버 시작 시 `load_seed_data`가 실행됩니다.
    - 만약 DB에 특정 기준(Middle 1 개념 등)이 없으면 시드 로드 로직이 전체 문항을 다시 검토합니다.
    - 시드 파일 내의 카테고리가 `computation`이고, DB에는 이미 `concept`으로 수정되어 있는 경우에도 (일부 환경이나 조건에서) 다시 덮어씌워지거나, 혹은 신규 ID로 추가되면서 초기 카테고리가 `computation`으로 부여됩니다.
    - 이후 `audit_question_categories`가 이를 탐지하여 `concept`으로 수정하고 로그를 남깁니다. 이것이 매번 반복되는 것처럼 보이는 원인입니다.

## 해결 방안 (Proposed Solution)

1. **시드 데이터 수정 (근본 해결)**:
    - `backend/app/seeds/elementary_3/computation.py` 파일에서 개념적 성격이 강한 문항들의 `category`를 `concept`으로 정식 수정합니다.
    - 이를 통해 `load_seed_data` 단계부터 올바른 카테고리가 부여되도록 합니다.

2. **자동 감사 로직 강화 (보완)**:
    - `backend/app/main.py`의 `audit_question_categories` 함수 내 `COMP_TO_CONCEPT_PATTERNS`에 "이유", "과정", "틀린" 등 개념적 패턴을 추가하여 더 넓은 범위를 자동으로 커버하도록 합니다.
    - 로그 메시지에 기존 카테고리와 변경된 카테고리를 명시하여 가독성을 높입니다.

## 수정 대상 문항 (Elementary 3)

| ID | 내용 요약 | 현재 | 변경 |
|----|----------|------|------|
| `e3-1-1-2-lv03-co-001` | 어느 자리에서 처음 실수가 발생했나요? | comp | concept |
| `e3-1-1-2-lv04-co-001` | 십의 자리에서 가져온 수는 실제로 얼마를 의미하나요? | comp | concept |
| `e3-1-4-2-lv03-co-001` | 빈칸에 들어갈 알맞은 수는? (원리 설명) | comp | concept |
| `e3-1-4-1-lv04-co-001` | 바르게 계산한 것은? (자릿값 원리) | comp | concept |
| `e3-1-4-2-lv06-co-001` | 영역으로 나누어 계산하는 이유는? | comp | concept |
| `e3-2-1-2-lv05-co-001` | 옳은 과정은? | comp | concept |
| `e3-2-2-1-lv06-co-001` | 틀린 이유를 설명하세요. | comp | concept |
| `e3-2-2-2-lv08-co-001` | 텐트는 최소 몇 개 필요한가요? (맥락 해석) | comp | concept |
| `e3-2-2-2-lv05-co-001` | 보트는 최소 몇 대 필요한가요? | comp | concept |
| `e3-2-2-2-lv05-co-002` | 한 명은 최대 몇 개 받나요? | comp | concept |
| `e3-2-2-2-lv06-co-001` | 최대 몇 도막을 만들 수 있나요? | comp | concept |
| `e3-2-2-2-lv07-co-001` | 차는 최소 몇 대 필요한가요? | comp | concept |
