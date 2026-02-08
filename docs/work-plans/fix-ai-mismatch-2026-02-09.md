# AI 문제 생성 불일치 수정 보고서 (Fix Report: AI Generation Mismatch)
**Date:** 2026-02-09
**Author:** AI Assistant

## 개요 (Overview)
AI 문제 생성 시, 사용자가 '개념' 유형을 요청했음에도 불구하고 연산(Computation) 문제로 생성되는 문제와 UI 라벨의 혼동을 해결하기 위해 백엔드 및 프론트엔드 수정 작업을 수행했습니다.

## 문제 원인 (Root Cause)
1. **백엔드 로직**: 기존 `admin_generate_questions` API는 생성하려는 단원(Concept)의 기본 카테고리(예: 'computation')를 강제로 적용했습니다. 이로 인해 '연산' 단원에서 '개념' 문제를 생성하려 해도 '연산' 트랙으로 강제 전환되었습니다.
2. **프론트엔드 설정**: 정밀 모드(Granular Config)에서 생성 요청 시, 카테고리 정보를 명시적으로 전달하지 않았습니다.
3. **UI 혼동**: "CC (개념)", "FB (빈칸)" 등의 라벨이 사용자가 이해하기 어려웠습니다.

## 수정 내용 (Changes)

### 1. Backend (`app/api/v1/admin.py`)
- **Category Override 허용**: `GranularConfigItem` 모델에 `category` 옵션 필드를 추가했습니다.
- **로직 수정**: API 요청에 `config.category`가 포함된 경우, 단원의 기본 카테고리 대신 요청된 카테고리를 우선 사용하도록 `admin_generate_questions` 함수를 수정했습니다.

### 2. Frontend (`src/pages/admin/QuestionGenerationPage.tsx`)
- **카테고리 정보 전송**: AI 생성 요청(`generateQuestionsAI`) 시, 정밀 모드 설정(`granular_config`)에 `category: 'concept'`를 명시적으로 포함하도록 수정했습니다. 이로 인해 '연산' 단원에서도 '개념' 트랙으로 생성이 가능해졌습니다.
- **UI 라벨 개선**:
  - `CC (개념)` -> `개념 (객관식)`
  - `FB (빈칸)` -> `개념 (빈칸)`
  으로 변경하여 명확성을 높였습니다.

## 검증 방법 (Verification Steps)
1. **관리자 페이지 접속**: `/admin/question-generation`으로 이동합니다.
2. **단원 선택**: '연산' 유형의 단원(예: 덧셈, 뺄셈 등)을 선택합니다.
3. **정밀 모드 활성화**: 'AI 생성 옵션'에서 '정밀 모드 ON'을 선택합니다.
4. **수량 입력**: '개념 (객관식)' 또는 '개념 (빈칸)' 행의 Lv.1~Lv.5 칸에 수량을 입력합니다 (예: 1개씩).
5. **AI 생성 실행**: 'AI 생성하기' 버튼을 클릭합니다.
6. **결과 확인**:
   - 생성된 문제 목록에서 **트랙** 배지가 **'개념'**으로 표시되는지 확인합니다. (이전에는 '연산'으로 표시됨)
   - 문제 내용이 단순 계산이 아닌 **개념 설명, 원리 이해**에 관한 내용인지 확인합니다.

---
**Status:** Completed & Ready for Testing
