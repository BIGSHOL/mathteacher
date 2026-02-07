import { answerToString, makeDistractors } from '../distractors'
import type { Answer, Fraction, Params } from '../types'

describe('answerToString', () => {
  it('정수를 문자열로 변환한다', () => {
    expect(answerToString(42)).toBe('42')
  })

  it('음수 정수를 문자열로 변환한다', () => {
    expect(answerToString(-7)).toBe('-7')
  })

  it('소수를 반올림하여 문자열로 변환한다', () => {
    expect(answerToString(3.14159)).toBe('3.14')
  })

  it('0은 "0"으로 변환한다', () => {
    expect(answerToString(0)).toBe('0')
  })

  it('문자열은 그대로 반환한다', () => {
    expect(answerToString('x = 5')).toBe('x = 5')
  })

  it('빈 문자열은 그대로 반환한다', () => {
    expect(answerToString('')).toBe('')
  })

  it('분수를 "분자/분모" 형식으로 변환한다', () => {
    const fraction: Fraction = { numerator: 3, denominator: 4 }
    expect(answerToString(fraction)).toBe('3/4')
  })

  it('분모가 1인 분수는 정수로 변환한다', () => {
    const fraction: Fraction = { numerator: 5, denominator: 1 }
    expect(answerToString(fraction)).toBe('5')
  })

  it('분자가 0인 분수는 "0"으로 변환한다', () => {
    const fraction: Fraction = { numerator: 0, denominator: 7 }
    expect(answerToString(fraction)).toBe('0')
  })

  it('음수 분수를 올바르게 변환한다', () => {
    const fraction: Fraction = { numerator: -2, denominator: 3 }
    expect(answerToString(fraction)).toBe('-2/3')
  })
})

describe('makeDistractors', () => {
  const params: Params = {
    a: 5,
    b: 3,
    c: 0,
    d: 0,
    e: 0,
    x: 0,
    y: 0,
    n: 0,
    variant: 0,
    total: 0,
    px: 0,
    py: 0,
  }

  it('요청한 개수만큼 오답을 생성한다', () => {
    const answer: Answer = 8
    const distractorFns = [
      (p: Params) => (p.a ?? 0) - (p.b ?? 0),
      (p: Params) => (p.a ?? 0) * (p.b ?? 0),
      (p: Params) => (p.a ?? 0) / (p.b ?? 0),
    ]

    const result = makeDistractors(params, answer, distractorFns, 3)
    expect(result.length).toBe(3)
  })

  it('정답과 중복되지 않는 오답을 생성한다', () => {
    const answer: Answer = 8
    const distractorFns = [
      (p: Params) => (p.a ?? 0) - (p.b ?? 0),
      (p: Params) => (p.a ?? 0) * (p.b ?? 0),
    ]

    const result = makeDistractors(params, answer, distractorFns, 3)
    expect(result).not.toContain('8')
  })

  it('오답끼리 중복되지 않는다', () => {
    const answer: Answer = 8
    const distractorFns = [
      (p: Params) => (p.a ?? 0) - (p.b ?? 0),
      (p: Params) => (p.a ?? 0) * (p.b ?? 0),
    ]

    const result = makeDistractors(params, answer, distractorFns, 3)
    const uniqueResults = new Set(result)
    expect(uniqueResults.size).toBe(result.length)
  })

  it('distractorFns가 부족하면 ±offset으로 채운다', () => {
    const answer: Answer = 10
    const distractorFns = [(p: Params) => (p.a ?? 0) * 2] // 한 개만

    const result = makeDistractors(params, answer, distractorFns, 3)
    expect(result.length).toBe(3)
    // 10이 아닌 다른 값들
    expect(result).not.toContain('10')
  })

  it('빈 distractorFns 배열이어도 작동한다', () => {
    const answer: Answer = 7
    const distractorFns: ((p: Params) => Answer)[] = []

    const result = makeDistractors(params, answer, distractorFns, 3)
    expect(result.length).toBe(3)
    expect(result).not.toContain('7')
  })

  it('문자열 답에 대해 기본 오답 세트를 사용한다', () => {
    const answer: Answer = '정답입니다'
    const distractorFns: ((p: Params) => Answer)[] = []

    const result = makeDistractors(params, answer, distractorFns, 3)
    expect(result.length).toBe(3)
    expect(result).not.toContain('정답입니다')
  })

  it('분수 답에 대해 오답을 생성한다', () => {
    const answer: Fraction = { numerator: 1, denominator: 2 }
    const distractorFns = [
      () => ({ numerator: 1, denominator: 3 } as Fraction),
      () => ({ numerator: 2, denominator: 3 } as Fraction),
    ]

    const result = makeDistractors(params, answer, distractorFns, 2)
    expect(result.length).toBe(2)
    expect(result).not.toContain('1/2')
  })

  it('distractorFn에서 에러가 발생해도 계속 진행한다', () => {
    const answer: Answer = 5
    const distractorFns = [
      () => {
        throw new Error('Test error')
      },
      (p: Params) => (p.a ?? 0) + 1,
      (p: Params) => (p.a ?? 0) - 1,
    ]

    const result = makeDistractors(params, answer, distractorFns, 2)
    expect(result.length).toBe(2)
  })

  it('count가 0이면 빈 배열을 반환한다', () => {
    const answer: Answer = 10
    const distractorFns = [(p: Params) => (p.a ?? 0) * 2]

    const result = makeDistractors(params, answer, distractorFns, 0)
    expect(result).toEqual([])
  })

  it('빈 문자열 오답은 제외한다', () => {
    const answer: Answer = 'valid'
    const distractorFns = [
      () => '',
      () => 'distractor1',
      () => 'distractor2',
    ]

    const result = makeDistractors(params, answer, distractorFns, 2)
    expect(result).not.toContain('')
  })

  it('정답과 동일한 오답은 제외한다', () => {
    const answer: Answer = 42
    const distractorFns = [
      () => 42, // 정답과 같음
      () => 43,
      () => 41,
    ]

    const result = makeDistractors(params, answer, distractorFns, 2)
    expect(result.filter((d) => d === '42').length).toBe(0)
  })

  it('숫자 답이 소수인 경우도 처리한다', () => {
    const answer: Answer = 3.5
    const distractorFns = [() => 2.5, () => 4.5]

    const result = makeDistractors(params, answer, distractorFns, 2)
    expect(result.length).toBe(2)
    expect(result).not.toContain('3.5')
  })
})
