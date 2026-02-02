// 고1 (high_1) 공통수학1 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import type { ProblemPart } from '../../../types'
import { signedStr } from '../utils/math'

const G = 'high_1' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 다항식 정리
  {
    id: 'h1-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-01',
    pattern: '',
    paramRanges: { a: [1, 5], b: [-10, 10], c: [1, 5], d: [-10, 10] },
    constraints: ({ b, d }) => b !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a}x² ${signedStr(b)}x) + (${c}x² ${signedStr(d)}x)의 x² 계수는?`,
    answerFn: ({ a, c }) => a + c,
    distractorFns: [
      ({ b, d }) => b + d,
      ({ a, c }) => a - c,
      ({ a, c }) => a * c,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a}x² ${signedStr(b)}x) + (${c}x² ${signedStr(d)}x) = ${a + c}x² + ${b + d}x\n` +
      `x² 계수는 ${ans}`,
  },
  {
    id: 'h1-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-01',
    pattern: '',
    paramRanges: { a: [1, 5], b: [-10, 10], c: [1, 5], d: [-10, 10] },
    constraints: ({ b, d }) => b !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a}x² ${signedStr(b)}x) + (${c}x² ${signedStr(d)}x)의 x 계수는?`,
    answerFn: ({ b, d }) => b + d,
    distractorFns: [
      ({ a, c }) => a + c,
      ({ b, d }) => b - d,
      ({ b, d }) => b * d,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a}x² ${signedStr(b)}x) + (${c}x² ${signedStr(d)}x) = ${a + c}x² + ${b + d}x\n` +
      `x 계수는 ${ans}`,
  },

  // Lv.2: 다항식 나눗셈
  {
    id: 'h1-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 9], b: [-15, 15], c: [-10, 10] },
    constraints: ({ b, c }) => b !== 0 && c !== 0,
    contentFn: ({ a, b, c }) =>
      `(${a}x² ${signedStr(b)}x ${signedStr(c)}) ÷ x의 x 계수는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ b }) => b,
      ({ a }) => a * 2,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a, b, c }) =>
      `(${a}x² ${signedStr(b)}x ${signedStr(c)}) ÷ x = ${a}x ${signedStr(b)} + ${c}/x\n` +
      `x 계수는 ${a}`,
  },
  {
    id: 'h1-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-02',
    pattern: '',
    paramRanges: { a: [2, 9], b: [-15, 15], c: [-10, 10] },
    constraints: ({ b, c }) => b !== 0 && c !== 0,
    contentFn: ({ a, b, c }) =>
      `(${a}x² ${signedStr(b)}x ${signedStr(c)}) ÷ x의 상수항은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ c }) => c,
      ({ b }) => -b,
    ],
    explanationFn: ({ a, b, c }) =>
      `(${a}x² ${signedStr(b)}x ${signedStr(c)}) ÷ x = ${a}x ${signedStr(b)} + ${c}/x\n` +
      `상수항은 ${b}`,
  },

  // Lv.3: 인수분해 (고급)
  {
    id: 'h1-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-05',
    pattern: '',
    paramRanges: { a: [1, 8], b: [1, 8] },
    constraints: ({ a, b }) => a > 0 && b > 0 && a !== b,
    contentFn: ({ a, b }) =>
      `x² + ${a + b}x + ${a * b}를 인수분해하면 (x+p)(x+q)이다. p > q일 때 p는?`,
    answerFn: ({ a, b }) => Math.max(a, b),
    distractorFns: [
      ({ a, b }) => Math.min(a, b),
      ({ a, b }) => a + b,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x² + ${a + b}x + ${a * b} = (x + ${a})(x + ${b})\n` +
      `큰 값은 ${ans}`,
  },

  // Lv.4: 복소수 덧뺄셈
  {
    id: 'h1-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-5, 5], b: [-5, 5], c: [-5, 5], d: [-5, 5] },
    constraints: ({ a, b, c, d }) => a !== 0 && b !== 0 && c !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a} + ${b}i) + (${c} + ${d}i)의 실수부는?`,
    answerFn: ({ a, c }) => a + c,
    distractorFns: [
      ({ b, d }) => b + d,
      ({ a, c }) => a - c,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a} + ${b}i) + (${c} + ${d}i) = ${a + c} + ${b + d}i\n` +
      `실수부는 ${ans}`,
  },
  {
    id: 'h1-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-5, 5], b: [-5, 5], c: [-5, 5], d: [-5, 5] },
    constraints: ({ a, b, c, d }) => a !== 0 && b !== 0 && c !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a} + ${b}i) + (${c} + ${d}i)의 허수부는?`,
    answerFn: ({ b, d }) => b + d,
    distractorFns: [
      ({ a, c }) => a + c,
      ({ b, d }) => b - d,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a} + ${b}i) + (${c} + ${d}i) = ${a + c} + ${b + d}i\n` +
      `허수부는 ${ans}`,
  },

  // Lv.5: 복소수 곱셈
  {
    id: 'h1-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-4, 4], b: [-4, 4], c: [-4, 4], d: [-4, 4] },
    constraints: ({ a, b, c, d }) => a !== 0 && b !== 0 && c !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a} + ${b}i)(${c} + ${d}i)의 실수부는?`,
    answerFn: ({ a, b, c, d }) => a * c - b * d,
    distractorFns: [
      ({ a, b, c, d }) => a * c + b * d,
      ({ a, d, b, c }) => a * d + b * c,
      ({ a, c }) => a * c,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a} + ${b}i)(${c} + ${d}i) = ${a * c} + ${a * d}i + ${b * c}i + ${b * d}i²\n` +
      `= ${a * c} + ${a * d}i + ${b * c}i - ${b * d}\n` +
      `= ${a * c - b * d} + ${a * d + b * c}i\n` +
      `실수부는 ${ans}`,
  },
  {
    id: 'h1-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-4, 4], b: [-4, 4], c: [-4, 4], d: [-4, 4] },
    constraints: ({ a, b, c, d }) => a !== 0 && b !== 0 && c !== 0 && d !== 0,
    contentFn: ({ a, b, c, d }) =>
      `(${a} + ${b}i)(${c} + ${d}i)의 허수부는?`,
    answerFn: ({ a, d, b, c }) => a * d + b * c,
    distractorFns: [
      ({ a, d, b, c }) => a * d - b * c,
      ({ a, c, b, d }) => a * c - b * d,
      ({ b, c }) => b * c,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${a} + ${b}i)(${c} + ${d}i) = ${a * c - b * d} + ${a * d + b * c}i\n` +
      `허수부는 ${ans}`,
  },

  // Lv.6: 복소수 나눗셈 (켤레)
  {
    id: 'h1-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-6, 6], b: [-6, 6] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `(${a} + ${b}i)의 켤레복소수의 허수부는?`,
    answerFn: ({ b }) => -b,
    distractorFns: [
      ({ b }) => b,
      ({ a }) => -a,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${a} + ${b}i)의 켤레복소수는 ${a} - ${b}i\n` +
      `허수부는 ${ans}`,
  },
  {
    id: 'h1-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'H1-ALG-07',
    pattern: '',
    paramRanges: { a: [-6, 6], b: [-6, 6] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `(${a} + ${b}i)의 켤레복소수의 실수부는?`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => -a,
      ({ b }) => b,
      ({ b }) => -b,
    ],
    explanationFn: ({ a, b }) =>
      `(${a} + ${b}i)의 켤레복소수는 ${a} - ${b}i\n` +
      `실수부는 ${a}`,
  },

  // Lv.7: 나머지정리 계산
  {
    id: 'h1-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-03',
    pattern: '',
    paramRanges: { a: [-5, 5], b: [-10, 10], c: [1, 5] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b, c }) =>
      `P(x) = x² ${signedStr(a)}x ${signedStr(b)}를 (x-${c})로 나눈 나머지는?`,
    answerFn: ({ a, b, c }) => c * c + a * c + b,
    distractorFns: [
      ({ a, c }) => a * c,
      ({ b, c }) => b + c,
      ({ a, b, c }) => c * c - a * c + b,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `나머지정리: P(${c}) = ${c}² ${signedStr(a)}×${c} ${signedStr(b)}\n` +
      `= ${c * c} ${signedStr(a * c)} ${signedStr(b)} = ${ans}`,
  },

  // Lv.8: 이차방정식 판별식
  {
    id: 'h1-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-08',
    pattern: '',
    paramRanges: { a: [-6, 6], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `x² ${signedStr(a)}x ${signedStr(b)} = 0의 판별식 D값은?`,
    answerFn: ({ a, b }) => a * a - 4 * b,
    distractorFns: [
      ({ a, b }) => a * a + 4 * b,
      ({ a, b }) => 4 * b - a * a,
      ({ a }) => a * a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `판별식 D = a² - 4b = ${a}² - 4×${signedStr(b)}\n` +
      `= ${a * a} - ${4 * b} = ${ans}`,
  },

  // Lv.9: 연립부등식 계산
  {
    id: 'h1-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-12',
    pattern: '',
    paramRanges: { a: [1, 10], b: [5, 20] },
    constraints: ({ a, b }) => b > a + 1,
    contentFn: ({ a, b }) =>
      `x > ${a}이고 x < ${b}일 때 정수 x의 개수는?`,
    answerFn: ({ a, b }) => Math.max(0, b - a - 1),
    distractorFns: [
      ({ a, b }) => b - a,
      ({ a, b }) => b - a + 1,
      ({ a, b }) => b - a - 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} < x < ${b}를 만족하는 정수 x는 ${a + 1}, ${a + 2}, ..., ${b - 1}\n` +
      `개수는 ${ans}개`,
  },

  // Lv.10: 절대값 방정식
  {
    id: 'h1-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-13',
    pattern: '',
    paramRanges: { a: [-5, 5], b: [1, 8] },
    constraints: ({ a }) => a !== 0,
    contentFn: ({ a, b }) =>
      `|x - ${signedStr(a)}| = ${b}의 두 근의 합은?`,
    answerFn: ({ a }) => 2 * a,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a - b,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `|x - ${signedStr(a)}| = ${b}\n` +
      `x - ${signedStr(a)} = ±${b}\n` +
      `x = ${a + b} 또는 x = ${a - b}\n` +
      `두 근의 합 = ${a + b} + ${a - b} = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const conc: QuestionTemplate[] = [
  // Lv.1: 집합의 뜻과 표현
  {
    id: 'h1-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'data' as ProblemPart,
    conceptId: 'H1-STA-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '원소가 1, 2, 3인 집합의 원소 개수는?',
        '공집합의 원소 개수는?',
        '집합 {x | x는 10 이하의 자연수}의 원소 개수는?',
        '집합 A = {1, 2, 3, 4, 5}에서 3은 집합 A의 무엇인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = [3, 0, 10, '원소']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => [4, 1, 9, '부분집합'][variant]!,
      ({ variant }) => [2, -1, 11, '집합'][variant]!,
      ({ variant }) => [1, 2, 5, '교집합'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '집합 {1, 2, 3}의 원소는 1, 2, 3으로 3개입니다.',
        '공집합 ∅는 원소가 하나도 없으므로 원소 개수는 0입니다.',
        '10 이하의 자연수는 1, 2, 3, ..., 10으로 10개입니다.',
        '집합에 속하는 대상 하나하나를 그 집합의 원소라고 합니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.2: 부분집합 · 교집합 · 합집합
  {
    id: 'h1-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'data' as ProblemPart,
    conceptId: 'H1-STA-03',
    pattern: '',
    paramRanges: { n: [1, 5] },
    contentFn: ({ n }) =>
      `원소가 ${n}개인 집합의 부분집합의 개수는?`,
    answerFn: ({ n }) => Math.pow(2, n),
    distractorFns: [
      ({ n }) => n,
      ({ n }) => n * 2,
      ({ n }) => Math.pow(2, n) - 1,
    ],
    explanationFn: ({ n }, ans) =>
      `원소가 n개인 집합의 부분집합 개수는 2^n\n` +
      `2^${n} = ${ans}`,
  },
  {
    id: 'h1-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'data' as ProblemPart,
    conceptId: 'H1-STA-03',
    pattern: '',
    paramRanges: { a: [1, 5], b: [1, 5] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) =>
      `집합 A = {1, 2, ${a}}, B = {2, ${b}, 5}일 때 A ∩ B의 원소 개수는?`,
    answerFn: ({ a, b }) => {
      const set1 = new Set([1, 2, a])
      const set2 = new Set([2, b, 5])
      let count = 0
      for (const x of set1) {
        if (set2.has(x)) count++
      }
      return count
    },
    distractorFns: [
      () => 0,
      () => 1,
      () => 2,
      () => 3,
    ],
    explanationFn: ({ a, b }, ans) => {
      const set1 = [1, 2, a]
      const set2 = [2, b, 5]
      const intersection: number[] = []
      for (const x of set1) {
        if (set2.includes(x)) intersection.push(x)
      }
      return `A ∩ B = {${intersection.join(', ')}}이므로 원소 개수는 ${ans}개`
    },
  },

  // Lv.3: 명제와 조건
  {
    id: 'h1-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'data' as ProblemPart,
    conceptId: 'H1-STA-05',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '명제 "p → q"의 대우는?',
        '명제 "p → q"의 역은?',
        '명제 "p → q"의 이는?',
        '원명제가 거짓이면 대우는?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['~q → ~p', 'q → p', '~p → ~q', '거짓']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['q → p', '~q → ~p', 'p → q', '참'][variant]!,
      ({ variant }) => ['~p → ~q', 'p → q', 'q → p', '알 수 없다'][variant]!,
      ({ variant }) => ['p → q', '~p → ~q', '~q → ~p', '거짓'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '명제 p → q의 대우는 ~q → ~p입니다.',
        '명제 p → q의 역은 q → p입니다.',
        '명제 p → q의 이는 ~p → ~q입니다.',
        '원명제와 대우는 진리값이 항상 같습니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.4: 필요조건 · 충분조건
  {
    id: 'h1-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'data' as ProblemPart,
    conceptId: 'H1-STA-07',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        'p → q가 참일 때, p는 q의 무엇인가?',
        'p → q가 참일 때, q는 p의 무엇인가?',
        'p → q이고 q → p이면 p와 q의 관계는?',
        'x = 2이면 x² = 4이다. x = 2는 x² = 4의 무엇인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['충분조건', '필요조건', '필요충분조건', '충분조건']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['필요조건', '충분조건', '충분조건', '필요조건'][variant]!,
      ({ variant }) => ['필요충분조건', '필요충분조건', '필요조건', '필요충분조건'][variant]!,
      ({ variant }) => ['무관', '무관', '역', '무관'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        'p → q가 참이면 p는 q의 충분조건입니다.',
        'p → q가 참이면 q는 p의 필요조건입니다.',
        'p → q이고 q → p이면 p와 q는 필요충분조건 관계입니다.',
        'x = 2이면 x² = 4이므로 x = 2는 x² = 4의 충분조건입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.5: 이차부등식
  {
    id: 'h1-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-11',
    pattern: '',
    paramRanges: { a: [1, 6], b: [2, 8] },
    constraints: ({ a, b }) => b > a,
    contentFn: ({ a, b }) =>
      `x² - ${a + b}x + ${a * b} < 0의 해가 ${a} < x < ${b}일 때, 두 근의 합은?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => b - a,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x² - ${a + b}x + ${a * b} = (x - ${a})(x - ${b})\n` +
      `해가 ${a} < x < ${b}이므로 두 근은 ${a}, ${b}\n` +
      `합은 ${ans}`,
  },

  // Lv.6: 이차함수 최대 · 최소
  {
    id: 'h1-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'H1-ALG-14',
    pattern: '',
    paramRanges: { a: [-5, 5], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `y = (x - ${signedStr(a)})² ${signedStr(b)}의 최솟값은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => a + b,
      ({ b }) => -b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `이차함수 y = (x - ${signedStr(a)})² ${signedStr(b)}는\n` +
      `꼭짓점이 (${a}, ${b})이고 아래로 볼록이므로\n` +
      `최솟값은 ${ans}`,
  },

  // Lv.7: 절대값 함수 그래프
  {
    id: 'h1-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func' as ProblemPart,
    conceptId: 'H1-ALG-13',
    pattern: '',
    paramRanges: { a: [-6, 6], b: [-10, 10] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `y = |x - ${signedStr(a)}| ${signedStr(b)}의 최솟값은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ a }) => a,
      ({ a, b }) => Math.abs(a) + b,
      ({ b }) => -b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `|x - ${signedStr(a)}| ≥ 0이므로\n` +
      `y = |x - ${signedStr(a)}| ${signedStr(b)}의 최솟값은\n` +
      `x = ${a}일 때 ${ans}`,
  },

  // Lv.8: 방정식 · 부등식의 활용
  {
    id: 'h1-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'word' as ProblemPart,
    conceptId: 'H1-ALG-11',
    pattern: '',
    paramRanges: { a: [1, 10] },
    contentFn: ({ a }) =>
      `연속하는 두 정수의 곱이 ${a * (a + 1)}이다. 두 수의 합은?`,
    answerFn: ({ a }) => 2 * a + 1,
    distractorFns: [
      ({ a }) => a * (a + 1),
      ({ a }) => 2 * a,
      ({ a }) => a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `연속하는 두 정수를 n, n+1이라 하면\n` +
      `n(n+1) = ${a * (a + 1)}\n` +
      `n = ${a}, n+1 = ${a + 1}\n` +
      `합 = ${a} + ${a + 1} = ${ans}`,
  },

  // Lv.9: 복소수와 이차방정식 관계
  {
    id: 'h1-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-08',
    pattern: '',
    paramRanges: { a: [-8, 8], b: [-15, 15] },
    constraints: ({ a, b }) => a !== 0 && b !== 0,
    contentFn: ({ a, b }) =>
      `x² ${signedStr(a)}x ${signedStr(b)} = 0에서 근과 계수의 관계로 두 근의 합은?`,
    answerFn: ({ a }) => -a,
    distractorFns: [
      ({ a }) => a,
      ({ b }) => b,
      ({ b }) => -b,
    ],
    explanationFn: (_params, ans) =>
      `이차방정식 x² + px + q = 0의 두 근의 합은 -p\n` +
      `따라서 두 근의 합 = ${ans}`,
  },

  // Lv.10: 종합 응용
  {
    id: 'h1-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'H1-ALG-16',
    pattern: '',
    paramRanges: { a: [-8, 8], b: [-10, 10] },
    constraints: ({ a }) => a !== 0 && a % 2 === 0,
    contentFn: ({ a, b }) =>
      `이차함수 y = x² ${signedStr(a)}x ${signedStr(b)}의 꼭짓점 x좌표는?`,
    answerFn: ({ a }) => -a / 2,
    distractorFns: [
      ({ a }) => a / 2,
      ({ a }) => -a,
      ({ b }) => b,
    ],
    explanationFn: ({ a }, ans) =>
      `y = x² ${signedStr(a)}x + ...의 꼭짓점 x좌표는\n` +
      `x = -a/2 = ${signedStr(-a)}/2 = ${ans}`,
  },
]

export const high1Templates: QuestionTemplate[] = [...comp, ...conc]
