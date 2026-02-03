// 중1 (middle_1) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import { signedStr } from '../utils/math'

const G = 'middle_1' as const

// Helper: gcd for template closures
function gcdHelper(a: number, b: number): number {
  a = Math.abs(a)
  b = Math.abs(b)
  while (b) {
    ;[a, b] = [b, a % b]
  }
  return a || 1
}

// Helper: lcm
function lcmHelper(a: number, b: number): number {
  return Math.abs(a * b) / gcdHelper(a, b)
}

// Helper: 소수 판별
function isPrime(n: number): boolean {
  if (n < 2) return false
  if (n === 2) return true
  if (n % 2 === 0) return false
  for (let i = 3; i * i <= n; i += 2) {
    if (n % i === 0) return false
  }
  return true
}

// Helper: 소인수분해 결과 객체 (p^a × q^b 형태)
function primeFactorize(n: number): Map<number, number> {
  const factors = new Map<number, number>()
  let temp = n
  for (let i = 2; i * i <= temp; i++) {
    while (temp % i === 0) {
      factors.set(i, (factors.get(i) || 0) + 1)
      temp /= i
    }
  }
  if (temp > 1) factors.set(temp, 1)
  return factors
}

// Helper: 소인수분해 문자열 표현
function primeFactorString(n: number): string {
  const factors = primeFactorize(n)
  const parts: string[] = []
  for (const [p, exp] of Array.from(factors.entries()).sort((a, b) => a[0] - b[0])) {
    if (exp === 1) {
      parts.push(`${p}`)
    } else {
      parts.push(`${p}^${exp}`)
    }
  }
  return parts.join(' × ')
}

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 소인수분해 기본 (Phase A1)
  {
    id: 'm1-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { n: [2, 30] },
    contentFn: (_p) => `다음 중 소수인 것은?`,
    answerFn: ({ n }) => {
      // n 근처의 소수 찾기
      for (let i = n; i <= 50; i++) {
        if (isPrime(i)) return i
      }
      return 2
    },
    distractorFns: [
      ({ n }) => {
        // 합성수 찾기
        for (let i = n; i <= 50; i++) {
          if (!isPrime(i) && i > 1) return i
        }
        return 4
      },
      () => 1, // 1은 소수가 아님 (흔한 오답)
      ({ n }) => {
        // 짝수 (소수가 아닌)
        const even = n % 2 === 0 ? n : n + 1
        return even > 2 ? even : 4
      },
    ],
    explanationFn: (_params, ans) => {
      const num = ans as number
      if (isPrime(num)) {
        return `소수는 1과 자기 자신만을 약수로 가지는 1보다 큰 자연수입니다.\n${num}은(는) 소수입니다.\n참고: 1은 소수가 아닙니다.`
      }
      return `소수 판별 중 오류가 발생했습니다.`
    },
  },
  {
    id: 'm1-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { n: [12, 100] },
    constraints: ({ n }) => !isPrime(n) && n > 1,
    contentFn: ({ n }) => `${n}을(를) 소인수분해하시오.`,
    answerFn: ({ n }) => primeFactorString(n),
    distractorFns: [
      ({ n }) => {
        // 잘못된 지수
        const factors = primeFactorize(n)
        const parts: string[] = []
        for (const [p, exp] of Array.from(factors.entries()).sort((a, b) => a[0] - b[0])) {
          parts.push(`${p}^${exp + 1}`)
        }
        return parts.join(' × ')
      },
      ({ n }) => `${n}`,
      ({ n }) => {
        // 일부만 분해
        const factors = Array.from(primeFactorize(n).entries())
        if (factors.length > 1) {
          const [p] = factors[0]!
          return `${p} × ${n / p}`
        }
        return `${n}`
      },
    ],
    explanationFn: ({ n }, ans) =>
      `소인수분해 공식에 의해 ${n}을 소인수의 거듭제곱으로 나타내면:\n${n} = ${ans}`,
  },

  // Lv.2: 약수/배수 개념 (Phase A1)
  {
    id: 'm1-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 4], b: [1, 3] },
    contentFn: ({ a, b }) => {
      const base1 = 2
      const base2 = 3
      return `${base1}^${a} × ${base2}^${b}의 약수의 개수는?`
    },
    answerFn: ({ a, b }) => (a + 1) * (b + 1),
    distractorFns: [
      ({ a, b }) => a * b, // 잘못된 공식
      ({ a, b }) => a + b,
      ({ a, b }) => (a + 1) * b, // 일부만 적용
    ],
    explanationFn: ({ a, b }, ans) => {
      const num = Math.pow(2, a) * Math.pow(3, b)
      return `약수 개수 공식: N = p^a × q^b일 때 약수의 개수는 (a+1)(b+1)\n` +
        `2^${a} × 3^${b} = ${num}의 약수의 개수 = (${a}+1)(${b}+1) = ${ans}`
    },
  },
  {
    id: 'm1-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { a: [6, 24], b: [8, 30] },
    constraints: ({ a, b }) => a !== b && gcdHelper(a, b) > 1,
    contentFn: ({ a, b }) => `두 수 ${a}와 ${b}의 최대공약수는?`,
    answerFn: ({ a, b }) => gcdHelper(a, b),
    distractorFns: [
      ({ a, b }) => lcmHelper(a, b), // GCD와 LCM 혼동
      ({ a, b }) => a * b,
      ({ a, b }) => Math.min(a, b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `최대공약수(GCD)는 두 수의 공통 약수 중 가장 큰 수입니다.\n` +
      `${a}와 ${b}의 최대공약수 = ${ans}`,
  },

  // Lv.3: 음수 포함 덧셈
  {
    id: 'm1-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) + ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a + b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => -(a + b),
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 덧셈 규칙:\n(${-a}) + ${b} = ${b} - ${a} = ${ans}`,
  },
  {
    id: 'm1-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `${a} + (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => a + (-b),
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => -(a - b),
      (_, ans) => (ans as number) - 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 덧셈 규칙:\n${a} + (${-b}) = ${a} - ${b} = ${ans}`,
  },

  // Lv.4: 음수 뺄셈
  {
    id: 'm1-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) - (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => -a - (-b),
    distractorFns: [
      ({ a, b }) => -(a + b),
      ({ a, b }) => a - b,
      ({ a, b }) => -(a - b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 뺄셈 규칙 (빼기는 더하기로):\n(${-a}) - (${-b}) = -${a} + ${b} = ${ans}`,
  },
  {
    id: 'm1-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) - ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a - b,
    distractorFns: [
      ({ a, b }) => -a + b,
      ({ a, b }) => a - b,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 뺄셈 규칙:\n(${-a}) - ${b} = -(${a} + ${b}) = ${ans}`,
  },

  // Lv.5: 정수 곱셈
  {
    id: 'm1-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-a}) × ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a * b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => -(a + b),
      (_, ans) => (ans as number) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 곱셈 규칙 (음수 × 양수 = 음수):\n(${-a}) × ${b} = -(${a} × ${b}) = ${ans}`,
  },
  {
    id: 'm1-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-a}) × (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => -(a * b),
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `음수의 곱셈 규칙 (음수 × 음수 = 양수):\n(${-a}) × (${-b}) = ${a} × ${b} = ${ans}`,
  },

  // Lv.6: 정수 나눗셈
  {
    id: 'm1-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-(a * b)}) ÷ ${a} 의 값은?`,
    answerFn: ({ b }) => -b,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => -(a * b),
      ({ a }) => -a,
    ],
    explanationFn: ({ a, b }) =>
      `음수의 나눗셈 규칙 (음수 ÷ 양수 = 음수):\n(${-(a * b)}) ÷ ${a} = ${-b}`,
  },
  {
    id: 'm1-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-(a * b)}) ÷ (${-a}) 의 값은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ b }) => -b,
      ({ a, b }) => a * b,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }) =>
      `음수의 나눗셈 규칙 (음수 ÷ 음수 = 양수):\n(${-(a * b)}) ÷ (${-a}) = ${b}`,
  },

  // Lv.7: 정수 혼합 연산
  {
    id: 'm1-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 7], b: [2, 7], c: [-10, 10] },
    constraints: ({ c }) => c !== 0,
    contentFn: ({ a, b, c }) =>
      `(${-a}) × (${-b}) + ${signedStr(c)} 의 값은?`,
    answerFn: ({ a, b, c }) => a * b + c,
    distractorFns: [
      ({ a, b, c }) => -(a * b) + c,
      ({ a, b, c }) => a * b - c,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `혼합 연산 순서 (곱셈 먼저):\n(${-a}) × (${-b}) + ${signedStr(c)} = ${a * b} + ${signedStr(c)} = ${ans}`,
  },
  {
    id: 'm1-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6], c: [2, 6] },
    contentFn: ({ a, b, c }) =>
      `${a} × (${-b}) - (${-c}) 의 값은?`,
    answerFn: ({ a, b, c }) => a * (-b) - (-c),
    distractorFns: [
      ({ a, b, c }) => a * (-b) + (-c),
      ({ a, b, c }) => a * b + c,
      ({ a, b, c }) => -(a * b + c),
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `혼합 연산 순서:\n${a} × (${-b}) - (${-c}) = ${-a * b} + ${c} = ${ans}`,
  },

  // Lv.8: 유리수 덧뺄셈
  {
    id: 'm1-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && (a * d + c * b) % (b * d) !== 0,
    contentFn: ({ a, b, c, d }) => `${a}/${b} + ${c}/${d} 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = a * d + c * b
      const den = b * d
      const g = gcdHelper(Math.abs(num), den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a + c}/${b + d}`,
      ({ a, b, c, d }) => `${a * d - c * b}/${b * d}`,
      ({ a, c }) => `${a + c}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `분수의 덧셈 (통분 후 더하기):\n${a}/${b} + ${c}/${d} = ${a * d}/${b * d} + ${c * b}/${b * d} = ${ans}`,
  },

  // Lv.9: 유리수 곱셈·나눗셈
  {
    id: 'm1-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a !== b && c !== d,
    contentFn: ({ a, b, c, d }) =>
      `(${-a}/${b}) × (${c}/${d}) 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = -(a * c)
      const den = b * d
      const g = gcdHelper(Math.abs(num), den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const num = a * c
        const den = b * d
        const g = gcdHelper(num, den)
        return `${num / g}/${den / g}`
      },
      ({ a, b, c, d }) => `${a * c}/${b + d}`,
      ({ a, b }) => `${-a}/${b}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `분수의 곱셈 (분자끼리, 분모끼리):\n(${-a}/${b}) × (${c}/${d}) = -(${a}×${c})/(${b}×${d}) = ${ans}`,
  },

  // Lv.10: 유리수 복합 연산
  {
    id: 'm1-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'M1-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 5], c: [1, 4], d: [2, 5], e: [-5, 5] },
    constraints: ({ a, b, c, d, e }) => c !== 0 && d !== 0 && e !== 0 && a < b && c < d,
    contentFn: ({ a, b, c, d, e }) =>
      `(${-a}/${b}) ÷ (${c}/${d}) + ${signedStr(e)} 의 값은?`,
    answerFn: ({ a, b, c, d, e }) => {
      // (-a/b) ÷ (c/d) = (-a/b) × (d/c) = -ad/(bc)
      const num = -a * d
      const den = b * c
      const g = gcdHelper(Math.abs(num), Math.abs(den))
      const rNum = num / g
      const rDen = den / g
      // + e = (rNum + e * rDen) / rDen
      const finalNum = rNum + e * rDen
      const finalDen = rDen
      if (finalNum % finalDen === 0) return finalNum / finalDen
      const g2 = gcdHelper(Math.abs(finalNum), Math.abs(finalDen))
      return `${finalNum / g2}/${finalDen / g2}`
    },
    distractorFns: [
      ({ a, b, c, d, e }) => {
        const val = (a * d) / (b * c) + e
        return Math.round(val * 10) / 10
      },
      ({ e }) => e,
      (_, ans) => {
        const n = typeof ans === 'number' ? ans : 0
        return n + 1
      },
    ],
    explanationFn: ({ a, b, c, d, e }, ans) =>
      `분수의 나눗셈과 덧셈 (나눗셈은 역수의 곱셈):\n(${-a}/${b}) ÷ (${c}/${d}) + ${signedStr(e)} = (${-a}/${b}) × (${d}/${c}) + ${signedStr(e)} = ${ans}`,
  },

  // Lv.11: 소인수분해 응용 계산 (Phase B7)
  {
    id: 'm1-comp-11a',
    grade: G,
    category: 'computation',
    level: 11,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 3], b: [1, 3] },
    contentFn: ({ a, b }) => `2^${a} × 3^${b}의 약수의 개수는?`,
    answerFn: ({ a, b }) => (a + 1) * (b + 1),
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b,
      ({ a, b }) => (a + 1) + (b + 1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `약수 개수 공식 (지수+1)의 곱:\nN = p^a × q^b의 약수 개수 = (a+1)(b+1)\n2^${a} × 3^${b}의 약수 개수 = (${a}+1)(${b}+1) = ${ans}`,
  },
  {
    id: 'm1-comp-11b',
    grade: G,
    category: 'computation',
    level: 11,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { a: [12, 36], b: [18, 48] },
    constraints: ({ a, b }) => a !== b && gcdHelper(a, b) > 2,
    contentFn: ({ a, b }) => `GCD(${a}, ${b}) = ?`,
    answerFn: ({ a, b }) => gcdHelper(a, b),
    distractorFns: [
      ({ a, b }) => lcmHelper(a, b),
      ({ a, b }) => Math.abs(a - b),
      ({ a, b }) => Math.min(a, b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `최대공약수 계산 (유클리드 호제법):\nGCD(${a}, ${b}) = ${ans}`,
  },

  // Lv.12: 최소공배수 계산 (Phase B7)
  {
    id: 'm1-comp-12a',
    grade: G,
    category: 'computation',
    level: 12,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { a: [6, 24], b: [8, 30] },
    constraints: ({ a, b }) => a !== b && gcdHelper(a, b) > 1,
    contentFn: ({ a, b }) => `LCM(${a}, ${b}) = ?`,
    answerFn: ({ a, b }) => lcmHelper(a, b),
    distractorFns: [
      ({ a, b }) => gcdHelper(a, b),
      ({ a, b }) => a * b,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `최소공배수 공식:\nLCM(a, b) = (a × b) / GCD(a, b)\nLCM(${a}, ${b}) = ${a * b} / ${gcdHelper(a, b)} = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const concept: QuestionTemplate[] = [
  // Lv.1: 용어 확인
  {
    id: 'm1-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '양의 정수, 0, 음의 정수를 통틀어 무엇이라 하는가?',
        '자연수에 0과 음의 정수를 포함한 수의 집합을 무엇이라 하는가?',
        '수직선에서 원점의 오른쪽에 있는 정수를 무엇이라 하는가?',
        '두 수의 절댓값은 같고 부호가 다른 관계를 무엇이라 하는가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['정수', '정수', '양의 정수', '서로 반대']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) =>
        ['유리수', '유리수', '음의 정수', '서로 역수'][variant]!,
      ({ variant }) =>
        ['자연수', '자연수', '자연수', '서로 같다'][variant]!,
      ({ variant }) =>
        ['실수', '실수', '정수', '절댓값'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '정수의 정의:\n양의 정수, 0, 음의 정수를 통틀어 정수라고 합니다.',
        '정수의 집합:\n자연수(양의 정수)에 0과 음의 정수를 합하면 정수의 집합이 됩니다.',
        '양의 정수:\n수직선에서 원점(0)의 오른쪽에 있는 정수는 양의 정수입니다.',
        '서로 반대인 수:\n절댓값이 같고 부호가 반대인 두 수는 서로 반대 관계입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.2: 기본 판별 — 약수 찾기, 수 분류
  {
    id: 'm1-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { n: [6, 30] },
    constraints: ({ n }) => {
      // 약수가 4개 이상인 수만
      let count = 0
      for (let i = 1; i <= n; i++) {
        if (n % i === 0) count++
      }
      return count >= 4
    },
    contentFn: ({ n }) => `${n}의 약수가 아닌 것은?`,
    answerFn: ({ n }) => {
      // n의 약수가 아닌 가장 작은 2 이상의 수
      for (let i = 2; i <= n; i++) {
        if (n % i !== 0) return i
      }
      return n + 1
    },
    distractorFns: [
      () => 1,
      ({ n }) => n,
      ({ n }) => {
        // n의 약수 중 하나
        for (let i = 2; i < n; i++) {
          if (n % i === 0) return i
        }
        return 1
      },
    ],
    explanationFn: ({ n }, ans) => {
      const divisors: number[] = []
      for (let i = 1; i <= n; i++) {
        if (n % i === 0) divisors.push(i)
      }
      return `약수 판별:\n${n}의 약수는 ${divisors.join(', ')}입니다.\n${ans}은(는) ${n}의 약수가 아닙니다.`
    },
  },

  // Lv.3: 단순 방정식 x + a = b
  {
    id: 'm1-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 15], b: [5, 25] },
    constraints: ({ a, b }) => b > a,
    contentFn: ({ a, b }) => `x + ${a} = ${b} 일 때, x의 값은?`,
    answerFn: ({ a, b }) => b - a,
    distractorFns: [
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) + 1,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `일차방정식 풀이 (이항):\nx + ${a} = ${b}\nx = ${b} - ${a} = ${ans}`,
  },
  {
    id: 'm1-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 10], b: [1, 15] },
    contentFn: ({ a, b }) => `x - ${a} = ${b} 일 때, x의 값은?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => b - a,
      (_, ans) => (ans as number) + 2,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `일차방정식 풀이 (이항):\nx - ${a} = ${b}\nx = ${b} + ${a} = ${ans}`,
  },

  // Lv.4: 계수 방정식 ax = b
  {
    id: 'm1-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 9], x: [1, 10] },
    contentFn: ({ a, x }) => `${a}x = ${a * x} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x }) => a * x,
      ({ a }) => a,
      ({ x }) => x + 1,
    ],
    explanationFn: ({ a, x }) =>
      `일차방정식 풀이 (양변을 a로 나누기):\n${a}x = ${a * x}\nx = ${a * x} ÷ ${a} = ${x}`,
  },

  // Lv.5: 다단계 방정식 ax - b = c
  {
    id: 'm1-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 6], x: [1, 10], b: [1, 10] },
    contentFn: ({ a, x, b }) =>
      `${a}x - ${b} = ${a * x - b} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x, b }) => a * x - b,
      ({ x }) => x + 1,
      ({ x }) => x - 1,
    ],
    explanationFn: ({ a, x, b }) => {
      const rhs = a * x - b
      return `일차방정식 풀이:\n${a}x - ${b} = ${rhs}\n${a}x = ${rhs} + ${b} = ${rhs + b}\nx = ${rhs + b} ÷ ${a} = ${x}`
    },
  },
  {
    id: 'm1-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5], x: [1, 8], b: [1, 10] },
    contentFn: ({ a, x, b }) =>
      `${a}x + ${b} = ${a * x + b} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x, b }) => a * x + b,
      ({ a }) => a,
      ({ x }) => x * 2,
    ],
    explanationFn: ({ a, x, b }) => {
      const rhs = a * x + b
      return `일차방정식 풀이:\n${a}x + ${b} = ${rhs}\n${a}x = ${rhs} - ${b} = ${a * x}\nx = ${a * x} ÷ ${a} = ${x}`
    },
  },

  // Lv.6: 좌표 (사분면 판별) - Phase A2에서 6b 교체
  {
    id: 'm1-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'algebra',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { x: [-10, 10], y: [-10, 10] },
    constraints: ({ x, y }) => x !== 0 && y !== 0,
    contentFn: ({ x, y }) => `점 (${x}, ${y})는 어느 사분면에 있는가?`,
    answerFn: ({ x, y }) => {
      if (x > 0 && y > 0) return '제1사분면'
      if (x < 0 && y > 0) return '제2사분면'
      if (x < 0 && y < 0) return '제3사분면'
      return '제4사분면'
    },
    distractorFns: [
      () => '제1사분면',
      () => '제2사분면',
      () => '제3사분면',
      () => '제4사분면',
    ],
    explanationFn: ({ x, y }, ans) => {
      const xSign = x > 0 ? '양수(+)' : '음수(-)'
      const ySign = y > 0 ? '양수(+)' : '음수(-)'
      return `좌표평면 사분면 판별:\nx좌표가 ${xSign}이고 y좌표가 ${ySign}이면 ${ans}입니다.`
    },
  },
  {
    id: 'm1-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'algebra',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [-8, 8], b: [-8, 8], c: [-8, 8], d: [-8, 8] },
    constraints: ({ a, c }) => a !== c,
    contentFn: ({ a, b, c, d }) =>
      `점 A(${a}, ${b})과 점 B(${c}, ${d}) 사이의 x좌표 차이는?`,
    answerFn: ({ a, c }) => Math.abs(c - a),
    distractorFns: [
      ({ b, d }) => Math.abs(d - b),
      ({ a, c }) => c - a,
      ({ a, b, c, d }) => Math.abs(c - a) + Math.abs(d - b),
    ],
    explanationFn: ({ a, c }, ans) =>
      `좌표평면 거리 개념:\nx좌표 차이 = |x2 - x1| = |${c} - ${a}| = ${ans}`,
  },

  // Lv.7: 정비례/반비례 - Phase A3에서 7b 교체
  {
    id: 'm1-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [2, 8], x: [-5, 5] },
    constraints: ({ x }) => x !== 0,
    contentFn: ({ a, x }) => `y = ${a}x 일 때, x = ${x}이면 y의 값은?`,
    answerFn: ({ a, x }) => a * x,
    distractorFns: [
      ({ a, x }) => a + x,
      ({ a, x }) => -(a * x),
      ({ a }, ans) => (ans as number) + a,
    ],
    explanationFn: ({ a, x }, ans) =>
      `정비례 관계 (y = ax):\ny = ${a}x에 x = ${x}을 대입하면\ny = ${a} × ${signedStr(x)} = ${ans}`,
  },
  {
    id: 'm1-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [6, 24], n: [2, 6] },
    constraints: ({ a, n }) => a % n === 0,
    contentFn: ({ a, n }) => `y = ${a}/x 에서 x = ${n}일 때 y의 값은?`,
    answerFn: ({ a, n }) => a / n,
    distractorFns: [
      ({ a, n }) => a * n,
      ({ a, n }) => a - n,
      ({ a, n }) => a + n,
    ],
    explanationFn: ({ a, n }, ans) =>
      `반비례 관계 (y = a/x):\ny = ${a}/x에 x = ${n}을 대입하면\ny = ${a}/${n} = ${ans}`,
  },

  // Lv.8: 복합 방정식 a(x - b) = cx + d
  {
    id: 'm1-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'algebra',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 5], c: [1, 4], x: [-5, 5] },
    constraints: ({ a, c, x }) => a !== c && x !== 0,
    contentFn: ({ a, b, c, x }) => {
      const rhs = c * x + (a * x - a * b - c * x)
      return `${a}(x - ${b}) = ${c}x + ${signedStr(rhs)} 를 풀면 x = ?`
    },
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ x }) => -x,
      ({ x }) => x + 1,
      ({ x }) => x - 1,
    ],
    explanationFn: ({ a, b, c, x }) => {
      const d = a * x - a * b - c * x
      return `복합 일차방정식 풀이:\n${a}(x - ${b}) = ${c}x + ${signedStr(d)}\n` +
        `${a}x - ${a * b} = ${c}x + ${signedStr(d)}\n` +
        `${a}x - ${c}x = ${signedStr(d)} + ${a * b}\n` +
        `${a - c}x = ${d + a * b}\n` +
        `x = ${x}`
    },
  },

  // Lv.9: 문장제
  {
    id: 'm1-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [3, 8], total: [20, 50] },
    constraints: ({ a, total }) => total % a === 0,
    contentFn: ({ a, total }) =>
      `어떤 수에 ${a}를 곱하면 ${total}이 됩니다. 어떤 수를 구하시오.`,
    answerFn: ({ a, total }) => total / a,
    distractorFns: [
      ({ a, total }) => total - a,
      ({ a, total }) => total + a,
      ({ a, total }) => a * total,
    ],
    explanationFn: ({ a, total }, ans) =>
      `문장제 방정식:\n어떤 수를 x라 하면\n${a}x = ${total}\nx = ${total} ÷ ${a} = ${ans}`,
  },
  {
    id: 'm1-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'M1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 10], total: [15, 40] },
    constraints: ({ a, b, total }) => (total - b) % a === 0 && (total - b) / a > 0,
    contentFn: ({ a, b, total }) =>
      `어떤 수에 ${a}를 곱하고 ${b}를 더하면 ${total}이 됩니다. 어떤 수는?`,
    answerFn: ({ a, b, total }) => (total - b) / a,
    distractorFns: [
      ({ a, b, total }) => (total + b) / a,
      ({ total, b }) => total - b,
      ({ a, total }) => total / a,
    ],
    explanationFn: ({ a, b, total }, ans) =>
      `문장제 방정식:\n어떤 수를 x라 하면\n${a}x + ${b} = ${total}\n${a}x = ${total - b}\nx = ${ans}`,
  },

  // Lv.10: 종합 응용 (방정식 + 좌표)
  {
    id: 'm1-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [2, 5], b: [-5, 5], px: [1, 5] },
    constraints: ({ b }) => b !== 0,
    contentFn: ({ a, b, px }) =>
      `일차함수 y = ${a}x + ${signedStr(b)} 의 그래프가 점 (${px}, k)를 지날 때, k의 값은?`,
    answerFn: ({ a, b, px }) => a * px + b,
    distractorFns: [
      ({ a, b, px }) => a * px - b,
      ({ a, px }) => a * px,
      ({ a, b, px }) => a + b + px,
    ],
    explanationFn: ({ a, b, px }, ans) =>
      `일차함수 그래프와 점:\ny = ${a}x + ${signedStr(b)}에 x = ${px}을 대입\n` +
      `k = ${a} × ${px} + ${signedStr(b)} = ${a * px} + ${signedStr(b)} = ${ans}`,
  },
  {
    id: 'm1-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 6], c: [1, 5] },
    constraints: ({ a, b, c }) => {
      // a * x = b + c에서 x가 정수가 되도록
      return (b + c) % a === 0
    },
    contentFn: ({ a, b, c }) =>
      `${a}x - ${b} = ${c} 의 해가 x = p일 때, 점 (p, 2p)가 위치하는 사분면은?`,
    answerFn: ({ a, b, c }) => {
      const x = (b + c) / a
      if (x > 0) return '제1사분면'
      if (x < 0) return '제3사분면'
      return '원점'
    },
    distractorFns: [
      () => '제2사분면',
      () => '제4사분면',
      () => '제3사분면',
    ],
    explanationFn: ({ a, b, c }) => {
      const x = (b + c) / a
      return `방정식과 좌표평면:\n${a}x - ${b} = ${c}\n${a}x = ${b + c}\nx = ${x}\n` +
        `점 (${x}, ${2 * x})은 x=${x}, y=${2 * x}이므로 제1사분면`
    },
  },

  // Phase B2: 기본 도형 concepts (conceptId: 'M1-GEO-01')
  {
    id: 'm1-conc-11a',
    grade: G,
    category: 'concept',
    level: 11,
    part: 'geo',
    conceptId: 'M1-GEO-01',
    pattern: '',
    paramRanges: { a: [30, 150] },
    contentFn: ({ a }) => `두 직선이 만날 때 한 각이 ${a}°이면 맞꼭지각은?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => 180 - a,
      ({ a }) => 90 - a,
      ({ a }) => a / 2,
    ],
    explanationFn: (_p, ans) =>
      `맞꼭지각의 성질:\n두 직선이 만날 때 생기는 맞꼭지각은 크기가 같습니다.\n따라서 맞꼭지각 = ${ans}°`,
  },
  {
    id: 'm1-conc-11b',
    grade: G,
    category: 'concept',
    level: 11,
    part: 'geo',
    conceptId: 'M1-GEO-01',
    pattern: '',
    paramRanges: { a: [40, 140], variant: [0, 1] },
    contentFn: ({ a, variant }) => {
      const types = ['동위각', '엇각']
      return `평행선에서 한 각이 ${a}°이면 ${types[variant]}은?`
    },
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => 180 - a,
      ({ a }) => 90 - a,
      ({ a }) => 90 + a,
    ],
    explanationFn: ({ variant }, ans) => {
      const types = ['동위각', '엇각']
      return `평행선의 성질:\n평행선에서 ${types[variant]}은 크기가 같습니다.\n따라서 ${types[variant]} = ${ans}°`
    },
  },

  // Phase B3: 평면도형 concepts (conceptId: 'M1-GEO-02')
  {
    id: 'm1-conc-12a',
    grade: G,
    category: 'concept',
    level: 12,
    part: 'geo',
    conceptId: 'M1-GEO-02',
    pattern: '',
    paramRanges: { n: [3, 8] },
    contentFn: ({ n }) => `${n}각형의 내각의 합은?`,
    answerFn: ({ n }) => 180 * (n - 2),
    distractorFns: [
      ({ n }) => 180 * n,
      ({ n }) => 180 * (n - 1),
      ({ n }) => 360 * (n - 2),
    ],
    explanationFn: ({ n }, ans) =>
      `n각형 내각의 합 공식:\n내각의 합 = 180° × (n - 2)\n${n}각형의 내각의 합 = 180° × (${n} - 2) = ${ans}°`,
  },
  {
    id: 'm1-conc-12b',
    grade: G,
    category: 'concept',
    level: 12,
    part: 'geo',
    conceptId: 'M1-GEO-02',
    pattern: '',
    paramRanges: { a: [3, 10], b: [60, 180] },
    constraints: ({ b }) => b % 30 === 0,
    contentFn: ({ a, b }) =>
      `반지름 ${a}, 중심각 ${b}°인 부채꼴의 호의 길이는? (원주율 π 사용)`,
    answerFn: ({ a, b }) => {
      const simplified = (2 * a * b) / 360
      if (simplified === Math.floor(simplified)) {
        return `${simplified}π`
      }
      return `${a * b}/180π`
    },
    distractorFns: [
      ({ a }) => `${a}π`,
      ({ a, b }) => `${a * b}π`,
      ({ a }) => `${2 * a}π`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `부채꼴 호의 길이 공식:\n호의 길이 = 2πr × (θ/360)\n= 2π × ${a} × (${b}/360) = ${ans}`,
  },

  // Phase B4: 입체도형 concepts (conceptId: 'M1-GEO-03')
  {
    id: 'm1-conc-13a',
    grade: G,
    category: 'concept',
    level: 13,
    part: 'geo',
    conceptId: 'M1-GEO-03',
    pattern: '',
    paramRanges: { a: [2, 6], b: [4, 10] },
    contentFn: ({ a, b }) =>
      `밑면 반지름 ${a}, 높이 ${b}인 원기둥의 부피는? (원주율 π 사용)`,
    answerFn: ({ a, b }) => `${a * a * b}π`,
    distractorFns: [
      ({ a, b }) => `${a * b}π`,
      ({ a, b }) => `${2 * a * b}π`,
      ({ a }) => `${a * a}π`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `원기둥 부피 공식:\n부피 = πr²h\n= π × ${a}² × ${b} = ${ans}`,
  },
  {
    id: 'm1-conc-13b',
    grade: G,
    category: 'concept',
    level: 13,
    part: 'geo',
    conceptId: 'M1-GEO-03',
    pattern: '',
    paramRanges: { a: [3, 9], variant: [0, 1] },
    contentFn: ({ a, variant }) => {
      const types = ['겉넓이', '부피']
      return `반지름 ${a}인 구의 ${types[variant]}는? (원주율 π 사용)`
    },
    answerFn: ({ a, variant }) => {
      if (variant === 0) {
        // 겉넓이 4πr²
        return `${4 * a * a}π`
      } else {
        // 부피 4/3πr³
        return `${4 * a * a * a}/3π`
      }
    },
    distractorFns: [
      ({ a }) => `${a * a}π`,
      ({ a }) => `${2 * a * a}π`,
      ({ a, variant }) => {
        if (variant === 0) return `${a * a * a}π`
        return `${a * a}π`
      },
    ],
    explanationFn: ({ a, variant }, ans) => {
      if (variant === 0) {
        return `구의 겉넓이 공식:\n겉넓이 = 4πr²\n= 4π × ${a}² = ${ans}`
      } else {
        return `구의 부피 공식:\n부피 = (4/3)πr³\n= (4/3)π × ${a}³ = ${ans}`
      }
    },
  },

  // Phase B5: 자료와 가능성 concepts (conceptId: 'M1-STA-01')
  {
    id: 'm1-conc-14a',
    grade: G,
    category: 'concept',
    level: 14,
    part: 'data',
    conceptId: 'M1-STA-01',
    pattern: '',
    paramRanges: { a: [10, 30], b: [15, 35], c: [20, 40], d: [12, 28] },
    contentFn: ({ a, b, c, d }) => `자료 ${a}, ${b}, ${c}, ${d}의 평균은?`,
    answerFn: ({ a, b, c, d }) => {
      const sum = a + b + c + d
      if (sum % 4 === 0) return sum / 4
      return `${sum}/4`
    },
    distractorFns: [
      ({ a, b, c, d }) => (a + b + c + d) / 2,
      ({ a, b, c, d }) => Math.max(a, b, c, d),
      ({ a, b, c, d }) => Math.min(a, b, c, d),
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `평균 계산:\n평균 = (자료의 총합) / (자료의 개수)\n= (${a} + ${b} + ${c} + ${d}) / 4 = ${a + b + c + d} / 4 = ${ans}`,
  },
  {
    id: 'm1-conc-14b',
    grade: G,
    category: 'concept',
    level: 14,
    part: 'data',
    conceptId: 'M1-STA-01',
    pattern: '',
    paramRanges: { a: [10, 20], b: [25, 35], c: [40, 50], d: [55, 65] },
    contentFn: ({ a, b, c, d }) => `자료 ${a}, ${b}, ${c}, ${d}를 크기순으로 정렬할 때 중앙값은?`,
    answerFn: ({ a, b, c, d }) => {
      const sorted = [a, b, c, d].sort((x, y) => x - y)
      return (sorted[1]! + sorted[2]!) / 2
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const sorted = [a, b, c, d].sort((x, y) => x - y)
        return sorted[1]!
      },
      ({ a, b, c, d }) => {
        const sorted = [a, b, c, d].sort((x, y) => x - y)
        return sorted[2]!
      },
      ({ a, b, c, d }) => (a + b + c + d) / 4,
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const sorted = [a, b, c, d].sort((x, y) => x - y)
      return `중앙값 계산:\n자료를 크기순으로 정렬: ${sorted.join(', ')}\n` +
        `자료가 4개(짝수)이므로 중앙값 = (2번째 + 3번째) / 2 = (${sorted[1]} + ${sorted[2]}) / 2 = ${ans}`
    },
  },
  {
    id: 'm1-conc-15a',
    grade: G,
    category: 'concept',
    level: 15,
    part: 'data',
    conceptId: 'M1-STA-01',
    pattern: '',
    paramRanges: { a: [5, 10], b: [8, 15], c: [3, 8] },
    constraints: ({ a, b, c }) => a !== b && b !== c && a !== c,
    contentFn: ({ a, b, c }) =>
      `도수가 각각 ${a}, ${b}, ${c}인 세 계급이 있을 때, 최빈값은 도수가 몇인 계급인가?`,
    answerFn: ({ a, b, c }) => Math.max(a, b, c),
    distractorFns: [
      ({ a, b, c }) => Math.min(a, b, c),
      ({ a, b, c }) => (a + b + c) / 3,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `최빈값(mode):\n도수가 가장 많은 계급의 값이 최빈값입니다.\n도수: ${a}, ${b}, ${c} 중 최댓값 = ${ans}`,
  },
  {
    id: 'm1-conc-15b',
    grade: G,
    category: 'concept',
    level: 15,
    part: 'data',
    conceptId: 'M1-STA-01',
    pattern: '',
    paramRanges: { a: [5, 15], total: [30, 50] },
    constraints: ({ a, total }) => a < total,
    contentFn: ({ a, total }) =>
      `계급의 도수가 ${a}이고 전체 도수가 ${total}일 때 상대도수는? (소수 둘째자리까지)`,
    answerFn: ({ a, total }) => Math.round((a / total) * 100) / 100,
    distractorFns: [
      ({ a, total }) => a / total,
      ({ a, total }) => total / a,
      ({ a, total }) => (total - a) / total,
    ],
    explanationFn: ({ a, total }, ans) =>
      `상대도수 계산:\n상대도수 = (계급의 도수) / (전체 도수)\n= ${a} / ${total} ≈ ${ans}`,
  },

  // Phase B6: 정비례/반비례 concepts (conceptId: 'M1-FUNC-01')
  {
    id: 'm1-conc-16a',
    grade: G,
    category: 'concept',
    level: 16,
    part: 'func',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [2, 8], b: [4, 16], c: [3, 10] },
    constraints: ({ a, b, c }) => (b * c) % a === 0,
    contentFn: ({ a, b, c }) =>
      `y가 x에 정비례하고 x = ${a}일 때 y = ${b}이면, x = ${c}일 때 y의 값은?`,
    answerFn: ({ a, b, c }) => (b * c) / a,
    distractorFns: [
      ({ a, b, c }) => (a * b) / c,
      ({ b, c }) => b + c,
      ({ a, c }) => a * c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `정비례 관계:\ny가 x에 정비례하면 y = kx (k는 비례상수)\n` +
      `x = ${a}일 때 y = ${b}이므로 ${b} = k × ${a}, k = ${b / a}\n` +
      `x = ${c}일 때 y = ${b / a} × ${c} = ${ans}`,
  },
  {
    id: 'm1-conc-16b',
    grade: G,
    category: 'concept',
    level: 16,
    part: 'func',
    conceptId: 'M1-FUNC-01',
    pattern: '',
    paramRanges: { a: [2, 6], b: [12, 36], c: [3, 9] },
    constraints: ({ a, b, c }) => b % a === 0 && (a * b) % c === 0,
    contentFn: ({ a, b, c }) =>
      `y가 x에 반비례하고 x = ${a}일 때 y = ${b}이면, x = ${c}일 때 y의 값은?`,
    answerFn: ({ a, b, c }) => (a * b) / c,
    distractorFns: [
      ({ a, b, c }) => (b * c) / a,
      ({ b, c }) => b / c,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `반비례 관계:\ny가 x에 반비례하면 y = k/x (k는 비례상수)\n` +
      `x = ${a}일 때 y = ${b}이므로 ${b} = k / ${a}, k = ${a * b}\n` +
      `x = ${c}일 때 y = ${a * b} / ${c} = ${ans}`,
  },

  // ── Lv.5: 최대공약수·최소공배수와 소인수분해 (M1-NUM-02) ──
  {
    id: 'm1-conc-17a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-02',
    pattern: '',
    paramRanges: { a: [12, 60], b: [12, 60] },
    constraints: ({ a, b }) =>
      a !== b && gcdHelper(a, b) > 1 && gcdHelper(a, b) < Math.min(a, b),
    contentFn: ({ a, b }) =>
      `소인수분해를 이용하여 ${a}과 ${b}의 최대공약수를 구하시오.`,
    answerFn: ({ a, b }) => gcdHelper(a, b),
    distractorFns: [
      ({ a, b }) => lcmHelper(a, b),
      ({ a, b }) => a * b,
      ({ a, b }) => gcdHelper(a, b) * 2,
    ],
    explanationFn: ({ a, b }, ans) => {
      const fA = primeFactorString(a)
      const fB = primeFactorString(b)
      return `${a} = ${fA}\n${b} = ${fB}\n공통 소인수의 최소 지수를 곱하면\n최대공약수 = ${ans}`
    },
  },
  {
    id: 'm1-conc-17b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-02',
    pattern: '',
    paramRanges: { a: [6, 30], b: [6, 30] },
    constraints: ({ a, b }) =>
      a !== b && gcdHelper(a, b) > 1 && lcmHelper(a, b) <= 300,
    contentFn: ({ a, b }) =>
      `소인수분해를 이용하여 ${a}과 ${b}의 최소공배수를 구하시오.`,
    answerFn: ({ a, b }) => lcmHelper(a, b),
    distractorFns: [
      ({ a, b }) => gcdHelper(a, b),
      ({ a, b }) => a * b,
      ({ a, b }) => lcmHelper(a, b) + gcdHelper(a, b),
    ],
    explanationFn: ({ a, b }, ans) => {
      const fA = primeFactorString(a)
      const fB = primeFactorString(b)
      return `${a} = ${fA}\n${b} = ${fB}\n모든 소인수의 최대 지수를 곱하면\n최소공배수 = ${ans}`
    },
  },

  // ── Lv.3: 문자와 식 (M1-ALG-01) ──
  {
    id: 'm1-conc-18a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        'a × b를 곱셈 기호를 생략하여 나타내면?',
        'x × x × x를 거듭제곱으로 나타내면?',
        '(a + b) ÷ 2를 분수 꼴로 나타내면?',
        'a × 1을 곱셈 기호를 생략하여 나타내면?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => ['ab', 'x³', '(a+b)/2', 'a'][variant]!,
    distractorFns: [
      ({ variant }) => ['a + b', 'x3', 'a+b/2', '1a'][variant]!,
      ({ variant }) => ['a·b', '3x', '(a+b)×2', 'a×1'][variant]!,
      ({ variant }) => ['ba', 'xxx', 'a/2+b', '1'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '곱셈 기호 생략: a × b = ab (알파벳 순서로 씀)',
        '같은 문자의 곱: x × x × x = x³',
        '나눗셈은 분수로: (a + b) ÷ 2 = (a+b)/2',
        'a × 1 = a (1은 생략)',
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'm1-conc-18b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 9], b: [1, 5], c: [1, 10] },
    contentFn: ({ a, b, c }) =>
      `x = ${c}일 때, ${a}x + ${b}의 값을 구하시오.`,
    answerFn: ({ a, b, c }) => a * c + b,
    distractorFns: [
      ({ a, b, c }) => a + b + c,
      ({ a, b, c }) => a * c - b,
      ({ a, b, c }) => a * (b + c),
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `식의 값 = 문자에 수를 대입하여 계산\n${a}x + ${b}에 x = ${c}을 대입\n= ${a} × ${c} + ${b}\n= ${a * c} + ${b}\n= ${ans}`,
  },
]

export const middle1Templates: QuestionTemplate[] = [...comp, ...concept]
