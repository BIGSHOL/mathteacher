// 수학 유틸리티 함수

import type { Fraction } from '../types'

/** 최대공약수 */
export function gcd(a: number, b: number): number {
  a = Math.abs(a)
  b = Math.abs(b)
  while (b) {
    ;[a, b] = [b, a % b]
  }
  return a
}

/** 최소공배수 */
export function lcm(a: number, b: number): number {
  return Math.abs(a * b) / gcd(a, b)
}

/** 분수 기약 */
export function simplifyFraction(num: number, den: number): Fraction {
  if (den === 0) throw new Error('0으로 나눌 수 없습니다')
  const sign = den < 0 ? -1 : 1
  const g = gcd(Math.abs(num), Math.abs(den))
  return {
    numerator: (sign * num) / g,
    denominator: (sign * den) / g,
  }
}

/** 분수를 문자열로 */
export function fractionToString(f: Fraction): string {
  if (f.denominator === 1) return `${f.numerator}`
  if (f.numerator === 0) return '0'
  return `${f.numerator}/${f.denominator}`
}

/** 분수 덧셈 */
export function addFractions(a: Fraction, b: Fraction): Fraction {
  const num = a.numerator * b.denominator + b.numerator * a.denominator
  const den = a.denominator * b.denominator
  return simplifyFraction(num, den)
}

/** 분수 뺄셈 */
export function subtractFractions(a: Fraction, b: Fraction): Fraction {
  const num = a.numerator * b.denominator - b.numerator * a.denominator
  const den = a.denominator * b.denominator
  return simplifyFraction(num, den)
}

/** 분수 곱셈 */
export function multiplyFractions(a: Fraction, b: Fraction): Fraction {
  return simplifyFraction(a.numerator * b.numerator, a.denominator * b.denominator)
}

/** 분수 나눗셈 */
export function divideFractions(a: Fraction, b: Fraction): Fraction {
  if (b.numerator === 0) throw new Error('0으로 나눌 수 없습니다')
  return simplifyFraction(a.numerator * b.denominator, a.denominator * b.numerator)
}

/** 숫자를 부호 포함 문자열로 (양수면 그대로, 음수면 괄호) */
export function signedStr(n: number): string {
  return n < 0 ? `(${n})` : `${n}`
}

/** 분수를 부호 포함 문자열로 */
export function signedFractionStr(f: Fraction): string {
  const s = fractionToString(f)
  return f.numerator < 0 ? `(${s})` : s
}
