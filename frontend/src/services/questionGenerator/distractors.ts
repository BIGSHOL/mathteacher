// 오답 보기(Distractor) 생성 모듈

import type { Answer, Fraction, Params } from './types'
import { fractionToString } from './utils/math'

/** Answer를 숫자로 변환 (가능한 경우) */
function answerToNumber(a: Answer): number | null {
  if (typeof a === 'number') return a
  if (typeof a === 'string') {
    const n = Number(a)
    return isNaN(n) ? null : n
  }
  // Fraction: 소수로 변환
  return (a as Fraction).numerator / (a as Fraction).denominator
}

/** Answer를 문자열로 변환 */
export function answerToString(a: Answer): string {
  if (typeof a === 'number') {
    return Number.isInteger(a) ? `${a}` : `${Math.round(a * 100) / 100}`
  }
  if (typeof a === 'string') return a
  return fractionToString(a as Fraction)
}

/**
 * 오답 보기 생성.
 * distractorFns로 먼저 시도하고, 부족하면 ±1, ±2 등으로 채움.
 * 정답과 중복 없이 count개를 반환.
 */
export function makeDistractors(
  params: Params,
  answer: Answer,
  distractorFns: ((params: Params, answer: Answer) => Answer)[],
  count = 3
): string[] {
  const correctStr = answerToString(answer)
  const distractors = new Set<string>()

  // 1단계: distractorFns로 생성
  for (const fn of distractorFns) {
    try {
      const d = fn(params, answer)
      const ds = answerToString(d)
      if (ds !== correctStr && ds !== '') {
        distractors.add(ds)
      }
    } catch {
      // 생성 실패 무시
    }
    if (distractors.size >= count) break
  }

  // 2단계: 숫자 답인 경우 ±offset으로 채움
  const numAnswer = answerToNumber(answer)
  if (numAnswer !== null && distractors.size < count) {
    let offset = 1
    while (distractors.size < count && offset <= 20) {
      for (const delta of [offset, -offset]) {
        const candidate = Number.isInteger(numAnswer)
          ? `${numAnswer + delta}`
          : `${Math.round((numAnswer + delta) * 100) / 100}`
        if (candidate !== correctStr) {
          distractors.add(candidate)
        }
      }
      offset++
    }
  }

  // 3단계: 문자열 답인 경우 기본 오답 세트
  if (distractors.size < count) {
    const fallbacks = ['알 수 없다', '해 없음', '무한', '0']
    for (const f of fallbacks) {
      if (f !== correctStr) distractors.add(f)
      if (distractors.size >= count) break
    }
  }

  return Array.from(distractors).slice(0, count)
}
