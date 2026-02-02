// 중3 (middle_3) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import { signedStr } from '../utils/math'

const G = 'middle_3' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 제곱근 계산
  {
    id: 'm3-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M3-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 12] },
    contentFn: ({ a }) => `√${a * a}의 값은?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => a * a,
      ({ a }) => a + 1,
      ({ a }) => a - 1,
    ],
    explanationFn: ({ a }, ans) => `√${a * a} = √(${a}²) = ${ans}`,
  },
  {
    id: 'm3-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M3-NUM-01',
    pattern: '',
    paramRanges: { a: [2, 10] },
    contentFn: ({ a }) => `제곱근 ${a * a}의 양의 값은?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => -a,
      ({ a }) => a * a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a }, ans) => `√${a * a} = ${ans}`,
  },

  // Lv.2: 근호 간소화
  {
    id: 'm3-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-03',
    pattern: '',
    paramRanges: { a: [2, 5], b: [2, 7] },
    constraints: ({ b }) => {
      // b는 제곱인수가 없는 수
      const primes = [2, 3, 5, 7]
      for (const p of primes) {
        if (b % (p * p) === 0) return false
      }
      return true
    },
    contentFn: ({ a, b }) => `√${a * a * b}을 간단히 하면 ?√${b} 형태입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a }) => a * a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `√${a * a * b} = √(${a}² × ${b}) = ${ans}√${b}`,
  },
  {
    id: 'm3-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-03',
    pattern: '',
    paramRanges: { a: [2, 4], b: [2, 5] },
    constraints: ({ b }) => {
      const primes = [2, 3, 5]
      for (const p of primes) {
        if (b % (p * p) === 0) return false
      }
      return true
    },
    contentFn: ({ a, b }) => `√${a * a * b}를 간단히 하시오.`,
    answerFn: ({ a, b }) => `${a}√${b}`,
    distractorFns: [
      ({ a, b }) => `√${a * a * b}`,
      ({ a, b }) => `${a * b}`,
      ({ a, b }) => `${a}√${a * b}`,
    ],
    explanationFn: ({ a, b }) =>
      `√${a * a * b} = ${a}√${b}`,
  },

  // Lv.3: 근호 덧뺄셈
  {
    id: 'm3-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M3-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 7], b: [1, 7], n: [2, 7] },
    constraints: ({ n }) => {
      const primes = [2, 3, 5, 7]
      for (const p of primes) {
        if (n % (p * p) === 0) return false
      }
      return true
    },
    contentFn: ({ a, b, n }) => `${a}√${n} + ${b}√${n} = ?√${n}. ?에 들어갈 수는?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b, n }, ans) =>
      `${a}√${n} + ${b}√${n} = (${a} + ${b})√${n} = ${ans}√${n}`,
  },
  {
    id: 'm3-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M3-NUM-04',
    pattern: '',
    paramRanges: { a: [3, 9], b: [1, 6], n: [2, 5] },
    constraints: ({ a, b, n }) => {
      const primes = [2, 3, 5]
      for (const p of primes) {
        if (n % (p * p) === 0) return false
      }
      return a > b
    },
    contentFn: ({ a, b, n }) => `${a}√${n} - ${b}√${n}의 값은?`,
    answerFn: ({ a, b, n }) => `${a - b}√${n}`,
    distractorFns: [
      ({ a, b }) => `${a - b}`,
      ({ a, b, n }) => `${a + b}√${n}`,
      ({ a, b, n }) => `${a * b}√${n}`,
    ],
    explanationFn: ({ a, b, n }, ans) =>
      `${a}√${n} - ${b}√${n} = (${a} - ${b})√${n} = ${ans}`,
  },

  // Lv.4: 근호 곱셈
  {
    id: 'm3-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M3-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `√${a} × √${b} = √?. ?에 들어갈 수는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => (a * b) / 2,
      ({ a, b }) => a * b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `√${a} × √${b} = √(${a} × ${b}) = √${ans}`,
  },
  {
    id: 'm3-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M3-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6], c: [2, 5] },
    contentFn: ({ a, b, c }) => `${a}√${b} × ${c}의 값은?`,
    answerFn: ({ a, b, c }) => `${a * c}√${b}`,
    distractorFns: [
      ({ a, c }) => `${a * c}`,
      ({ a, b, c }) => `${a + c}√${b}`,
      ({ a, b, c }) => `${a}√${b * c}`,
    ],
    explanationFn: ({ a, b, c }) =>
      `${a}√${b} × ${c} = ${a * c}√${b}`,
  },

  // Lv.5: 근호 나눗셈
  {
    id: 'm3-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M3-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `√${a * b} ÷ √${a} = √?. ?에 들어갈 수는?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => a * b,
      ({ b }) => b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `√${a * b} ÷ √${a} = √(${a * b} ÷ ${a}) = √${ans}`,
  },
  {
    id: 'm3-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M3-NUM-05',
    pattern: '',
    paramRanges: { a: [3, 8], b: [2, 6], c: [2, 5] },
    constraints: ({ a, c }) => a % c === 0,
    contentFn: ({ a, b, c }) => `${a}√${b} ÷ ${c}의 값은?`,
    answerFn: ({ a, b, c }) => `${a / c}√${b}`,
    distractorFns: [
      ({ a, b, c }) => `${a}√${b / c}`,
      ({ a, c }) => `${a / c}`,
      ({ a, b, c }) => `${a - c}√${b}`,
    ],
    explanationFn: ({ a, b, c }) =>
      `${a}√${b} ÷ ${c} = ${a / c}√${b}`,
  },

  // Lv.6: 유리화
  {
    id: 'm3-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M3-NUM-06',
    pattern: '',
    paramRanges: { a: [1, 9], b: [2, 7] },
    constraints: ({ b }) => {
      const primes = [2, 3, 5, 7]
      for (const p of primes) {
        if (b % (p * p) === 0) return false
      }
      return true
    },
    contentFn: ({ a, b }) => `${a}/√${b}를 유리화하면 분모는?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => a * b,
      ({ b }) => b * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}/√${b} = (${a}√${b})/${b}이므로 분모는 ${ans}`,
  },
  {
    id: 'm3-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M3-NUM-06',
    pattern: '',
    paramRanges: { a: [2, 8], b: [2, 7] },
    constraints: ({ b }) => {
      const primes = [2, 3, 5, 7]
      for (const p of primes) {
        if (b % (p * p) === 0) return false
      }
      return true
    },
    contentFn: ({ a, b }) => `${a}/√${b}를 유리화하면 분자는?`,
    answerFn: ({ a, b }) => `${a}√${b}`,
    distractorFns: [
      ({ a }) => `${a}`,
      ({ a, b }) => `√${a * b}`,
      ({ a, b }) => `${a * b}`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}/√${b} = (${a}√${b})/(√${b} × √${b}) = ${ans}/${b}`,
  },

  // Lv.7: 인수분해 (공통인수)
  {
    id: 'm3-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 7], b: [2, 7] },
    contentFn: ({ a, b }) => `${a}x² + ${b}x의 공통인수 x로 묶으면 x(?x + ?)입니다. 첫 번째 ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => a + b,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}x² + ${b}x = x(${ans}x + ${b})`,
  },
  {
    id: 'm3-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6], c: [2, 5] },
    contentFn: ({ a, b, c }) => `${a * c}x² + ${b * c}x를 인수분해하면 ?x(?x + ?)입니다. 가장 왼쪽 ?에 들어갈 수는?`,
    answerFn: ({ c }) => c,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => b,
      ({ a, c }) => a * c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a * c}x² + ${b * c}x = ${ans}x(${a}x + ${b})`,
  },

  // Lv.8: 인수분해 (x² + bx + c)
  {
    id: 'm3-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 6], b: [2, 7] },
    constraints: ({ a, b }) => a > 0 && b > 0 && a !== b,
    contentFn: ({ a, b }) => `x² + ${a + b}x + ${a * b}을 인수분해하면 (x + ?)(x + ?)입니다. 작은 ?의 값은?`,
    answerFn: ({ a, b }) => Math.min(a, b),
    distractorFns: [
      ({ a, b }) => Math.max(a, b),
      ({ a, b }) => a + b,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b }) => {
      const min = Math.min(a, b)
      const max = Math.max(a, b)
      return `x² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
    },
  },
  {
    id: 'm3-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6] },
    constraints: ({ a, b }) => a > 0 && b > 0 && a !== b,
    contentFn: ({ a, b }) => `x² + ${a + b}x + ${a * b}을 인수분해하면 (x + ?)(x + ?)입니다. 큰 ?의 값은?`,
    answerFn: ({ a, b }) => Math.max(a, b),
    distractorFns: [
      ({ a, b }) => Math.min(a, b),
      ({ a, b }) => a + b,
      ({ a, b }) => (a + b) / 2,
    ],
    explanationFn: ({ a, b }) => {
      const min = Math.min(a, b)
      const max = Math.max(a, b)
      return `x² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
    },
  },

  // Lv.9: 인수분해 (완전제곱식)
  {
    id: 'm3-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra',
    conceptId: 'M3-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `x² + ${2 * a}x + ${a * a} = (x + ?)²입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => 2 * a,
      ({ a }) => a * a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `x² + ${2 * a}x + ${a * a} = x² + 2 × ${a}x + ${a}² = (x + ${ans})²`,
  },
  {
    id: 'm3-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra',
    conceptId: 'M3-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 8] },
    contentFn: ({ a }) => `x² - ${2 * a}x + ${a * a} = (x - ?)²입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => -a,
      ({ a }) => 2 * a,
      ({ a }) => a * a,
    ],
    explanationFn: ({ a }, ans) =>
      `x² - ${2 * a}x + ${a * a} = (x - ${ans})²`,
  },

  // Lv.10: 복합 인수분해
  {
    id: 'm3-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `x² - ${a * a} = (x + ?)(x - ?)입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => a * a,
      ({ a }) => 2 * a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `x² - ${a * a} = x² - ${a}² = (x + ${ans})(x - ${ans})`,
  },
  {
    id: 'm3-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6] },
    contentFn: ({ a, b }) => `${a * a}x² - ${b * b} = (?x + ${b})(?x - ${b})입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => a * b,
      ({ a }) => a * a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a * a}x² - ${b * b} = (${a}x)² - ${b}² = (${ans}x + ${b})(${ans}x - ${b})`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 제곱근의 뜻
  {
    id: 'm3-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'M3-NUM-01',
    pattern: '',
    paramRanges: { a: [4, 100], variant: [0, 3] },
    constraints: ({ a }) => {
      const sqrt = Math.sqrt(a)
      return sqrt === Math.floor(sqrt)
    },
    contentFn: ({ a, variant }) => {
      const questions = [
        `어떤 수를 제곱하면 ${a}가 되는 양수는?`,
        `제곱하여 ${a}가 되는 수 중 양수는?`,
        `${a}의 제곱근 중 양의 제곱근은?`,
        `√${a}의 값은?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ a }) => Math.sqrt(a),
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a / 2,
      ({ a }) => -Math.sqrt(a),
    ],
    explanationFn: ({ a }, ans) =>
      `${ans}² = ${a}이므로 제곱근 ${a}의 양수는 ${ans}입니다.`,
  },
  {
    id: 'm3-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'M3-NUM-01',
    pattern: '',
    paramRanges: { a: [4, 64], variant: [0, 2] },
    constraints: ({ a }) => {
      const sqrt = Math.sqrt(a)
      return sqrt === Math.floor(sqrt)
    },
    contentFn: ({ a, variant }) => {
      const questions = [
        `${a}의 제곱근은 ±?입니다. ?에 들어갈 수는?`,
        `제곱하여 ${a}가 되는 수의 절댓값은?`,
        `-√${a}의 절댓값은?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ a }) => Math.sqrt(a),
    distractorFns: [
      ({ a }) => a,
      ({ a }) => -Math.sqrt(a),
      ({ a }) => a / 2,
    ],
    explanationFn: ({ a }, ans) =>
      `${a}의 제곱근은 ±${ans}입니다.`,
  },

  // Lv.2: 무리수 판별
  {
    id: 'm3-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '다음 중 무리수인 것은?',
        '다음 중 유리수가 아닌 것은?',
        '다음 중 순환하지 않는 무한소수인 것은?',
        '다음 중 분수로 나타낼 수 없는 것은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['√2', '√3', '√5', '√7']
      return answers[variant]!
    },
    distractorFns: [
      () => '√4',
      () => '0.333...',
      () => '22/7',
    ],
    explanationFn: (_, ans) =>
      `${ans}는 제곱근이 정수가 아닌 무리수입니다.`,
    questionType: 'multiple_choice',
  },
  {
    id: 'm3-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-02',
    pattern: '',
    paramRanges: { a: [2, 15], variant: [0, 2] },
    constraints: ({ a }) => {
      const sqrt = Math.sqrt(a)
      return sqrt !== Math.floor(sqrt)
    },
    contentFn: ({ a, variant }) => {
      const questions = [
        `√${a}는 무리수입니까?`,
        `√${a}를 분수로 나타낼 수 있습니까?`,
        `√${a}는 순환소수입니까?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['무리수', '없다', '아니다']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['유리수', '있다', '순환소수'][variant]!,
      ({ variant }) => ['정수', '가능하다', '맞다'][variant]!,
      ({ variant }) => ['자연수', '분수', '순환'][variant]!,
    ],
    explanationFn: ({ a }, ans) =>
      `√${a}는 ${ans}입니다.`,
    questionType: 'multiple_choice',
  },

  // Lv.3: 인수분해 개념
  {
    id: 'm3-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [2, 5], variant: [0, 2] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b, variant }) => {
      const questions = [
        `x² + ${a + b}x + ${a * b}을 인수분해하면?`,
        `x² + ${a + b}x + ${a * b} = (x + ?)(x + ?)일 때, 두 ?의 곱은?`,
        `x² + ${a + b}x + ${a * b}을 인수의 곱으로 나타내면?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ a, b, variant }) => {
      const min = Math.min(a, b)
      const max = Math.max(a, b)
      if (variant === 1) return a * b
      return `(x + ${min})(x + ${max})`
    },
    distractorFns: [
      ({ a, b }) => `(x + ${a + b})(x + 1)`,
      ({ a, b, variant }) => variant === 1 ? a + b : `x² + ${a * b}`,
      ({ a, b, variant }) => variant === 1 ? (a + b) * 2 : `(x + ${a})(x + ${b + 1})`,
    ],
    explanationFn: ({ a, b }) => {
      const min = Math.min(a, b)
      const max = Math.max(a, b)
      return `x² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
    },
    questionType: 'multiple_choice',
  },

  // Lv.4: 이차방정식 (인수분해)
  {
    id: 'm3-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'M3-ALG-05',
    pattern: '',
    paramRanges: { a: [1, 6], b: [2, 7] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `x² - ${a + b}x + ${a * b} = 0의 두 근의 합은?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a - b,
      ({ a, b }) => -(a + b),
    ],
    explanationFn: ({ a, b }, ans) => {
      return `x² - ${a + b}x + ${a * b} = (x - ${a})(x - ${b}) = 0\n` +
        `x = ${a} 또는 x = ${b}\n두 근의 합 = ${a} + ${b} = ${ans}`
    },
  },
  {
    id: 'm3-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'M3-ALG-05',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `x² - ${a + b}x + ${a * b} = 0의 두 근의 곱은?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => -(a * b),
      ({ a, b }) => (a + b) * 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(x - ${a})(x - ${b}) = 0의 두 근은 ${a}, ${b}이므로 곱은 ${ans}`,
  },

  // Lv.5: 이차방정식 (근의 공식)
  {
    id: 'm3-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M3-ALG-06',
    pattern: '',
    paramRanges: { b: [2, 8], c: [1, 10] },
    contentFn: ({ b, c }) => `x² + ${b}x + ${c} = 0에서 판별식 b² - 4c의 값은?`,
    answerFn: ({ b, c }) => b * b - 4 * c,
    distractorFns: [
      ({ b, c }) => b * b + 4 * c,
      ({ b, c }) => b - 4 * c,
      ({ b, c }) => 4 * c - b * b,
    ],
    explanationFn: ({ b, c }, ans) =>
      `판별식 D = b² - 4ac = ${b}² - 4 × 1 × ${c} = ${b * b} - ${4 * c} = ${ans}`,
  },
  {
    id: 'm3-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M3-ALG-06',
    pattern: '',
    paramRanges: { a: [1, 3], b: [2, 6], c: [1, 8] },
    contentFn: ({ a, b, c }) => `${a}x² + ${b}x + ${c} = 0의 판별식은?`,
    answerFn: ({ a, b, c }) => b * b - 4 * a * c,
    distractorFns: [
      ({ a, b, c }) => b * b + 4 * a * c,
      ({ b, c }) => b * b - 4 * c,
      ({ a, b, c }) => b - 4 * a * c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `D = b² - 4ac = ${b}² - 4 × ${a} × ${c} = ${ans}`,
  },

  // Lv.6: 이차함수 y = ax²
  {
    id: 'm3-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func',
    conceptId: 'M3-ALG-08',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 5] },
    contentFn: ({ a, b }) => `y = ${a}x²에서 x = ${b}일 때 y의 값은?`,
    answerFn: ({ a, b }) => a * b * b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b * b,
      ({ b }) => b * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `y = ${a} × ${b}² = ${a} × ${b * b} = ${ans}`,
  },
  {
    id: 'm3-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func',
    conceptId: 'M3-ALG-08',
    pattern: '',
    paramRanges: { a: [1, 4], b: [-4, 4] },
    constraints: ({ b }) => b !== 0,
    contentFn: ({ a, b }) => `y = ${a}x²에서 x = ${b}일 때 y의 값은?`,
    answerFn: ({ a, b }) => a * b * b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => -(a * b * b),
      ({ a, b }) => a * b + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `y = ${a} × (${b})² = ${a} × ${b * b} = ${ans}`,
  },

  // Lv.7: 이차함수 그래프 (꼭짓점, 축)
  {
    id: 'm3-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M3-ALG-09',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 8], c: [-5, 5] },
    contentFn: ({ a, b, c }) => `y = ${a}(x - ${b})² + ${signedStr(c)}의 꼭짓점 x좌표는?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ b }) => -b,
      ({ c }) => c,
      ({ a }) => a,
    ],
    explanationFn: ({ b }) =>
      `y = a(x - p)² + q 형태에서 꼭짓점의 x좌표는 p = ${b}`,
  },
  {
    id: 'm3-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M3-ALG-09',
    pattern: '',
    paramRanges: { a: [1, 4], b: [1, 7], c: [-6, 6] },
    contentFn: ({ a, b, c }) => `y = ${a}(x - ${b})² + ${signedStr(c)}의 축의 방정식은?`,
    answerFn: ({ b }) => `x = ${b}`,
    distractorFns: [
      ({ b }) => `x = ${-b}`,
      ({ c }) => `y = ${c}`,
      ({ b }) => `y = ${b}`,
    ],
    explanationFn: ({ b }) =>
      `이차함수의 축은 x = ${b}입니다.`,
    questionType: 'multiple_choice',
  },

  // Lv.8: 삼각비 (sin, cos, tan)
  {
    id: 'm3-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'M3-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '직각삼각형에서 빗변의 길이가 5, 높이가 3일 때 sin θ의 값은?',
        '직각삼각형에서 빗변이 5, 밑변이 4일 때 cos θ의 값은?',
        '직각삼각형에서 높이가 3, 밑변이 4일 때 tan θ의 값은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['3/5', '4/5', '3/4']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['5/3', '5/4', '4/3'][variant]!,
      ({ variant }) => ['4/5', '3/5', '4/5'][variant]!,
      ({ variant }) => ['3/4', '4/3', '5/3'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        'sin θ = 높이/빗변 = 3/5',
        'cos θ = 밑변/빗변 = 4/5',
        'tan θ = 높이/밑변 = 3/4',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },
  {
    id: 'm3-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'M3-GEO-02',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9], variant: [0, 2] },
    constraints: ({ a, b }) => {
      const c = Math.sqrt(a * a + b * b)
      return c === Math.floor(c)
    },
    contentFn: ({ a, b, variant }) => {
      const c = Math.sqrt(a * a + b * b)
      const questions = [
        `직각삼각형에서 높이 ${a}, 밑변 ${b}, 빗변 ${c}일 때 sin θ는?`,
        `직각삼각형에서 밑변 ${b}, 빗변 ${c}일 때 cos θ는?`,
        `높이 ${a}, 밑변 ${b}인 직각삼각형에서 tan θ는?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ a, b, variant }) => {
      const c = Math.sqrt(a * a + b * b)
      const answers = [`${a}/${c}`, `${b}/${c}`, `${a}/${b}`]
      return answers[variant]!
    },
    distractorFns: [
      ({ a, b, variant }) => {
        const c = Math.sqrt(a * a + b * b)
        return [`${b}/${c}`, `${a}/${c}`, `${b}/${a}`][variant]!
      },
      ({ a, b, variant }) => {
        const c = Math.sqrt(a * a + b * b)
        return [`${c}/${a}`, `${c}/${b}`, `${c}/${a}`][variant]!
      },
      ({ a, b, variant }) => [`${a}/${b}`, `${b}/${a}`, `${a + b}`][variant]!,
    ],
    explanationFn: ({ a, b, variant }) => {
      const c = Math.sqrt(a * a + b * b)
      const explanations = [
        `sin θ = 높이/빗변 = ${a}/${c}`,
        `cos θ = 밑변/빗변 = ${b}/${c}`,
        `tan θ = 높이/밑변 = ${a}/${b}`,
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.9: 원과 접선
  {
    id: 'm3-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo',
    conceptId: 'M3-GEO-05',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '원의 접선과 그 접점을 지나는 반지름은 항상 어떤 관계인가?',
        '원의 중심에서 접선까지의 거리는 무엇과 같은가?',
        '한 점에서 원에 그은 두 접선의 길이는?',
        '원의 접선은 접점에서 반지름과 이루는 각은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['수직', '반지름', '같다', '90도']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['평행', '지름', '다르다', '45도'][variant]!,
      ({ variant }) => ['같다', '현', '두 배', '180도'][variant]!,
      ({ variant }) => ['반대', '접선', '절반', '60도'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '원의 접선은 접점에서 반지름과 수직입니다.',
        '원의 중심에서 접선까지의 거리는 반지름과 같습니다.',
        '한 점에서 원에 그은 두 접선의 길이는 같습니다.',
        '접선은 접점에서 반지름과 직각(90도)을 이룹니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.10: 복합 응용
  {
    id: 'm3-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-07',
    pattern: '',
    paramRanges: { a: [1, 4], b: [1, 7], c: [-8, 8] },
    constraints: ({ a }) => a > 0,
    contentFn: ({ a, b, c }) => `이차함수 y = ${a}(x - ${b})² + ${signedStr(c)}의 최솟값은?`,
    answerFn: ({ c }) => c,
    distractorFns: [
      ({ b }) => b,
      ({ a }) => a,
      ({ b, c }) => b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `y = ${a}(x - ${b})² + ${signedStr(c)}는 a > 0이므로 아래로 볼록.\n꼭짓점 (${b}, ${c})에서 최솟값 = ${ans}`,
  },
  {
    id: 'm3-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-07',
    pattern: '',
    paramRanges: { a: [-4, -1], b: [1, 6], c: [-6, 6] },
    constraints: ({ a }) => a < 0,
    contentFn: ({ a, b, c }) => `이차함수 y = ${a}(x - ${b})² + ${signedStr(c)}의 최댓값은?`,
    answerFn: ({ c }) => c,
    distractorFns: [
      ({ b }) => b,
      ({ a, c }) => a + c,
      ({ c }) => -c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `y = ${a}(x - ${b})² + ${signedStr(c)}는 a < 0이므로 위로 볼록.\n꼭짓점 (${b}, ${c})에서 최댓값 = ${ans}`,
  },
]

export const middle3Templates: QuestionTemplate[] = [...comp, ...conc]
