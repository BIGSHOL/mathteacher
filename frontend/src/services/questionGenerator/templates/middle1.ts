// 중1 (middle_1) 연산 + 개념 템플릿 Lv.1~10

import type { QuestionTemplate } from '../types'
import { signedStr } from '../utils/math'

const G = 'middle_1' as const

// ============================
// 연산(computation) Lv.1~10
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 양의 정수 덧셈
  {
    id: 'm1-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '{a} + {b}',
    paramRanges: { a: [1, 20], b: [1, 20] },
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a - b,
      (_, ans) => (ans as number) + 1,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) => `${a} + ${b} = ${ans}`,
  },
  {
    id: 'm1-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '{a} + {b} + {c}',
    paramRanges: { a: [1, 10], b: [1, 10], c: [1, 10] },
    answerFn: ({ a, b, c }) => a + b + c,
    distractorFns: [
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) + 2,
      (_, ans) => (ans as number) - 2,
    ],
    explanationFn: ({ a, b, c }, ans) => `${a} + ${b} + ${c} = ${ans}`,
  },

  // Lv.2: 양의 정수 뺄셈
  {
    id: 'm1-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '{a} - {b}',
    paramRanges: { a: [5, 30], b: [1, 29] },
    constraints: ({ a, b }) => a > b,
    answerFn: ({ a, b }) => a - b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => b - a,
      (_, ans) => (ans as number) + 1,
    ],
    explanationFn: ({ a, b }, ans) => `${a} - ${b} = ${ans}`,
  },

  // Lv.3: 음수 포함 덧셈
  {
    id: 'm1-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) + ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a + b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => -(a + b),
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${-a}) + ${b} = ${b} - ${a} = ${ans}`,
  },
  {
    id: 'm1-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `${a} + (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => a + (-b),
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => -(a - b),
      (_, ans) => (ans as number) - 2,
    ],
    explanationFn: ({ a, b }, ans) =>
      `${a} + (${-b}) = ${a} - ${b} = ${ans}`,
  },

  // Lv.4: 음수 뺄셈
  {
    id: 'm1-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) - (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => -a - (-b),
    distractorFns: [
      ({ a, b }) => -(a + b),
      ({ a, b }) => a - b,
      ({ a, b }) => -(a - b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${-a}) - (${-b}) = -${a} + ${b} = ${ans}`,
  },
  {
    id: 'm1-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [1, 15], b: [1, 15] },
    contentFn: ({ a, b }) => `(${-a}) - ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a - b,
    distractorFns: [
      ({ a, b }) => -a + b,
      ({ a, b }) => a - b,
      ({ a, b }) => a + b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${-a}) - ${b} = -(${a} + ${b}) = ${ans}`,
  },

  // Lv.5: 정수 곱셈
  {
    id: 'm1-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-a}) × ${b} 의 값은?`,
    answerFn: ({ a, b }) => -a * b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => -(a + b),
      (_, ans) => (ans as number) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${-a}) × ${b} = -(${a} × ${b}) = ${ans}`,
  },
  {
    id: 'm1-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-a}) × (${-b}) 의 값은?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => -(a * b),
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `(${-a}) × (${-b}) = ${a} × ${b} = ${ans} (음수 × 음수 = 양수)`,
  },

  // Lv.6: 정수 나눗셈
  {
    id: 'm1-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-(a * b)}) ÷ ${a} 의 값은?`,
    answerFn: ({ b }) => -b,
    distractorFns: [
      ({ b }) => b,
      ({ a, b }) => -(a * b),
      ({ a }) => -a,
    ],
    explanationFn: ({ a, b }) =>
      `(${-(a * b)}) ÷ ${a} = ${-b}`,
  },
  {
    id: 'm1-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: ({ a, b }) => `(${-(a * b)}) ÷ (${-a}) 의 값은?`,
    answerFn: ({ b }) => b,
    distractorFns: [
      ({ b }) => -b,
      ({ a, b }) => a * b,
      ({ a }) => a,
    ],
    explanationFn: ({ a, b }) =>
      `(${-(a * b)}) ÷ (${-a}) = ${b} (음수 ÷ 음수 = 양수)`,
  },

  // Lv.7: 정수 혼합 연산
  {
    id: 'm1-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 7], b: [2, 7], c: [-10, 10] },
    constraints: ({ c }) => c !== 0,
    contentFn: ({ a, b, c }) =>
      `(${-a}) × (${-b}) + ${signedStr(c)} 의 값은?`,
    answerFn: ({ a, b, c }) => a * b + c,
    distractorFns: [
      ({ a, b, c }) => -(a * b) + c,
      ({ a, b, c }) => a * b - c,
      ({ a, b }) => a * b,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `(${-a}) × (${-b}) + ${signedStr(c)} = ${a * b} + ${signedStr(c)} = ${ans}`,
  },
  {
    id: 'm1-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc',
    conceptId: 'M1-NUM-05',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6], c: [2, 6] },
    contentFn: ({ a, b, c }) =>
      `${a} × (${-b}) - (${-c}) 의 값은?`,
    answerFn: ({ a, b, c }) => a * (-b) - (-c),
    distractorFns: [
      ({ a, b, c }) => a * (-b) + (-c),
      ({ a, b, c }) => a * b + c,
      ({ a, b, c }) => -(a * b + c),
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a} × (${-b}) - (${-c}) = ${-a * b} + ${c} = ${ans}`,
  },

  // Lv.8: 유리수 덧뺄셈
  {
    id: 'm1-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc',
    conceptId: 'M1-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a < b && c < d && (a * d + c * b) % (b * d) !== 0,
    contentFn: ({ a, b, c, d }) => `${a}/${b} + ${c}/${d} 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = a * d + c * b
      const den = b * d
      const g = gcdHelper(Math.abs(num), den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => `${a + c}/${b + d}`,
      ({ a, b, c, d }) => `${a * d - c * b}/${b * d}`,
      ({ a, c }) => `${a + c}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `${a}/${b} + ${c}/${d} = ${a * d}/${b * d} + ${c * b}/${b * d} = ${ans}`,
  },

  // Lv.9: 유리수 곱셈·나눗셈
  {
    id: 'm1-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc',
    conceptId: 'M1-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6], c: [1, 5], d: [2, 6] },
    constraints: ({ a, b, c, d }) => a !== b && c !== d,
    contentFn: ({ a, b, c, d }) =>
      `(${-a}/${b}) × (${c}/${d}) 의 값은?`,
    answerFn: ({ a, b, c, d }) => {
      const num = -(a * c)
      const den = b * d
      const g = gcdHelper(Math.abs(num), den)
      return `${num / g}/${den / g}`
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const num = a * c
        const den = b * d
        const g = gcdHelper(num, den)
        return `${num / g}/${den / g}`
      },
      ({ a, b, c, d }) => `${a * c}/${b + d}`,
      ({ a, b }) => `${-a}/${b}`,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `(${-a}/${b}) × (${c}/${d}) = -(${a}×${c})/(${b}×${d}) = ${ans}`,
  },

  // Lv.10: 유리수 복합 연산
  {
    id: 'm1-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc',
    conceptId: 'M1-NUM-07',
    pattern: '',
    paramRanges: { a: [1, 4], b: [2, 5], c: [1, 4], d: [2, 5], e: [-5, 5] },
    constraints: ({ a, b, c, d, e }) => c !== 0 && d !== 0 && e !== 0 && a < b && c < d,
    contentFn: ({ a, b, c, d, e }) =>
      `(${-a}/${b}) ÷ (${c}/${d}) + ${signedStr(e)} 의 값은?`,
    answerFn: ({ a, b, c, d, e }) => {
      // (-a/b) ÷ (c/d) = (-a/b) × (d/c) = -ad/(bc)
      const num = -a * d
      const den = b * c
      const g = gcdHelper(Math.abs(num), Math.abs(den))
      const rNum = num / g
      const rDen = den / g
      // + e = (rNum + e * rDen) / rDen
      const finalNum = rNum + e * rDen
      const finalDen = rDen
      if (finalNum % finalDen === 0) return finalNum / finalDen
      const g2 = gcdHelper(Math.abs(finalNum), Math.abs(finalDen))
      return `${finalNum / g2}/${finalDen / g2}`
    },
    distractorFns: [
      ({ a, b, c, d, e }) => {
        const val = (a * d) / (b * c) + e
        return Math.round(val * 10) / 10
      },
      ({ e }) => e,
      (_, ans) => {
        const n = typeof ans === 'number' ? ans : 0
        return n + 1
      },
    ],
    explanationFn: ({ a, b, c, d, e }, ans) =>
      `(${-a}/${b}) ÷ (${c}/${d}) + ${signedStr(e)} = (${-a}/${b}) × (${d}/${c}) + ${signedStr(e)} = ${ans}`,
  },
]

// ============================
// 개념(concept) Lv.1~10
// ============================

const concept: QuestionTemplate[] = [
  // Lv.1: 용어 확인
  {
    id: 'm1-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc',
    conceptId: 'M1-NUM-02',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '양의 정수, 0, 음의 정수를 통틀어 무엇이라 하는가?',
        '자연수에 0과 음의 정수를 포함한 수의 집합을 무엇이라 하는가?',
        '수직선에서 원점의 오른쪽에 있는 정수를 무엇이라 하는가?',
        '두 수의 절댓값은 같고 부호가 다른 관계를 무엇이라 하는가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['정수', '정수', '양의 정수', '서로 반대']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) =>
        ['유리수', '유리수', '음의 정수', '서로 역수'][variant]!,
      ({ variant }) =>
        ['자연수', '자연수', '자연수', '서로 같다'][variant]!,
      ({ variant }) =>
        ['실수', '실수', '정수', '절댓값'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '양의 정수, 0, 음의 정수를 통틀어 정수라고 합니다.',
        '자연수(양의 정수)에 0과 음의 정수를 합하면 정수의 집합이 됩니다.',
        '수직선에서 원점(0)의 오른쪽에 있는 정수는 양의 정수입니다.',
        '절댓값이 같고 부호가 반대인 두 수는 서로 반대 관계입니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.2: 기본 판별 — 약수 찾기, 수 분류
  {
    id: 'm1-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc',
    conceptId: 'M1-NUM-01',
    pattern: '',
    paramRanges: { n: [6, 30] },
    constraints: ({ n }) => {
      // 약수가 4개 이상인 수만
      let count = 0
      for (let i = 1; i <= n; i++) {
        if (n % i === 0) count++
      }
      return count >= 4
    },
    contentFn: ({ n }) => `${n}의 약수가 아닌 것은?`,
    answerFn: ({ n }) => {
      // n의 약수가 아닌 가장 작은 2 이상의 수
      for (let i = 2; i <= n; i++) {
        if (n % i !== 0) return i
      }
      return n + 1
    },
    distractorFns: [
      () => 1,
      ({ n }) => n,
      ({ n }) => {
        // n의 약수 중 하나
        for (let i = 2; i < n; i++) {
          if (n % i === 0) return i
        }
        return 1
      },
    ],
    explanationFn: ({ n }, ans) => {
      const divisors: number[] = []
      for (let i = 1; i <= n; i++) {
        if (n % i === 0) divisors.push(i)
      }
      return `${n}의 약수는 ${divisors.join(', ')}입니다. ${ans}은(는) ${n}의 약수가 아닙니다.`
    },
  },

  // Lv.3: 단순 방정식 x + a = b
  {
    id: 'm1-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 15], b: [5, 25] },
    constraints: ({ a, b }) => b > a,
    contentFn: ({ a, b }) => `x + ${a} = ${b} 일 때, x의 값은?`,
    answerFn: ({ a, b }) => b - a,
    distractorFns: [
      ({ a, b }) => a + b,
      (_, ans) => (ans as number) + 1,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x + ${a} = ${b}\nx = ${b} - ${a} = ${ans}`,
  },
  {
    id: 'm1-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 10], b: [1, 15] },
    contentFn: ({ a, b }) => `x - ${a} = ${b} 일 때, x의 값은?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => b - a,
      (_, ans) => (ans as number) + 2,
      (_, ans) => (ans as number) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x - ${a} = ${b}\nx = ${b} + ${a} = ${ans}`,
  },

  // Lv.4: 계수 방정식 ax = b
  {
    id: 'm1-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 9], x: [1, 10] },
    contentFn: ({ a, x }) => `${a}x = ${a * x} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x }) => a * x,
      ({ a }) => a,
      ({ x }) => x + 1,
    ],
    explanationFn: ({ a, x }) =>
      `${a}x = ${a * x}\nx = ${a * x} ÷ ${a} = ${x}`,
  },

  // Lv.5: 다단계 방정식 ax - b = c
  {
    id: 'm1-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 6], x: [1, 10], b: [1, 10] },
    contentFn: ({ a, x, b }) =>
      `${a}x - ${b} = ${a * x - b} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x, b }) => a * x - b,
      ({ x }) => x + 1,
      ({ x }) => x - 1,
    ],
    explanationFn: ({ a, x, b }) => {
      const rhs = a * x - b
      return `${a}x - ${b} = ${rhs}\n${a}x = ${rhs} + ${b} = ${rhs + b}\nx = ${rhs + b} ÷ ${a} = ${x}`
    },
  },
  {
    id: 'm1-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 5], x: [1, 8], b: [1, 10] },
    contentFn: ({ a, x, b }) =>
      `${a}x + ${b} = ${a * x + b} 일 때, x의 값은?`,
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ a, x, b }) => a * x + b,
      ({ a }) => a,
      ({ x }) => x * 2,
    ],
    explanationFn: ({ a, x, b }) => {
      const rhs = a * x + b
      return `${a}x + ${b} = ${rhs}\n${a}x = ${rhs} - ${b} = ${a * x}\nx = ${a * x} ÷ ${a} = ${x}`
    },
  },

  // Lv.6: 부등식·좌표 (사분면 판별)
  {
    id: 'm1-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'algebra',
    conceptId: 'M1-ALG-05',
    pattern: '',
    paramRanges: { x: [-10, 10], y: [-10, 10] },
    constraints: ({ x, y }) => x !== 0 && y !== 0,
    contentFn: ({ x, y }) => `점 (${x}, ${y})는 어느 사분면에 있는가?`,
    answerFn: ({ x, y }) => {
      if (x > 0 && y > 0) return '제1사분면'
      if (x < 0 && y > 0) return '제2사분면'
      if (x < 0 && y < 0) return '제3사분면'
      return '제4사분면'
    },
    distractorFns: [
      () => '제1사분면',
      () => '제2사분면',
      () => '제3사분면',
      () => '제4사분면',
    ],
    explanationFn: ({ x, y }, ans) => {
      const xSign = x > 0 ? '양수(+)' : '음수(-)'
      const ySign = y > 0 ? '양수(+)' : '음수(-)'
      return `x좌표가 ${xSign}이고 y좌표가 ${ySign}이면 ${ans}입니다.`
    },
  },
  {
    id: 'm1-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'algebra',
    conceptId: 'M1-ALG-05',
    pattern: '',
    paramRanges: { a: [1, 10], b: [2, 15] },
    constraints: ({ a, b }) => b > a,
    contentFn: ({ a, b }) => `x + ${a} > ${b} 를 만족하는 가장 작은 자연수 x는?`,
    answerFn: ({ a, b }) => b - a + 1,
    distractorFns: [
      ({ a, b }) => b - a,
      ({ a, b }) => b - a + 2,
      ({ a, b }) => b + a,
    ],
    explanationFn: ({ a, b }, ans) =>
      `x + ${a} > ${b}\nx > ${b - a}\n가장 작은 자연수 x = ${ans}`,
  },

  // Lv.7: 함수 기본 (y = ax 대입)
  {
    id: 'm1-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M1-ALG-06',
    pattern: '',
    paramRanges: { a: [2, 8], x: [-5, 5] },
    constraints: ({ x }) => x !== 0,
    contentFn: ({ a, x }) => `y = ${a}x 일 때, x = ${x}이면 y의 값은?`,
    answerFn: ({ a, x }) => a * x,
    distractorFns: [
      ({ a, x }) => a + x,
      ({ a, x }) => -(a * x),
      ({ a }, ans) => (ans as number) + a,
    ],
    explanationFn: ({ a, x }, ans) =>
      `y = ${a}x에 x = ${x}을 대입하면\ny = ${a} × ${signedStr(x)} = ${ans}`,
  },
  {
    id: 'm1-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M1-ALG-06',
    pattern: '',
    paramRanges: { a: [2, 6], b: [-5, 5], x: [-3, 5] },
    constraints: ({ b, x }) => b !== 0 && x !== 0,
    contentFn: ({ a, b, x }) =>
      `y = ${a}x + ${signedStr(b)} 일 때, x = ${x}이면 y의 값은?`,
    answerFn: ({ a, b, x }) => a * x + b,
    distractorFns: [
      ({ a, b, x }) => a * x - b,
      ({ a, x }) => a * x,
      ({ a, b, x }) => a + b + x,
    ],
    explanationFn: ({ a, b, x }, ans) =>
      `y = ${a}×${signedStr(x)} + ${signedStr(b)} = ${a * x} + ${signedStr(b)} = ${ans}`,
  },

  // Lv.8: 복합 방정식 a(x - b) = cx + d
  {
    id: 'm1-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'algebra',
    conceptId: 'M1-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 5], c: [1, 4], x: [-5, 5] },
    constraints: ({ a, c, x }) => a !== c && x !== 0,
    contentFn: ({ a, b, c, x }) => {
      const rhs = c * x + (a * x - a * b - c * x)
      return `${a}(x - ${b}) = ${c}x + ${signedStr(rhs)} 를 풀면 x = ?`
    },
    answerFn: ({ x }) => x,
    distractorFns: [
      ({ x }) => -x,
      ({ x }) => x + 1,
      ({ x }) => x - 1,
    ],
    explanationFn: ({ a, b, c, x }) => {
      const d = a * x - a * b - c * x
      return `${a}(x - ${b}) = ${c}x + ${signedStr(d)}\n` +
        `${a}x - ${a * b} = ${c}x + ${signedStr(d)}\n` +
        `${a}x - ${c}x = ${signedStr(d)} + ${a * b}\n` +
        `${a - c}x = ${d + a * b}\n` +
        `x = ${x}`
    },
  },

  // Lv.9: 문장제
  {
    id: 'm1-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'M1-ALG-04',
    pattern: '',
    paramRanges: { a: [3, 8], total: [20, 50] },
    constraints: ({ a, total }) => total % a === 0,
    contentFn: ({ a, total }) =>
      `어떤 수에 ${a}를 곱하면 ${total}이 됩니다. 어떤 수를 구하시오.`,
    answerFn: ({ a, total }) => total / a,
    distractorFns: [
      ({ a, total }) => total - a,
      ({ a, total }) => total + a,
      ({ a, total }) => a * total,
    ],
    explanationFn: ({ a, total }, ans) =>
      `어떤 수를 x라 하면\n${a}x = ${total}\nx = ${total} ÷ ${a} = ${ans}`,
  },
  {
    id: 'm1-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'word',
    conceptId: 'M1-ALG-04',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 10], total: [15, 40] },
    constraints: ({ a, b, total }) => (total - b) % a === 0 && (total - b) / a > 0,
    contentFn: ({ a, b, total }) =>
      `어떤 수에 ${a}를 곱하고 ${b}를 더하면 ${total}이 됩니다. 어떤 수는?`,
    answerFn: ({ a, b, total }) => (total - b) / a,
    distractorFns: [
      ({ a, b, total }) => (total + b) / a,
      ({ total, b }) => total - b,
      ({ a, total }) => total / a,
    ],
    explanationFn: ({ a, b, total }, ans) =>
      `어떤 수를 x라 하면\n${a}x + ${b} = ${total}\n${a}x = ${total - b}\nx = ${ans}`,
  },

  // Lv.10: 종합 응용 (방정식 + 좌표)
  {
    id: 'm1-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M1-ALG-08',
    pattern: '',
    paramRanges: { a: [2, 5], b: [-5, 5], px: [1, 5] },
    constraints: ({ b }) => b !== 0,
    contentFn: ({ a, b, px }) =>
      `일차함수 y = ${a}x + ${signedStr(b)} 의 그래프가 점 (${px}, k)를 지날 때, k의 값은?`,
    answerFn: ({ a, b, px }) => a * px + b,
    distractorFns: [
      ({ a, b, px }) => a * px - b,
      ({ a, px }) => a * px,
      ({ a, b, px }) => a + b + px,
    ],
    explanationFn: ({ a, b, px }, ans) =>
      `y = ${a}x + ${signedStr(b)}에 x = ${px}을 대입\n` +
      `k = ${a} × ${px} + ${signedStr(b)} = ${a * px} + ${signedStr(b)} = ${ans}`,
  },
  {
    id: 'm1-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M1-ALG-08',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 6], c: [1, 5] },
    constraints: ({ a, b, c }) => {
      // a * x = b + c에서 x가 정수가 되도록
      return (b + c) % a === 0
    },
    contentFn: ({ a, b, c }) =>
      `${a}x - ${b} = ${c} 의 해가 x = p일 때, 점 (p, 2p)가 위치하는 사분면은?`,
    answerFn: ({ a, b, c }) => {
      const x = (b + c) / a
      if (x > 0) return '제1사분면'
      if (x < 0) return '제3사분면'
      return '원점'
    },
    distractorFns: [
      () => '제2사분면',
      () => '제4사분면',
      () => '제3사분면',
    ],
    explanationFn: ({ a, b, c }) => {
      const x = (b + c) / a
      return `${a}x - ${b} = ${c}\n${a}x = ${b + c}\nx = ${x}\n` +
        `점 (${x}, ${2 * x})은 x=${x}, y=${2 * x}이므로 제1사분면`
    },
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

export const middle1Templates: QuestionTemplate[] = [...comp, ...concept]
