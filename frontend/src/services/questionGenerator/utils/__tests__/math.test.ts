import {
  gcd,
  lcm,
  simplifyFraction,
  fractionToString,
  addFractions,
  subtractFractions,
  multiplyFractions,
  divideFractions,
  signedStr,
  signedFractionStr,
} from '../math'
import type { Fraction } from '../../types'

describe('gcd', () => {
  it('12와 8의 최대공약수는 4이다', () => {
    expect(gcd(12, 8)).toBe(4)
  })

  it('7과 13의 최대공약수는 1이다 (서로소)', () => {
    expect(gcd(7, 13)).toBe(1)
  })

  it('0과 5의 최대공약수는 5이다', () => {
    expect(gcd(0, 5)).toBe(5)
  })

  it('5와 0의 최대공약수는 5이다', () => {
    expect(gcd(5, 0)).toBe(5)
  })

  it('음수를 절댓값으로 처리한다', () => {
    expect(gcd(-12, 8)).toBe(4)
    expect(gcd(12, -8)).toBe(4)
    expect(gcd(-12, -8)).toBe(4)
  })

  it('같은 수의 최대공약수는 그 수이다', () => {
    expect(gcd(15, 15)).toBe(15)
  })
})

describe('lcm', () => {
  it('4와 6의 최소공배수는 12이다', () => {
    expect(lcm(4, 6)).toBe(12)
  })

  it('3과 3의 최소공배수는 3이다', () => {
    expect(lcm(3, 3)).toBe(3)
  })

  it('1과 어떤 수의 최소공배수는 그 수이다', () => {
    expect(lcm(1, 7)).toBe(7)
    expect(lcm(9, 1)).toBe(9)
  })

  it('음수를 절댓값으로 처리한다', () => {
    expect(lcm(-4, 6)).toBe(12)
    expect(lcm(4, -6)).toBe(12)
  })
})

describe('simplifyFraction', () => {
  it('6/8을 기약분수 3/4로 간소화한다', () => {
    const result = simplifyFraction(6, 8)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(4)
  })

  it('분모가 음수면 부호를 분자로 옮긴다', () => {
    const result = simplifyFraction(3, -4)
    expect(result.numerator).toBe(-3)
    expect(result.denominator).toBe(4)
  })

  it('분자와 분모가 모두 음수면 양수가 된다', () => {
    const result = simplifyFraction(-6, -8)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(4)
  })

  it('분자가 0이면 0/1로 간소화한다', () => {
    const result = simplifyFraction(0, 5)
    expect(result.numerator).toBe(0)
    expect(result.denominator).toBe(1)
  })

  it('이미 기약분수인 경우 그대로 반환한다', () => {
    const result = simplifyFraction(3, 7)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(7)
  })

  it('분모가 0이면 에러를 발생시킨다', () => {
    expect(() => simplifyFraction(5, 0)).toThrow('0으로 나눌 수 없습니다')
  })
})

describe('fractionToString', () => {
  it('분모가 1이면 분자만 반환한다', () => {
    const fraction: Fraction = { numerator: 5, denominator: 1 }
    expect(fractionToString(fraction)).toBe('5')
  })

  it('분자가 0이면 "0"을 반환한다', () => {
    const fraction: Fraction = { numerator: 0, denominator: 7 }
    expect(fractionToString(fraction)).toBe('0')
  })

  it('일반적인 분수는 "분자/분모" 형식으로 반환한다', () => {
    const fraction: Fraction = { numerator: 3, denominator: 4 }
    expect(fractionToString(fraction)).toBe('3/4')
  })

  it('음수 분수를 올바르게 표현한다', () => {
    const fraction: Fraction = { numerator: -3, denominator: 4 }
    expect(fractionToString(fraction)).toBe('-3/4')
  })
})

describe('addFractions', () => {
  it('1/2 + 1/3 = 5/6', () => {
    const a: Fraction = { numerator: 1, denominator: 2 }
    const b: Fraction = { numerator: 1, denominator: 3 }
    const result = addFractions(a, b)
    expect(result.numerator).toBe(5)
    expect(result.denominator).toBe(6)
  })

  it('분모가 같은 분수를 더한다', () => {
    const a: Fraction = { numerator: 1, denominator: 4 }
    const b: Fraction = { numerator: 2, denominator: 4 }
    const result = addFractions(a, b)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(4)
  })

  it('결과를 기약분수로 반환한다', () => {
    const a: Fraction = { numerator: 1, denominator: 2 }
    const b: Fraction = { numerator: 1, denominator: 2 }
    const result = addFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(1)
  })

  it('음수 분수를 더한다', () => {
    const a: Fraction = { numerator: 1, denominator: 2 }
    const b: Fraction = { numerator: -1, denominator: 3 }
    const result = addFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(6)
  })
})

