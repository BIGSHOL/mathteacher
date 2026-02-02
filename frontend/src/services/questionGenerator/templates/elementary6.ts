// 초등 6학년 (elementary_6) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'

const G = 'elementary_6' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 분수 × 자연수
  {
    id: 'e6-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E6-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [2, 5] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b, c }) => `${a}/${b} × ${c} 의 값은?`,
    answerFn: ({ a, b, c }) => {
      const num = a * c
      const den = b
      const g = gcdHelper(num, den)
      if (num / g === den / g) return num / g
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, c }) => a * c,
      ({ a, b, c }) => `${a}/${b * c}`,
      ({ a, b, c }) => {
        const num = a * c
        return `${num}/${b}`
      },
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a}/${b} × ${c} = ${a * c}/${b} = ${ans}`,
  },
  {
    id: 'e6-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E6-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 5], c: [2, 6] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b, c }) => `${c} × ${a}/${b} 의 값은?`,
    answerFn: ({ a, b, c }) => {
      const num = a * c
      const den = b
      const g = gcdHelper(num, den)
      if (num / g === den / g) return num / g
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, c }) => `${a + c}`,
      ({ a, b }) => `${a}/${b}`,
      ({ a, b, c }) => `${a * c}/${b * c}`,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${c} × ${a}/${b} = ${c * a}/${b} = ${ans}`,
  },

  // Lv.2: 분수 × 분수
  {
    id: 'e6-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E6-NUM-02',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d,
    contentFn: ({ a, b, c, d }) => `${a}/${b} × ${c}/${d} 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = a * c
      const den = b * d
      const g = gcdHelper(num, den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a * c}/${b + d}`,
      ({ a, c }) => `${a * c}`,
      ({ a, b, c, d }) => `${a + c}/${b * d}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} × ${c}/${d} = (${a} × ${c}) / (${b} × ${d}) = ${a * c}/${b * d} = ${ans}`,
  },

  // Lv.3: 분수 ÷ 자연수
  {
    id: 'e6-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E6-NUM-03',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [2, 5] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b, c }) => `${a}/${b} ÷ ${c} 의 값은?`,
    answerFn: ({ a, b, c }) => {
      const num = a
      const den = b * c
      const g = gcdHelper(num, den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c }) => `${a}/${b - c}`,
      ({ a, c }) => `${a}/${c}`,
      ({ a, b }) => `${a}/${b}`,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a}/${b} ÷ ${c} = ${a}/${b} × 1/${c} = ${a}/${b * c} = ${ans}`,
  },

  // Lv.4: 분수 ÷ 분수
  {
    id: 'e6-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E6-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && c !== 0,
    contentFn: ({ a, b, c, d }) => `${a}/${b} ÷ ${c}/${d} 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = a * d
      const den = b * c
      const g = gcdHelper(num, den)
      if (num / g === den / g) return 1
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a * c}/${b * d}`,
      ({ a, b }) => `${a}/${b}`,
      ({ a, b, c, d }) => `${a * d}/${b + c}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} ÷ ${c}/${d} = ${a}/${b} × ${d}/${c} = ${a * d}/${b * c} = ${ans}`,
  },

  // Lv.5: 소수 ÷ 소수
  {
    id: 'e6-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E6-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], c: [2, 9] },
    contentFn: ({ a, c }) => {
      const dividend = (a * c) / 10
      const divisor = c / 10
      return `${dividend} ÷ ${divisor} 의 값은?`
    },
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => a + 1,
      ({ a }) => a - 1,
      ({ a, c }) => (a * c) / 10,
    ],
    explanationFn: ({ a, c }) => {
      const dividend = (a * c) / 10
      const divisor = c / 10
      return `${dividend} ÷ ${divisor} = ${dividend * 10} ÷ ${divisor * 10} = ${a * c} ÷ ${c} = ${a}`
    },
  },

  // Lv.6: 비율 계산 (백분율)
  {
    id: 'e6-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E6-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 9], b: [2, 10] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b }) => `${a}/${b}를 백분율로 나타내면? (소수 첫째 자리까지)`,
    answerFn: ({ a, b }) => {
      const percent = Math.round((a / b) * 1000) / 10
      return percent
    },
    distractorFns: [
      ({ a, b }) => Math.round((a / b) * 100),
      ({ a, b }) => Math.round((a / b) * 10),
      ({ a, b }) => a / b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}/${b} = ${a / b} = ${ans}%`,
  },

  // Lv.7: 비례식 계산
  {
    id: 'e6-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra',
    conceptId: 'E6-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 8], b: [3, 9], c: [2, 8] },
    constraints: ({ a, b, c }) => (b * c) % a === 0,
    contentFn: ({ a, b, c }) => `${a} : ${b} = ${c} : x 일 때, x의 값은?`,
    answerFn: ({ a, b, c }) => (b * c) / a,
    distractorFns: [
      ({ a, b, c }) => (a * c) / b,
      ({ a, b }) => b / a,
      ({ b, c }) => b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} : ${b} = ${c} : x\n외항의 곱 = 내항의 곱\n${a} × x = ${b} × ${c}\n${a}x = ${b * c}\nx = ${ans}`,
  },

  // Lv.8: 분수·소수 혼합 연산
  {
    id: 'e6-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E6-NUM-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const problems = [
        '1/2 + 0.5 의 값은?',
        '3/4 - 0.25 의 값은?',
        '1/5 × 2 + 0.6 의 값은?',
        '2/5 + 0.3 × 2 의 값은?',
      ]
      return problems[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [1, 0.5, 1, 1]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [1.5, 1, 0.8, 0.7][variant]!,
      ({ variant }) => [0.5, 0.25, 0.6, 0.4][variant]!,
      ({ variant }) => [2, 0.75, 1.2, 1.6][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '1/2 + 0.5 = 0.5 + 0.5 = 1',
        '3/4 - 0.25 = 0.75 - 0.25 = 0.5',
        '1/5 × 2 + 0.6 = 0.2 × 2 + 0.6 = 0.4 + 0.6 = 1',
        '2/5 + 0.3 × 2 = 0.4 + 0.6 = 1',
      ]
      return explanations[variant]!
    },
  },

  // Lv.9: 비율 혼합 문제
  {
    id: 'e6-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra',
    conceptId: 'E6-ALG-01',
    pattern: '',
    paramRanges: { a: [20, 100], b: [10, 50] },
    constraints: ({ a, b }) => (a * b) % 100 === 0,
    contentFn: ({ a, b }) => `${a}의 ${b}%는?`,
    answerFn: ({ a, b }) => (a * b) / 100,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b,
      ({ a, b }) => a / b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}의 ${b}% = ${a} × ${b}/100 = ${a} × 0.${b < 10 ? '0' + b : b} = ${ans}`,
  },

  // Lv.10: 복합 연산 (분수+소수+비율)
  {
    id: 'e6-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E6-NUM-05',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const problems = [
        '80의 25%를 분수로 나타내면?',
        '1/4를 백분율로 나타낸 후 2배하면?',
        '60의 1/3은 전체의 몇 %인가? (전체 = 100)',
        '0.75 × 20의 50%는?',
      ]
      return problems[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['1/5', 50, 20, 7.5]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['1/4', 25, 30, 15][variant]!,
      ({ variant }) => ['20', 100, 10, 10][variant]!,
      ({ variant }) => ['1/3', 75, 15, 5][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '80 × 25/100 = 20, 20/100 = 1/5',
        '1/4 = 25%, 25% × 2 = 50%',
        '60 × 1/3 = 20, 20/100 = 20%',
        '0.75 × 20 = 15, 15 × 50% = 7.5',
      ]
      return explanations[variant]!
    },
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 비와 비율 개념
  {
    id: 'e6-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'algebra',
    conceptId: 'E6-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 12], b: [3, 15] },
    constraints: ({ a, b }) => {
      const g = gcdHelper(a, b)
      return g > 1
    },
    contentFn: ({ a, b }) => `${a} : ${b}를 가장 간단한 비로 나타내면?`,
    answerFn: ({ a, b }) => {
      const g = gcdHelper(a, b)
      return `${a / g} : ${b / g}`
    },
    distractorFns: [
      ({ a, b }) => `${a} : ${b}`,
      ({ a, b }) => `${a * 2} : ${b * 2}`,
      ({ a, b }) => {
        const g = gcdHelper(a, b)
        return `${a / g} : ${b}`
      },
    ],
    explanationFn: ({ a, b }) => {
      const g = gcdHelper(a, b)
      return `${a}와 ${b}의 최대공약수는 ${g}입니다.\n${a} : ${b} = ${a / g} : ${b / g}`
    },
  },

  // Lv.2: 백분율 개념
  {
    id: 'e6-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra',
    conceptId: 'E6-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 5] },
    constraints: ({ a, b }) => a < b && (100 * a) % b === 0,
    contentFn: ({ a, b }) => `${a}/${b}를 백분율로 나타내면?`,
    answerFn: ({ a, b }) => `${(100 * a) / b}%`,
    distractorFns: [
      ({ a, b }) => `${(10 * a) / b}%`,
      ({ a, b }) => `${a / b}%`,
      ({ a, b }) => `${((100 * a) / b) * 2}%`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}/${b} = ${a / b} = ${ans}`,
  },

  // Lv.3: 비례식
  {
    id: 'e6-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'E6-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 6], b: [3, 8], c: [2, 6], d: [3, 8] },
    constraints: ({ a, b, c, d }) => a * d === b * c,
    contentFn: ({ a, b, c, d }) =>
      `${a} : ${b} = ${c} : ${d} 에서 외항의 곱은?`,
    answerFn: ({ a, d }) => a * d,
    distractorFns: [
      ({ b, c }) => b * c,
      ({ a, b }) => a * b,
      ({ c, d }) => c * d,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `비례식 ${a} : ${b} = ${c} : ${d}에서\n외항은 ${a}, ${d}이므로 외항의 곱 = ${a} × ${d} = ${ans}\n내항의 곱 = ${b} × ${c} = ${b * c}`,
  },

  // Lv.4: 비례배분
  {
    id: 'e6-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'E6-ALG-04',
    pattern: '',
    paramRanges: { total: [20, 60], a: [2, 5], b: [3, 6] },
    constraints: ({ total, a, b }) => total % (a + b) === 0,
    contentFn: ({ total, a, b }) =>
      `${total}을 ${a} : ${b}로 나눌 때, 큰 쪽의 몫은?`,
    answerFn: ({ total, a, b }) => {
      const larger = Math.max(a, b)
      return (total * larger) / (a + b)
    },
    distractorFns: [
      ({ total, a, b }) => {
        const smaller = Math.min(a, b)
        return (total * smaller) / (a + b)
      },
      ({ total, a, b }) => total / (a + b),
      ({ total, a, b }) => total - (total * a) / (a + b),
    ],
    explanationFn: ({ total, a, b }, ans) => {
      const larger = Math.max(a, b)
      return `${total}을 ${a} : ${b}로 나누면\n큰 쪽 = ${total} × ${larger}/${a + b} = ${ans}`
    },
  },

  // Lv.5: 원의 넓이
  {
    id: 'e6-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E6-GEO-01',
    pattern: '',
    paramRanges: { a: [2, 10] },
    contentFn: ({ a }) => `반지름이 ${a}cm인 원의 넓이는? (π = 3.14)`,
    answerFn: ({ a }) => Math.round(3.14 * a * a * 10) / 10,
    distractorFns: [
      ({ a }) => Math.round(2 * 3.14 * a * 10) / 10,
      ({ a }) => a * a,
      ({ a }) => Math.round(3.14 * a * 10) / 10,
    ],
    explanationFn: ({ a }, ans) =>
      `원의 넓이 = π × r²\n= 3.14 × ${a}² = 3.14 × ${a * a} = ${ans}cm²`,
  },

  // Lv.6: 원기둥 부피
  {
    id: 'e6-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo',
    conceptId: 'E6-GEO-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 8] },
    contentFn: ({ a, b }) =>
      `밑면의 반지름이 ${a}cm, 높이가 ${b}cm인 원기둥의 부피는? (π = 3, 간단히)`,
    answerFn: ({ a, b }) => 3 * a * a * b,
    distractorFns: [
      ({ a, b }) => 2 * 3 * a * b,
      ({ a, b }) => a * a * b,
      ({ a, b }) => 3 * a * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `원기둥 부피 = (밑넓이) × (높이)\n= π × ${a}² × ${b} = 3 × ${a * a} × ${b} = ${ans}cm³`,
  },

  // Lv.7: 경우의 수
  {
    id: 'e6-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'data',
    conceptId: 'E6-STA-01',
    pattern: '',
    paramRanges: { a: [3, 6] },
    contentFn: ({ a }) =>
      `서로 다른 ${a}개의 구슬 중 2개를 뽑는 경우의 수는?`,
    answerFn: ({ a }) => (a * (a - 1)) / 2,
    distractorFns: [
      ({ a }) => a * (a - 1),
      ({ a }) => a * a,
      ({ a }) => a + (a - 1),
    ],
    explanationFn: ({ a }, ans) =>
      `${a}개 중 2개를 뽑는 경우의 수 = ${a} × ${a - 1} / 2 = ${a * (a - 1)} / 2 = ${ans}`,
  },

  // Lv.8: 띠그래프/원그래프
  {
    id: 'e6-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'data',
    conceptId: 'E6-STA-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '원그래프에서 전체는 몇 도인가?',
        '띠그래프에서 전체의 비율은 몇 %인가?',
        '원그래프에서 30%는 몇 도인가?',
        '띠그래프에서 1/4는 몇 %인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [360, 100, 108, 25]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [180, 50, 90, 50][variant]!,
      ({ variant }) => [100, 360, 120, 20][variant]!,
      ({ variant }) => [90, 25, 30, 75][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '원그래프는 원 전체 = 360도로 표현합니다.',
        '띠그래프는 전체 = 100%로 표현합니다.',
        '30% = 360 × 30/100 = 108도',
        '1/4 = 0.25 = 25%',
      ]
      return explanations[variant]!
    },
  },

  // Lv.9: 문장제 (비율)
  {
    id: 'e6-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E6-ALG-01',
    pattern: '',
    paramRanges: { a: [40, 100], b: [20, 80] },
    constraints: ({ a, b }) => (a * b) % 100 === 0 && a * b <= 5000,
    contentFn: ({ a, b }) =>
      `전체 학생 ${a}명 중 ${b}%가 합격했다면 몇 명이 합격했는가?`,
    answerFn: ({ a, b }) => (a * b) / 100,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, b }) => a + b,
      ({ a, b }) => a - (a * b) / 100,
    ],
    explanationFn: ({ a, b }, ans) =>
      `합격자 수 = ${a} × ${b}/100 = ${a} × ${b / 100} = ${ans}명`,
  },

  // Lv.10: 복합 응용
  {
    id: 'e6-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E6-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 4], b: [3, 5], c: [30, 60], d: [20, 50] },
    constraints: ({ a, b, c, d }) => {
      const sum = a + b
      return c % sum === 0 && ((c * a) / sum) * d % 100 === 0
    },
    contentFn: ({ a, b, c, d }) =>
      `${c}을 ${a} : ${b}로 나눈 후 큰 쪽의 ${d}%는?`,
    answerFn: ({ a, b, c, d }) => {
      const larger = Math.max(a, b)
      const portion = (c * larger) / (a + b)
      return (portion * d) / 100
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const smaller = Math.min(a, b)
        const portion = (c * smaller) / (a + b)
        return (portion * d) / 100
      },
      ({ c, d }) => (c * d) / 100,
      ({ a, b, c }) => (c * a) / (a + b),
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const larger = Math.max(a, b)
      const portion = (c * larger) / (a + b)
      return `${c}을 ${a} : ${b}로 나누면 큰 쪽 = ${portion}\n${portion}의 ${d}% = ${portion} × ${d}/100 = ${ans}`
    },
  },
]

// Helper: gcd for template closures
function gcdHelper(x: number, y: number): number {
  x = Math.abs(x)
  y = Math.abs(y)
  while (y) {
    ;[x, y] = [y, x % y]
  }
  return x || 1
}

export const elementary6Templates: QuestionTemplate[] = [...comp, ...conc]
