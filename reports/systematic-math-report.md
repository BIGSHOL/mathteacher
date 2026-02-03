# 계통수학 총정리 보고서

> 2022 개정 교육과정 기반 수학 문제 생성 시스템의 계통수학(Systematic Mathematics) 전체 구현 현황
>
> **작성일**: 2026-02-03
> **대상 범위**: 초4 ~ 고1 (128개 개념, 156개 선수관계)

---

## 목차

1. [계통수학이란](#1-계통수학이란)
2. [시스템 아키텍처](#2-시스템-아키텍처)
3. [개념 데이터 현황](#3-개념-데이터-현황)
4. [학년별 선수관계 전체 맵](#4-학년별-선수관계-전체-맵)
5. [11대 크로스학년 계통 체인](#5-11대-크로스학년-계통-체인)
6. [데이터베이스 스키마](#6-데이터베이스-스키마)
7. [백엔드 구현](#7-백엔드-구현)
8. [프론트엔드 구현](#8-프론트엔드-구현)
9. [적응형 학습과 계통수학 연계](#9-적응형-학습과-계통수학-연계)
10. [관련 파일 인덱스](#10-관련-파일-인덱스)
11. [향후 과제](#11-향후-과제)

---

## 1. 계통수학이란

**계통수학**(系統數學)은 수학 개념들의 위계적 연결과 점진적 확장 구조를 의미합니다.

- 초등학교에서 배운 자연수 → 중학교의 정수/유리수 → 고등학교의 실수/복소수
- 패턴 찾기 → 등식 → 변수 → 방정식 → 함수 → 미적분

모든 수학 개념은 **선수 개념(prerequisite)** 위에 쌓이며, 선수 개념의 이해 없이 상위 개념을 학습하면 구조적 결손이 발생합니다.

### 2022 개정 교육과정 반영 사항

| 변경 사항 | 내용 |
|-----------|------|
| 행렬 신설 | 고1에 행렬의 뜻, 연산, 역행렬, 케일리-해밀턴 정리 추가 |
| 공간벡터 복원 | 기하 영역 강화 |
| 상자그림 신설 | 통계 영역 확장 |
| 모비율 추정 복원 | 통계 추론 강화 |

### 4대 영역별 사고 발달 경로

| 영역 | 초등 | 중등 | 고등 |
|------|------|------|------|
| 수와 연산 | N (자연수) | Z, Q (정수, 유리수) | R, C (실수, 복소수) |
| 변화와 관계 | 패턴 → 비/비율 | 방정식 → 일차함수 | 이차함수 → 고차방정식 |
| 도형과 측정 | 직관적 인식 → 넓이 | 증명 → 닮음 | 삼각비 → 원의 성질 |
| 자료와 가능성 | 분류 → 그래프 | 대푯값 → 확률 | 집합/명제 → 순열/조합 |

---

## 2. 시스템 아키텍처

```
┌──────────────────────────────────────────────────────┐
│                    seed_concepts.py                   │
│         128개 개념 + 156개 선수관계 정의              │
│         11개 크로스학년 체인 정의                     │
│         get_prerequisite_chain() 유틸리티             │
└───────────────┬──────────────────────────────────────┘
                │ seed_db.py --clear
                ▼
┌──────────────────────────────────────────────────────┐
│              PostgreSQL (Docker)                      │
│  ┌─────────────┐  ┌──────────────────────┐           │
│  │  concepts    │  │ concept_prerequisites │           │
│  │  (128 rows)  │──│ (156 rows)           │           │
│  └──────┬──────┘  └──────────────────────┘           │
│         │ FK                                          │
│  ┌──────▼──────┐                                     │
│  │  questions   │  prerequisite_concept_ids (JSON)    │
│  └─────────────┘                                     │
└───────────────┬──────────────────────────────────────┘
                │ API
                ▼
┌──────────────────────────────────────────────────────┐
│              FastAPI 백엔드                           │
│  /api/v1/questions     문제 CRUD + 필터링             │
│  adaptive_service      난이도 적응 (개념 정확도 기반) │
│  prompt_builder        AI 프롬프트에 선수관계 주입    │
│  exam_prep_strategy    선수학습 약점 진단             │
└───────────────┬──────────────────────────────────────┘
                │ axios
                ▼
┌──────────────────────────────────────────────────────┐
│              React 프론트엔드                         │
│  questionGenerator/    템플릿 기반 문제 생성 엔진     │
│  questionService.ts    생성된 문제 → DB 저장 파이프   │
│  types: Concept.prerequisite_ids                     │
│  types: Question.prerequisite_concept_ids            │
└──────────────────────────────────────────────────────┘
```

---

## 3. 개념 데이터 현황

### 3.1 학년별 통계

| 학년 | 코드 | 개념 수 | 선수관계 | 루트(선수 없음) | 템플릿 커버 |
|------|------|---------|---------|----------------|------------|
| 초4 | E4 | 23 | 18 | 10 | 100% (23/23) |
| 초5 | E5 | 24 | 29 | 4 | 100% (24/24) |
| 초6 | E6 | 16 | 22 | 0 | 100% (16/16) |
| 중1 | M1 | 11 | 17 | 0 | 100% (11/11) |
| 중2 | M2 | 9 | 14 | 0 | 100% (9/9) |
| 중3 | M3 | 10 | 14 | 0 | 100% (10/10) |
| 고1 | H1 | 35 | 42 | 3 | 템플릿 미작성 |
| **합계** | | **128** | **156** | **17** | |

### 3.2 영역별 분포

| 영역(part) | 초4 | 초5 | 초6 | 중1 | 중2 | 중3 | 고1 | 합계 |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| calc (수와 연산) | 12 | 16 | 5 | 4 | 1 | 2 | 0 | 40 |
| algebra (대수) | 1 | 1 | 4 | 2 | 4 | 3 | 23 | 38 |
| geo (도형) | 8 | 7 | 6 | 3 | 2 | 2 | 0 | 28 |
| data (통계) | 2 | 0 | 1 | 1 | 1 | 2 | 12 | 19 |
| func (함수) | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 3 |

---

## 4. 학년별 선수관계 전체 맵

### 4.1 초등학교 4학년 (E4) — 23개 개념

```
[수와 연산]
E4-NUM-01 만 단위 이해
├── E4-NUM-02 억 단위 이해
│   └── E4-NUM-03 조 단위 이해
└── E4-NUM-04 큰 수 비교

E4-NUM-05 세 자리 × 두 자리 곱셈
└── E4-NUM-06 세 자리 ÷ 두 자리 나눗셈

E4-NUM-07 동분모 분수 덧셈
├── E4-NUM-08 동분모 분수 뺄셈
│   └── E4-NUM-09 1에서 분수 빼기
└── E4-NUM-10 대분수 연산 (← E4-NUM-07, E4-NUM-08)

E4-NUM-11 소수 덧셈
└── E4-NUM-12 소수 뺄셈

[도형]
E4-GEO-01 예각 ──┐
E4-GEO-02 직각 ──┼── E4-GEO-04 삼각형 분류 (변)
│                 │   E4-GEO-05 삼각형 분류 (각)
└─ E4-GEO-03 둔각┘

E4-GEO-06 사각형 분류 (독립)
E4-GEO-07 다각형과 대각선 (독립)
E4-GEO-08 평면도형의 이동 (독립)

[통계/규칙]
E4-STA-01 막대그래프
└── E4-STA-02 꺾은선그래프

E4-ALG-01 규칙 찾기 (독립)
```

### 4.2 초등학교 5학년 (E5) — 24개 개념

```
[수와 연산]
E4-NUM-06 ─→ E5-NUM-01 약수
              └── E5-NUM-03 공약수/GCD
                  └── E5-NUM-05 약분/기약분수

E4-NUM-05 ─→ E5-NUM-02 배수
              └── E5-NUM-04 공배수/LCM (← E5-NUM-02, E5-NUM-03)
                  └── E5-NUM-06 통분

E5-NUM-06 + E4-NUM-07 → E5-NUM-08 이분모 분수 덧셈
E5-NUM-06 + E4-NUM-08 → E5-NUM-09 이분모 분수 뺄셈
E5-NUM-08 + E5-NUM-09 + E4-NUM-10 → E5-NUM-10 대분수 연산 (이분모)

E4-NUM-05 + E4-NUM-06 → E5-NUM-07 혼합 계산
E5-NUM-05 → E5-NUM-13 분수의 곱셈
E4-NUM-11 → E5-NUM-14 소수의 곱셈
E5-NUM-07 → E5-NUM-15 평균
E5-NUM-11 수의 범위 → E5-NUM-12 어림하기
E5-NUM-16 가능성 (독립)

[도형]
E5-GEO-01 다각형의 둘레
└── E5-GEO-02 직사각형/평행사변형 넓이
    └── E5-GEO-03 삼각형 넓이
        └── E5-GEO-04 마름모/사다리꼴 넓이

E4-GEO-04 → E5-GEO-05 합동
            └── E5-GEO-06 선대칭/점대칭 (← E5-GEO-05, E4-GEO-08)

E4-GEO-06 → E5-GEO-07 직육면체/정육면체

[대수]
E4-ALG-01 → E5-ALG-01 규칙과 대응
```

### 4.3 초등학교 6학년 (E6) — 16개 개념

```
[수와 연산]
E5-NUM-05 → E6-NUM-01 자연수÷자연수→분수
             └── E6-NUM-02 분수÷자연수 (← E6-NUM-01, E5-NUM-13)
                 └── E6-NUM-03 분수÷분수 (← E6-NUM-02, E5-NUM-13)

E5-NUM-14 → E6-NUM-04 소수÷자연수
             └── E6-NUM-05 소수÷소수

[대수 — 비와 비율]
E5-NUM-05 → E6-ALG-01 비와 비율
             ├── E6-ALG-02 백분율
             └── E6-ALG-03 비례식
                 └── E6-ALG-04 비례배분

[도형]
E5-GEO-07 → E6-GEO-01 각기둥/각뿔
E5-GEO-07 + E5-GEO-02 → E6-GEO-02 직육면체 부피/겉넓이
E6-GEO-03 원주/원주율
└── E6-GEO-04 원의 넓이 (← E6-GEO-03, E5-GEO-02)
    └── E6-GEO-05 원기둥/원뿔/구 (← E6-GEO-04, E6-GEO-01)
E5-GEO-07 → E6-GEO-06 쌓기나무/투영도

[통계]
E4-STA-02 + E6-ALG-02 → E6-STA-01 띠그래프/원그래프
```

### 4.4 중학교 1학년 (M1) — 11개 개념

```
[수]
E5-NUM-01 + E5-NUM-03 → M1-NUM-01 소인수분해
                         └── M1-NUM-02 GCD/LCM 소인수분해 (← M1-NUM-01, E5-NUM-03, E5-NUM-04)

E6-NUM-03 → M1-NUM-03 정수와 유리수
             └── M1-NUM-04 정수/유리수 사칙연산 (← M1-NUM-03, E5-NUM-07)

[대수]
E5-ALG-01 + M1-NUM-04 → M1-ALG-01 문자와 식
                         └── M1-ALG-02 일차방정식

[함수]
E5-ALG-01 → M1-FUNC-01 좌표평면과 그래프

[도형]
E4-GEO-02 → M1-GEO-01 기본 도형과 작도
             └── M1-GEO-02 삼각형 합동조건 (← M1-GEO-01, E5-GEO-05)
                 └── M1-GEO-03 평면도형 성질 (← M1-GEO-02, E4-GEO-07)

[통계]
E6-STA-01 + E5-NUM-15 → M1-STA-01 자료의 정리와 해석
```

### 4.5 중학교 2학년 (M2) — 9개 개념

```
M1-NUM-03 + M1-NUM-04 → M2-NUM-01 유리수와 순환소수

M1-ALG-01 + M1-NUM-01 → M2-ALG-01 지수법칙/단항식
                         └── M2-ALG-02 다항식 연산

M1-ALG-02 → M2-ALG-03 일차부등식
M1-ALG-02 + M2-ALG-03 → M2-ALG-04 연립방정식

M1-FUNC-01 + M1-ALG-02 → M2-FUNC-01 일차함수

M1-GEO-02 → M2-GEO-01 삼각형/사각형 성질
             └── M2-GEO-02 닮음/피타고라스

E5-NUM-16 + M1-STA-01 → M2-STA-01 경우의 수와 확률
```

### 4.6 중학교 3학년 (M3) — 10개 개념

```
M1-NUM-04 + M2-ALG-01 → M3-NUM-01 제곱근과 실수
                         └── M3-NUM-02 근호 포함 식의 계산

M2-ALG-02 → M3-ALG-01 곱셈공식
             └── M3-ALG-02 인수분해
                 └── M3-ALG-03 이차방정식 (← M3-ALG-02, M3-NUM-02)

M2-FUNC-01 + M3-ALG-03 → M3-FUNC-01 이차함수

M2-GEO-02 → M3-GEO-01 삼각비
E6-GEO-04 + M2-GEO-02 → M3-GEO-02 원의 성질

E5-NUM-15 + M2-STA-01 → M3-STA-01 대푯값/산포도
                         └── M3-STA-02 상관관계 (← M3-STA-01, M1-FUNC-01)
```

### 4.7 고등학교 1학년 (H1) — 35개 개념

```
[다항식/방정식 계통]
M3-ALG-01 → H1-ALG-01 다항식 정리
             └── H1-ALG-02 다항식 나눗셈
                 └── H1-ALG-03 나머지정리
                     └── H1-ALG-04 인수정리
                         └── H1-ALG-05 인수분해 고급 (← H1-ALG-04, M3-ALG-02)
                             └── H1-ALG-10 고차방정식 (← H1-ALG-05, H1-ALG-04)
                                 └── H1-ALG-17 연립이차방정식 (← H1-ALG-10, M2-ALG-04)

[복소수/판별식 계통]
M3-NUM-02 → H1-ALG-06 복소수
             ├── H1-ALG-07 복소수 사칙연산
             └── H1-ALG-08 판별식 (← H1-ALG-06, M3-ALG-03)
                 └── H1-ALG-09 근과 계수의 관계

[부등식 계통]
M2-ALG-03 → H1-ALG-11 이차부등식 (← M2-ALG-03, M3-FUNC-01)
             └── H1-ALG-12 연립부등식
M2-ALG-03 → H1-ALG-13 절대값 방정식/부등식

[이차함수 계통]
M3-FUNC-01 → H1-ALG-14 이차함수 최대/최소
              └── H1-ALG-15 이차함수와 이차방정식 (← H1-ALG-14, H1-ALG-08)
                  └── H1-ALG-16 이차함수와 이차부등식 (← H1-ALG-15, H1-ALG-11)

[집합/명제 계통]
H1-STA-01 집합의 뜻
├── H1-STA-02 부분집합
├── H1-STA-03 집합의 연산
│   └── H1-STA-04 드모르간 법칙
└── H1-STA-05 명제와 조건
    ├── H1-STA-06 역/이/대우
    └── H1-STA-07 필요조건/충분조건 (← H1-STA-05, H1-STA-02)

[경우의 수 계통]
M2-STA-01 → H1-STA-10 합의 법칙/곱의 법칙
             └── H1-STA-08 순열
                 ├── H1-STA-09 조합
                 │   └── H1-STA-12 조합의 활용
                 └── H1-STA-11 순열의 활용

[행렬 계통 — 2022 신설]
H1-ALG-18 행렬의 뜻
└── H1-ALG-19 행렬 덧셈/뺄셈/실수배
    └── H1-ALG-20 행렬의 곱셈
        └── H1-ALG-21 단위행렬
            └── H1-ALG-22 역행렬
                └── H1-ALG-23 케일리-해밀턴 정리
```

---

## 5. 11대 크로스학년 계통 체인

초등~고등을 관통하는 핵심 학습 경로입니다.

### 5.1 분수 계통

```
E4-NUM-07 → E5-NUM-06 → E5-NUM-08 → E5-NUM-13 → E6-NUM-03 → M1-NUM-04
동분모 덧셈    통분     이분모 덧셈  분수 곱셈   분수÷분수  유리수 사칙
```

### 5.2 소수 계통

```
E4-NUM-11 → E5-NUM-14 → E6-NUM-05
소수 덧셈    소수 곱셈    소수÷소수
```

### 5.3 도형 계통

```
E4-GEO-01 → E5-GEO-03 → E6-GEO-04 → M1-GEO-03 → M2-GEO-02 → M3-GEO-01
  예각       삼각형넓이    원의넓이   평면도형성질  닮음/피타    삼각비
```

### 5.4 그래프/통계 계통

```
E4-STA-01 → E4-STA-02 → E6-STA-01 → M1-STA-01 → M2-STA-01 → M3-STA-01
막대그래프   꺾은선     띠/원그래프  자료정리    경우의수     대푯값/산포도
```

### 5.5 방정식 계통

```
E5-ALG-01 → E6-ALG-03 → M1-ALG-02 → M2-ALG-04 → M3-ALG-03 → H1-ALG-08 → H1-ALG-10 → H1-ALG-17
규칙대응    비례식     일차방정식  연립방정식  이차방정식   판별식    고차방정식 연립이차
```

### 5.6 함수 계통

```
E4-ALG-01 → E5-ALG-01 → M1-FUNC-01 → M2-FUNC-01 → M3-FUNC-01 → H1-ALG-14 → H1-ALG-15
규칙찾기    규칙대응    좌표평면     일차함수     이차함수    최대/최소  함수와방정식
```

### 5.7 다항식/인수분해 계통

```
M2-ALG-02 → M3-ALG-01 → M3-ALG-02 → H1-ALG-01 → H1-ALG-02 → H1-ALG-03 → H1-ALG-04 → H1-ALG-05
다항식연산   곱셈공식    인수분해   다항식정리  다항식나눗셈  나머지정리   인수정리   인수분해고급
```

### 5.8 부등식 계통

```
M2-ALG-03 → H1-ALG-11 → H1-ALG-12 → H1-ALG-13 → H1-ALG-16
일차부등식   이차부등식   연립부등식   절대값     함수와부등식
```

### 5.9 수 체계 계통

```
E4-NUM-07 → M1-NUM-04 → M3-NUM-01 → M3-NUM-02 → H1-ALG-06 → H1-ALG-07
분수 덧셈   유리수연산   제곱근/실수  근호계산    복소수     복소수연산
```

### 5.10 경우의 수/확률 계통

```
M2-STA-01 → H1-STA-10 → H1-STA-08 → H1-STA-09
경우의수     합의법칙     순열        조합
```

### 5.11 행렬 계통 (2022 신설)

```
H1-ALG-18 → H1-ALG-19 → H1-ALG-20 → H1-ALG-21 → H1-ALG-22 → H1-ALG-23
행렬의뜻    덧셈/뺄셈    곱셈       단위행렬     역행렬     케일리-해밀턴
```

---

## 6. 데이터베이스 스키마

### 6.1 concepts 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | STRING(36) PK | 개념 ID (예: E4-NUM-01) |
| name | STRING(200) | 개념명 |
| grade | ENUM(Grade) | 학년 |
| category | ENUM(QuestionCategory) | 트랙: computation / concept |
| part | ENUM(ProblemPart) | 영역: calc / algebra / func / geo / data / word |
| description | TEXT | 설명 |
| parent_id | STRING(36) FK → concepts.id | 상위 개념 (같은 계열 내 부모) |

### 6.2 concept_prerequisites 연결 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| concept_id | STRING(36) FK PK | 배우려는 개념 |
| prerequisite_id | STRING(36) FK PK | 먼저 알아야 하는 개념 |

> "concept_id를 배우려면 prerequisite_id를 먼저 알아야 함"

### 6.3 questions 테이블 (계통수학 관련 컬럼)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| concept_id | STRING(36) FK → concepts.id | 이 문제가 속한 개념 |
| prerequisite_concept_ids | JSON (list[str]) | 선수 개념 ID 목록 (빠른 조회용) |

### 6.4 parent_id vs prerequisites 차이

| 관계 | 용도 | 예시 |
|------|------|------|
| **parent_id** | 같은 계열 내 계층 구조 | E4-NUM-02.parent = E4-NUM-01 (억→만) |
| **prerequisites** | 학습 선수관계 (크로스학년 가능) | M1-ALG-01.prereqs = [E5-ALG-01, M1-NUM-04] |

---

## 7. 백엔드 구현

### 7.1 시드 데이터 (seed_concepts.py)

- 128개 개념 정의 (E4~H1)
- 156개 선수관계 정의
- 11개 CROSS_GRADE_CHAINS 명시
- `get_prerequisite_chain(concept_id)`: 재귀적 전이적 폐포(transitive closure) 반환

```python
# 사용 예시
chain = get_prerequisite_chain("H1-ALG-08")
# → ["M3-ALG-03", "M3-ALG-02", "M3-ALG-01", "M2-ALG-02", "M2-ALG-01",
#     "M1-ALG-01", "E5-ALG-01", "E4-ALG-01", "M3-NUM-02", "M3-NUM-01",
#     "M1-NUM-04", "M1-NUM-03", "E6-NUM-03", ...]
```

### 7.2 API 엔드포인트 (questions.py)

| 엔드포인트 | 메서드 | 계통수학 활용 |
|-----------|--------|-------------|
| `/api/v1/questions` | POST | prerequisite_concept_ids 저장 |
| `/api/v1/questions/batch` | POST | concept_id 유효성 검증 후 일괄 저장 |
| `/api/v1/questions/by-concept/{id}` | GET | 개념별 문제 조회 |
| `/api/v1/questions/stats` | GET | 개념별 문제 수 통계 |

### 7.3 적응형 서비스 (adaptive_service.py)

- `determine_initial_difficulty()`: 학생의 **개념별 정확도**로 시작 난이도 산출
- `_get_concept_accuracy()`: `AnswerLog` + `Question.concept_id` 기반 정확도 쿼리
- 현재는 난이도 1~10 조절에 집중, **선수개념 마스터리 체크는 설계 완료 / 구현 예정**

### 7.4 AI 프롬프트 (prompt_builder.py, exam_prep_strategy_agent.py)

- 고등학교 문제 분석 시 `get_prerequisite_if_high_school()`로 중학교 선수관계 자동 주입
- 시험 대비 전략에서 50% 이하 학생에게 중학교 선수개념 복습 추천

---

## 8. 프론트엔드 구현

### 8.1 타입 정의

```typescript
// types/index.ts
interface Concept {
  prerequisite_ids?: string[]      // 계통수학 체인
}

interface Question {
  prerequisite_concept_ids?: string[]  // 선수 개념 ID 목록
}
```

### 8.2 문제 생성 → DB 저장 파이프라인

```typescript
// 1. 템플릿에서 문제 생성
const questions = generateQuestions(request, templates)

// 2. 백엔드에 일괄 저장
const saved = await saveQuestionsBatch(questions)
```

### 8.3 템플릿 커버리지

| 파일 | 개념 수 | 템플릿 수 | 커버 |
|------|--------|----------|------|
| elementary4.ts | 23 | ~50 | 100% |
| elementary5.ts | 24 | ~48 | 100% |
| elementary6.ts | 16 | ~30 | 100% |
| middle1.ts | 11 | ~22 | 100% |
| middle2.ts | 9 | ~18 | 100% |
| middle3.ts | 10 | ~20 | 100% |
| high1.ts | 35 | - | 미작성 |

---

## 9. 적응형 학습과 계통수학 연계

### 9.1 현재 구현

```
학생이 문제를 풂
  → AnswerLog에 기록
    → concept_id별 정확도 계산
      → 정확도 기반 난이도 조절 (±1~2)
```

### 9.2 설계된 미래 구현 (adaptive-learning-specialist 에이전트 설계)

```
학생이 개념 C를 학습 시작
  → C의 선수개념 prerequisites 조회
    → 각 선수개념의 마스터리(정확도) 확인
      → 마스터리 < 70%인 선수개념 발견
        → 해당 선수개념부터 복습 안내
        → 선수개념 마스터리 70% 달성 후 C 진입
```

### 9.3 약점 진단 시나리오

| 학생 상태 | 시스템 대응 |
|----------|-----------|
| H1-ALG-08 (판별식) 오답률 높음 | M3-ALG-03 (이차방정식) 마스터리 확인 |
| M3-ALG-03도 낮음 | M3-ALG-02 (인수분해) → M3-ALG-01 (곱셈공식) 순으로 추적 |
| 근본 원인 발견: M2-ALG-02 (다항식 연산) 부족 | M2-ALG-02부터 재학습 안내 |

---

## 10. 관련 파일 인덱스

### 데이터

| 파일 | 역할 |
|------|------|
| `backend/app/data/seed_concepts.py` | 128개 개념 + 156개 선수관계 마스터 소스 |
| `backend/app/data/seed_db.py` | DB 시딩 스크립트 |

### 모델 / 스키마

| 파일 | 역할 |
|------|------|
| `backend/app/models/concept.py` | Concept 모델 + concept_prerequisites 테이블 |
| `backend/app/models/question.py` | Question 모델 (prerequisite_concept_ids) |
| `backend/app/schemas/test.py` | ConceptResponse, QuestionCreate 등 스키마 |
| `backend/app/schemas/common.py` | Grade, ProblemPart 등 공통 Enum |

### API / 서비스

| 파일 | 역할 |
|------|------|
| `backend/app/api/v1/questions.py` | 문제 CRUD API |
| `backend/app/services/adaptive_service.py` | 난이도 적응 서비스 |
| `backend/app/services/prompt_builder.py` | AI 프롬프트 선수관계 주입 |
| `backend/app/services/agents/exam_prep_strategy_agent.py` | 시험 대비 선수학습 진단 |

### 프론트엔드

| 파일 | 역할 |
|------|------|
| `frontend/src/types/index.ts` | Concept, Question 타입 (prerequisite_ids) |
| `frontend/src/services/questionService.ts` | 문제 생성→DB 파이프라인 |
| `frontend/src/services/questionGenerator/templates/*.ts` | 학년별 문제 템플릿 |

### 문서

| 파일 | 역할 |
|------|------|
| `docs/work-plans/systematic-math-connection-guide.md` | 계통수학 철학 및 4대 영역 가이드 |
| `docs/work-plans/concept-coverage-report.md` | 개념 커버리지 분석 |
| `docs/work-plans/remaining-work-report.md` | 잔여 작업 현황 |
| `reports/math-concepts-full.md` | 전체 개념 참조 문서 |

---

## 11. 향후 과제

| 우선순위 | 과제 | 설명 |
|---------|------|------|
| 1 | 고1 (H1) 템플릿 작성 | 35개 개념에 대한 문제 템플릿 미작성 |
| 2 | 선수개념 마스터리 체크 구현 | adaptive_service에 prerequisite mastery gate 추가 |
| 3 | 학습 경로 시각화 UI | 프론트엔드에 계통수학 트리맵 / 학습 진도 표시 |
| 4 | 약점 자동 진단 API | 학생 오답 패턴에서 선수개념 결손 자동 추적 |
| 5 | 초1~초3 개념 확장 | 현재 E4부터만 정의, 하위 학년 추가 시 체인 연장 |
