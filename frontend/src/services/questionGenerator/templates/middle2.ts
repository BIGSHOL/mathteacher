// 중2 (middle_2) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import type { ProblemPart } from '../../../types'
import { signedStr } from '../utils/math'

const G = 'middle_2' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 단항식 × 단항식
  {
    id: 'm2-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [2, 4], c: [2, 5], d: [2, 4] },
    contentFn: ({ a, b, c, d }) => `${a}x^${b} × ${c}x^${d}의 계수는?`,
    answerFn: ({ a, c }) => a * c,
    distractorFns: [
      ({ a, c }) => a + c,
      ({ a, c }) => a * c + 1,
      ({ a, c }) => a * c - 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}x^${b} × ${c}x^${d} = ${ans}x^${b + d}\n계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 6], b: [1, 3], c: [2, 6], d: [1, 3] },
    contentFn: ({ a, b, c, d }) => `${a}x^${b} × ${c}x^${d}의 지수는?`,
    answerFn: ({ b, d }) => b + d,
    distractorFns: [
      ({ b, d }) => b * d,
      ({ b, d }) => b + d + 1,
      ({ b, d }) => b + d - 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}x^${b} × ${c}x^${d} = ${a * c}x^${ans}\n지수는 ${ans}입니다.`,
  },

  // Lv.2: 단항식 ÷ 단항식
  {
    id: 'm2-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 6], b: [3, 5], c: [2, 6], d: [1, 4] },
    constraints: ({ b, d }) => b > d,
    contentFn: ({ a, b, c, d }) => {
      const coef = a * c
      const exp = b + d
      return `${coef}x^${exp} ÷ ${c}x^${d}의 계수는?`
    },
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a, c }) => a * c,
      ({ a }) => a + 1,
      ({ a }) => a - 1,
    ],
    explanationFn: ({ a, b, c, d }) => {
      const coef = a * c
      const exp = b + d
      return `${coef}x^${exp} ÷ ${c}x^${d} = ${a}x^${b}\n계수는 ${a}입니다.`
    },
  },

  // Lv.3: 다항식 + 다항식
  {
    id: 'm2-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 8], b: [1, 10], c: [1, 8], d: [1, 10] },
    contentFn: ({ a, b, c, d }) => `(${a}x + ${b}) + (${c}x + ${d})에서 x의 계수는?`,
    answerFn: ({ a, c }) => a + c,
    distractorFns: [
      ({ b, d }) => b + d,
      ({ a, c }) => a + c + 1,
      ({ a, c }) => a + c - 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a}x + ${b}) + (${c}x + ${d}) = ${ans}x + ${b + d}\nx의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 8], b: [1, 10], c: [1, 8], d: [1, 10] },
    contentFn: ({ a, b, c, d }) => `(${a}x + ${b}) + (${c}x + ${d})에서 상수항은?`,
    answerFn: ({ b, d }) => b + d,
    distractorFns: [
      ({ a, c }) => a + c,
      ({ b, d }) => b + d + 1,
      ({ b, d }) => b + d - 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a}x + ${b}) + (${c}x + ${d}) = ${a + c}x + ${ans}\n상수항은 ${ans}입니다.`,
  },

  // Lv.4: 다항식 - 다항식
  {
    id: 'm2-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 9], b: [1, 10], c: [1, 8], d: [1, 10] },
    contentFn: ({ a, b, c, d }) => `(${a}x + ${b}) - (${c}x + ${d})에서 x의 계수는?`,
    answerFn: ({ a, c }) => a - c,
    distractorFns: [
      ({ a, c }) => a + c,
      ({ b, d }) => b - d,
      ({ a, c }) => a - c + 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a}x + ${b}) - (${c}x + ${d}) = ${ans}x + ${b - d}\nx의 계수는 ${ans}입니다.`,
  },

  // Lv.5: 단항식 × 다항식
  {
    id: 'm2-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 8], c: [1, 10] },
    contentFn: ({ a, b, c }) => `${a}(${b}x + ${c}) 전개 시 x의 계수는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, c }) => a * c,
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a}(${b}x + ${c}) = ${ans}x + ${a * c}\nx의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 8], c: [1, 10] },
    contentFn: ({ a, b, c }) => `${a}(${b}x + ${c}) 전개 시 상수항은?`,
    answerFn: ({ a, c }) => a * c,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, c }) => a + c,
      ({ a, c }) => a * c + 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a}(${b}x + ${c}) = ${a * b}x + ${ans}\n상수항은 ${ans}입니다.`,
  },

  // Lv.6: 다항식 × 다항식 (전개)
  {
    id: 'm2-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 8], b: [1, 8] },
    contentFn: ({ a, b }) => `(x + ${a})(x + ${b}) 전개 시 x의 계수는?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(x + ${a})(x + ${b}) = x² + ${ans}x + ${a * b}\nx의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 8], b: [1, 8] },
    contentFn: ({ a, b }) => `(x + ${a})(x + ${b}) 전개 시 상수항은?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(x + ${a})(x + ${b}) = x² + ${a + b}x + ${ans}\n상수항은 ${ans}입니다.`,
  },

  // Lv.7: 곱셈 공식 (a+b)²
  {
    id: 'm2-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `(x + ${a})²에서 x의 계수는?`,
    answerFn: ({ a }) => 2 * a,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a * a,
      ({ a }) => 2 * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `(x + ${a})² = x² + ${ans}x + ${a * a}\nx의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `(x + ${a})²에서 상수항은?`,
    answerFn: ({ a }) => a * a,
    distractorFns: [
      ({ a }) => 2 * a,
      ({ a }) => a,
      ({ a }) => a * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `(x + ${a})² = x² + ${2 * a}x + ${ans}\n상수항은 ${ans}입니다.`,
  },

  // Lv.8: 곱셈 공식 (a-b)², (a+b)(a-b)
  {
    id: 'm2-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `(x + ${a})(x - ${a}) = x² - ? (물음표에 들어갈 수는?)`,
    answerFn: ({ a }) => a * a,
    distractorFns: [
      ({ a }) => 2 * a,
      ({ a }) => a,
      ({ a }) => a * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `(x + ${a})(x - ${a}) = x² - ${ans}\n공식: (a+b)(a-b) = a² - b²`,
  },
  {
    id: 'm2-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `(x - ${a})²에서 x의 계수는?`,
    answerFn: ({ a }) => -2 * a,
    distractorFns: [
      ({ a }) => 2 * a,
      ({ a }) => -a,
      ({ a }) => -2 * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `(x - ${a})² = x² - ${2 * a}x + ${a * a}\nx의 계수는 ${ans}입니다.`,
  },

  // Lv.9: 연립방정식 계산 (대입법)
  {
    id: 'm2-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-07',
    pattern: '',
    paramRanges: { a: [5, 20], b: [1, 10] },
    constraints: ({ a, b }) => (a + b) % 2 === 0 && a > b,
    contentFn: ({ a, b }) => `x + y = ${a}, x - y = ${b} 일 때, x = ?`,
    answerFn: ({ a, b }) => (a + b) / 2,
    distractorFns: [
      ({ a, b }) => (a - b) / 2,
      ({ a, b }) => a + b,
      ({ a, b }) => (a + b) / 2 + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x + y = ${a}\nx - y = ${b}\n두 식을 더하면: 2x = ${a + b}\nx = ${ans}`,
  },
  {
    id: 'm2-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-07',
    pattern: '',
    paramRanges: { a: [5, 20], b: [1, 10] },
    constraints: ({ a, b }) => (a - b) % 2 === 0 && a > b,
    contentFn: ({ a, b }) => `x + y = ${a}, x - y = ${b} 일 때, y = ?`,
    answerFn: ({ a, b }) => (a - b) / 2,
    distractorFns: [
      ({ a, b }) => (a + b) / 2,
      ({ a, b }) => a - b,
      ({ a, b }) => (a - b) / 2 + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x + y = ${a}\nx - y = ${b}\n첫 번째 식에서 두 번째 식을 빼면: 2y = ${a - b}\ny = ${ans}`,
  },

  // Lv.10: 연립방정식 계산 (가감법)
  {
    id: 'm2-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-08',
    pattern: '',
    paramRanges: { a: [2, 5], c: [10, 30], d: [5, 20] },
    constraints: ({ c, d }) => (c - d) % 2 === 0 && c > d,
    contentFn: ({ a, c, d }) => `${a}x + y = ${c}, ${a}x - y = ${d} 일 때, y = ?`,
    answerFn: ({ c, d }) => (c - d) / 2,
    distractorFns: [
      ({ c, d }) => (c + d) / 2,
      ({ c, d }) => c - d,
      ({ c, d }) => (c - d) / 2 + 1,
    ],
    explanationFn: ({ a, c, d }, ans) =>
      `${a}x + y = ${c}\n${a}x - y = ${d}\n첫 번째 식에서 두 번째 식을 빼면: 2y = ${c - d}\ny = ${ans}`,
  },
  {
    id: 'm2-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-08',
    pattern: '',
    paramRanges: { a: [2, 5], c: [10, 30], d: [5, 20] },
    constraints: ({ a, c, d }) => (c + d) % (2 * a) === 0 && c > d,
    contentFn: ({ a, c, d }) => `${a}x + y = ${c}, ${a}x - y = ${d} 일 때, x = ?`,
    answerFn: ({ a, c, d }) => (c + d) / (2 * a),
    distractorFns: [
      ({ c, d }) => (c + d) / 2,
      ({ a, c, d }) => (c - d) / a,
      ({ a, c, d }) => (c + d) / (2 * a) + 1,
    ],
    explanationFn: ({ a, c, d }, ans) =>
      `${a}x + y = ${c}\n${a}x - y = ${d}\n두 식을 더하면: ${2 * a}x = ${c + d}\nx = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 단항식/다항식 구분
  {
    id: 'm2-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '3x² + 2x는 단항식인가, 다항식인가?',
        '5x³은 단항식인가, 다항식인가?',
        '2x + 3y - 1은 단항식인가, 다항식인가?',
        '7은 단항식인가, 다항식인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['다항식', '단항식', '다항식', '단항식']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['단항식', '다항식', '단항식', '다항식'][variant]!),
      () => '이항식',
      () => '상수',
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '3x² + 2x는 두 개의 단항식의 합이므로 다항식입니다.',
        '5x³은 하나의 항으로 이루어져 있으므로 단항식입니다.',
        '2x + 3y - 1은 세 개의 단항식의 합이므로 다항식입니다.',
        '7은 하나의 항(상수항)이므로 단항식입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.2: 부등식의 해 판별
  {
    id: 'm2-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-05',
    pattern: '',
    paramRanges: { a: [3, 10], b: [1, 12] },
    contentFn: ({ a, b }) => `x > ${a}일 때, x = ${b}는 해인가?`,
    answerFn: ({ a, b }) => (b > a ? '해이다' : '해가 아니다'),
    distractorFns: [
      ({ a, b }) => (b > a ? '해가 아니다' : '해이다'),
      () => '알 수 없다',
      () => '경계값이다',
    ],
    explanationFn: ({ a, b }) => {
      if (b > a) {
        return `${b} > ${a}이므로 x = ${b}는 해입니다.`
      } else {
        return `${b} ≤ ${a}이므로 x = ${b}는 해가 아닙니다.`
      }
    },
  },
  {
    id: 'm2-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-05',
    pattern: '',
    paramRanges: { a: [3, 10], b: [1, 12] },
    contentFn: ({ a, b }) => `x ≥ ${a}일 때, x = ${b}는 해인가?`,
    answerFn: ({ a, b }) => (b >= a ? '해이다' : '해가 아니다'),
    distractorFns: [
      ({ a, b }) => (b >= a ? '해가 아니다' : '해이다'),
      () => '알 수 없다',
      () => '경계값이다',
    ],
    explanationFn: ({ a, b }) => {
      if (b >= a) {
        return `${b} ≥ ${a}이므로 x = ${b}는 해입니다.`
      } else {
        return `${b} < ${a}이므로 x = ${b}는 해가 아닙니다.`
      }
    },
  },

  // Lv.3: 연립방정식 (대입법)
  {
    id: 'm2-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-07',
    pattern: '',
    paramRanges: { a: [2, 6], b: [6, 20] },
    constraints: ({ a, b }) => b % (a + 1) === 0,
    contentFn: ({ a, b }) => `y = ${a}x, x + y = ${b} 일 때, x = ?`,
    answerFn: ({ a, b }) => b / (a + 1),
    distractorFns: [
      ({ a, b }) => b / a,
      ({ b }) => b,
      ({ a, b }) => b / (a + 1) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `y = ${a}x를 x + y = ${b}에 대입\n` +
      `x + ${a}x = ${b}\n${a + 1}x = ${b}\nx = ${ans}`,
  },

  // Lv.4: 연립방정식 (가감법)
  {
    id: 'm2-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-08',
    pattern: '',
    paramRanges: { a: [5, 20], b: [1, 10] },
    constraints: ({ a, b }) => (a + b) % 2 === 0 && a > b,
    contentFn: ({ a, b }) => `x + y = ${a}, x - y = ${b} 일 때, x = ?`,
    answerFn: ({ a, b }) => (a + b) / 2,
    distractorFns: [
      ({ a, b }) => (a - b) / 2,
      ({ a }) => a,
      ({ a, b }) => (a + b) / 2 + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `두 식을 더하면: 2x = ${a + b}\nx = ${ans}`,
  },
  {
    id: 'm2-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-08',
    pattern: '',
    paramRanges: { a: [5, 20], b: [1, 10] },
    constraints: ({ a, b }) => (a - b) % 2 === 0 && a > b,
    contentFn: ({ a, b }) => `x + y = ${a}, x - y = ${b} 일 때, y = ?`,
    answerFn: ({ a, b }) => (a - b) / 2,
    distractorFns: [
      ({ a, b }) => (a + b) / 2,
      ({ a }) => a,
      ({ a, b }) => (a - b) / 2 + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `첫 번째 식에서 두 번째 식을 빼면: 2y = ${a - b}\ny = ${ans}`,
  },

  // Lv.5: 일차함수 y = ax + b
  {
    id: 'm2-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-10',
    pattern: '',
    paramRanges: { a: [-5, 8], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) => `y = ${a}x + ${signedStr(b)}에서 기울기는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ b }) => b,
      ({ a }) => -a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a, b }) =>
      `일차함수 y = ax + b에서 기울기는 a입니다.\ny = ${a}x + ${signedStr(b)}의 기울기는 ${a}입니다.`,
  },
  {
    id: 'm2-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-10',
    pattern: '',
    paramRanges: { a: [-5, 8], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) => `y = ${a}x + ${signedStr(b)}에서 y절편은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => -b,
      ({ b }) => b + 1,
    ],
    explanationFn: ({ a, b }) =>
      `일차함수 y = ax + b에서 y절편은 b입니다.\ny = ${a}x + ${signedStr(b)}의 y절편은 ${b}입니다.`,
  },

  // Lv.6: 일차함수 그래프 해석
  {
    id: 'm2-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-11',
    pattern: '',
    paramRanges: { a: [-5, 8], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) => `y = ${a}x + ${signedStr(b)}가 y축과 만나는 점의 y좌표는?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => -b,
      () => 0,
    ],
    explanationFn: ({ b }) =>
      `y축과 만나는 점은 x = 0일 때입니다.\nx = 0을 대입하면 y = ${b}입니다.`,
  },
  {
    id: 'm2-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-11',
    pattern: '',
    paramRanges: { a: [-5, 8], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0 && b % a === 0,
    contentFn: ({ a, b }) => `y = ${a}x + ${signedStr(b)}가 x축과 만나는 점의 x좌표는?`,
    answerFn: ({ a, b }) => -b / a,
    distractorFns: [
      ({ a, b }) => b / a,
      ({ b }) => -b,
      ({ a, b }) => -b / a + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x축과 만나는 점은 y = 0일 때입니다.\n0 = ${a}x + ${signedStr(b)}\n${a}x = ${-b}\nx = ${ans}`,
  },

  // Lv.7: 삼각형 합동 조건
  {
    id: 'm2-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '두 삼각형에서 대응하는 세 변의 길이가 각각 같을 때, 이것을 무슨 합동 조건이라 하는가?',
        '두 삼각형에서 대응하는 두 변의 길이와 그 끼인각의 크기가 각각 같을 때, 이것을 무슨 합동 조건이라 하는가?',
        '두 삼각형에서 대응하는 한 변의 길이와 그 양 끝각의 크기가 각각 같을 때, 이것을 무슨 합동 조건이라 하는가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['SSS 합동', 'SAS 합동', 'ASA 합동']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['SAS 합동', 'ASA 합동', 'SSS 합동'][variant]!),
      ({ variant }) => (['ASA 합동', 'SSS 합동', 'SAS 합동'][variant]!),
      () => 'AAA 합동',
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '세 변의 길이가 각각 같으면 SSS(Side-Side-Side) 합동입니다.',
        '두 변의 길이와 그 끼인각이 같으면 SAS(Side-Angle-Side) 합동입니다.',
        '한 변의 길이와 그 양 끝각이 같으면 ASA(Angle-Side-Angle) 합동입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.8: 사각형 성질
  {
    id: 'm2-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '평행사변형에서 대변의 길이는 어떤 관계인가?',
        '평행사변형에서 대각의 크기는 어떤 관계인가?',
        '직사각형에서 대각선의 길이는 어떤 관계인가?',
        '마름모에서 대각선은 어떤 관계인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['같다', '같다', '같다', '서로 수직이등분한다']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['다르다', '다르다', '다르다', '평행하다'][variant]!),
      ({ variant }) => (['수직이다', '수직이다', '수직이다', '같다'][variant]!),
      () => '알 수 없다',
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '평행사변형의 대변의 길이는 같습니다.',
        '평행사변형의 대각의 크기는 같습니다.',
        '직사각형의 대각선의 길이는 같습니다.',
        '마름모의 대각선은 서로 수직이등분합니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.9: 확률 기본
  {
    id: 'm2-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'M2-STA-02',
    pattern: '',
    paramRanges: { a: [1, 6] },
    contentFn: ({ a }) => `주사위 하나를 던져 ${a} 이하의 눈이 나올 확률은?`,
    answerFn: ({ a }) => `${a}/6`,
    distractorFns: [
      ({ a }) => `${7 - a}/6`,
      ({ a }) => `${a}/12`,
      ({ a }) => `${a + 1}/6`,
    ],
    explanationFn: ({ a }, ans) =>
      `전체 경우의 수는 6가지입니다.\n${a} 이하의 눈은 1, 2, ..., ${a}로 ${a}가지입니다.\n확률은 ${ans}입니다.`,
  },
  {
    id: 'm2-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'M2-STA-02',
    pattern: '',
    paramRanges: { a: [1, 5] },
    contentFn: ({ a }) => `주사위 하나를 던져 ${a}보다 큰 눈이 나올 확률은?`,
    answerFn: ({ a }) => `${6 - a}/6`,
    distractorFns: [
      ({ a }) => `${a}/6`,
      ({ a }) => `${6 - a}/12`,
      ({ a }) => `${7 - a}/6`,
    ],
    explanationFn: ({ a }, ans) =>
      `전체 경우의 수는 6가지입니다.\n${a}보다 큰 눈은 ${a + 1}, ${a + 2}, ..., 6으로 ${6 - a}가지입니다.\n확률은 ${ans}입니다.`,
  },

  // Lv.10: 복합 응용 (함수 + 방정식)
  {
    id: 'm2-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-12',
    pattern: '',
    paramRanges: { a: [1, 5], b: [-5, 5], c: [-3, -1], d: [1, 8] },
    constraints: ({ a, b, c, d }) => a !== c && (d - b) % (a - c) === 0,
    contentFn: ({ a, b, c, d }) =>
      `y = ${a}x + ${signedStr(b)}와 y = ${c}x + ${signedStr(d)}의 교점의 x좌표는?`,
    answerFn: ({ a, b, c, d }) => (d - b) / (a - c),
    distractorFns: [
      ({ a, b, c, d }) => (b - d) / (a - c),
      ({ a, b, c, d }) => (d - b) / (c - a),
      ({ a, b, c, d }) => (d - b) / (a - c) + 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const xVal = ans as number
      const yVal = a * xVal + b
      return `두 일차함수가 만나는 점에서:\n` +
        `${a}x + ${signedStr(b)} = ${c}x + ${signedStr(d)}\n` +
        `${a - c}x = ${d - b}\n` +
        `x = ${ans}\n` +
        `교점: (${ans}, ${yVal})`
    },
  },
  {
    id: 'm2-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'func' as ProblemPart,
    conceptId: 'M2-ALG-12',
    pattern: '',
    paramRanges: { a: [1, 5], b: [-5, 5], c: [-3, -1], d: [1, 8] },
    constraints: ({ a, b, c, d }) => a !== c && (d - b) % (a - c) === 0,
    contentFn: ({ a, b, c, d }) =>
      `y = ${a}x + ${signedStr(b)}와 y = ${c}x + ${signedStr(d)}의 교점의 y좌표는?`,
    answerFn: ({ a, b, c, d }) => {
      const x = (d - b) / (a - c)
      return a * x + b
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const x = (d - b) / (a - c)
        return c * x + d
      },
      ({ b, d }) => b + d,
      ({ a, b, c, d }) => {
        const x = (d - b) / (a - c)
        return a * x + b + 1
      },
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const xVal = (d - b) / (a - c)
      return `먼저 x좌표를 구하면:\n` +
        `${a}x + ${signedStr(b)} = ${c}x + ${signedStr(d)}\n` +
        `x = ${xVal}\n` +
        `y = ${a} × ${xVal} + ${signedStr(b)} = ${ans}`
    },
  },
]

export const middle2Templates: QuestionTemplate[] = [...comp, ...conc]
