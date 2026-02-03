// 초2 (elementary_2) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'

const G = 'elementary_2' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 두 자리 + 두 자리 (받아올림 없음)
  {
    id: 'e2-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} + {b}',
    paramRanges: { a: [10, 99], b: [10, 99] },
    constraints: ({ a, b }) => {
      const a1 = a % 10
      const a10 = Math.floor(a / 10)
      const b1 = b % 10
      const b10 = Math.floor(b / 10)
      return a1 + b1 < 10 && a10 + b10 < 10
    },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
      ({ a, b }) => a + b + 10,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const a10 = Math.floor(a / 10)
      const b1 = b % 10; const b10 = Math.floor(b / 10)
      return `① 일의 자리: ${a1} + ${b1} = ${a1 + b1}\n② 십의 자리: ${a10} + ${b10} = ${a10 + b10}\n③ ${a} + ${b} = ${ans}`
    },
  },

  // Lv.2: 두 자리 + 두 자리 (받아올림 있음)
  {
    id: 'e2-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} + {b}',
    paramRanges: { a: [10, 99], b: [10, 99] },
    constraints: ({ a, b }) => {
      const a1 = a % 10
      const b1 = b % 10
      return a1 + b1 >= 10
    },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 1,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const a10 = Math.floor(a / 10)
      const b1 = b % 10; const b10 = Math.floor(b / 10)
      return `① 일의 자리: ${a1} + ${b1} = ${a1 + b1} (10이 넘으므로 받아올림)\n② 십의 자리: ${a10} + ${b10} + 1 = ${a10 + b10 + 1}\n③ ${a} + ${b} = ${ans}\n\n💡 흔한 실수: 받아올림을 빠뜨려 ${a + b - 10}(으)로 답하는 경우가 있습니다.`
    },
  },

  // Lv.3: 두 자리 - 두 자리 (받아내림 없음)
  {
    id: 'e2-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'E2-NUM-07',
    pattern: '{a} - {b}',
    paramRanges: { a: [20, 99], b: [10, 98] },
    constraints: ({ a, b }) => {
      if (a <= b) return false
      const a1 = a % 10
      const a10 = Math.floor(a / 10)
      const b1 = b % 10
      const b10 = Math.floor(b / 10)
      return a1 >= b1 && a10 >= b10
    },
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a - b + 1,
      ({ a, b }) => a - b - 1,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const a10 = Math.floor(a / 10)
      const b1 = b % 10; const b10 = Math.floor(b / 10)
      return `① 일의 자리: ${a1} - ${b1} = ${a1 - b1}\n② 십의 자리: ${a10} - ${b10} = ${a10 - b10}\n③ ${a} - ${b} = ${ans}`
    },
  },

  // Lv.4: 두 자리 - 두 자리 (받아내림 있음)
  {
    id: 'e2-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'E2-NUM-07',
    pattern: '{a} - {b}',
    paramRanges: { a: [20, 99], b: [10, 98] },
    constraints: ({ a, b }) => {
      if (a <= b) return false
      const a1 = a % 10
      const b1 = b % 10
      return a1 < b1
    },
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a - b + 10,
      ({ a, b }) => {
        // 감산 방향 오류: 큰수에서 작은수 빼기
        const a1 = a % 10; const b1 = b % 10
        const a10 = Math.floor(a / 10); const b10 = Math.floor(b / 10)
        return (a10 - b10) * 10 + (b1 - a1)
      },
      ({ a, b }) => a - b + 1,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const a10 = Math.floor(a / 10)
      const b1 = b % 10; const b10 = Math.floor(b / 10)
      return `① 일의 자리: ${a1} < ${b1}이므로 십의 자리에서 10을 빌려옵니다.\n② 일의 자리: ${a1 + 10} - ${b1} = ${a1 + 10 - b1}\n③ 십의 자리: ${a10} - 1 - ${b10} = ${a10 - 1 - b10}\n④ ${a} - ${b} = ${ans}\n\n💡 흔한 실수: ${b1} - ${a1} = ${b1 - a1}로 뒤집어 빼거나, 받아내림 후 십의 자리 감소를 잊는 경우가 있습니다.`
    },
  },

  // Lv.5: 세 자리 + 두 자리
  {
    id: 'e2-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} + {b}',
    paramRanges: { a: [100, 999], b: [10, 99] },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
      ({ a, b }) => a + b + 10,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① 자릿값을 맞추어 세로로 더합니다.\n② ${a} + ${b} = ${ans}`,
  },
  {
    id: 'e2-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} + {b}',
    paramRanges: { a: [100, 999], b: [10, 99] },
    constraints: ({ a, b }) => {
      const a1 = a % 10
      const b1 = b % 10
      return a1 + b1 >= 10
    },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a + b - 10,
      ({ a, b }) => a + b + 10,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const b1 = b % 10
      return `① 일의 자리: ${a1} + ${b1} = ${a1 + b1} (받아올림)\n② ${a} + ${b} = ${ans}`
    },
  },

  // Lv.6: 세 자리 - 두 자리
  {
    id: 'e2-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E2-NUM-07',
    pattern: '{a} - {b}',
    paramRanges: { a: [100, 999], b: [10, 99] },
    constraints: ({ a, b }) => a > b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a - b + 1,
      ({ a, b }) => a - b - 1,
      ({ a, b }) => a - b + 10,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① 자릿값을 맞추어 세로로 뺍니다.\n② ${a} - ${b} = ${ans}`,
  },
  {
    id: 'e2-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'E2-NUM-07',
    pattern: '{a} - {b}',
    paramRanges: { a: [100, 999], b: [10, 99] },
    constraints: ({ a, b }) => {
      if (a <= b) return false
      const a1 = a % 10
      const b1 = b % 10
      return a1 < b1
    },
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a - b + 10,
      ({ a, b }) => a - b - 10,
      ({ a, b }) => a - b + 1,
    ],
    explanationFn: ({ a, b }, ans) => {
      const a1 = a % 10; const b1 = b % 10
      return `① 일의 자리: ${a1} < ${b1}이므로 받아내림합니다.\n② ${a} - ${b} = ${ans}\n\n💡 흔한 실수: 받아내림을 잊어 ${a - b + 10}(으)로 답하는 경우가 있습니다.`
    },
  },

  // Lv.7: 곱셈 구구단 (2,5단)
  {
    id: 'e2-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [2, 2], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 2,
      ({ a, b }) => a * b - 2,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}단: ${a}씩 ${b}번 뛰어 세기입니다.\n② ${a} × ${b} = ${ans}\n\n💡 ${a} × ${b} = ${a}를 ${b}번 더한 것과 같습니다.`,
  },
  {
    id: 'e2-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [5, 5], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 5,
      ({ a, b }) => a * b - 5,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}단: ${a}씩 ${b}번 뛰어 세기입니다.\n② ${a} × ${b} = ${ans}\n\n💡 5단은 5, 10, 15, 20... 규칙적으로 늘어납니다.`,
  },

  // Lv.8: 곱셈 구구단 (3,4,6단)
  {
    id: 'e2-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [3, 3], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 3,
      ({ a, b }) => a * b - 3,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}단: ${a}씩 ${b}번 뛰어 세기입니다.\n② ${a} × ${b} = ${ans}`,
  },
  {
    id: 'e2-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [4, 4], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 4,
      ({ a, b }) => a * b - 4,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}단: ${a}씩 ${b}번 뛰어 세기입니다.\n② ${a} × ${b} = ${ans}`,
  },
  {
    id: 'e2-comp-8c',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [6, 6], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 6,
      ({ a, b }) => a * b - 6,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}단: ${a}씩 ${b}번 뛰어 세기입니다.\n② ${a} × ${b} = ${ans}\n\n💡 6단 = 3단의 2배입니다. (${a} × ${b} = 3 × ${b} × 2 = ${3 * b} × 2 = ${ans})`,
  },

  // Lv.9: 곱셈 구구단 (7,8,9단)
  {
    id: 'e2-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [7, 7], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 7,
      ({ a, b }) => a * b - 7,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a} × ${b} = ${ans}\n\n💡 흔한 실수: 곱셈과 덧셈을 혼동하여 ${a} + ${b} = ${a + b}(으)로 답하는 경우가 있습니다.`,
  },
  {
    id: 'e2-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [8, 8], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 8,
      ({ a, b }) => a * b - 8,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a} × ${b} = ${ans}\n\n💡 8단 = 4단의 2배입니다. (4 × ${b} = ${4 * b}, ${4 * b} × 2 = ${ans})`,
  },
  {
    id: 'e2-comp-9c',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × {b}',
    paramRanges: { a: [9, 9], b: [1, 9] },
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a * b + 9,
      ({ a, b }) => a * b - 9,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a} × ${b} = ${ans}\n\n💡 9단 규칙: 십의 자리가 1씩 커지고, 일의 자리가 1씩 작아집니다.`,
  },

  // Lv.10: 혼합 (덧뺄셈 + 곱셈 기초)
  {
    id: 'e2-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} × {b} + {c}',
    paramRanges: { a: [2, 5], b: [1, 9], c: [1, 20] },
    answerFn: ({ a, b, c }) => a * b + c,
    distractorFns: [
      ({ a, b, c }) => a * (b + c),
      ({ a, b, c }) => a * b - c,
      ({ a, b, c }) => a + b + c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① 곱셈을 먼저 계산합니다: ${a} × ${b} = ${a * b}\n② 그 다음 더합니다: ${a * b} + ${c} = ${ans}\n\n💡 흔한 실수: 곱셈과 덧셈을 혼동하여 ${a} + ${b} + ${c} = ${a + b + c}(으)로 답하는 경우가 있습니다.`,
  },
  {
    id: 'e2-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'E2-NUM-06',
    pattern: '{a} × {b} - {c}',
    paramRanges: { a: [2, 5], b: [2, 9], c: [1, 10] },
    constraints: ({ a, b, c }) => a * b > c,
    answerFn: ({ a, b, c }) => a * b - c,
    distractorFns: [
      ({ a, b, c }) => a * (b - c),
      ({ a, b, c }) => a * b + c,
      ({ a, b, c }) => a + b - c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① 곱셈을 먼저 계산합니다: ${a} × ${b} = ${a * b}\n② 그 다음 뺍니다: ${a * b} - ${c} = ${ans}`,
  },

  // --- B. 새 템플릿 추가 ---

  // 0과 1의 곱 (E2-NUM-12)
  {
    id: 'e2-comp-11a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × 0',
    paramRanges: { a: [2, 9] },
    answerFn: () => 0,
    distractorFns: [
      ({ a }) => a,
      () => 1,
      ({ a }) => a + 0,
    ],
    explanationFn: ({ a }) =>
      `① 어떤 수든 0을 곱하면 0입니다.\n② ${a} × 0 = 0`,
  },
  {
    id: 'e2-comp-11b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'E2-NUM-12',
    pattern: '{a} × 1',
    paramRanges: { a: [2, 9] },
    answerFn: ({ a }) => a,
    distractorFns: [
      () => 1,
      () => 0,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a }) =>
      `① 어떤 수든 1을 곱하면 자기 자신입니다.\n② ${a} × 1 = ${a}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 세 자리 수 읽기/쓰기
  {
    id: 'e2-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E2-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 9], b: [0, 9], c: [0, 9] },
    contentFn: ({ a, b, c }) =>
      `백의 자리가 ${a}, 십의 자리가 ${b}, 일의 자리가 ${c}인 수는?`,
    answerFn: ({ a, b, c }) => a * 100 + b * 10 + c,
    distractorFns: [
      ({ a, b, c }) => a * 10 + b + c * 100,
      ({ a, b, c }) => a + b * 10 + c,
      ({ a, b, c }) => a * 100 + b + c * 10,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① 백의 자리: ${a} × 100 = ${a * 100}\n② 십의 자리: ${b} × 10 = ${b * 10}\n③ 일의 자리: ${c}\n④ ${a * 100} + ${b * 10} + ${c} = ${ans}`,
  },
  {
    id: 'e2-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'E2-NUM-01',
    pattern: '',
    paramRanges: { n: [100, 999] },
    contentFn: ({ n }) => `${n}을 읽으면?`,
    answerFn: ({ n }) => {
      const h = Math.floor(n / 100)
      const t = Math.floor((n % 100) / 10)
      const o = n % 10
      let result = ''
      if (h > 0) result += ['', '백', '이백', '삼백', '사백', '오백', '육백', '칠백', '팔백', '구백'][h]
      if (t > 0) result += ['', '십', '이십', '삼십', '사십', '오십', '육십', '칠십', '팔십', '구십'][t]
      if (o > 0) result += ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구'][o]
      return result || '영'
    },
    distractorFns: [
      ({ n }) => n.toString(),
      ({ n }) => n + 1,
      ({ n }) => n - 1,
    ],
    explanationFn: ({ n }, ans) => `${n}은(는) ${ans}이라고 읽습니다.`,
  },

  // Lv.2: 자릿값 이해
  {
    id: 'e2-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra',
    conceptId: 'E2-ALG-01',
    pattern: '',
    paramRanges: { a: [1, 9], b: [0, 9], c: [0, 9] },
    contentFn: ({ a, b, c }) => {
      const n = a * 100 + b * 10 + c
      return `${n}에서 ${b}는 몇의 자리 숫자인가?`
    },
    answerFn: () => '십의 자리',
    distractorFns: [
      () => '백의 자리',
      () => '일의 자리',
      () => '천의 자리',
    ],
    explanationFn: ({ a, b, c }) => {
      const n = a * 100 + b * 10 + c
      return `${n}에서 ${b}는 십의 자리 숫자입니다.`
    },
  },
  {
    id: 'e2-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra',
    conceptId: 'E2-ALG-01',
    pattern: '',
    paramRanges: { a: [1, 9], b: [1, 9], c: [0, 9] },
    contentFn: ({ a, b, c }) => {
      const n = a * 100 + b * 10 + c
      return `${n}에서 십의 자리 숫자 ${b}는 얼마를 나타내는가?`
    },
    answerFn: ({ b }) => b * 10,
    distractorFns: [
      ({ b }) => b,
      ({ b }) => b * 100,
      ({ b }) => b * 10 + 1,
    ],
    explanationFn: ({ b }, ans) =>
      `십의 자리 숫자 ${b}는 ${ans}를 나타냅니다.`,
  },

  // Lv.3: 길이 단위 (cm, m)
  {
    id: 'e2-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'geo',
    conceptId: 'E2-GEO-01',
    pattern: '',
    paramRanges: {},
    contentFn: () => `1m는 몇 cm인가?`,
    answerFn: () => 100,
    distractorFns: [
      () => 10,
      () => 1000,
      () => 50,
    ],
    explanationFn: () => `1m = 100cm입니다.`,
  },
  {
    id: 'e2-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'geo',
    conceptId: 'E2-GEO-01',
    pattern: '',
    paramRanges: { a: [1, 5], b: [10, 99] },
    contentFn: ({ a, b }) => `${a}m ${b}cm는 모두 몇 cm인가?`,
    answerFn: ({ a, b }) => a * 100 + b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * 10 + b,
      ({ a, b }) => a * 100 - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a}m = ${a * 100}cm이므로 ${a}m ${b}cm = ${a * 100}cm + ${b}cm = ${ans}cm`,
  },
  {
    id: 'e2-conc-3c',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'geo',
    conceptId: 'E2-GEO-01',
    pattern: '',
    paramRanges: { a: [100, 500] },
    constraints: ({ a }) => a % 100 === 0,
    contentFn: ({ a }) => `${a}cm는 몇 m인가?`,
    answerFn: ({ a }) => a / 100,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a / 10,
      ({ a }) => a / 100 + 1,
    ],
    explanationFn: ({ a }, ans) => `${a}cm = ${ans}m (100cm = 1m)`,
  },

  // Lv.4: 시각과 시간
  {
    id: 'e2-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E2-STA-03',
    pattern: '',
    paramRanges: {},
    contentFn: () => `1시간은 몇 분인가?`,
    answerFn: () => 60,
    distractorFns: [
      () => 30,
      () => 100,
      () => 50,
    ],
    explanationFn: () => `1시간 = 60분입니다.`,
  },
  {
    id: 'e2-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E2-STA-03',
    pattern: '',
    paramRanges: { a: [1, 3], b: [10, 50], c: [0, 2], d: [10, 50] },
    constraints: ({ b, d }) => b + d < 60,
    contentFn: ({ a, b, c, d }) =>
      `${a}시간 ${b}분 + ${c}시간 ${d}분은?`,
    answerFn: ({ a, b, c, d }) => {
      const totalH = a + c
      const totalM = b + d
      return `${totalH}시간 ${totalM}분`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a + c}시간 ${b + d + 10}분`,
      ({ a, b, c, d }) => `${a + c + 1}시간 ${b + d}분`,
      ({ a, c }) => `${a + c}시간`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}시간 ${b}분 + ${c}시간 ${d}분 = ${a + c}시간 ${b + d}분 = ${ans}`,
  },
  {
    id: 'e2-conc-4c',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E2-STA-03',
    pattern: '',
    paramRanges: { a: [1, 2], b: [20, 50], c: [1, 2], d: [10, 40] },
    constraints: ({ a, b, c, d }) => a * 60 + b > c * 60 + d && b >= d,
    contentFn: ({ a, b, c, d }) =>
      `${a}시간 ${b}분 - ${c}시간 ${d}분은?`,
    answerFn: ({ a, b, c, d }) => {
      const totalH = a - c
      const totalM = b - d
      return `${totalH}시간 ${totalM}분`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a - c}시간 ${b - d + 10}분`,
      ({ a, b, c, d }) => `${a - c - 1}시간 ${b - d}분`,
      ({ a, c }) => `${a - c}시간`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}시간 ${b}분 - ${c}시간 ${d}분 = ${a - c}시간 ${b - d}분 = ${ans}`,
  },

  // Lv.5: 표 읽기
  {
    id: 'e2-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'data',
    conceptId: 'E2-STA-01',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const tables = [
        `다음 표는 학생들이 좋아하는 과일을 나타낸 것입니다.\n| 과일 | 사과 | 바나나 | 포도 |\n| 학생 수 | 15 | 12 | 18 |\n가장 많은 학생이 좋아하는 과일은?`,
        `다음 표는 요일별 방문자 수입니다.\n| 요일 | 월 | 화 | 수 | 목 |\n| 방문자 | 20 | 25 | 18 | 30 |\n방문자가 가장 적은 요일은?`,
        `다음 표는 동물 수를 나타낸 것입니다.\n| 동물 | 강아지 | 고양이 | 토끼 |\n| 수 | 8 | 12 | 10 |\n동물은 모두 몇 마리인가?`,
      ]
      return tables[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['포도', '수요일', 30]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['사과', '월요일', 20][variant]!,
      ({ variant }) => ['바나나', '화요일', 25][variant]!,
      ({ variant }) => ['사과', '목요일', 15][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '표에서 학생 수가 가장 많은 것은 포도(18명)입니다.',
        '표에서 방문자가 가장 적은 요일은 수요일(18명)입니다.',
        '① 8 + 12 + 10 = 30\n② 동물은 모두 30마리입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.6: 그래프 읽기
  {
    id: 'e2-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'data',
    conceptId: 'E2-STA-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        `막대그래프에서 A반 12명, B반 15명, C반 10명이 나타나 있습니다. 가장 많은 반은?`,
        `그래프에서 월요일 8권, 화요일 12권, 수요일 15권의 책을 읽었습니다. 가장 적은 날은?`,
        `그래프에서 사과 10개, 배 8개, 귤 12개가 있습니다. 모두 몇 개인가?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['B반', '월요일', 30]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['A반', '화요일', 20][variant]!,
      ({ variant }) => ['C반', '수요일', 25][variant]!,
      ({ variant }) => ['A반', '월요일', 15][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '그래프에서 가장 높은 막대는 B반(15명)입니다.',
        '그래프에서 가장 낮은 막대는 월요일(8권)입니다.',
        '① 10 + 8 + 12 = 30\n② 모두 30개입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.7: 규칙 찾기
  {
    id: 'e2-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra',
    conceptId: 'E2-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 5] },
    contentFn: ({ a }) => {
      const seq = [a, a * 2, a * 3, a * 4]
      return `다음 수의 규칙을 찾아 □에 알맞은 수를 구하시오.\n${seq.join(', ')}, □`
    },
    answerFn: ({ a }) => a * 5,
    distractorFns: [
      ({ a }) => a * 4 + 1,
      ({ a }) => a * 6,
      ({ a }) => a * 4 + a - 1,
    ],
    explanationFn: ({ a }, ans) =>
      `${a}씩 커지는 규칙입니다. ${a * 4} + ${a} = ${ans}`,
  },
  {
    id: 'e2-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra',
    conceptId: 'E2-ALG-02',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 4] },
    contentFn: ({ a, b }) => {
      const seq = [a, a + b, a + 2 * b, a + 3 * b]
      return `다음 수의 규칙을 찾아 □에 알맞은 수를 구하시오.\n${seq.join(', ')}, □`
    },
    answerFn: ({ a, b }) => a + 4 * b,
    distractorFns: [
      ({ a, b }) => a + 3 * b + 1,
      ({ a, b }) => a + 5 * b,
      ({ a, b }) => a + 3 * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${b}씩 커지는 규칙입니다. ${a + 3 * b} + ${b} = ${ans}`,
  },

  // Lv.8: 도형 분류
  {
    id: 'e2-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'E2-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '삼각형의 꼭짓점은 모두 몇 개인가?',
        '사각형의 변은 모두 몇 개인가?',
        '오각형의 꼭짓점은 모두 몇 개인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [3, 4, 5]
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [4, 3, 4][variant]!,
      ({ variant }) => [2, 5, 6][variant]!,
      ({ variant }) => [5, 6, 3][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '삼각형은 꼭짓점이 3개입니다.',
        '사각형은 변이 4개입니다.',
        '오각형은 꼭짓점이 5개입니다.',
      ]
      return explanations[variant]!
    },
  },
  {
    id: 'e2-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'E2-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 1] },
    contentFn: ({ variant }) => {
      const questions = [
        '네 변의 길이가 모두 같은 사각형은?',
        '네 각이 모두 직각인 사각형은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['정사각형', '직사각형']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['직사각형', '정사각형'][variant]!,
      ({ variant }) => ['삼각형', '삼각형'][variant]!,
      ({ variant }) => ['오각형', '원'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '네 변의 길이가 모두 같은 사각형은 정사각형입니다.',
        '네 각이 모두 직각인 사각형은 직사각형(정사각형 포함)입니다.',
      ]
      return explanations[variant]!
    },
  },

  // Lv.9: 문장제
  {
    id: 'e2-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E2-NUM-02',
    pattern: '',
    paramRanges: { a: [20, 50], b: [10, 30] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b }) =>
      `사과가 ${a}개 있었습니다. 그 중에서 ${b}개를 먹었습니다. 남은 사과는 몇 개인가?`,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b + 1,
      ({ a, b }) => a - b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① "먹었습니다" → 빼기입니다.\n② ${a} - ${b} = ${ans}개`,
  },
  {
    id: 'e2-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E2-NUM-02',
    pattern: '',
    paramRanges: { a: [15, 40], b: [10, 30] },
    contentFn: ({ a, b }) =>
      `철수는 공책을 ${a}권 가지고 있고, 영희는 ${b}권 가지고 있습니다. 두 사람의 공책은 모두 몇 권인가?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① "모두 몇 권" → 더하기입니다.\n② ${a} + ${b} = ${ans}권`,
  },
  {
    id: 'e2-conc-9c',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'E2-NUM-02',
    pattern: '',
    paramRanges: { a: [3, 5], b: [4, 8] },
    contentFn: ({ a, b }) =>
      `연필 한 묶음에 ${b}자루씩 들어 있습니다. ${a}묶음에는 모두 몇 자루인가?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① "몇 자루씩 × 몇 묶음" → 곱하기입니다.\n② ${b} × ${a} = ${ans}자루\n\n💡 흔한 실수: 곱셈 대신 덧셈을 하여 ${a} + ${b} = ${a + b}(으)로 답하는 경우가 있습니다.`,
  },

  // Lv.10: 복합 문장제
  {
    id: 'e2-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E2-NUM-06',
    pattern: '',
    paramRanges: { a: [30, 60], b: [10, 20], c: [15, 30] },
    constraints: ({ a, b, c }) => a + b > c,
    contentFn: ({ a, b, c }) =>
      `처음에 구슬이 ${a}개 있었습니다. ${b}개를 더 받았고, 그 중에서 ${c}개를 동생에게 주었습니다. 남은 구슬은 몇 개인가?`,
    answerFn: ({ a, b, c }) => a + b - c,
    distractorFns: [
      ({ a, b, c }) => a - b + c,
      ({ a, b, c }) => a + b + c,
      ({ a, b, c }) => a - b - c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① ${a} + ${b} = ${a + b}개 (더 받은 후)\n② ${a + b} - ${c} = ${ans}개 (준 후)\n③ 남은 구슬은 ${ans}개입니다.`,
  },
  {
    id: 'e2-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E2-NUM-06',
    pattern: '',
    paramRanges: { a: [20, 40], b: [3, 5], c: [5, 15] },
    contentFn: ({ a, b, c }) =>
      `한 상자에 사과가 ${b}개씩 들어 있습니다. ${a}개의 사과를 상자에 담고 ${c}개가 남았습니다. 상자는 모두 몇 개 필요했나요?`,
    answerFn: ({ a, b }) => Math.floor(a / b),
    distractorFns: [
      ({ a, b }) => Math.floor(a / b) + 1,
      ({ a, b }) => a - b,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}개를 ${b}개씩 나누면: ${a} ÷ ${b} = ${ans}\n② ${ans}상자가 필요합니다.`,
  },
  {
    id: 'e2-conc-10c',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'word',
    conceptId: 'E2-NUM-06',
    pattern: '',
    paramRanges: { a: [4, 6], b: [5, 8], c: [3, 5] },
    contentFn: ({ a, b, c }) =>
      `빵을 하루에 ${b}개씩 ${a}일 동안 만들었습니다. 그 중에서 ${c * a}개를 팔았습니다. 남은 빵은 몇 개인가?`,
    answerFn: ({ a, b, c }) => a * b - c * a,
    distractorFns: [
      ({ a, b, c }) => a * b + c * a,
      ({ a, b }) => a * b,
      ({ a, c }) => a * c,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `① 만든 빵: ${b} × ${a} = ${a * b}개\n② 판 빵: ${c * a}개\n③ 남은 빵: ${a * b} - ${c * a} = ${ans}개`,
  },

  // --- B. 새 템플릿 추가 ---

  // 네 자리 수 (E2-NUM-04)
  {
    id: 'e2-conc-11a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'E2-NUM-04',
    pattern: '',
    paramRanges: { a: [1, 9], b: [0, 9], c: [0, 9], d: [0, 9] },
    contentFn: ({ a, b, c, d }) =>
      `천의 자리가 ${a}, 백의 자리가 ${b}, 십의 자리가 ${c}, 일의 자리가 ${d}인 수는?`,
    answerFn: ({ a, b, c, d }) => a * 1000 + b * 100 + c * 10 + d,
    distractorFns: [
      ({ a, b, c, d }) => a * 100 + b * 10 + c + d * 1000,
      ({ a, b, c, d }) => a * 1000 + b * 100 + c + d * 10,
      ({ a, b, c, d }) => a * 1000 + b * 10 + c * 100 + d,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `① 천의 자리: ${a} × 1000 = ${a * 1000}\n② 백의 자리: ${b} × 100 = ${b * 100}\n③ 십의 자리: ${c} × 10 = ${c * 10}\n④ 일의 자리: ${d}\n⑤ ${a * 1000} + ${b * 100} + ${c * 10} + ${d} = ${ans}`,
  },

  // 뛰어 세기 (E2-NUM-05)
  {
    id: 'e2-conc-12a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc',
    conceptId: 'E2-NUM-05',
    pattern: '',
    paramRanges: { a: [100, 400], n: [2, 4] },
    constraints: ({ a }) => a % 10 === 0,
    contentFn: ({ a, n }) =>
      `${a}에서 10씩 ${n}번 뛰어 세면 얼마인가요?`,
    answerFn: ({ a, n }) => a + 10 * n,
    distractorFns: [
      ({ a, n }) => a + n,
      ({ a, n }) => a + 100 * n,
      ({ a, n }) => a + 10 * n + 10,
    ],
    explanationFn: ({ a, n }, ans) =>
      `① ${a}에서 10씩 ${n}번 뛰어 셉니다.\n② ${a} + ${10 * n} = ${ans}`,
  },

  // 역연산 관계 (E2-NUM-08)
  {
    id: 'e2-conc-13a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'calc',
    conceptId: 'E2-NUM-08',
    pattern: '',
    paramRanges: { a: [3, 12], b: [3, 12] },
    contentFn: ({ a, b }) => `□ + ${b} = ${a + b}일 때, □는 얼마인가요?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ b }) => b,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a, b }) =>
      `① □ + ${b} = ${a + b}\n② □ = ${a + b} - ${b} = ${a}\n\n💡 덧셈과 뺄셈은 역연산 관계입니다.`,
  },
  {
    id: 'e2-conc-13b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'calc',
    conceptId: 'E2-NUM-08',
    pattern: '',
    paramRanges: { a: [10, 20], b: [3, 9] },
    constraints: ({ a, b }) => a > b,
    contentFn: ({ a, b }) => `${a} - □ = ${a - b}일 때, □는 얼마인가요?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a, b }) => a - b,
      ({ a }) => a,
      ({ b }) => b + 1,
    ],
    explanationFn: ({ a, b }) =>
      `① ${a} - □ = ${a - b}\n② □ = ${a} - ${a - b} = ${b}\n\n💡 뺄셈의 빈칸은 덧셈으로 구할 수 있습니다.`,
  },

  // 동수누가 (E2-NUM-09)
  {
    id: 'e2-conc-14a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc',
    conceptId: 'E2-NUM-09',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 5] },
    contentFn: ({ a, b }) => {
      const terms = Array(b).fill(a).join(' + ')
      return `${terms} = ${a} × ?\n□에 알맞은 수는?`
    },
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => a * b,
      ({ b }) => b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}을(를) ${b}번 더하면 ${a} × ${b}입니다.\n② □ = ${ans}\n\n💡 같은 수를 여러 번 더하는 것이 곱셈입니다.`,
  },
  {
    id: 'e2-conc-14b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc',
    conceptId: 'E2-NUM-09',
    pattern: '',
    paramRanges: { a: [3, 6], b: [3, 5] },
    contentFn: ({ a, b }) =>
      `${a}를 ${b}번 더하면 얼마인가요?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + a,
      ({ a, b }) => a * b - a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}를 ${b}번 더하면 ${a} × ${b}입니다.\n② ${a} × ${b} = ${ans}`,
  },

  // 배(倍) (E2-NUM-10)
  {
    id: 'e2-conc-15a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc',
    conceptId: 'E2-NUM-10',
    pattern: '',
    paramRanges: { a: [2, 5], b: [2, 5] },
    contentFn: ({ a, b }) => `${a}의 ${b}배는 얼마인가요?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}의 ${b}배 = ${a} × ${b}\n② ${a} × ${b} = ${ans}`,
  },

  // 배열 모델 (E2-NUM-11)
  {
    id: 'e2-conc-16a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'calc',
    conceptId: 'E2-NUM-11',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 6] },
    contentFn: ({ a, b }) =>
      `사과가 ${a}줄에 ${b}개씩 놓여 있습니다. 사과는 모두 몇 개인가요?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a}줄 × ${b}개씩 = ${a} × ${b}\n② ${a} × ${b} = ${ans}개`,
  },

  // 몇 분 전 (E2-GEO-03)
  {
    id: 'e2-conc-17a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E2-GEO-03',
    pattern: '',
    paramRanges: { a: [2, 11], b: [1, 3] },
    constraints: ({ b }) => b * 10 <= 30,
    contentFn: ({ a, b }) =>
      `${a + 1}시 ${b * 10}분 전은 몇 시 몇 분인가요?`,
    answerFn: ({ a, b }) => `${a}시 ${60 - b * 10}분`,
    distractorFns: [
      ({ a, b }) => `${a + 1}시 ${b * 10}분`,
      ({ a, b }) => `${a}시 ${b * 10}분`,
      ({ a, b }) => `${a + 1}시 ${60 - b * 10}분`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① "${a + 1}시 ${b * 10}분 전"은 ${a + 1}시에서 ${b * 10}분을 빼는 것입니다.\n② ${a + 1}시 - ${b * 10}분 = ${a}시 ${60 - b * 10}분\n③ 답: ${ans}`,
    questionType: 'multiple_choice',
  },
  {
    id: 'e2-conc-17b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'geo',
    conceptId: 'E2-GEO-03',
    pattern: '',
    paramRanges: { a: [1, 11], b: [40, 55] },
    constraints: ({ b }) => b % 5 === 0,
    contentFn: ({ a, b }) =>
      `${a}시 ${b}분은 ${a + 1}시 몇 분 전인가요?`,
    answerFn: ({ b }) => `${60 - b}분 전`,
    distractorFns: [
      ({ b }) => `${b}분 전`,
      ({ b }) => `${60 - b + 10}분 전`,
      ({ b }) => `${60 - b - 5}분 전`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `① ${a + 1}시가 되려면 ${60 - b}분이 더 필요합니다.\n② ${a}시 ${b}분 = ${a + 1}시 ${60 - b}분 전\n③ 답: ${ans}`,
    questionType: 'multiple_choice',
  },
]

export const elementary2Templates: QuestionTemplate[] = [...comp, ...conc]
