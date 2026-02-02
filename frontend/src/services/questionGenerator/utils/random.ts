// 랜덤 파라미터 생성 유틸리티

import type { Params, ParamRange } from '../types'

/** min 이상 max 이하 정수 랜덤 */
export function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

/** 배열에서 랜덤 선택 */
export function randChoice<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]!
}

/** 배열 셔플 (Fisher-Yates) */
export function shuffle<T>(arr: T[]): T[] {
  const result = [...arr]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[result[i], result[j]] = [result[j]!, result[i]!]
  }
  return result
}

/**
 * 파라미터 범위로부터 랜덤 파라미터 맵 생성.
 * constraints가 있으면 만족할 때까지 재시도 (최대 100회).
 */
export function generateParams(
  ranges: Record<string, ParamRange>,
  constraints?: (params: Params) => boolean,
  maxRetries = 100
): Params {
  for (let i = 0; i < maxRetries; i++) {
    const params = {} as Params
    for (const [key, [min, max]] of Object.entries(ranges)) {
      params[key] = randInt(min, max)
    }
    if (!constraints || constraints(params)) {
      return params
    }
  }
  // 제약 조건 만족 실패 시 범위 중간값 반환
  const fallback = {} as Params
  for (const [key, [min, max]] of Object.entries(ranges)) {
    fallback[key] = Math.floor((min + max) / 2)
  }
  return fallback
}

/** UUID v4 생성 (간이) */
export function uuid(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}
