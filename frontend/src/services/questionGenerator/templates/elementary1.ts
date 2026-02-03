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
    conceptId: 'E1-NUM-07',
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
      `① ${a}와 ${b}를 더합니다.\n② ${a} + ${b} = ${ans}\n\n💡 합이 9 이하인 덧셈입니다.`,
  },
  {
    id: 'e1-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-07',
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
      `① ${a}와 ${b}를 더합니다.\n② ${a} + ${b} = ${ans}`,
  },

  // Lv.2: 한 자리 + 한 자리 (합 ≤ 18, 받아올림)
  {
    id: 'e1-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b}',
    paramRanges: { a: [5, 9], b: [6, 9] },
    constraints: ({ a, b }) => a + b >= 10 && a + b <= 18,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 1,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) => {
      const comp10 = 10 - a
      const rest = b - comp10
      return `① 10 만들어 더하기 전략을 씁니다.\n② ${b}를 ${comp10}와 ${rest}(으)로 가르기합니다.\n③ ${a} + ${comp10} = 10\n④ 10 + ${rest} = ${ans}\n\n💡 흔한 실수: 받아올림을 빠뜨려 ${a + b - 10}(으)로 답하는 경우가 있습니다.`
    },
  },
  {
    id: 'e1-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b}',
    paramRanges: { a: [6, 9], b: [5, 9] },
    constraints: ({ a, b }) => a + b >= 11 && a >= b,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b - 2,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) => {
      const comp10 = 10 - a
      const rest = b - comp10
      return `① ${b}를 ${comp10}와 ${rest}(으)로 가르기합니다.\n② ${a} + ${comp10} = 10\n③ 10 + ${rest} = ${ans}\n\n💡 10 만들어 더하기 전략을 사용하면 쉽습니다.`
    },
  },

  // Lv.3: 한 자리 - 한 자리
  {
    id: 'e1-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-08',
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
      `① ${a}에서 ${b}를 뺍니다.\n② ${a} - ${b} = ${ans}`,
  },
  {
    id: 'e1-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-08',
    pattern: '{a} - {b}',
    paramRanges: { a: [6, 9], b: [2, 7] },
    constraints: ({ a, b }) => a > b + 1,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}에서 ${b}를 뺍니다.\n② ${a} - ${b} = ${ans}`,
  },

  // Lv.4: 10 만들기
  {
    id: 'e1-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `${a} + ? = 10`,
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => a,
      () => 10,
      ({ a }) => 10 - a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `① 10에서 ${a}를 빼면 됩니다.\n② 10 - ${a} = ${ans}\n③ 확인: ${a} + ${ans} = 10 ✓\n\n💡 흔한 실수: 10 자체를 답으로 쓰는 경우가 있습니다.`,
  },
  {
    id: 'e1-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-09',
    pattern: '',
    paramRanges: { a: [2, 8] },
    contentFn: ({ a }) => `? + ${a} = 10`,
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => 10 + a,
      () => 10,
      ({ a }) => a,
    ],
    explanationFn: ({ a }, ans) =>
      `① 10에서 ${a}를 빼면 됩니다.\n② 10 - ${a} = ${ans}\n③ 확인: ${ans} + ${a} = 10 ✓\n\n💡 흔한 실수: 10 자체를 답으로 쓰는 경우가 있습니다.`,
  },

  // Lv.5: 두 자리 + 한 자리 (받아올림 없음)
  {
    id: 'e1-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E1-NUM-11',
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
      `① 일의 자리끼리 더합니다: ${a % 10} + ${b} = ${(a % 10) + b}\n② 십의 자리는 그대로: ${Math.floor(a / 10)}\n③ 답: ${ans}`,
  },
  {
    id: 'e1-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E1-NUM-11',
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
      `① 일의 자리끼리 더합니다: ${a % 10} + ${b} = ${(a % 10) + b}\n② 십의 자리는 그대로: ${Math.floor(a / 10)}\n③ 답: ${ans}`,
  },

  // Lv.6: 두 자리 - 한 자리 (받아내림 없음)
  {
    id: 'e1-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E1-NUM-12',
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
      `① 일의 자리에서 뺍니다: ${a % 10} - ${b} = ${(a % 10) - b}\n② 십의 자리는 그대로: ${Math.floor(a / 10)}\n③ 답: ${ans}`,
  },
  {
    id: 'e1-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E1-NUM-12',
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
      `① 일의 자리에서 뺍니다: ${a % 10} - ${b} = ${(a % 10) - b}\n② 십의 자리는 그대로: ${Math.floor(a / 10)}\n③ 답: ${ans}`,
  },

  // Lv.7: 두 자리 + 한 자리 (받아올림)
  {
    id: 'e1-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b}',
    paramRanges: { a: [15, 19], b: [3, 8] },
    constraints: ({ a, b }) => (a % 10) + b >= 10,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => Math.floor(a / 10) * 10 + ((a % 10) + b - 10),
      ({ a, b }) => a + b + 1,
    ],
    explanationFn: ({ a, b }, ans) => {
      const ones = a % 10
      const tens = Math.floor(a / 10)
      const onesSum = ones + b
      const comp10 = 10 - ones
      const rest = b - comp10
      return `① 10 만들어 더하기 전략을 씁니다.\n② ${b}를 ${comp10}와 ${rest}(으)로 가르기합니다.\n③ ${a} + ${comp10} = ${tens + 1}0\n④ ${(tens + 1) * 10} + ${rest} = ${ans}\n\n💡 흔한 실수: 받아올림을 빠뜨려 ${Math.floor(a / 10) * 10 + (onesSum - 10)}(으)로 답하는 경우가 있습니다.`
    },
  },
  {
    id: 'e1-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E1-NUM-11',
    pattern: '{a} + {b}',
    paramRanges: { a: [16, 18], b: [4, 7] },
    constraints: ({ a, b }) => (a % 10) + b > 10,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + (b % 10),
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) => {
      const ones = a % 10
      const comp10 = 10 - ones
      const rest = b - comp10
      return `① ${b}를 ${comp10}와 ${rest}(으)로 가르기합니다.\n② ${a} + ${comp10} = ${a + comp10}\n③ ${a + comp10} + ${rest} = ${ans}\n\n💡 10 만들어 더하기 전략을 사용하세요.`
    },
  },

  // Lv.8: 두 자리 - 한 자리 (받아내림)
  {
    id: 'e1-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E1-NUM-12',
    pattern: '{a} - {b}',
    paramRanges: { a: [21, 29], b: [3, 9] },
    constraints: ({ a, b }) => (a % 10) < b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 10,
      ({ b }) => 20 - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① 일의 자리 ${a % 10}이 ${b}보다 작으므로 십의 자리에서 10을 빌려옵니다.\n② ${a % 10} + 10 = ${(a % 10) + 10}, ${(a % 10) + 10} - ${b} = ${(a % 10) + 10 - b}\n③ 십의 자리: ${Math.floor(a / 10)} - 1 = ${Math.floor(a / 10) - 1}\n④ 답: ${ans}\n\n💡 흔한 실수: 받아내림을 안 해서 ${a - b + 10}(으)로 답하는 경우가 있습니다.`,
  },
  {
    id: 'e1-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E1-NUM-12',
    pattern: '{a} - {b}',
    paramRanges: { a: [22, 28], b: [4, 8] },
    constraints: ({ a, b }) => (a % 10) < b && a - b >= 10,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a - b + 10,
      ({ a, b }) => a - b - 1,
      ({ a, b }) => b - (a % 10),
    ],
    explanationFn: ({ a, b }, ans) =>
      `① 일의 자리 ${a % 10}이 ${b}보다 작으므로 받아내림합니다.\n② ${(a % 10) + 10} - ${b} = ${(a % 10) + 10 - b}\n③ 십의 자리: ${Math.floor(a / 10)} - 1 = ${Math.floor(a / 10) - 1}\n④ 답: ${ans}`,
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
      `① 앞에서부터 차례로 더합니다.\n② ${a} + ${b} = ${a + b}\n③ ${a + b} + ${c} = ${ans}`,
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
      `① 앞에서부터 차례로 더합니다.\n② ${a} + ${b} = ${a + b}\n③ ${a + b} + ${c} = ${ans}`,
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
      `① 왼쪽부터 차례로 계산합니다.\n② ${a} + ${b} = ${a + b}\n③ ${a + b} - ${c} = ${ans}`,
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
      `① 왼쪽부터 차례로 계산합니다.\n② ${a} - ${b} = ${a - b}\n③ ${a - b} + ${c} = ${ans}`,
  },

  // --- B. 새 템플릿 추가 ---

  // 10에서 빼기 (E1-NUM-10)
  {
    id: 'e1-comp-11a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '10 - {a}',
    paramRanges: { a: [1, 9] },
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => a,
      () => 10,
      ({ a }) => 10 - a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `① 10에서 ${a}를 뺍니다.\n② 10 - ${a} = ${ans}\n\n💡 10의 보수: ${a}와 ${ans}를 합하면 10입니다.`,
  },
  {
    id: 'e1-comp-11b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E1-NUM-10',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `10 - ? = ${a}`,
    answerFn: ({ a }) => 10 - a,
    distractorFns: [
      ({ a }) => a,
      () => 10,
      ({ a }) => 10 - a - 1,
    ],
    explanationFn: ({ a }, ans) =>
      `① 10에서 빼서 ${a}가 되는 수를 구합니다.\n② 10 - ${ans} = ${a}\n③ 확인: 10 - ${ans} = ${a} ✓`,
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
      `하나씩 세어 보면 ${ans}개입니다.`,
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
    conceptId: 'E1-NUM-04',
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
    conceptId: 'E1-NUM-04',
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

  // Lv.3: 순서/차이
  {
    id: 'e1-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-04',
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
    conceptId: 'E1-NUM-04',
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
    conceptId: 'E1-NUM-08',
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
      `① "먹었습니다" → 빼기입니다.\n② ${a} - ${b} = ${ans}\n③ 남은 사탕은 ${ans}개입니다.`,
  },
  {
    id: 'e1-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E1-NUM-07',
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
      `① "더 샀습니다" → 더하기입니다.\n② ${a} + ${b} = ${ans}\n③ 모두 ${ans}권입니다.`,
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
      `① 처음 ${a}개에서 ${b}개를 받았으므로: ${a} + ${b} = ${a + b}\n② ${c}개를 주었으므로: ${a + b} - ${c} = ${ans}\n③ 남은 구슬은 ${ans}개입니다.`,
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
      `① ${a}장에서 ${b}장을 사용: ${a} - ${b} = ${a - b}\n② ${c}장을 더 받음: ${a - b} + ${c} = ${ans}\n③ 지금 색종이는 ${ans}장입니다.`,
  },

  // --- B. 새 템플릿 추가 ---

  // 모으기/가르기 (E1-NUM-05, E1-NUM-06)
  {
    id: 'e1-conc-11a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 5] },
    constraints: ({ a, b }) => a + b <= 9,
    contentFn: ({ a, b }) => `${a}와 ${b}를 모으면 얼마인가요?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 1,
      ({ a }) => a,
      ({ a, b }) => Math.abs(a - b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `① 모으기는 두 묶음을 합치는 것입니다.\n② ${a}와 ${b}를 모으면 ${ans}입니다.`,
  },
  {
    id: 'e1-conc-11b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E1-NUM-06',
    pattern: '',
    paramRanges: { n: [5, 9], a: [1, 4] },
    constraints: ({ n, a }) => a < n,
    contentFn: ({ n, a }) => `${n}을 ${a}와 얼마로 가를 수 있나요?`,
    answerFn: ({ n, a }) => n - a,
    distractorFns: [
      ({ n, a }) => n + a,
      ({ a }) => a,
      ({ n, a }) => n - a + 1,
    ],
    explanationFn: ({ n, a }, ans) =>
      `① 가르기는 한 묶음을 두 부분으로 나누는 것입니다.\n② ${n} = ${a} + ${ans}\n③ ${n}을 ${a}와 ${ans}(으)로 가를 수 있습니다.`,
  },

  // 뛰어 세기 (E1-NUM-03)
  {
    id: 'e1-conc-12a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-03',
    pattern: '',
    paramRanges: { a: [2, 10], variant: [0, 2] },
    constraints: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      return a + step * 4 <= 50
    },
    contentFn: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      const seq = [a, a + step, a + step * 2, a + step * 3]
      return `${step}씩 뛰어 세기: ${seq[0]}, ${seq[1]}, ${seq[2]}, ${seq[3]}, ?\n빈칸에 알맞은 수는?`
    },
    answerFn: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      return a + step * 4
    },
    distractorFns: [
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a + step * 3 + 1
      },
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a + step * 5
      },
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a + step * 3
      },
    ],
    explanationFn: ({ a, variant }, ans) => {
      const step = [2, 5, 10][variant]!
      return `${step}씩 뛰어 세는 규칙입니다. ${a + step * 3} 다음은 ${a + step * 3} + ${step} = ${ans}입니다.`
    },
  },
  {
    id: 'e1-conc-12b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E1-NUM-03',
    pattern: '',
    paramRanges: { a: [20, 50], variant: [0, 2] },
    constraints: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      return a - step * 4 >= 0
    },
    contentFn: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      const seq = [a, a - step, a - step * 2, a - step * 3]
      return `${step}씩 거꾸로 뛰어 세기: ${seq[0]}, ${seq[1]}, ${seq[2]}, ${seq[3]}, ?\n빈칸에 알맞은 수는?`
    },
    answerFn: ({ a, variant }) => {
      const step = [2, 5, 10][variant]!
      return a - step * 4
    },
    distractorFns: [
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a - step * 3
      },
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a - step * 4 - 1
      },
      ({ a, variant }) => {
        const step = [2, 5, 10][variant]!
        return a - step * 5
      },
    ],
    explanationFn: ({ a, variant }, ans) => {
      const step = [2, 5, 10][variant]!
      return `${step}씩 거꾸로 뛰어 세는 규칙입니다. ${a - step * 3} 다음은 ${a - step * 3} - ${step} = ${ans}입니다.`
    },
  },

  // 분류하기 (E1-STA-01)
  {
    id: 'e1-conc-13a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'data',
    conceptId: 'E1-STA-01',
    pattern: '',
    paramRanges: { a: [3, 7], b: [2, 6], c: [4, 8] },
    constraints: ({ a, b, c }) => a !== b && b !== c && a !== c,
    contentFn: ({ a, b, c }) =>
      `빨간색 구슬 ${a}개, 파란색 구슬 ${b}개, 노란색 구슬 ${c}개가 있습니다. 구슬은 모두 몇 개인가요?`,
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ a, b, c }) => a + b + c + 1,
      ({ a, c }) => a + c,
      ({ a, b, c }) => Math.max(a, b, c),
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① 색깔별로 세어 봅니다: 빨강 ${a}개, 파랑 ${b}개, 노랑 ${c}개\n② 전부 더합니다: ${a} + ${b} + ${c} = ${ans}개`,
  },
  {
    id: 'e1-conc-13b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'data',
    conceptId: 'E1-STA-01',
    pattern: '',
    paramRanges: { a: [3, 8], b: [2, 7], c: [4, 9] },
    constraints: ({ a, b, c }) => a !== b && b !== c && a !== c && (a > b && a > c || b > a && b > c || c > a && c > b),
    contentFn: ({ a, b, c }) => {
      const items = ['사과', '배', '귤']
      return `${items[0]} ${a}개, ${items[1]} ${b}개, ${items[2]} ${c}개가 있습니다. 가장 많은 과일은 무엇인가요?`
    },
    answerFn: ({ a, b, c }) => {
      const items = ['사과', '배', '귤']
      const max = Math.max(a, b, c)
      if (a === max) return items[0]!
      if (b === max) return items[1]!
      return items[2]!
    },
    distractorFns: [
      ({ a, b, c }) => {
        const items = ['사과', '배', '귤']
        const min = Math.min(a, b, c)
        if (a === min) return items[0]!
        if (b === min) return items[1]!
        return items[2]!
      },
      ({ a, b, c }) => `${a + b + c}개`,
      ({ a, b, c }) => {
        const items = ['사과', '배', '귤']
        const vals = [a, b, c]
        const sorted = [...vals].sort((x, y) => x - y)
        const midIdx = vals.indexOf(sorted[1]!)
        return items[midIdx]!
      },
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `사과 ${a}개, 배 ${b}개, 귤 ${c}개를 비교하면 ${ans}이(가) 가장 많습니다.`,
    questionType: 'multiple_choice',
  },

  // 양의 비교 확장 (E1-GEO-03)
  {
    id: 'e1-conc-14a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo',
    conceptId: 'E1-GEO-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '수박과 사과 중 더 무거운 것은?',
        '교실과 책상 중 더 넓은 것은?',
        '양동이와 컵 중 물을 더 많이 담을 수 있는 것은?',
        '코끼리와 강아지 중 더 무거운 것은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['수박', '교실', '양동이', '코끼리']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['사과', '책상', '컵', '강아지'][variant]!,
      ({ variant }) => ['같다', '같다', '같다', '같다'][variant]!,
      ({ variant }) => ['모른다', '모른다', '모른다', '모른다'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '수박이 사과보다 더 무겁습니다. (무겁다/가볍다로 비교)',
        '교실이 책상보다 더 넓습니다. (넓다/좁다로 비교)',
        '양동이가 컵보다 물을 더 많이 담을 수 있습니다. (많다/적다로 비교)',
        '코끼리가 강아지보다 더 무겁습니다. (무겁다/가볍다로 비교)',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },
  {
    id: 'e1-conc-14b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo',
    conceptId: 'E1-GEO-03',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '무게를 비교할 때 쓰는 말로 알맞은 것은?',
        '넓이를 비교할 때 쓰는 말로 알맞은 것은?',
        '들이를 비교할 때 쓰는 말로 알맞은 것은?',
        '길이를 비교할 때 쓰는 말로 알맞은 것은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['무겁다/가볍다', '넓다/좁다', '많다/적다', '길다/짧다']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['길다/짧다', '무겁다/가볍다', '넓다/좁다', '많다/적다'][variant]!,
      ({ variant }) => ['넓다/좁다', '길다/짧다', '길다/짧다', '넓다/좁다'][variant]!,
      ({ variant }) => ['많다/적다', '많다/적다', '무겁다/가볍다', '무겁다/가볍다'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '무게를 비교할 때는 "무겁다/가볍다"를 씁니다.',
        '넓이를 비교할 때는 "넓다/좁다"를 씁니다.',
        '들이를 비교할 때는 "많다/적다"를 씁니다.',
        '길이를 비교할 때는 "길다/짧다"를 씁니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // 0의 의미 (E1-NUM-02)
  {
    id: 'e1-conc-15a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '바구니에 사과가 하나도 없습니다. 사과는 몇 개인가요?',
        '접시에 과자가 하나도 없습니다. 과자는 몇 개인가요?',
        '상자에 공이 하나도 없습니다. 공은 몇 개인가요?',
      ]
      return questions[variant]!
    },
    answerFn: () => 0,
    distractorFns: [
      () => 1,
      () => 10,
      () => -1,
    ],
    explanationFn: ({ variant }) => {
      const items = ['사과', '과자', '공']
      return `아무것도 없을 때 0이라고 합니다. ${items[variant]}이(가) 하나도 없으므로 0개입니다.`
    },
  },
  {
    id: 'e1-conc-15b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E1-NUM-02',
    pattern: '',
    paramRanges: { a: [1, 4] },
    contentFn: ({ a }) => `${a}0에서 0은 어떤 역할을 하나요?`,
    answerFn: () => '일의 자리가 비어있음을 나타냄',
    distractorFns: [
      () => '아무 뜻도 없다',
      () => '10을 나타낸다',
      () => '0개를 나타낸다',
    ],
    explanationFn: ({ a }) =>
      `${a}0에서 0은 일의 자리에 아무것도 없음을 나타냅니다. 0이 없으면 ${a}0이 ${a}로 바뀌어 버립니다.`,
    questionType: 'multiple_choice',
  },
]

export const elementary1Templates: QuestionTemplate[] = [...comp, ...conc]