describe('subtractFractions', () => {
  it('1/2 - 1/3 = 1/6', () => {
    const a: Fraction = { numerator: 1, denominator: 2 }
    const b: Fraction = { numerator: 1, denominator: 3 }
    const result = subtractFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(6)
  })

  it('같은 분수를 빼면 0이 된다', () => {
    const a: Fraction = { numerator: 3, denominator: 4 }
    const b: Fraction = { numerator: 3, denominator: 4 }
    const result = subtractFractions(a, b)
    expect(result.numerator).toBe(0)
  })

  it('결과를 기약분수로 반환한다', () => {
    const a: Fraction = { numerator: 3, denominator: 4 }
    const b: Fraction = { numerator: 1, denominator: 4 }
    const result = subtractFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(2)
  })
})

describe('multiplyFractions', () => {
  it('2/3 × 3/4 = 1/2', () => {
    const a: Fraction = { numerator: 2, denominator: 3 }
    const b: Fraction = { numerator: 3, denominator: 4 }
    const result = multiplyFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(2)
  })

  it('분수에 0을 곱하면 0이 된다', () => {
    const a: Fraction = { numerator: 5, denominator: 7 }
    const b: Fraction = { numerator: 0, denominator: 1 }
    const result = multiplyFractions(a, b)
    expect(result.numerator).toBe(0)
  })

  it('결과를 기약분수로 반환한다', () => {
    const a: Fraction = { numerator: 2, denominator: 5 }
    const b: Fraction = { numerator: 5, denominator: 6 }
    const result = multiplyFractions(a, b)
    expect(result.numerator).toBe(1)
    expect(result.denominator).toBe(3)
  })

  it('음수 분수를 곱한다', () => {
    const a: Fraction = { numerator: -2, denominator: 3 }
    const b: Fraction = { numerator: 3, denominator: 4 }
    const result = multiplyFractions(a, b)
    expect(result.numerator).toBe(-1)
    expect(result.denominator).toBe(2)
  })
})

describe('divideFractions', () => {
  it('1/2 ÷ 1/3 = 3/2', () => {
    const a: Fraction = { numerator: 1, denominator: 2 }
    const b: Fraction = { numerator: 1, denominator: 3 }
    const result = divideFractions(a, b)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(2)
  })

  it('분수를 1로 나누면 그대로이다', () => {
    const a: Fraction = { numerator: 3, denominator: 4 }
    const b: Fraction = { numerator: 1, denominator: 1 }
    const result = divideFractions(a, b)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(4)
  })

  it('0으로 나누면 에러를 발생시킨다', () => {
    const a: Fraction = { numerator: 3, denominator: 4 }
    const b: Fraction = { numerator: 0, denominator: 1 }
    expect(() => divideFractions(a, b)).toThrow('0으로 나눌 수 없습니다')
  })

  it('결과를 기약분수로 반환한다', () => {
    const a: Fraction = { numerator: 2, denominator: 3 }
    const b: Fraction = { numerator: 4, denominator: 9 }
    const result = divideFractions(a, b)
    expect(result.numerator).toBe(3)
    expect(result.denominator).toBe(2)
  })
})

describe('signedStr', () => {
  it('양수는 괄호 없이 반환한다', () => {
    expect(signedStr(5)).toBe('5')
  })

  it('음수는 괄호로 감싼다', () => {
    expect(signedStr(-3)).toBe('(-3)')
  })

  it('0은 괄호 없이 반환한다', () => {
    expect(signedStr(0)).toBe('0')
  })
})

describe('signedFractionStr', () => {
  it('양수 분수는 괄호 없이 반환한다', () => {
    const fraction: Fraction = { numerator: 3, denominator: 4 }
    expect(signedFractionStr(fraction)).toBe('3/4')
  })

  it('음수 분수는 괄호로 감싼다', () => {
    const fraction: Fraction = { numerator: -3, denominator: 4 }
    expect(signedFractionStr(fraction)).toBe('(-3/4)')
  })

  it('0은 괄호 없이 반환한다', () => {
    const fraction: Fraction = { numerator: 0, denominator: 1 }
    expect(signedFractionStr(fraction)).toBe('0')
  })

  it('분모가 1인 양수는 정수로 표현한다', () => {
    const fraction: Fraction = { numerator: 5, denominator: 1 }
    expect(signedFractionStr(fraction)).toBe('5')
  })

  it('분모가 1인 음수는 괄호로 감싼 정수로 표현한다', () => {
    const fraction: Fraction = { numerator: -5, denominator: 1 }
    expect(signedFractionStr(fraction)).toBe('(-5)')
  })
})
