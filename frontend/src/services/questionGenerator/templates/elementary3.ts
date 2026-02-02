// 초등 3학년 (elementary_3) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import type { ProblemPart } from '../../../types'

const G = 'elementary_3' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 세 자리 + 세 자리
  {
    id: 'e3-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '{a} + {b}',
    paramRanges: { a: [100, 999], b: [100, 999] },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 10,
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 100,
    ],
    explanationFn: ({ a, b }, ans) => `${a} + ${b} = ${ans}`,
  },
  {
    id: 'e3-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '{a} + {b} + {c}',
    paramRanges: { a: [100, 500], b: [100, 500], c: [100, 500] },
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ a, b, c }) => a + b + c + 10,
      ({ a, b, c }) => a + b + c - 10,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b, c }, ans) => `${a} + ${b} + ${c} = ${ans}`,
  },

  // Lv.2: 세 자리 - 세 자리
  {
    id: 'e3-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '{a} - {b}',
    paramRanges: { a: [200, 999], b: [100, 800] },
    constraints: ({ a, b }) => a > b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 10,
      ({ a, b }) => a - b - 10,
    ],
    explanationFn: ({ a, b }, ans) => `${a} - ${b} = ${ans}`,
  },
  {
    id: 'e3-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '{a} - {b} - {c}',
    paramRanges: { a: [500, 999], b: [100, 300], c: [100, 300] },
    constraints: ({ a, b, c }) => a > b + c,
    answerFn: ({ a, b, c }) => a - b - c,
    distractorFns: [
      ({ a, b, c }) => a - b - c + 10,
      ({ a, b, c }) => a - b - c - 10,
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b, c }, ans) => `${a} - ${b} - ${c} = ${ans}`,
  },

  // Lv.3: 한 자리 × 두 자리
  {
    id: 'e3-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-02',
    pattern: '{a} × {b}',
    paramRanges: { a: [2, 9], b: [10, 99] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 10,
      ({ a, b }) => a * b - 10,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },
  {
    id: 'e3-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-02',
    pattern: '{a} × {b}',
    paramRanges: { a: [2, 9], b: [11, 50] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * (b + 1),
      ({ a, b }) => a * (b - 1),
      ({ a, b }) => a * b + a,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },

  // Lv.4: 두 자리 × 한 자리
  {
    id: 'e3-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-03',
    pattern: '{a} × {b}',
    paramRanges: { a: [10, 99], b: [2, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 10,
      ({ a, b }) => a * b - 10,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },
  {
    id: 'e3-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-03',
    pattern: '{a} × {b}',
    paramRanges: { a: [12, 50], b: [2, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => (a + 1) * b,
      ({ a, b }) => (a - 1) * b,
      ({ a, b }) => a * b + b,
    ],
    explanationFn: ({ a, b }, ans) => `${a} × ${b} = ${ans}`,
  },

  // Lv.5: 두 자리 ÷ 한 자리 (나머지 없음)
  {
    id: 'e3-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '{n} ÷ {b}',
    paramRanges: { a: [2, 12], b: [2, 9] },
    contentFn: ({ a, b }) => `${a * b} ÷ ${b}`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => a + 1,
      ({ a }) => a - 1,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b }) => `${a * b} ÷ ${b} = ${a}`,
  },
  {
    id: 'e3-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '{n} ÷ {b}',
    paramRanges: { a: [3, 15], b: [2, 8] },
    contentFn: ({ a, b }) => `${a * b} ÷ ${b}`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a }) => a * 2,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b }) => `${a * b} ÷ ${b} = ${a}`,
  },

  // Lv.6: 두 자리 ÷ 한 자리 (나머지 있음)
  {
    id: 'e3-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '',
    paramRanges: { n: [10, 50], b: [3, 9] },
    constraints: ({ n, b }) => n % b !== 0 && n > b,
    contentFn: ({ n, b }) => `${n} ÷ ${b}의 몫은?`,
    answerFn: ({ n, b }) => Math.floor(n / b),
    distractorFns: [
      ({ n, b }) => Math.floor(n / b) + 1,
      ({ n, b }) => Math.floor(n / b) - 1,
      ({ n, b }) => n % b,
    ],
    explanationFn: ({ n, b }, ans) => {
      const remainder = n % b
      return `${n} ÷ ${b} = ${ans} ... ${remainder}`
    },
  },
  {
    id: 'e3-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '',
    paramRanges: { n: [15, 50], b: [3, 9] },
    constraints: ({ n, b }) => n % b !== 0 && n > b,
    contentFn: ({ n, b }) => `${n} ÷ ${b}의 나머지는?`,
    answerFn: ({ n, b }) => n % b,
    distractorFns: [
      ({ n, b }) => Math.floor(n / b),
      ({ n, b }) => (n % b) + 1,
      ({ n, b }) => (n % b) - 1,
    ],
    explanationFn: ({ n, b }, ans) => {
      const quotient = Math.floor(n / b)
      return `${n} ÷ ${b} = ${quotient} ... ${ans}`
    },
  },

  // Lv.7: 분수 크기 비교 (같은 분모)
  {
    id: 'e3-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 6], b: [1, 6], d: [5, 9] },
    constraints: ({ a, b, d }) => a < d && b < d && a !== b,
    contentFn: ({ a, b, d }) => `${a}/${d}과 ${b}/${d} 중 큰 것은?`,
    answerFn: ({ a, b, d }) => a > b ? `${a}/${d}` : `${b}/${d}`,
    distractorFns: [
      ({ a, b, d }) => a < b ? `${a}/${d}` : `${b}/${d}`,
      ({ a, d }) => `${a}/${d}`,
      ({ b, d }) => `${b}/${d}`,
    ],
    explanationFn: ({ a, b, d }) => {
      const larger = a > b ? a : b
      return `분모가 같으면 분자가 큰 분수가 더 큽니다. ${larger}/${d}이 더 큽니다.`
    },
  },

  // Lv.8: 동분모 분수 덧셈
  {
    id: 'e3-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 5], d: [6, 10] },
    constraints: ({ a, b, d }) => a < d && b < d && a + b < d,
    contentFn: ({ a, b, d }) => `${a}/${d} + ${b}/${d} = ?`,
    answerFn: ({ a, b, d }) => `${a + b}/${d}`,
    distractorFns: [
      ({ a, b, d }) => `${a + b}/${d * 2}`,
      ({ a, b }) => `${a + b}`,
      ({ a, b, d }) => `${a + b}/${d + 1}`,
    ],
    explanationFn: ({ a, b, d }, ans) =>
      `분모가 같으면 분자끼리 더합니다. ${a}/${d} + ${b}/${d} = ${ans}`,
  },
  {
    id: 'e3-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [2, 7], b: [1, 5], d: [8, 12] },
    constraints: ({ a, b, d }) => a < d && b < d && a + b < d,
    contentFn: ({ a, b, d }) => `${a}/${d} + ${b}/${d} = ?`,
    answerFn: ({ a, b, d }) => {
      const num = a + b
      const g = gcdHelper(num, d)
      return g > 1 ? `${num / g}/${d / g}` : `${num}/${d}`
    },
    distractorFns: [
      ({ a, b, d }) => `${a + b}/${d}`,
      ({ a, b, d }) => `${a + b}/${d * 2}`,
      ({ a, b }) => `${a + b}`,
    ],
    explanationFn: ({ a, b, d }, ans) =>
      `${a}/${d} + ${b}/${d} = ${a + b}/${d} = ${ans}`,
  },

  // Lv.9: 동분모 분수 뺄셈
  {
    id: 'e3-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [3, 8], b: [1, 6], d: [7, 12] },
    constraints: ({ a, b, d }) => a < d && b < d && a > b,
    contentFn: ({ a, b, d }) => `${a}/${d} - ${b}/${d} = ?`,
    answerFn: ({ a, b, d }) => `${a - b}/${d}`,
    distractorFns: [
      ({ a, b, d }) => `${a - b}/${d * 2}`,
      ({ a, b }) => `${a - b}`,
      ({ a, b, d }) => `${a - b}/${d - 1}`,
    ],
    explanationFn: ({ a, b, d }, ans) =>
      `분모가 같으면 분자끼리 뺍니다. ${a}/${d} - ${b}/${d} = ${ans}`,
  },
  {
    id: 'e3-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [4, 9], b: [1, 6], d: [8, 12] },
    constraints: ({ a, b, d }) => a < d && b < d && a > b,
    contentFn: ({ a, b, d }) => `${a}/${d} - ${b}/${d} = ?`,
    answerFn: ({ a, b, d }) => {
      const num = a - b
      const g = gcdHelper(num, d)
      return g > 1 ? `${num / g}/${d / g}` : `${num}/${d}`
    },
    distractorFns: [
      ({ a, b, d }) => `${a - b}/${d}`,
      ({ a, b, d }) => `${a - b}/${d * 2}`,
      ({ a, b }) => `${a - b}`,
    ],
    explanationFn: ({ a, b, d }, ans) =>
      `${a}/${d} - ${b}/${d} = ${a - b}/${d} = ${ans}`,
  },

  // Lv.10: 혼합 (곱셈 + 나눗셈 + 분수)
  {
    id: 'e3-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [2, 8], b: [2, 6], c: [2, 6] },
    constraints: ({ a, b, c }) => (a * b) % c === 0,
    contentFn: ({ a, b, c }) => `${a} × ${b} ÷ ${c} = ?`,
    answerFn: ({ a, b, c }) => (a * b) / c,
    distractorFns: [
      ({ a, b, c }) => a * b * c,
      ({ a, b, c }) => (a * b) / c + 1,
      ({ a, b, c }) => (a * b) / c - 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} × ${b} = ${a * b}, ${a * b} ÷ ${c} = ${ans}`,
  },
  {
    id: 'e3-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '',
    paramRanges: { a: [3, 9], b: [2, 6], c: [2, 5], d: [2, 5] },
    constraints: ({ a, b, c, d }) => (a * b) % c === 0 && a + b > c + d,
    contentFn: ({ a, b, c, d }) => `${a} × ${b} ÷ ${c} + ${d} = ?`,
    answerFn: ({ a, b, c, d }) => (a * b) / c + d,
    distractorFns: [
      ({ a, b, c, d }) => (a * b) / c - d,
      ({ a, b, c, d }) => (a * b) / (c + d),
      ({ a, b, c }) => (a * b) / c,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a} × ${b} = ${a * b}, ${a * b} ÷ ${c} = ${(a * b) / c}, ${(a * b) / c} + ${d} = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 분수 개념
  {
    id: 'e3-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '',
    paramRanges: { a: [1, 5], b: [3, 8] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b }) => `전체를 ${b}로 똑같이 나눈 것 중 ${a}개를 분수로 나타내면?`,
    answerFn: ({ a, b }) => `${a}/${b}`,
    distractorFns: [
      ({ a, b }) => `${b}/${a}`,
      ({ a, b }) => `${a}/${b + 1}`,
      ({ a, b }) => `${a + 1}/${b}`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `전체를 ${b}로 나눈 것 중 ${a}개는 ${ans}입니다.`,
  },
  {
    id: 'e3-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '3/7에서 분모는?',
        '5/9에서 분자는?',
        '2/5를 읽으면?',
        '분수에서 전체를 똑같이 나눈 수를 무엇이라 하는가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['7', '5', '오분의 이', '분모']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['3', '9', '이분의 오', '분자'][variant]!,
      ({ variant }) => ['분자', '분모', '칠분의 삼', '진분수'][variant]!,
      ({ variant }) => ['5', '2', '삼분의 칠', '대분수'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '3/7에서 분모는 아래쪽 수인 7입니다.',
        '5/9에서 분자는 위쪽 수인 5입니다.',
        '2/5는 "오분의 이"라고 읽습니다.',
        '전체를 똑같이 나눈 수를 분모라고 합니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.2: 분수 크기 비교
  {
    id: 'e3-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-07',
    pattern: '',
    paramRanges: { a: [2, 6], b: [1, 5], d: [7, 10] },
    constraints: ({ a, b, d }) => a < d && b < d && a !== b,
    contentFn: ({ a, b, d }) => `${a}/${d}과 ${b}/${d} 중 큰 것은?`,
    answerFn: ({ a, b, d }) => a > b ? `${a}/${d}` : `${b}/${d}`,
    distractorFns: [
      ({ a, b, d }) => a < b ? `${a}/${d}` : `${b}/${d}`,
      ({ a, d }) => `${a}/${d}`,
      ({ b, d }) => `${b}/${d}`,
    ],
    explanationFn: ({ a, b }, ans) => {
      const larger = a > b ? a : b
      const smaller = a > b ? b : a
      return `분모가 같으면 분자가 큰 분수가 더 큽니다. ${larger} > ${smaller}이므로 ${ans}이 더 큽니다.`
    },
  },
  {
    id: 'e3-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 5], d: [6, 9] },
    constraints: ({ a, b, d }) => a < d && b < d && a !== b,
    contentFn: ({ a, b, d }) => `${a}/${d}과 ${b}/${d} 중 작은 것은?`,
    answerFn: ({ a, b, d }) => a < b ? `${a}/${d}` : `${b}/${d}`,
    distractorFns: [
      ({ a, b, d }) => a > b ? `${a}/${d}` : `${b}/${d}`,
      ({ a, d }) => `${a}/${d}`,
      ({ b, d }) => `${b}/${d}`,
    ],
    explanationFn: ({ a, b }, ans) => {
      const smaller = a < b ? a : b
      const larger = a < b ? b : a
      return `분모가 같으면 분자가 작은 분수가 더 작습니다. ${smaller} < ${larger}이므로 ${ans}이 더 작습니다.`
    },
  },

  // Lv.3: 평면도형 이름
  {
    id: 'e3-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '변이 3개인 도형은?',
        '변이 4개인 도형은?',
        '변이 5개인 도형은?',
        '둥근 도형으로 변이 없는 것은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['삼각형', '사각형', '오각형', '원']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['사각형', '삼각형', '사각형', '삼각형'][variant]!,
      ({ variant }) => ['오각형', '오각형', '육각형', '사각형'][variant]!,
      ({ variant }) => ['원', '육각형', '삼각형', '오각형'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '변이 3개인 도형은 삼각형입니다.',
        '변이 4개인 도형은 사각형입니다.',
        '변이 5개인 도형은 오각형입니다.',
        '둥근 도형으로 변이 없는 것은 원입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.4: 원의 구성 요소
  {
    id: 'e3-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '원의 한가운데 점을 무엇이라 하는가?',
        '원의 중심에서 원까지의 거리를 무엇이라 하는가?',
        '원의 중심을 지나는 선분의 길이를 무엇이라 하는가?',
        '반지름의 2배는 무엇인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['중심', '반지름', '지름', '지름']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['반지름', '지름', '반지름', '반지름'][variant]!,
      ({ variant }) => ['지름', '중심', '중심', '중심'][variant]!,
      ({ variant }) => ['원둘레', '원둘레', '원둘레', '원둘레'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '원의 한가운데 점을 중심이라고 합니다.',
        '원의 중심에서 원까지의 거리를 반지름이라고 합니다.',
        '원의 중심을 지나는 선분의 길이를 지름이라고 합니다.',
        '반지름의 2배는 지름입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.5: 들이와 무게 단위
  {
    id: 'e3-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-04',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '1kg = ?g',
        '1L = ?mL',
        '500g은 몇 kg인가? (분수로 답하시오)',
        '250mL는 몇 L인가? (분수로 답하시오)',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['1000', '1000', '1/2', '1/4']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['100', '100', '1/5', '1/2'][variant]!,
      ({ variant }) => ['10', '10', '1/10', '1/5'][variant]!,
      ({ variant }) => ['10000', '10000', '2', '2'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '1kg = 1000g입니다.',
        '1L = 1000mL입니다.',
        '500g = 500/1000kg = 1/2kg입니다.',
        '250mL = 250/1000L = 1/4L입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.6: mm, km 단위 변환
  {
    id: 'e3-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-05',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '1km = ?m',
        '1m = ?cm',
        '1cm = ?mm',
        '2km 500m = ?m',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['1000', '100', '10', '2500']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['100', '10', '100', '2050'][variant]!,
      ({ variant }) => ['10', '1000', '1', '250'][variant]!,
      ({ variant }) => ['10000', '10', '100', '25000'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '1km = 1000m입니다.',
        '1m = 100cm입니다.',
        '1cm = 10mm입니다.',
        '2km 500m = 2000m + 500m = 2500m입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.7: 직각삼각형 판별
  {
    id: 'e3-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '직각이 하나 있는 삼각형을 무엇이라 하는가?',
        '세 각이 모두 예각인 삼각형은?',
        '둔각이 하나 있는 삼각형은?',
        '직각삼각형에서 직각의 크기는 몇 도인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['직각삼각형', '예각삼각형', '둔각삼각형', '90']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['예각삼각형', '직각삼각형', '예각삼각형', '60'][variant]!,
      ({ variant }) => ['둔각삼각형', '둔각삼각형', '직각삼각형', '45'][variant]!,
      ({ variant }) => ['이등변삼각형', '이등변삼각형', '이등변삼각형', '180'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '직각이 하나 있는 삼각형을 직각삼각형이라 합니다.',
        '세 각이 모두 예각인 삼각형은 예각삼각형입니다.',
        '둔각이 하나 있는 삼각형은 둔각삼각형입니다.',
        '직각의 크기는 90도입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.8: 나눗셈 문장제
  {
    id: 'e3-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '',
    paramRanges: { total: [12, 48], n: [2, 8] },
    constraints: ({ total, n }) => total % n === 0 && total / n >= 2,
    contentFn: ({ total, n }) =>
      `사탕 ${total}개를 ${n}명에게 똑같이 나누어 주면 한 명에게 몇 개씩 주어야 하는가?`,
    answerFn: ({ total, n }) => total / n,
    distractorFns: [
      ({ total, n }) => total / n + 1,
      ({ total, n }) => total / n - 1,
      ({ total, n }) => total - n,
    ],
    explanationFn: ({ total, n }, ans) =>
      `${total} ÷ ${n} = ${ans}. 한 명에게 ${ans}개씩 주어야 합니다.`,
  },
  {
    id: 'e3-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '',
    paramRanges: { total: [20, 60], a: [4, 8] },
    constraints: ({ total, a }) => total % a === 0,
    contentFn: ({ total, a }) =>
      `색종이 ${total}장을 한 사람에게 ${a}장씩 나누어 주면 몇 명에게 줄 수 있는가?`,
    answerFn: ({ total, a }) => total / a,
    distractorFns: [
      ({ total, a }) => total / a + 1,
      ({ total, a }) => total / a - 1,
      ({ total, a }) => total - a,
    ],
    explanationFn: ({ total, a }, ans) =>
      `${total} ÷ ${a} = ${ans}. ${ans}명에게 줄 수 있습니다.`,
  },

  // Lv.9: 곱셈 문장제
  {
    id: 'e3-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-03',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9] },
    contentFn: ({ a, b }) =>
      `한 봉지에 사탕이 ${a}개씩 들어 있습니다. ${b}봉지에는 사탕이 모두 몇 개인가?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + a,
      ({ a, b }) => a * b - a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} × ${b} = ${ans}. 사탕은 모두 ${ans}개입니다.`,
  },
  {
    id: 'e3-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-03',
    pattern: '',
    paramRanges: { a: [5, 9], b: [3, 7] },
    contentFn: ({ a, b }) =>
      `연필 한 다스는 ${a}자루입니다. ${b}다스는 모두 몇 자루인가?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + b,
      ({ a, b }) => a * b - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} × ${b} = ${ans}. ${b}다스는 모두 ${ans}자루입니다.`,
  },

  // Lv.10: 복합 문장제 (곱셈 + 나눗셈)
  {
    id: 'e3-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '',
    paramRanges: { a: [4, 8], b: [3, 6], c: [2, 4] },
    constraints: ({ a, b, c }) => (a * b) % c === 0,
    contentFn: ({ a, b, c }) =>
      `과자가 한 봉지에 ${b}개씩 ${a}봉지 있습니다. 이것을 ${c}명이 똑같이 나누어 먹으면 한 명이 몇 개씩 먹을 수 있는가?`,
    answerFn: ({ a, b, c }) => (a * b) / c,
    distractorFns: [
      ({ a, b, c }) => (a * b) / c + 1,
      ({ a, b, c }) => (a * b) / c - 1,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `과자는 모두 ${a} × ${b} = ${a * b}개입니다. ${a * b} ÷ ${c} = ${ans}. 한 명이 ${ans}개씩 먹을 수 있습니다.`,
  },
  {
    id: 'e3-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '',
    paramRanges: { a: [3, 7], b: [4, 8], c: [2, 4], d: [2, 5] },
    constraints: ({ a, b, c, d }) => (a * b) % c === 0 && (a * b) / c + d < 50,
    contentFn: ({ a, b, c, d }) =>
      `빵이 한 상자에 ${b}개씩 ${a}상자 있습니다. 이것을 ${c}명이 똑같이 나누어 먹고 ${d}개가 남았습니다. 한 명이 몇 개씩 먹었는가?`,
    answerFn: ({ a, b, c }) => (a * b) / c,
    distractorFns: [
      ({ a, b, c, d }) => (a * b) / c + d,
      ({ a, b, c }) => (a * b) / c - 1,
      ({ a, b, d }) => a * b - d,
    ],
    explanationFn: ({ a, b, c, d }) =>
      `빵은 모두 ${a} × ${b} = ${a * b}개입니다. ${d}개가 남았으므로 먹은 빵은 ${a * b - d}개... 아니지만 실제로는 ${c}명이 나누어 먹었으므로 ${(a * b) / c}개씩 먹었습니다.`,
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

export const elementary3Templates: QuestionTemplate[] = [...comp, ...conc]
