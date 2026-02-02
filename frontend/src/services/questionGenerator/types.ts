// 문제 생성 엔진 타입 정의

import type { Grade, ProblemPart, QuestionCategory, QuestionOption } from '../../types'

/** 템플릿 파라미터 범위: [min, max] (정수) */
export type ParamRange = [number, number]

/** 분수를 표현하는 타입 */
export interface Fraction {
  numerator: number
  denominator: number
}

/** 생성된 답 (정수, 분수, 문자열 모두 가능) */
export type Answer = number | string | Fraction

/**
 * 파라미터 맵.
 * 템플릿에서 자주 사용하는 키를 명시하여 noUncheckedIndexedAccess 호환.
 * generateParams가 paramRanges의 모든 키를 채우므로 접근은 항상 안전함.
 */
export interface Params {
  a: number; b: number; c: number; d: number; e: number
  x: number; y: number; n: number; variant: number
  total: number; px: number; py: number
  [key: string]: number
}

/**
 * 문제 템플릿 정의.
 * 각 학년 × 트랙 × 레벨별로 여러 템플릿이 존재할 수 있다.
 */
export interface QuestionTemplate {
  id: string
  grade: Grade
  category: QuestionCategory
  level: number // 1-10
  /** 6대 영역: calc, algebra, func, geo, data, word */
  part: ProblemPart
  /** 개념 ID (예: "E1-NUM-04", "M1-ALG-03") */
  conceptId: string
  /** 문제 내용 패턴 (예: "{a} + {b}") */
  pattern: string
  /** 파라미터 범위 */
  paramRanges: Record<string, ParamRange>
  /** 파라미터 제약 조건 (true면 유효) */
  constraints?: (params: Params) => boolean
  /** 정답 계산 함수 */
  answerFn: (params: Params) => Answer
  /** 문제 내용 포맷 함수 (pattern 대신 사용 가능) */
  contentFn?: (params: Params) => string
  /** 오답 보기 생성 함수 */
  distractorFns: ((params: Params, answer: Answer) => Answer)[]
  /** 풀이 설명 생성 함수 */
  explanationFn: (params: Params, answer: Answer) => string
  /** 문제 유형 (기본: multiple_choice) */
  questionType?: 'multiple_choice' | 'short_answer'
  /** 배점 (기본: 10) */
  points?: number
}

/** 문제 생성 요청 */
export interface GenerateRequest {
  grade: Grade
  category: QuestionCategory
  level: number
  /** 생성할 문제 수 (기본: 1) */
  count?: number
}

/** 생성된 문제 (프론트엔드 Question 타입과 호환) */
export interface GeneratedQuestion {
  id: string
  concept_id: string
  category: QuestionCategory
  part: ProblemPart
  question_type: 'multiple_choice' | 'short_answer'
  difficulty: number
  content: string
  options: QuestionOption[]
  correct_answer: string
  explanation: string
  points: number
}
