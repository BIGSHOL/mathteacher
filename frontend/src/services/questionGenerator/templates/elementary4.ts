// 초등학교 4학년 (elementary_4) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'

const G = 'elementary_4' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 큰 수 덧셈 (만 단위)
  {
    id: 'e4-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E4-NUM-02',
    pattern: '{a} + {b}',
    paramRanges: { a: [1000, 9000], b: [1000, 9000] },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 1000,
      ({ a, b }) => a + b - 1000,
      ({ a, b }) => a + b + 100,
    ],
    explanationFn: ({ a, b }, ans) => `${a} + ${b} = ${ans}`,
  },
  {
    id: 'e4-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E4-NUM-02',
    pattern: '{a} + {b} + {c}',
    paramRanges: { a: [1000, 5000], b: [1000, 5000], c: [1000, 5000] },
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ a, b, c }) => a + b + c + 1000,
      ({ a, b, c }) => a + b + c - 1000,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b, c }, ans) => `${a} + ${b} + ${c} = ${ans}`,
  },

  // Lv.2: 큰 수 뺄셈
  {
    id: 'e4-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E4-NUM-02',
    pattern: '{a} - {b}',
    paramRanges: { a: [5000, 9999], b: [1000, 8999] },
    constraints: ({ a, b }) => a > b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => b - a,
      ({ a, b }) => a - b + 1000,
    ],
    explanationFn: ({ a, b }, ans) => `${a} - ${b} = ${ans}`,
  },
  {
    id: 'e4-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E4-NUM-02',
    pattern: '{a} - {b} - {c}',
    paramRanges: { a: [5000, 9999], b: [500, 2000], c: [500, 2000] },
    constraints: ({ a, b, c }) => a > b + c,
    answerFn: ({ a, b, c }) => a - b - c,
    distractorFns: [
      ({ a, b, c }) => a - b + c,
      ({ a, b, c }) => a - (b + c) + 100,
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b, c }, ans) => `${a} - ${b} - ${c} = ${ans}`,
  },

  // Lv.3: 두 자리 × 두 자리
  {
    id: 'e4-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E4-NUM-03',
    pattern: '{a} × {b}',
    paramRanges: { a: [11, 99], b: [11, 99] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 10,
      ({ a, b }) => a * b - 10,
      ({ a, b }) => (a + 1) * b,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },
  {
    id: 'e4-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E4-NUM-03',
    pattern: '{a} × {b}',
    paramRanges: { a: [12, 89], b: [12, 89] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * (b + 1),
      ({ a, b }) => (a - 1) * b,
      ({ a, b }) => a * b + 100,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },

  // Lv.4: 세 자리 × 두 자리
  {
    id: 'e4-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E4-NUM-04',
    pattern: '{a} × {b}',
    paramRanges: { a: [101, 250], b: [11, 39] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 100,
      ({ a, b }) => a * b - 100,
      ({ a, b }) => a * (b + 1),
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },
  {
    id: 'e4-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E4-NUM-04',
    pattern: '{a} × {b}',
    paramRanges: { a: [105, 299], b: [12, 49] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => (a + 10) * b,
      ({ a, b }) => a * b + 50,
      ({ a, b }) => a * b - 50,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },

  // Lv.5: 세 자리 ÷ 두 자리 (나누어떨어지는 경우)
  {
    id: 'e4-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E4-NUM-05',
    pattern: '',
    paramRanges: { a: [11, 25], b: [2, 9] },
    contentFn: ({ a, b }) => `${a * b} ÷ ${a} = ?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => b + 1,
      ({ b }) => b - 1,
    ],
    explanationFn: ({ a, b }) => `${a * b} ÷ ${a} = ${b}`,
  },
  {
    id: 'e4-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E4-NUM-05',
    pattern: '',
    paramRanges: { a: [12, 30], b: [3, 9] },
    contentFn: ({ a, b }) => `${a * b} ÷ ${a} = ?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ b }) => b + 2,
      ({ a }) => a / 2,
    ],
    explanationFn: ({ a, b }) => `${a * b} ÷ ${a} = ${b}`,
  },

  // Lv.6: 혼합 연산 (덧뺄셈 + 곱셈)
  {
    id: 'e4-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E4-NUM-06',
    pattern: '',
    paramRanges: { a: [3, 15], b: [2, 9], c: [10, 50] },
    contentFn: ({ a, b, c }) => `${a} × ${b} + ${c} = ?`,
    answerFn: ({ a, b, c }) => a * b + c,
    distractorFns: [
      ({ a, b, c }) => (a + b) * c,
      ({ a, b, c }) => a * (b + c),
      ({ a, b, c }) => a * b - c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `곱셈을 먼저 계산합니다.\n${a} × ${b} + ${c} = ${a * b} + ${c} = ${ans}`,
  },
  {
    id: 'e4-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E4-NUM-06',
    pattern: '',
    paramRanges: { a: [50, 200], b: [3, 12], c: [10, 40] },
    constraints: ({ a, b, c }) => a > b * c,
    contentFn: ({ a, b, c }) => `${a} - ${b} × ${c} = ?`,
    answerFn: ({ a, b, c }) => a - b * c,
    distractorFns: [
      ({ a, b, c }) => (a - b) * c,
      ({ a, b, c }) => a - (b + c),
      ({ a, b, c }) => a - b - c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `곱셈을 먼저 계산합니다.\n${a} - ${b} × ${c} = ${a} - ${b * c} = ${ans}`,
  },

  // Lv.7: 혼합 연산 (괄호 포함)
  {
    id: 'e4-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E4-NUM-07',
    pattern: '',
    paramRanges: { a: [10, 50], b: [10, 50], c: [2, 9] },
    contentFn: ({ a, b, c }) => `(${a} + ${b}) × ${c} = ?`,
    answerFn: ({ a, b, c }) => (a + b) * c,
    distractorFns: [
      ({ a, b, c }) => a + b * c,
      ({ a, b, c }) => a * c + b,
      ({ a, b, c }) => (a + b) * c + 10,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `괄호 안을 먼저 계산합니다.\n(${a} + ${b}) × ${c} = ${a + b} × ${c} = ${ans}`,
  },
  {
    id: 'e4-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E4-NUM-07',
    pattern: '',
    paramRanges: { a: [100, 300], b: [20, 80], c: [2, 8] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b, c }) => `(${a} - ${b}) × ${c} = ?`,
    answerFn: ({ a, b, c }) => (a - b) * c,
    distractorFns: [
      ({ a, b, c }) => a - b * c,
      ({ a, b, c }) => (a + b) * c,
      ({ a, b, c }) => (a - b) * c + 100,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `괄호 안을 먼저 계산합니다.\n(${a} - ${b}) × ${c} = ${a - b} × ${c} = ${ans}`,
  },

  // Lv.8: 이분모 분수 비교 (통분)
  {
    id: 'e4-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E4-NUM-08',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && a * d !== c * b && b !== d,
    contentFn: ({ a, b, c, d }) => `${a}/${b}와 ${c}/${d} 중 큰 것은?`,
    answerFn: ({ a, b, c, d }) => {
      if (a * d > c * b) return `${a}/${b}`
      return `${c}/${d}`
    },
    distractorFns: [
      ({ a, b }) => `${a}/${b}`,
      ({ c, d }) => `${c}/${d}`,
      () => '같다',
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const lcm = (b * d) / gcdHelper(b, d)
      const num1 = (a * lcm) / b
      const num2 = (c * lcm) / d
      return `통분하면 ${num1}/${lcm}와 ${num2}/${lcm}이므로 ${ans}이 더 큽니다.`
    },
  },
  {
    id: 'e4-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E4-NUM-08',
    pattern: '',
    paramRanges: { a: [2, 7], b: [3, 8], c: [2, 7], d: [3, 8] },
    constraints: ({ a, b, c, d }) => a < b && c < d && a * d !== c * b && b !== d,
    contentFn: ({ a, b, c, d }) => `${a}/${b}와 ${c}/${d} 중 작은 것은?`,
    answerFn: ({ a, b, c, d }) => {
      if (a * d < c * b) return `${a}/${b}`
      return `${c}/${d}`
    },
    distractorFns: [
      ({ a, b }) => `${a}/${b}`,
      ({ c, d }) => `${c}/${d}`,
      () => '같다',
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const lcm = (b * d) / gcdHelper(b, d)
      const num1 = (a * lcm) / b
      const num2 = (c * lcm) / d
      return `통분하면 ${num1}/${lcm}와 ${num2}/${lcm}이므로 ${ans}이 더 작습니다.`
    },
  },

  // Lv.9: 소수 덧뺄셈 기초
  {
    id: 'e4-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E4-NUM-10',
    pattern: '',
    paramRanges: { a: [1, 9], b: [1, 9] },
    contentFn: ({ a, b }) => `${a / 10} + ${b / 10} = ?`,
    answerFn: ({ a, b }) => (a + b) / 10,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => (a + b) / 10 + 0.1,
      ({ a, b }) => (a + b) / 100,
    ],
    explanationFn: ({ a, b }, ans) =>
      `0.${a} + 0.${b} = 0.${a + b} = ${ans}`,
  },
  {
    id: 'e4-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E4-NUM-10',
    pattern: '',
    paramRanges: { a: [5, 9], b: [1, 4] },
    contentFn: ({ a, b }) => `${a / 10} - ${b / 10} = ?`,
    answerFn: ({ a, b }) => (a - b) / 10,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, b }) => (a - b) / 10 + 0.1,
      ({ a, b }) => (a + b) / 10,
    ],
    explanationFn: ({ a, b }, ans) =>
      `0.${a} - 0.${b} = 0.${a - b} = ${ans}`,
  },

  // Lv.10: 혼합 연산 (사칙 + 괄호)
  {
    id: 'e4-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E4-NUM-07',
    pattern: '',
    paramRanges: { a: [3, 9], b: [10, 30], c: [5, 20], d: [10, 50] },
    contentFn: ({ a, b, c, d }) => `${a} × (${b} + ${c}) - ${d} = ?`,
    answerFn: ({ a, b, c, d }) => a * (b + c) - d,
    distractorFns: [
      ({ a, b, c, d }) => a * b + c - d,
      ({ a, b, c, d }) => (a * b + c) - d,
      ({ a, b, c, d }) => a * (b + c) + d,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a} × (${b} + ${c}) - ${d} = ${a} × ${b + c} - ${d} = ${a * (b + c)} - ${d} = ${ans}`,
  },
  {
    id: 'e4-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E4-NUM-07',
    pattern: '',
    paramRanges: { a: [100, 300], b: [20, 50], c: [2, 8], d: [10, 40] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b, c, d }) => `(${a} - ${b}) × ${c} + ${d} = ?`,
    answerFn: ({ a, b, c, d }) => (a - b) * c + d,
    distractorFns: [
      ({ a, b, c, d }) => a - b * c + d,
      ({ a, b, c, d }) => (a - b) * (c + d),
      ({ a, b, c, d }) => (a - b) * c - d,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a} - ${b}) × ${c} + ${d} = ${a - b} × ${c} + ${d} = ${(a - b) * c} + ${d} = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 각도 개념
  {
    id: 'e4-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'geo',
    conceptId: 'E4-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '직각은 몇 도입니까?',
        '평각은 몇 도입니까?',
        '한 바퀴는 몇 도입니까?',
        '직선은 몇 도입니까?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [90, 180, 360, 180]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [180, 90, 180, 90][variant]!,
      ({ variant }) => [45, 360, 90, 360][variant]!,
      ({ variant }) => [60, 270, 270, 270][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '직각은 90도입니다.',
        '평각은 180도입니다.',
        '한 바퀴는 360도입니다.',
        '직선은 180도입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.2: 예각/둔각/직각 판별
  {
    id: 'e4-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'geo',
    conceptId: 'E4-GEO-02',
    pattern: '',
    paramRanges: { a: [0, 180] },
    contentFn: ({ a }) => `${a}도는 예각, 둔각, 직각 중 무엇입니까?`,
    answerFn: ({ a }) => {
      if (a === 90) return '직각'
      if (a < 90) return '예각'
      return '둔각'
    },
    distractorFns: [
      () => '예각',
      () => '둔각',
      () => '직각',
    ],
    explanationFn: ({ a }) => {
      if (a === 90) return '90도는 직각입니다.'
      if (a < 90) return `${a}도는 90도보다 작으므로 예각입니다.`
      return `${a}도는 90도보다 크므로 둔각입니다.`
    },
  },
  {
    id: 'e4-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'geo',
    conceptId: 'E4-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '90도보다 작은 각을 무엇이라 합니까?',
        '90도보다 큰 각을 무엇이라 합니까?',
        '정확히 90도인 각을 무엇이라 합니까?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['예각', '둔각', '직각']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['둔각', '예각', '예각'][variant]!,
      ({ variant }) => ['직각', '직각', '둔각'][variant]!,
      ({ variant }) => ['평각', '평각', '평각'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '90도보다 작은 각을 예각이라 합니다.',
        '90도보다 큰 각을 둔각이라 합니다.',
        '정확히 90도인 각을 직각이라 합니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.3: 삼각형 분류
  {
    id: 'e4-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'geo',
    conceptId: 'E4-GEO-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '세 변의 길이가 모두 같은 삼각형을 무엇이라 합니까?',
        '두 변의 길이가 같은 삼각형을 무엇이라 합니까?',
        '세 각이 모두 예각인 삼각형을 무엇이라 합니까?',
        '한 각이 직각인 삼각형을 무엇이라 합니까?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['정삼각형', '이등변삼각형', '예각삼각형', '직각삼각형']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['이등변삼각형', '정삼각형', '둔각삼각형', '예각삼각형'][variant]!,
      ({ variant }) => ['직각삼각형', '직각삼각형', '직각삼각형', '둔각삼각형'][variant]!,
      ({ variant }) => ['예각삼각형', '예각삼각형', '정삼각형', '이등변삼각형'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '세 변의 길이가 모두 같은 삼각형을 정삼각형이라 합니다.',
        '두 변의 길이가 같은 삼각형을 이등변삼각형이라 합니다.',
        '세 각이 모두 예각인 삼각형을 예각삼각형이라 합니다.',
        '한 각이 직각인 삼각형을 직각삼각형이라 합니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.4: 사각형 분류
  {
    id: 'e4-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E4-GEO-04',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '네 변의 길이가 모두 같고 네 각이 모두 직각인 도형은?',
        '마주보는 두 쌍의 변이 평행한 사각형은?',
        '네 변의 길이가 모두 같은 사각형은?',
        '네 각이 모두 직각인 사각형은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['정사각형', '평행사변형', '마름모', '직사각형']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['직사각형', '직사각형', '정사각형', '정사각형'][variant]!,
      ({ variant }) => ['마름모', '마름모', '평행사변형', '평행사변형'][variant]!,
      ({ variant }) => ['평행사변형', '정사각형', '직사각형', '마름모'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '네 변의 길이가 모두 같고 네 각이 모두 직각인 도형은 정사각형입니다.',
        '마주보는 두 쌍의 변이 평행한 사각형은 평행사변형입니다.',
        '네 변의 길이가 모두 같은 사각형은 마름모입니다.',
        '네 각이 모두 직각인 사각형은 직사각형입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.5: 수직과 평행
  {
    id: 'e4-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E4-GEO-05',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '두 직선이 만나서 이루는 각이 직각일 때, 두 직선의 관계는?',
        '한 평면에서 만나지 않는 두 직선의 관계는?',
        '수직으로 만나는 두 직선이 이루는 각은 몇 도입니까?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['수직', '평행', 90]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['평행', '수직', 180][variant]!,
      ({ variant }) => ['교차', '교차', 45][variant]!,
      ({ variant }) => ['일치', '일치', 60][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '두 직선이 만나서 이루는 각이 직각일 때, 두 직선은 수직입니다.',
        '한 평면에서 만나지 않는 두 직선은 평행합니다.',
        '수직으로 만나는 두 직선이 이루는 각은 90도입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.6: 소수 개념
  {
    id: 'e4-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc',
    conceptId: 'E4-NUM-09',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `0.1이 ${a}개이면 얼마입니까?`,
    answerFn: ({ a }) => a / 10,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a / 100,
      ({ a }) => a * 10,
    ],
    explanationFn: ({ a }, ans) =>
      `0.1이 ${a}개이면 0.${a} = ${ans}입니다.`,
  },
  {
    id: 'e4-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc',
    conceptId: 'E4-NUM-09',
    pattern: '',
    paramRanges: { a: [1, 9], b: [0, 9] },
    contentFn: ({ a, b }) => `${a}.${b}는 0.1이 몇 개인 수입니까?`,
    answerFn: ({ a, b }) => a * 10 + b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => a + b,
      ({ a }) => a * 10,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}.${b} = ${a} + 0.${b} = 0.1이 ${ans}개입니다.`,
  },

  // Lv.7: 규칙과 대응
  {
    id: 'e4-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra',
    conceptId: 'E4-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) =>
      `x가 1일 때 y = 3, x가 2일 때 y = 6입니다. x가 ${a}일 때 y는 얼마입니까?`,
    answerFn: ({ a }) => a * 3,
    distractorFns: [
      ({ a }) => a + 3,
      ({ a }) => a * 2,
      ({ a }) => a + 2,
    ],
    explanationFn: ({ a }, ans) =>
      `y는 x의 3배이므로 x = ${a}일 때 y = ${a} × 3 = ${ans}입니다.`,
  },
  {
    id: 'e4-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra',
    conceptId: 'E4-ALG-01',
    pattern: '',
    paramRanges: { a: [3, 8], b: [2, 5] },
    contentFn: ({ a, b }) =>
      `x가 1일 때 y = ${b}, x가 2일 때 y = ${2 * b}입니다. x가 ${a}일 때 y는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => (a - 1) * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `y는 x의 ${b}배이므로 x = ${a}일 때 y = ${a} × ${b} = ${ans}입니다.`,
  },

  // Lv.8: 꺾은선 그래프 읽기
  {
    id: 'e4-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'data',
    conceptId: 'E4-STA-01',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '꺾은선 그래프로 나타내기에 가장 알맞은 자료는?',
        '꺾은선 그래프에서 알 수 있는 것은?',
        '꺾은선 그래프의 장점은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [
        '시간에 따른 기온의 변화',
        '변화하는 경향',
        '변화하는 모습을 한눈에 알 수 있다',
      ]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['좋아하는 과일', '전체에서 차지하는 비율', '정확한 수치를 알 수 있다'][variant]!,
      ({ variant }) => ['학생 수 조사', '각 항목의 순위', '부분과 전체의 관계를 알 수 있다'][variant]!,
      ({ variant }) => ['혈액형 조사', '정확한 값', '각 항목을 비교할 수 있다'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '시간에 따라 변하는 자료는 꺾은선 그래프로 나타내기 좋습니다.',
        '꺾은선 그래프에서는 변화하는 경향을 알 수 있습니다.',
        '꺾은선 그래프는 변화하는 모습을 한눈에 알 수 있는 장점이 있습니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.9: 문장제 (연산 순서)
  {
    id: 'e4-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E4-NUM-06',
    pattern: '',
    paramRanges: { a: [5, 15], b: [3, 6], c: [10, 30] },
    contentFn: ({ a, b, c }) =>
      `사탕이 ${a}개씩 ${b}줄로 있습니다. 여기에 사탕 ${c}개를 더 추가했습니다. 사탕은 모두 몇 개입니까?`,
    answerFn: ({ a, b, c }) => a * b + c,
    distractorFns: [
      ({ a, b, c }) => (a + b) * c,
      ({ a, b, c }) => a * (b + c),
      ({ a, b, c }) => a * b - c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} × ${b} + ${c} = ${a * b} + ${c} = ${ans}개`,
  },
  {
    id: 'e4-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E4-NUM-06',
    pattern: '',
    paramRanges: { a: [8, 20], b: [3, 7], c: [5, 15] },
    constraints: ({ a, b, c }) => a * b > c,
    contentFn: ({ a, b, c }) =>
      `연필이 ${a}자루씩 ${b}상자 있습니다. 그 중에서 ${c}자루를 사용했습니다. 남은 연필은 몇 자루입니까?`,
    answerFn: ({ a, b, c }) => a * b - c,
    distractorFns: [
      ({ a, b, c }) => (a - b) * c,
      ({ a, b, c }) => a * (b - c),
      ({ a, b, c }) => a * b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} × ${b} - ${c} = ${a * b} - ${c} = ${ans}자루`,
  },

  // Lv.10: 복합 도형 문제
  {
    id: 'e4-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'geo',
    conceptId: 'E4-GEO-03',
    pattern: '',
    paramRanges: { a: [5, 20], b: [3, 15] },
    contentFn: ({ a, b }) =>
      `직사각형의 가로가 ${a}cm, 세로가 ${b}cm입니다. 둘레는 몇 cm입니까?`,
    answerFn: ({ a, b }) => 2 * (a + b),
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b,
      ({ a, b }) => 2 * a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `둘레 = (가로 + 세로) × 2 = (${a} + ${b}) × 2 = ${a + b} × 2 = ${ans}cm`,
  },
  {
    id: 'e4-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'geo',
    conceptId: 'E4-GEO-03',
    pattern: '',
    paramRanges: { a: [4, 12] },
    contentFn: ({ a }) =>
      `정사각형의 한 변이 ${a}cm입니다. 둘레는 몇 cm입니까?`,
    answerFn: ({ a }) => 4 * a,
    distractorFns: [
      ({ a }) => a * a,
      ({ a }) => 2 * a,
      ({ a }) => 3 * a,
    ],
    explanationFn: ({ a }, ans) =>
      `정사각형의 둘레 = 한 변 × 4 = ${a} × 4 = ${ans}cm`,
  },
]

// Helper: gcd for template closures
function gcdHelper(a: number, b: number): number {
  a = Math.abs(a)
  b = Math.abs(b)
  while (b) {
    ;[a, b] = [b, a % b]
  }
  return a || 1
}

export const elementary4Templates: QuestionTemplate[] = [...comp, ...conc]
