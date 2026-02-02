// 초등1 (elementary_1) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'

const G = 'elementary_1' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 한 자리 + 한 자리 (합 ≤ 9)
  {
    id: 'e1-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-04',
    pattern: '{a} + {b}',
    paramRanges: { a: [1, 4], b: [1, 5] },
    constraints: ({ a, b }) => a + b <= 9,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
      ({ a, b }) => Math.abs(a - b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b} = ${ans}입니다.`,
  },
  {
    id: 'e1-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-04',
    pattern: '{a} + {b}',
    paramRanges: { a: [2, 5], b: [1, 4] },
    constraints: ({ a, b }) => a + b <= 9 && a >= b,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => b,
      ({ a, b }) => a + b + 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}와 ${b}를 더하면 ${ans}입니다.`,
  },

  // Lv.2: 한 자리 + 한 자리 (합 ≤ 18)
  {
    id: 'e1-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-05',
    pattern: '{a} + {b}',
    paramRanges: { a: [5, 9], b: [6, 9] },
    constraints: ({ a, b }) => a + b >= 10 && a + b <= 18,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b} = ${ans}입니다. 10이 넘으므로 받아올림이 있습니다.`,
  },
  {
    id: 'e1-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-05',
    pattern: '{a} + {b}',
    paramRanges: { a: [6, 9], b: [5, 9] },
    constraints: ({ a, b }) => a + b >= 11 && a >= b,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => 10 + (a - 5) + (b - 5),
      ({ a, b }) => a + b - 2,
      ({ a, b }) => a + b + 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b}는 10을 넘어서 ${ans}이 됩니다.`,
  },

  // Lv.3: 한 자리 - 한 자리
  {
    id: 'e1-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-06',
    pattern: '{a} - {b}',
    paramRanges: { a: [5, 9], b: [1, 8] },
    constraints: ({ a, b }) => a > b && a - b >= 1,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 1,
      ({ a, b }) => a - b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}입니다.`,
  },
  {
    id: 'e1-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-06',
    pattern: '{a} - {b}',
    paramRanges: { a: [6, 9], b: [2, 7] },
    constraints: ({ a, b }) => a > b + 1,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => b - a,
      (_, ans) => (ans as number) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}에서 ${b}를 빼면 ${ans}입니다.`,
  },

  // Lv.4: 10 만들기
  {
    id: 'e1-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `${a} + ? = 10`,
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => 10 - a + 1,
      ({ a }) => 10 - a - 1,
    ],
    explanationFn: ({ a }, ans) =>
      `${a} + ${ans} = 10이 됩니다. 10에서 ${a}를 빼면 ${ans}입니다.`,
  },
  {
    id: 'e1-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-07',
    pattern: '',
    paramRanges: { a: [2, 8] },
    contentFn: ({ a }) => `? + ${a} = 10`,
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => 10 + a,
      ({ a }) => a,
      ({ a }) => 10 - a + 2,
    ],
    explanationFn: ({ a }, ans) =>
      `${ans} + ${a} = 10입니다. 10을 만들려면 ${ans}가 필요합니다.`,
  },

  // Lv.5: 두 자리 + 한 자리 (받아올림 없음)
  {
    id: 'e1-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '{a} + {b}',
    paramRanges: { a: [11, 18], b: [1, 5] },
    constraints: ({ a, b }) => (a % 10) + b < 10,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b} = ${ans}입니다. 일의 자리끼리 더하면 ${(a % 10) + b}이고, 십의 자리는 ${Math.floor(a / 10)}이므로 답은 ${ans}입니다.`,
  },
  {
    id: 'e1-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '{a} + {b}',
    paramRanges: { a: [12, 17], b: [2, 6] },
    constraints: ({ a, b }) => (a % 10) + b <= 9,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => 10 + ((a % 10) + b),
      ({ a, b }) => a + b - 1,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}의 일의 자리 ${a % 10}와 ${b}를 더하면 ${(a % 10) + b}입니다. 답은 ${ans}입니다.`,
  },

  // Lv.6: 두 자리 - 한 자리 (받아내림 없음)
  {
    id: 'e1-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '{a} - {b}',
    paramRanges: { a: [15, 19], b: [1, 8] },
    constraints: ({ a, b }) => (a % 10) >= b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b - 10,
      ({ a, b }) => a - b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}입니다. 일의 자리에서 빼면 ${(a % 10) - b}이므로 답은 ${ans}입니다.`,
  },
  {
    id: 'e1-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '{a} - {b}',
    paramRanges: { a: [16, 19], b: [2, 7] },
    constraints: ({ a, b }) => (a % 10) >= b && a - b >= 10,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => (a % 10) - b,
      ({ a, b }) => a - b - 1,
      ({ a, b }) => 20 - a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}의 일의 자리 ${a % 10}에서 ${b}를 빼면 ${(a % 10) - b}입니다. 답은 ${ans}입니다.`,
  },

  // Lv.7: 두 자리 + 한 자리 (받아올림)
  {
    id: 'e1-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '{a} + {b}',
    paramRanges: { a: [15, 19], b: [3, 8] },
    constraints: ({ a, b }) => (a % 10) + b >= 10,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => 10 + ((a % 10) + b - 10),
      ({ a, b }) => a + b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b} = ${ans}입니다. 일의 자리 ${a % 10} + ${b} = ${(a % 10) + b}이므로 받아올림이 있어 답은 ${ans}입니다.`,
  },
  {
    id: 'e1-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '{a} + {b}',
    paramRanges: { a: [16, 18], b: [4, 7] },
    constraints: ({ a, b }) => (a % 10) + b > 10,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + (b % 10),
      ({ a, b }) => 20 + ((a % 10) + b - 10),
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `일의 자리끼리 더하면 ${(a % 10) + b}이므로 십의 자리로 받아올림합니다. ${a} + ${b} = ${ans}`,
  },

  // Lv.8: 두 자리 - 한 자리 (받아내림)
  {
    id: 'e1-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '{a} - {b}',
    paramRanges: { a: [21, 29], b: [3, 9] },
    constraints: ({ a, b }) => (a % 10) < b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ b }) => 20 - b,
      ({ a, b }) => a - b + 10,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}입니다. 일의 자리 ${a % 10}이 ${b}보다 작으므로 십의 자리에서 받아내립니다.`,
  },
  {
    id: 'e1-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '{a} - {b}',
    paramRanges: { a: [22, 28], b: [4, 8] },
    constraints: ({ a, b }) => (a % 10) < b && a - b >= 10,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => (a % 10) + 10 - b,
      ({ a, b }) => a - b - 1,
      ({ a, b }) => b - (a % 10),
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}에서 ${b}를 빼려면 받아내림을 합니다. ${a} - ${b} = ${ans}`,
  },

  // Lv.9: 세 수의 덧셈
  {
    id: 'e1-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b} + {c}',
    paramRanges: { a: [1, 5], b: [2, 5], c: [1, 4] },
    constraints: ({ a, b, c }) => a + b + c <= 15,
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b, c }) => a + b + c + 1,
      ({ a, b, c }) => a + b + c - 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} + ${b} + ${c} = ${a + b} + ${c} = ${ans}입니다.`,
  },
  {
    id: 'e1-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b} + {c}',
    paramRanges: { a: [2, 6], b: [1, 5], c: [2, 5] },
    constraints: ({ a, b, c }) => a + b + c >= 6 && a + b + c <= 16,
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ b, c }) => b + c,
      ({ a, b, c }) => a + b + c + 2,
      ({ a, b, c }) => a + b + c - 2,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `세 수를 차례로 더합니다. ${a} + ${b} = ${a + b}, ${a + b} + ${c} = ${ans}`,
  },

  // Lv.10: 세 수의 혼합 (덧셈과 뺄셈)
  {
    id: 'e1-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b} - {c}',
    paramRanges: { a: [5, 10], b: [2, 6], c: [1, 5] },
    constraints: ({ a, b, c }) => a + b > c && a + b - c >= 1,
    answerFn: ({ a, b, c }) => a + b - c,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, c }) => a - c,
      ({ a, b, c }) => a + b - c + 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} + ${b} - ${c} = ${a + b} - ${c} = ${ans}입니다. 먼저 더하고 나중에 뺍니다.`,
  },
  {
    id: 'e1-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} - {b} + {c}',
    paramRanges: { a: [8, 12], b: [1, 5], c: [2, 6] },
    constraints: ({ a, b }) => a > b,
    answerFn: ({ a, b, c }) => a - b + c,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, b, c }) => a + b + c,
      ({ a, b, c }) => a - b + c - 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} - ${b} + ${c} = ${a - b} + ${c} = ${ans}입니다. 왼쪽부터 차례로 계산합니다.`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 수 세기
  {
    id: 'e1-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-01',
    pattern: '',
    paramRanges: { n: [3, 9], variant: [0, 3] },
    contentFn: ({ n, variant }) => {
      const items = ['사과', '연필', '공', '꽃']
      return `${items[variant]}가 ${n}개 있습니다. 몇 개인가요?`
    },
    answerFn: ({ n }) => n,
    distractorFns: [
      ({ n }) => n + 1,
      ({ n }) => n - 1,
      ({ n }) => n + 2,
    ],
    explanationFn: ({}, ans) =>
      `개수를 세어 보면 ${ans}개입니다.`,
  },
  {
    id: 'e1-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-01',
    pattern: '',
    paramRanges: { n: [5, 10], variant: [0, 3] },
    contentFn: ({ n, variant }) => {
      const items = ['학생', '의자', '책', '풍선']
      return `${items[variant]}이(가) 모두 몇 개인가요? (${n}개가 있습니다)`
    },
    answerFn: ({ n }) => n,
    distractorFns: [
      ({ n }) => n - 2,
      ({ n }) => n + 1,
      ({ n }) => n * 2,
    ],
    explanationFn: ({ n }) =>
      `하나씩 세어 보면 모두 ${n}개입니다.`,
  },

  // Lv.2: 수 크기 비교
  {
    id: 'e1-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-02',
    pattern: '',
    paramRanges: { a: [1, 9], b: [1, 9] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `${a}와 ${b} 중 큰 수는 어느 것인가요?`,
    answerFn: ({ a, b }) => a > b ? a : b,
    distractorFns: [
      ({ a, b }) => a < b ? a : b,
      ({ a, b }) => a + b,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}와 ${b}를 비교하면 ${ans}이(가) 더 큽니다.`,
  },
  {
    id: 'e1-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-02',
    pattern: '',
    paramRanges: { a: [2, 9], b: [1, 8] },
    constraints: ({ a, b }) => a > b + 1,
    contentFn: ({ a, b }) => `${a}와 ${b} 중 작은 수는 무엇인가요?`,
    answerFn: ({ a, b }) => a < b ? a : b,
    distractorFns: [
      ({ a, b }) => a > b ? a : b,
      ({ a, b }) => (a + b) / 2,
      ({ b }) => b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}와 ${b} 중에서 ${ans}이(가) 더 작습니다.`,
  },

  // Lv.3: 순서
  {
    id: 'e1-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-03',
    pattern: '',
    paramRanges: { a: [3, 5], b: [6, 8], c: [1, 2] },
    constraints: ({ a, b, c }) => a > c && b > a,
    contentFn: ({ a, b, c }) => `${c}, ${a}, ${b} 중 두 번째로 큰 수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ b }) => b,
      ({ c }) => c,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b, c }) =>
      `크기 순서대로 나열하면 ${b} > ${a} > ${c}이므로 두 번째로 큰 수는 ${a}입니다.`,
  },
  {
    id: 'e1-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-03',
    pattern: '',
    paramRanges: { a: [5, 9], b: [1, 4] },
    constraints: ({ a, b }) => a > b + 2,
    contentFn: ({ a, b }) => `${a}는 ${b}보다 얼마나 더 큰가요?`,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => b - a,
      ({ a, b }) => a - b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}이므로 ${a}는 ${b}보다 ${ans}만큼 더 큽니다.`,
  },

  // Lv.4: 묶어 세기
  {
    id: 'e1-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'E1-ALG-01',
    pattern: '',
    paramRanges: { n: [4, 10] },
    constraints: ({ n }) => n % 2 === 0,
    contentFn: ({ n }) => `사탕 ${n}개를 2개씩 묶으면 몇 묶음인가요?`,
    answerFn: ({ n }) => n / 2,
    distractorFns: [
      ({ n }) => n,
      ({ n }) => n - 2,
      ({ n }) => n / 2 + 1,
    ],
    explanationFn: ({ n }, ans) =>
      `${n}개를 2개씩 묶으면 ${ans}묶음입니다. (${n} ÷ 2 = ${ans})`,
  },
  {
    id: 'e1-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'E1-ALG-01',
    pattern: '',
    paramRanges: { n: [6, 15] },
    constraints: ({ n }) => n % 3 === 0,
    contentFn: ({ n }) => `공책 ${n}권을 3권씩 묶으면 몇 묶음이 되나요?`,
    answerFn: ({ n }) => n / 3,
    distractorFns: [
      ({ n }) => n - 3,
      ({ n }) => n / 3 + 1,
      ({ n }) => n,
    ],
    explanationFn: ({ n }, ans) =>
      `${n}권을 3권씩 묶으면 ${ans}묶음입니다.`,
  },

  // Lv.5: 모양 찾기 (variant-based)
  {
    id: 'e1-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E1-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '삼각형은 몇 개의 꼭짓점이 있나요?',
        '사각형은 몇 개의 변이 있나요?',
        '원은 몇 개의 꼭짓점이 있나요?',
        '삼각형은 몇 개의 변이 있나요?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [3, 4, 0, 3]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [4, 3, 1, 4][variant]!,
      ({ variant }) => [2, 5, 2, 2][variant]!,
      ({ variant }) => [5, 6, 3, 5][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        `삼각형은 꼭짓점이 3개 있습니다.`,
        `사각형은 변이 4개 있습니다.`,
        `원은 꼭짓점이 없습니다(0개).`,
        `삼각형은 변이 3개 있습니다.`,
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'e1-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo',
    conceptId: 'E1-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '네모 모양을 무엇이라고 하나요?',
        '세모 모양을 무엇이라고 하나요?',
        '동그란 모양을 무엇이라고 하나요?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['사각형', '삼각형', '원']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['삼각형', '사각형', '사각형'][variant]!,
      ({ variant }) => ['원', '원', '삼각형'][variant]!,
      ({ variant }) => ['오각형', '육각형', '타원'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '네모 모양은 사각형입니다.',
        '세모 모양은 삼각형입니다.',
        '동그란 모양은 원입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.6: 시계 읽기
  {
    id: 'e1-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo',
    conceptId: 'E1-GEO-02',
    pattern: '',
    paramRanges: { n: [1, 12] },
    contentFn: ({ n }) => `시계의 짧은 바늘이 ${n}을 가리키고, 긴 바늘이 12를 가리킵니다. 몇 시인가요?`,
    answerFn: ({ n }) => `${n}시`,
    distractorFns: [
      ({ n }) => `${n + 1}시`,
      ({ n }) => `${n}시 30분`,
      ({ n }) => `${n - 1}시`,
    ],
    explanationFn: ({ n }) =>
      `짧은 바늘이 ${n}, 긴 바늘이 12를 가리키면 ${n}시입니다.`,
    questionType: 'multiple_choice',
  },
  {
    id: 'e1-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo',
    conceptId: 'E1-GEO-02',
    pattern: '',
    paramRanges: { n: [1, 11] },
    contentFn: ({ n }) => `시계의 짧은 바늘이 ${n}과 ${n + 1} 사이에 있고, 긴 바늘이 6을 가리킵니다. 몇 시 몇 분인가요?`,
    answerFn: ({ n }) => `${n}시 30분`,
    distractorFns: [
      ({ n }) => `${n}시`,
      ({ n }) => `${n + 1}시`,
      ({ n }) => `${n}시 15분`,
    ],
    explanationFn: ({ n }) =>
      `긴 바늘이 6을 가리키면 30분입니다. ${n}시 30분입니다.`,
    questionType: 'multiple_choice',
  },

  // Lv.7: 길이 비교
  {
    id: 'e1-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo',
    conceptId: 'E1-GEO-02',
    pattern: '',
    paramRanges: { a: [5, 12], b: [3, 10] },
    constraints: ({ a, b }) => a > b + 1,
    contentFn: ({ a, b }) => `연필 가는 길이 ${a}cm이고, 연필 나는 ${b}cm입니다. 더 긴 연필은?`,
    answerFn: () => '가',
    distractorFns: [
      () => '나',
      () => '같다',
      ({ a, b }) => `${a - b}cm`,
    ],
    explanationFn: ({ a, b }) =>
      `${a}cm가 ${b}cm보다 크므로 연필 가가 더 깁니다.`,
    questionType: 'multiple_choice',
  },
  {
    id: 'e1-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo',
    conceptId: 'E1-GEO-02',
    pattern: '',
    paramRanges: { a: [6, 10], b: [3, 8] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b }) => `끈 가는 ${a}cm이고, 끈 나는 ${b}cm입니다. 두 끈의 길이 차이는 몇 cm인가요?`,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 1,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}이므로 길이 차이는 ${ans}cm입니다.`,
  },

  // Lv.8: 규칙 찾기 기초
  {
    id: 'e1-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'algebra',
    conceptId: 'E1-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 5] },
    contentFn: ({ a }) => {
      const seq = [a, a + 2, a + 4, a + 6]
      return `${seq[0]}, ${seq[1]}, ${seq[2]}, ${seq[3]}, ? \n다음에 올 수는?`
    },
    answerFn: ({ a }) => a + 8,
    distractorFns: [
      ({ a }) => a + 6,
      ({ a }) => a + 7,
      ({ a }) => a + 10,
    ],
    explanationFn: ({ a }, ans) =>
      `2씩 커지는 규칙입니다. ${a + 6} 다음은 ${ans}입니다.`,
  },
  {
    id: 'e1-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'algebra',
    conceptId: 'E1-ALG-02',
    pattern: '',
    paramRanges: { a: [10, 15] },
    contentFn: ({ a }) => {
      const seq = [a, a - 1, a - 2, a - 3]
      return `${seq[0]}, ${seq[1]}, ${seq[2]}, ${seq[3]}, ? \n다음 수는?`
    },
    answerFn: ({ a }) => a - 4,
    distractorFns: [
      ({ a }) => a - 3,
      ({ a }) => a - 5,
      ({ a }) => a,
    ],
    explanationFn: ({ a }, ans) =>
      `1씩 작아지는 규칙입니다. ${a - 3} 다음은 ${ans}입니다.`,
  },

  // Lv.9: 문장제 기초
  {
    id: 'e1-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E1-NUM-04',
    pattern: '',
    paramRanges: { a: [5, 9], b: [1, 4] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b }) => `사탕이 ${a}개 있었습니다. ${b}개를 먹었습니다. 남은 사탕은 몇 개인가요?`,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 1,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} - ${b} = ${ans}이므로 남은 사탕은 ${ans}개입니다.`,
  },
  {
    id: 'e1-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E1-NUM-04',
    pattern: '',
    paramRanges: { a: [3, 7], b: [2, 6] },
    contentFn: ({ a, b }) => `공책이 ${a}권 있습니다. ${b}권을 더 샀습니다. 모두 몇 권인가요?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, b }) => a + b + 1,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + ${b} = ${ans}이므로 모두 ${ans}권입니다.`,
  },

  // Lv.10: 복합 문장제
  {
    id: 'e1-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E1-NUM-11',
    pattern: '',
    paramRanges: { a: [5, 10], b: [2, 5], c: [1, 4] },
    constraints: ({ a, b, c }) => a + b > c,
    contentFn: ({ a, b, c }) =>
      `처음에 구슬이 ${a}개 있었습니다. ${b}개를 더 받고, ${c}개를 동생에게 주었습니다. 남은 구슬은 몇 개인가요?`,
    answerFn: ({ a, b, c }) => a + b - c,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, c }) => a - c,
      ({ a, b, c }) => a + b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `처음 ${a}개, ${b}개 받아서 ${a + b}개, ${c}개 주어서 ${a + b} - ${c} = ${ans}개 남았습니다.`,
  },
  {
    id: 'e1-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E1-NUM-11',
    pattern: '',
    paramRanges: { a: [12, 18], b: [3, 6], c: [2, 5] },
    constraints: ({ a, b, c }) => a > b && a - b + c <= 20,
    contentFn: ({ a, b, c }) =>
      `색종이가 ${a}장 있었습니다. ${b}장을 사용하고 ${c}장을 더 받았습니다. 지금 색종이는 몇 장인가요?`,
    answerFn: ({ a, b, c }) => a - b + c,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, c }) => a + c,
      ({ a, b, c }) => a + b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} - ${b} + ${c} = ${a - b} + ${c} = ${ans}장입니다.`,
  },
]

export const elementary1Templates: QuestionTemplate[] = [...comp, ...conc]
