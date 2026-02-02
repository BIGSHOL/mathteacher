// 초등 5학년 (elementary_5) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'

const G = 'elementary_5' as const

// Helper: 최대공약수
function gcdHelper(x: number, y: number): number {
  x = Math.abs(x)
  y = Math.abs(y)
  while (y) {
    ;[x, y] = [y, x % y]
  }
  return x || 1
}

// Helper: 최소공배수
function lcmHelper(x: number, y: number): number {
  return Math.abs(x * y) / gcdHelper(x, y)
}

// Helper: 약분된 분수 문자열 반환
function simplifyFraction(num: number, den: number): string {
  const g = gcdHelper(Math.abs(num), Math.abs(den))
  return `${num / g}/${den / g}`
}

// Helper: 약수 개수 세기
function countDivisors(n: number): number {
  let count = 0
  for (let i = 1; i <= n; i++) {
    if (n % i === 0) count++
  }
  return count
}

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 이분모 분수 덧셈 (통분)
  {
    id: 'e5-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E5-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && b !== d,
    contentFn: ({ a, b, c, d }) => `${a}/${b} + ${c}/${d} = ?`,
    answerFn: ({ a, b, c, d }) => {
      const num = a * d + c * b
      const den = b * d
      return simplifyFraction(num, den)
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a + c}/${b + d}`,
      ({ a, b, c, d }) => `${a * d + c * b}/${b * d}`,
      ({ a, b, c, d }) => simplifyFraction(a * d - c * b, b * d),
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const lcm = lcmHelper(b, d)
      return `${a}/${b} + ${c}/${d} = ${a * (lcm / b)}/${lcm} + ${c * (lcm / d)}/${lcm} = ${a * d + c * b}/${b * d} = ${ans}`
    },
  },
  {
    id: 'e5-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E5-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 3], b: [2, 5], c: [1, 3], d: [2, 5] },
    constraints: ({ a, b, c, d }) => a < b && c < d && b !== d && (a * d + c * b) % (b * d) !== 0,
    contentFn: ({ a, b, c, d }) => `${a}/${b} + ${c}/${d}를 기약분수로 나타내면?`,
    answerFn: ({ a, b, c, d }) => simplifyFraction(a * d + c * b, b * d),
    distractorFns: [
      ({ a, b, c, d }) => `${a + c}/${b + d}`,
      ({ a, b, c, d }) => `${a * d + c * b}/${b * d}`,
      ({ a, b, c, d }) => simplifyFraction(a * d + c * b + 1, b * d),
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} + ${c}/${d} = ${a * d}/${b * d} + ${c * b}/${b * d} = ${a * d + c * b}/${b * d} = ${ans}`,
  },

  // Lv.2: 이분모 분수 뺄셈
  {
    id: 'e5-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E5-NUM-06',
    pattern: '',
    paramRanges: { a: [2, 8], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && b !== d && a * d > c * b,
    contentFn: ({ a, b, c, d }) => `${a}/${b} - ${c}/${d} = ?`,
    answerFn: ({ a, b, c, d }) => simplifyFraction(a * d - c * b, b * d),
    distractorFns: [
      ({ a, b, c, d }) => `${a - c}/${b - d}`,
      ({ a, b, c, d }) => `${a * d - c * b}/${b * d}`,
      ({ a, b, c, d }) => simplifyFraction(a * d + c * b, b * d),
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} - ${c}/${d} = ${a * d}/${b * d} - ${c * b}/${b * d} = ${a * d - c * b}/${b * d} = ${ans}`,
  },
  {
    id: 'e5-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E5-NUM-06',
    pattern: '',
    paramRanges: { a: [3, 9], b: [3, 7], c: [1, 4], d: [3, 7] },
    constraints: ({ a, b, c, d }) => a < b && c < d && b !== d && a * d - c * b > 0,
    contentFn: ({ a, b, c, d }) => `${a}/${b} - ${c}/${d}를 기약분수로 나타내면?`,
    answerFn: ({ a, b, c, d }) => simplifyFraction(a * d - c * b, b * d),
    distractorFns: [
      ({ a, b, c, d }) => `${a * d - c * b}/${b * d}`,
      ({ a, b, c, d }) => simplifyFraction(a * d - c * b - 1, b * d),
      ({ a, c }) => `${a - c}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} - ${c}/${d} = ${a * d - c * b}/${b * d} = ${ans}`,
  },

  // Lv.3: 대분수 덧셈
  {
    id: 'e5-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E5-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 3], b: [1, 2], c: [1, 4], d: [3, 6] },
    constraints: ({ c, d }) => c < d,
    contentFn: ({ a, c, d, b }) => `${a} ${c}/${d} + ${b} ${c}/${d} = ?`,
    answerFn: ({ a, b, c, d }) => {
      const wholePart = a + b
      const fracNum = c + c
      if (fracNum >= d) {
        return `${wholePart + Math.floor(fracNum / d)} ${fracNum % d}/${d}`
      }
      return `${wholePart} ${fracNum}/${d}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a + b} ${c}/${d}`,
      ({ a, b, c, d }) => `${a + b} ${c + c}/${d}`,
      ({ a, b, c }) => `${a + b + c}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const wholePart = a + b
      const fracNum = c + c
      if (fracNum >= d) {
        return `${a} ${c}/${d} + ${b} ${c}/${d} = ${wholePart} ${fracNum}/${d} = ${ans} (받아올림)`
      }
      return `${a} ${c}/${d} + ${b} ${c}/${d} = ${wholePart} ${fracNum}/${d} = ${ans}`
    },
  },
  {
    id: 'e5-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E5-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 2], b: [1, 2], c: [2, 5], d: [4, 8] },
    constraints: ({ c, d }) => c < d && c * 2 < d,
    contentFn: ({ a, b, c, d }) => `${a} ${c}/${d} + ${b} ${c}/${d}를 대분수로 나타내면?`,
    answerFn: ({ a, b, c, d }) => `${a + b} ${simplifyFraction(c + c, d)}`,
    distractorFns: [
      ({ a, b, c, d }) => `${a + b} ${c + c}/${d}`,
      ({ a, b, c, d }) => `${a + b + 1} ${c}/${d}`,
      ({ a, b }) => `${a + b}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a} ${c}/${d} + ${b} ${c}/${d} = ${a + b} ${c + c}/${d} = ${ans}`,
  },

  // Lv.4: 대분수 뺄셈
  {
    id: 'e5-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E5-NUM-07',
    pattern: '',
    paramRanges: { a: [2, 4], b: [1, 2], c: [2, 5], d: [4, 8] },
    constraints: ({ a, b, c, d }) => a > b && c < d && c * 2 < d,
    contentFn: ({ a, b, c, d }) => `${a} ${c}/${d} - ${b} ${c}/${d} = ?`,
    answerFn: ({ a, b, c, d }) => {
      if (c >= c) {
        return `${a - b}`
      }
      return `${a - b} ${c - c}/${d}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a - b} ${c}/${d}`,
      ({ a, b, c, d }) => `${a - b - 1} ${c}/${d}`,
      ({ a, b }) => `${a - b + 1}`,
    ],
    explanationFn: ({ a, b, c, d }) =>
      `${a} ${c}/${d} - ${b} ${c}/${d} = ${a - b} ${c - c}/${d} = ${a - b}`,
  },
  {
    id: 'e5-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E5-NUM-07',
    pattern: '',
    paramRanges: { a: [3, 5], b: [1, 3], c: [1, 3], d: [4, 6], e: [2, 5] },
    constraints: ({ a, b, c, d, e }) => a > b && c < d && e < d && c < e,
    contentFn: ({ a, b, c, d, e }) => `${a} ${c}/${d} - ${b} ${e}/${d} = ?`,
    answerFn: ({ a, b, c, d, e }) => {
      let whole = a - b
      let frac = c - e
      if (frac < 0) {
        whole -= 1
        frac += d
      }
      if (frac === 0) return `${whole}`
      return `${whole} ${frac}/${d}`
    },
    distractorFns: [
      ({ a, b, c, e, d }) => `${a - b} ${Math.abs(c - e)}/${d}`,
      ({ a, b, c, e, d }) => `${a - b - 1} ${c + e}/${d}`,
      ({ a, b }) => `${a - b}`,
    ],
    explanationFn: ({ a, b, c, d, e }, ans) => {
      if (c < e) {
        return `${a} ${c}/${d} - ${b} ${e}/${d} = ${a - 1} ${c + d}/${d} - ${b} ${e}/${d} = ${ans} (받아내림)`
      }
      return `${a} ${c}/${d} - ${b} ${e}/${d} = ${a - b} ${c - e}/${d} = ${ans}`
    },
  },

  // Lv.5: 소수 × 자연수
  {
    id: 'e5-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E5-NUM-08',
    pattern: '',
    paramRanges: { a: [1, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `0.${a} × ${b} = ?`,
    answerFn: ({ a, b }) => {
      const result = (a / 10) * b
      return result % 1 === 0 ? result : result.toFixed(1)
    },
    distractorFns: [
      ({ a, b }) => (a * b).toFixed(1),
      ({ a, b }) => ((a / 10) * b + 0.1).toFixed(1),
      ({ a, b }) => ((a / 10) * b - 0.1).toFixed(1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `0.${a} × ${b} = ${a * b} ÷ 10 = ${ans}`,
  },
  {
    id: 'e5-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E5-NUM-08',
    pattern: '',
    paramRanges: { a: [11, 99], b: [2, 7] },
    contentFn: ({ a, b }) => `${(a / 10).toFixed(1)} × ${b} = ?`,
    answerFn: ({ a, b }) => {
      const result = (a / 10) * b
      return result % 1 === 0 ? result : result.toFixed(1)
    },
    distractorFns: [
      ({ a, b }) => ((a / 10) * b + 0.1).toFixed(1),
      ({ a, b }) => ((a / 10) * b * 10).toFixed(1),
      ({ a, b }) => (a * b).toFixed(1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${(a / 10).toFixed(1)} × ${b} = ${a * b} ÷ 10 = ${ans}`,
  },

  // Lv.6: 소수 × 소수
  {
    id: 'e5-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E5-NUM-09',
    pattern: '',
    paramRanges: { a: [1, 9], b: [1, 9] },
    contentFn: ({ a, b }) => `0.${a} × 0.${b} = ?`,
    answerFn: ({ a, b }) => ((a / 10) * (b / 10)).toFixed(2),
    distractorFns: [
      ({ a, b }) => ((a * b) / 10).toFixed(2),
      ({ a, b }) => (a * b).toFixed(2),
      ({ a, b }) => ((a / 10) * (b / 10) + 0.01).toFixed(2),
    ],
    explanationFn: ({ a, b }, ans) =>
      `0.${a} × 0.${b} = ${a * b} ÷ 100 = ${ans}`,
  },
  {
    id: 'e5-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E5-NUM-09',
    pattern: '',
    paramRanges: { a: [11, 99], b: [11, 99] },
    contentFn: ({ a, b }) => `${(a / 10).toFixed(1)} × ${(b / 10).toFixed(1)} = ?`,
    answerFn: ({ a, b }) => ((a / 10) * (b / 10)).toFixed(2),
    distractorFns: [
      ({ a, b }) => ((a * b) / 10).toFixed(2),
      ({ a, b }) => ((a * b) / 1000).toFixed(2),
      ({ a, b }) => ((a / 10) * (b / 10) + 0.1).toFixed(2),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${(a / 10).toFixed(1)} × ${(b / 10).toFixed(1)} = ${a * b} ÷ 100 = ${ans}`,
  },

  // Lv.7: 소수 ÷ 자연수
  {
    id: 'e5-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E5-NUM-10',
    pattern: '',
    paramRanges: { a: [1, 9], b: [2, 5] },
    contentFn: ({ a, b }) => `${(a * b / 10).toFixed(1)} ÷ ${b} = ?`,
    answerFn: ({ a, b }) => ((a * b / 10) / b).toFixed(1),
    distractorFns: [
      ({ a }) => a.toFixed(1),
      ({ a, b }) => ((a * b / 10) / b + 0.1).toFixed(1),
      ({ a, b }) => ((a * b / 10) / b - 0.1).toFixed(1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${(a * b / 10).toFixed(1)} ÷ ${b} = ${a * b} ÷ 10 ÷ ${b} = ${a} ÷ 10 = ${ans}`,
  },
  {
    id: 'e5-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E5-NUM-10',
    pattern: '',
    paramRanges: { a: [10, 50], b: [2, 5] },
    constraints: ({ a, b }) => a % b === 0,
    contentFn: ({ a, b }) => `${(a / 10).toFixed(1)} ÷ ${b} = ?`,
    answerFn: ({ a, b }) => ((a / 10) / b).toFixed(1),
    distractorFns: [
      ({ a, b }) => ((a / 10) / b + 0.1).toFixed(1),
      ({ a, b }) => ((a / 10) / b * 10).toFixed(1),
      ({ a, b }) => (a / b).toFixed(1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${(a / 10).toFixed(1)} ÷ ${b} = ${a} ÷ 10 ÷ ${b} = ${a / b} ÷ 10 = ${ans}`,
  },

  // Lv.8: 약분 · 통분
  {
    id: 'e5-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E5-NUM-04',
    pattern: '',
    paramRanges: { a: [2, 5], b: [2, 6], c: [2, 8] },
    constraints: ({ a, b, c }) => {
      const g = gcdHelper(a * c, b * c)
      return g > 1 && a * c / g > 1 && b * c / g > 1
    },
    contentFn: ({ a, b, c }) => `${a * c}/${b * c}를 약분하면?`,
    answerFn: ({ a, b, c }) => simplifyFraction(a * c, b * c),
    distractorFns: [
      ({ a, b, c }) => `${a * c}/${b * c}`,
      ({ a, b, c }) => simplifyFraction(a * c - 1, b * c),
      ({ a, b }) => `${a}/${b}`,
    ],
    explanationFn: ({ a, b, c }, ans) => {
      const g = gcdHelper(a * c, b * c)
      return `${a * c}/${b * c}의 최대공약수는 ${g}이므로 ${a * c}÷${g}/${b * c}÷${g} = ${ans}`
    },
  },
  {
    id: 'e5-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E5-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 5], c: [1, 4], d: [2, 5] },
    constraints: ({ a, b, c, d }) => a < b && c < d && b !== d,
    contentFn: ({ a, b, c, d }) => `${a}/${b}와 ${c}/${d}를 통분하면 분모는?`,
    answerFn: ({ b, d }) => lcmHelper(b, d),
    distractorFns: [
      ({ b, d }) => b * d,
      ({ b, d }) => lcmHelper(b, d) / 2,
      ({ b, d }) => gcdHelper(b, d),
    ],
    explanationFn: ({ b, d }, ans) =>
      `${b}와 ${d}의 최소공배수는 ${ans}이므로 공통분모는 ${ans}입니다.`,
  },

  // Lv.9: 분수 혼합 계산
  {
    id: 'e5-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E5-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 6], c: [2, 5], d: [2, 6], e: [1, 4] },
    constraints: ({ a, b, c, d, e }) => {
      const num = a * d + c * b - e * b
      return b !== d && a < b && c < d && e < d && num > 0
    },
    contentFn: ({ a, b, c, d, e }) => `${a}/${b} + ${c}/${d} - ${e}/${d} = ?`,
    answerFn: ({ a, b, c, d, e }) => {
      const num = a * d + c * b - e * b
      const den = b * d
      return simplifyFraction(num, den)
    },
    distractorFns: [
      ({ a, b, c, d, e }) => `${a + c - e}/${b + d - d}`,
      ({ a, b, c, d, e }) => `${a * d + c * b - e * b}/${b * d}`,
      ({ a, b, c, e }) => simplifyFraction(a + c - e, b),
    ],
    explanationFn: ({ a, b, c, d, e }, ans) =>
      `${a}/${b} + ${c}/${d} - ${e}/${d} = ${a * d}/${b * d} + ${c * b}/${b * d} - ${e * b}/${b * d} = ${a * d + c * b - e * b}/${b * d} = ${ans}`,
  },
  {
    id: 'e5-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E5-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 7], c: [1, 4], d: [3, 7], e: [1, 3] },
    constraints: ({ a, b, c, d, e }) => {
      const num = a * d - c * b + e * b
      return b !== d && a < b && c < d && e < d && num > 0
    },
    contentFn: ({ a, b, c, d, e }) => `${a}/${b} - ${c}/${d} + ${e}/${d} = ?`,
    answerFn: ({ a, b, c, d, e }) => {
      const num = a * d - c * b + e * b
      const den = b * d
      return simplifyFraction(num, den)
    },
    distractorFns: [
      ({ a, b, c, d, e }) => `${a * d - c * b + e * b}/${b * d}`,
      ({ a, c, e }) => `${a - c + e}`,
      ({ a, b, c, d, e }) => simplifyFraction(a * d + c * b + e * b, b * d),
    ],
    explanationFn: ({ a, b, c, d, e }, ans) =>
      `${a}/${b} - ${c}/${d} + ${e}/${d} = ${a * d}/${b * d} - ${c * b}/${b * d} + ${e * b}/${b * d} = ${ans}`,
  },

  // Lv.10: 소수 + 분수 혼합
  {
    id: 'e5-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E5-NUM-09',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '0.5 + 1/4 = ?',
        '0.25 + 1/2 = ?',
        '0.75 - 1/4 = ?',
        '1.5 - 1/2 = ?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['3/4', '3/4', '1/2', '1']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['1/2', '1/2', '1/4', '1/2'][variant]!,
      ({ variant }) => ['1', '1', '3/4', '2'][variant]!,
      ({ variant }) => ['0.75', '0.75', '0.5', '1.0'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '0.5 + 1/4 = 1/2 + 1/4 = 2/4 + 1/4 = 3/4',
        '0.25 + 1/2 = 1/4 + 1/2 = 1/4 + 2/4 = 3/4',
        '0.75 - 1/4 = 3/4 - 1/4 = 2/4 = 1/2',
        '1.5 - 1/2 = 3/2 - 1/2 = 2/2 = 1',
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'e5-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E5-NUM-09',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '2/5 + 0.4 = ?',
        '3/5 - 0.2 = ?',
        '0.6 + 1/5 = ?',
        '0.8 - 2/5 = ?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['4/5', '2/5', '4/5', '2/5']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['3/5', '3/5', '3/5', '3/5'][variant]!,
      ({ variant }) => ['1', '1/5', '1', '1/5'][variant]!,
      ({ variant }) => ['0.8', '0.4', '0.8', '0.4'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '2/5 + 0.4 = 2/5 + 2/5 = 4/5',
        '3/5 - 0.2 = 3/5 - 1/5 = 2/5',
        '0.6 + 1/5 = 3/5 + 1/5 = 4/5',
        '0.8 - 2/5 = 4/5 - 2/5 = 2/5',
      ]
      return explanations[variant]!
    },
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 약수와 배수 정의
  {
    id: 'e5-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E5-NUM-01',
    pattern: '',
    paramRanges: { a: [6, 24] },
    constraints: ({ a }) => countDivisors(a) >= 4,
    contentFn: ({ a }) => `${a}의 약수를 모두 구하면 몇 개입니까?`,
    answerFn: ({ a }) => countDivisors(a),
    distractorFns: [
      ({ a }) => countDivisors(a) + 1,
      ({ a }) => countDivisors(a) - 1,
      ({ a }) => Math.floor(a / 2),
    ],
    explanationFn: ({ a }, ans) => {
      const divisors: number[] = []
      for (let i = 1; i <= a; i++) {
        if (a % i === 0) divisors.push(i)
      }
      return `${a}의 약수는 ${divisors.join(', ')}이고, 총 ${ans}개입니다.`
    },
  },
  {
    id: 'e5-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E5-NUM-01',
    pattern: '',
    paramRanges: { a: [2, 9], b: [1, 5] },
    contentFn: ({ a, b }) => `${a}의 ${b}번째 배수는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * (b + 1),
      ({ a, b }) => a * (b - 1),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}의 배수는 ${a}, ${a * 2}, ${a * 3}, ... 이므로 ${b}번째 배수는 ${ans}입니다.`,
  },

  // Lv.2: 공약수 · 최대공약수
  {
    id: 'e5-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E5-NUM-02',
    pattern: '',
    paramRanges: { a: [4, 16], b: [4, 20] },
    constraints: ({ a, b }) => {
      const g = gcdHelper(a, b)
      return g > 1 && a !== b
    },
    contentFn: ({ a, b }) => `${a}와 ${b}의 최대공약수는?`,
    answerFn: ({ a, b }) => gcdHelper(a, b),
    distractorFns: [
      ({ a, b }) => gcdHelper(a, b) + 1,
      ({ a, b }) => gcdHelper(a, b) - 1,
      ({ a, b }) => gcdHelper(a, b) * 2,
    ],
    explanationFn: ({ a, b }, ans) => {
      const divisorsA: number[] = []
      const divisorsB: number[] = []
      for (let i = 1; i <= a; i++) if (a % i === 0) divisorsA.push(i)
      for (let i = 1; i <= b; i++) if (b % i === 0) divisorsB.push(i)
      const common = divisorsA.filter((d) => divisorsB.includes(d))
      return `${a}의 약수: ${divisorsA.join(', ')}\n${b}의 약수: ${divisorsB.join(', ')}\n공약수: ${common.join(', ')}\n최대공약수: ${ans}`
    },
  },
  {
    id: 'e5-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E5-NUM-02',
    pattern: '',
    paramRanges: { a: [6, 18], b: [8, 24] },
    constraints: ({ a, b }) => gcdHelper(a, b) > 2 && a !== b,
    contentFn: ({ a, b }) => `${a}와 ${b}의 공약수는 모두 몇 개입니까?`,
    answerFn: ({ a, b }) => {
      const g = gcdHelper(a, b)
      return countDivisors(g)
    },
    distractorFns: [
      ({ a, b }) => {
        const g = gcdHelper(a, b)
        return countDivisors(g) + 1
      },
      ({ a, b }) => {
        const g = gcdHelper(a, b)
        return countDivisors(g) - 1
      },
      ({ a, b }) => gcdHelper(a, b),
    ],
    explanationFn: ({ a, b }, ans) => {
      const g = gcdHelper(a, b)
      const divisors: number[] = []
      for (let i = 1; i <= g; i++) if (g % i === 0) divisors.push(i)
      return `최대공약수 ${g}의 약수는 ${divisors.join(', ')}이고, 총 ${ans}개입니다.`
    },
  },

  // Lv.3: 공배수 · 최소공배수
  {
    id: 'e5-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E5-NUM-03',
    pattern: '',
    paramRanges: { a: [2, 8], b: [3, 9] },
    constraints: ({ a, b }) => a !== b && lcmHelper(a, b) <= 72,
    contentFn: ({ a, b }) => `${a}와 ${b}의 최소공배수는?`,
    answerFn: ({ a, b }) => lcmHelper(a, b),
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => gcdHelper(a, b),
      ({ a, b }) => lcmHelper(a, b) / 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}와 ${b}의 최소공배수는 ${ans}입니다.`,
  },
  {
    id: 'e5-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E5-NUM-03',
    pattern: '',
    paramRanges: { a: [3, 7], b: [4, 8], n: [2, 3] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b, n }) => `${a}와 ${b}의 공배수 중 ${n}번째로 작은 수는?`,
    answerFn: ({ a, b, n }) => lcmHelper(a, b) * n,
    distractorFns: [
      ({ a, b, n }) => lcmHelper(a, b) * (n + 1),
      ({ a, b }) => lcmHelper(a, b),
      ({ a, b, n }) => a * b * n,
    ],
    explanationFn: ({ a, b, n }, ans) => {
      const lcm = lcmHelper(a, b)
      return `최소공배수는 ${lcm}이므로 ${n}번째 공배수는 ${lcm} × ${n} = ${ans}입니다.`
    },
  },

  // Lv.4: 직육면체 · 정육면체
  {
    id: 'e5-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E5-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '정육면체의 면은 몇 개입니까?',
        '정육면체의 모서리는 몇 개입니까?',
        '정육면체의 꼭짓점은 몇 개입니까?',
        '직육면체의 면은 몇 개입니까?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [6, 12, 8, 6]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [8, 8, 6, 8][variant]!,
      ({ variant }) => [12, 6, 12, 12][variant]!,
      ({ variant }) => [4, 4, 4, 4][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '정육면체는 6개의 정사각형 면으로 이루어져 있습니다.',
        '정육면체는 12개의 모서리가 있습니다.',
        '정육면체는 8개의 꼭짓점이 있습니다.',
        '직육면체는 6개의 직사각형 면으로 이루어져 있습니다.',
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'e5-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E5-GEO-01',
    pattern: '',
    paramRanges: { a: [2, 8] },
    contentFn: ({ a }) => `한 모서리가 ${a}cm인 정육면체의 모든 모서리의 길이의 합은?`,
    answerFn: ({ a }) => a * 12,
    distractorFns: [
      ({ a }) => a * 6,
      ({ a }) => a * 8,
      ({ a }) => a * 4,
    ],
    explanationFn: ({ a }, ans) =>
      `정육면체의 모서리는 12개이므로 ${a} × 12 = ${ans}cm입니다.`,
  },

  // Lv.5: 넓이 구하기 (직사각형)
  {
    id: 'e5-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E5-GEO-02',
    pattern: '',
    paramRanges: { a: [3, 12], b: [2, 10] },
    contentFn: ({ a, b }) => `가로가 ${a}cm, 세로가 ${b}cm인 직사각형의 넓이는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => (a + b) * 2,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `직사각형의 넓이 = 가로 × 세로 = ${a} × ${b} = ${ans}cm²`,
  },
  {
    id: 'e5-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E5-GEO-02',
    pattern: '',
    paramRanges: { a: [4, 15], b: [20, 100] },
    constraints: ({ a, b }) => b % a === 0,
    contentFn: ({ a, b }) => `넓이가 ${b}cm²이고 가로가 ${a}cm인 직사각형의 세로는?`,
    answerFn: ({ a, b }) => b / a,
    distractorFns: [
      ({ a, b }) => b - a,
      ({ a, b }) => b / a + 1,
      ({ a, b }) => b / a - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `세로 = 넓이 ÷ 가로 = ${b} ÷ ${a} = ${ans}cm`,
  },

  // Lv.6: 넓이 구하기 (삼각형)
  {
    id: 'e5-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo',
    conceptId: 'E5-GEO-03',
    pattern: '',
    paramRanges: { a: [4, 12], b: [3, 10] },
    constraints: ({ a, b }) => (a * b) % 2 === 0,
    contentFn: ({ a, b }) => `밑변이 ${a}cm, 높이가 ${b}cm인 삼각형의 넓이는?`,
    answerFn: ({ a, b }) => (a * b) / 2,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => (a * b) / 2 + 1,
      ({ a, b }) => (a + b) / 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `삼각형의 넓이 = (밑변 × 높이) ÷ 2 = (${a} × ${b}) ÷ 2 = ${ans}cm²`,
  },
  {
    id: 'e5-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo',
    conceptId: 'E5-GEO-03',
    pattern: '',
    paramRanges: { a: [6, 14], b: [4, 10] },
    contentFn: ({ a, b }) => `밑변이 ${a}cm, 높이가 ${b}cm인 평행사변형의 넓이는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => (a * b) / 2,
      ({ a, b }) => (a + b) * 2,
      ({ a, b }) => a * b + 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `평행사변형의 넓이 = 밑변 × 높이 = ${a} × ${b} = ${ans}cm²`,
  },

  // Lv.7: 평균 계산
  {
    id: 'e5-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'data',
    conceptId: 'E5-STA-01',
    pattern: '',
    paramRanges: { a: [60, 90], b: [65, 95], c: [70, 100] },
    constraints: ({ a, b, c }) => (a + b + c) % 3 === 0,
    contentFn: ({ a, b, c }) => `${a}점, ${b}점, ${c}점의 평균은?`,
    answerFn: ({ a, b, c }) => (a + b + c) / 3,
    distractorFns: [
      ({ a, b, c }) => (a + b + c) / 3 + 1,
      ({ a, b, c }) => (a + b + c) / 3 - 1,
      ({ a, b, c }) => a + b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `평균 = (${a} + ${b} + ${c}) ÷ 3 = ${a + b + c} ÷ 3 = ${ans}점`,
  },
  {
    id: 'e5-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'data',
    conceptId: 'E5-STA-01',
    pattern: '',
    paramRanges: { a: [10, 25], b: [15, 30], c: [20, 35], d: [12, 28] },
    constraints: ({ a, b, c, d }) => (a + b + c + d) % 4 === 0,
    contentFn: ({ a, b, c, d }) => `${a}, ${b}, ${c}, ${d}의 평균은?`,
    answerFn: ({ a, b, c, d }) => (a + b + c + d) / 4,
    distractorFns: [
      ({ a, b, c, d }) => (a + b + c + d) / 4 + 1,
      ({ a, b, c, d }) => (a + b + c + d) / 4 - 1,
      ({ a, b, c, d }) => (a + b + c + d) / 3,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `평균 = (${a} + ${b} + ${c} + ${d}) ÷ 4 = ${a + b + c + d} ÷ 4 = ${ans}`,
  },

  // Lv.8: 가능성과 경우의 수 기초
  {
    id: 'e5-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'data',
    conceptId: 'E5-STA-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '주사위를 한 번 던질 때 나올 수 있는 경우는 모두 몇 가지입니까?',
        '동전을 한 번 던질 때 나올 수 있는 경우는 모두 몇 가지입니까?',
        '1부터 5까지의 수 중 하나를 뽑을 때 경우의 수는?',
        '가위, 바위, 보 중 하나를 낼 때 경우의 수는?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [6, 2, 5, 3]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [5, 3, 4, 2][variant]!,
      ({ variant }) => [4, 1, 6, 4][variant]!,
      ({ variant }) => [3, 4, 3, 5][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '주사위의 눈은 1, 2, 3, 4, 5, 6으로 6가지입니다.',
        '동전은 앞면, 뒷면 2가지입니다.',
        '1, 2, 3, 4, 5로 5가지입니다.',
        '가위, 바위, 보로 3가지입니다.',
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'e5-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'data',
    conceptId: 'E5-STA-02',
    pattern: '',
    paramRanges: { a: [2, 4], b: [2, 5] },
    contentFn: ({ a, b }) => `모자 ${a}개와 신발 ${b}켤레가 있습니다. 한 개씩 골라 입을 수 있는 경우의 수는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `모자 ${a}가지 × 신발 ${b}가지 = ${ans}가지`,
  },

  // Lv.9: 문장제 (약수 · 배수)
  {
    id: 'e5-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E5-NUM-01',
    pattern: '',
    paramRanges: { a: [12, 36] },
    constraints: ({ a }) => countDivisors(a) >= 5,
    contentFn: ({ a }) => `사탕 ${a}개를 몇 명에게 남김없이 똑같이 나누어 줄 수 있는 방법은 몇 가지입니까?`,
    answerFn: ({ a }) => countDivisors(a),
    distractorFns: [
      ({ a }) => countDivisors(a) + 1,
      ({ a }) => countDivisors(a) - 1,
      ({ a }) => countDivisors(a) - 2,
    ],
    explanationFn: ({ a }, ans) => {
      const divisors: number[] = []
      for (let i = 1; i <= a; i++) {
        if (a % i === 0) divisors.push(i)
      }
      return `${a}의 약수는 ${divisors.join(', ')}이므로 ${ans}가지 방법이 있습니다.`
    },
  },
  {
    id: 'e5-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E5-NUM-01',
    pattern: '',
    paramRanges: { a: [8, 20], b: [6, 18] },
    constraints: ({ a, b }) => gcdHelper(a, b) > 1 && a !== b,
    contentFn: ({ a, b }) => `연필 ${a}자루와 지우개 ${b}개를 최대한 많은 학생에게 남김없이 똑같이 나누어 줄 때, 최대 몇 명에게 나누어 줄 수 있습니까?`,
    answerFn: ({ a, b }) => gcdHelper(a, b),
    distractorFns: [
      ({ a, b }) => gcdHelper(a, b) + 1,
      ({ a, b }) => gcdHelper(a, b) - 1,
      ({ a, b }) => Math.min(a, b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}와 ${b}의 최대공약수는 ${ans}이므로 최대 ${ans}명에게 나누어 줄 수 있습니다.`,
  },

  // Lv.10: 복합 넓이 문제
  {
    id: 'e5-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'geo',
    conceptId: 'E5-GEO-03',
    pattern: '',
    paramRanges: { a: [8, 16], b: [6, 12] },
    constraints: ({ a, b }) => a > b && (a * b) % 2 === 0,
    contentFn: ({ a, b }) => `가로 ${a}cm, 세로 ${b}cm인 직사각형에서 밑변 ${a}cm, 높이 ${b}cm인 삼각형을 뺀 넓이는?`,
    answerFn: ({ a, b }) => a * b - (a * b) / 2,
    distractorFns: [
      ({ a, b }) => (a * b) / 2,
      ({ a, b }) => a * b,
      ({ a, b }) => a * b - (a * b) / 2 + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `직사각형 넓이 ${a * b}cm² - 삼각형 넓이 ${(a * b) / 2}cm² = ${ans}cm²`,
  },
  {
    id: 'e5-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'geo',
    conceptId: 'E5-GEO-03',
    pattern: '',
    paramRanges: { a: [6, 12], b: [4, 10], c: [3, 7] },
    constraints: ({ a, b, c }) => a > c && (a * b) % 2 === 0 && (c * b) % 2 === 0,
    contentFn: ({ a, b, c }) => `밑변 ${a}cm, 높이 ${b}cm인 삼각형과 밑변 ${c}cm, 높이 ${b}cm인 삼각형의 넓이의 합은?`,
    answerFn: ({ a, b, c }) => (a * b) / 2 + (c * b) / 2,
    distractorFns: [
      ({ a, b, c }) => ((a + c) * b) / 2,
      ({ a, b }) => (a * b) / 2,
      ({ a, b, c }) => (a * b + c * b) / 2 + 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `첫 번째 삼각형: ${(a * b) / 2}cm² + 두 번째 삼각형: ${(c * b) / 2}cm² = ${ans}cm²`,
  },
]

export const elementary5Templates: QuestionTemplate[] = [...comp, ...conc]
