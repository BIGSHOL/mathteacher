// 중3 (middle_3) 연산 + 개념 템플릿 Lv.1~10
// Phase A: Curriculum corrections (Lv.8b special angles, Lv.9 inscribed angles)
// Phase B: New templates (곱셈공식, 이차방정식, 특수각, 원주각, 통계, 이차함수, 상관관계)
// Phase C: Improved explanations and distractors

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
    explanationFn: ({ a }, ans) =>
      `제곱근의 정의에 의해\n√${a * a} = √(${a}²) = ${ans}\n\n참고: √(a²) = |a|이지만, 여기서는 a > 0이므로 ${ans}입니다.`,
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
    explanationFn: ({ a }, ans) =>
      `제곱근 ${a * a}는 ±${ans}이지만,\n양의 값만 구하면 √${a * a} = ${ans}`,
  },

  // Lv.2: 근호 간소화
  {
    id: 'm3-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `근호의 성질에 의해\n√${a * a * b} = √(${a}² × ${b}) = ${ans}√${b}\n\n참고: √(a²b) = a√b (a > 0)`,
  },
  {
    id: 'm3-comp-2b',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
    explanationFn: ({ a, b }, ans) =>
      `√${a * a * b} = √(${a}² × ${b}) = ${ans}\n\n근호 안에서 완전제곱수를 찾아 밖으로 꺼냅니다.`,
  },

  // Lv.3: 근호 덧뺄셈
  {
    id: 'm3-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `근호가 같은 항끼리 덧셈\n${a}√${n} + ${b}√${n} = (${a} + ${b})√${n} = ${ans}√${n}\n\n흔한 실수: 근호 안의 값을 더하지 않도록 주의`,
  },
  {
    id: 'm3-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `근호가 같은 항끼리 뺄셈\n${a}√${n} - ${b}√${n} = (${a} - ${b})√${n} = ${ans}`,
  },

  // Lv.4: 근호 곱셈
  {
    id: 'm3-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `근호의 곱셈 공식: √a × √b = √(a × b)\n√${a} × √${b} = √(${a} × ${b}) = √${ans}`,
  },
  {
    id: 'm3-comp-4b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc',
    conceptId: 'M3-NUM-02',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 6], c: [2, 5] },
    contentFn: ({ a, b, c }) => `${a}√${b} × ${c}의 값은?`,
    answerFn: ({ a, b, c }) => `${a * c}√${b}`,
    distractorFns: [
      ({ a, c }) => `${a * c}`,
      ({ a, b, c }) => `${a + c}√${b}`,
      ({ a, b, c }) => `${a}√${b * c}`,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `${a}√${b} × ${c} = ${a} × ${c} × √${b} = ${ans}`,
  },

  // Lv.5: 근호 나눗셈
  {
    id: 'm3-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `근호의 나눗셈: √a ÷ √b = √(a ÷ b)\n√${a * b} ÷ √${a} = √(${a * b} ÷ ${a}) = √${ans}`,
  },
  {
    id: 'm3-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
    explanationFn: ({ a, b, c }, ans) =>
      `${a}√${b} ÷ ${c} = (${a} ÷ ${c})√${b} = ${ans}`,
  },

  // Lv.6: 유리화
  {
    id: 'm3-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `분모의 유리화: 분모·분자에 √${b}를 곱함\n${a}/√${b} = (${a} × √${b})/(√${b} × √${b}) = (${a}√${b})/${ans}\n\n흔한 실수: 분자만 변환하고 분모를 그대로 두지 않도록 주의`,
  },
  {
    id: 'm3-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc',
    conceptId: 'M3-NUM-02',
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
      `분모의 유리화: 분모·분자에 √${b}를 곱함\n${a}/√${b} = (${a} × √${b})/(√${b} × √${b}) = ${ans}/${b}\n\n주의: 분모만 유리화하는 것이 아니라 분자도 함께 변환됩니다.`,
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
      `공통인수로 묶기\n${a}x² + ${b}x = x × ${a}x + x × ${b} = x(${ans}x + ${b})`,
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
      `최대공약수 ${ans}x로 묶기\n${a * c}x² + ${b * c}x = ${ans}x × ${a}x + ${ans}x × ${b} = ${ans}x(${a}x + ${b})`,
  },

  // Lv.8: 인수분해 (x² + bx + c)
  {
    id: 'm3-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      return `x² + bx + c 인수분해: 합이 ${a + b}, 곱이 ${a * b}인 두 수를 찾음\n${min} + ${max} = ${a + b}, ${min} × ${max} = ${a * b}\nx² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
    },
  },
  {
    id: 'm3-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      return `합이 ${a + b}, 곱이 ${a * b}인 두 수: ${min}, ${max}\nx² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
    },
  },

  // Lv.9: 인수분해 (완전제곱식)
  {
    id: 'm3-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      `완전제곱식 공식: (x + a)² = x² + 2ax + a²\nx² + ${2 * a}x + ${a * a} = x² + 2 × ${a} × x + ${a}² = (x + ${ans})²\n\n흔한 실수: 중간 계수를 그대로 사용하지 않고 2로 나눔`,
  },
  {
    id: 'm3-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      `완전제곱식 공식: (x - a)² = x² - 2ax + a²\nx² - ${2 * a}x + ${a * a} = (x - ${ans})²\n\n주의: 부호를 바꾸지 않도록 주의`,
  },

  // Lv.10: 복합 인수분해 (a² - b²)
  {
    id: 'm3-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      `합차 공식: a² - b² = (a + b)(a - b)\nx² - ${a * a} = x² - ${a}² = (x + ${ans})(x - ${ans})`,
  },
  {
    id: 'm3-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-ALG-02',
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
      `합차 공식 응용\n${a * a}x² - ${b * b} = (${a}x)² - ${b}² = (${ans}x + ${b})(${ans}x - ${b})`,
  },

  // ========== Phase B: New computation templates ==========

  // Lv.11: 곱셈 공식 전개
  {
    id: 'm3-comp-11a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra',
    conceptId: 'M3-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `(x + ${a})²를 전개하면 x² + ?x + ${a * a}입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => 2 * a,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a * a,
      ({ a }) => 2 * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `완전제곱식 공식: (x + a)² = x² + 2ax + a²\n(x + ${a})² = x² + 2 × ${a} × x + ${a}² = x² + ${ans}x + ${a * a}`,
  },
  {
    id: 'm3-comp-11b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra',
    conceptId: 'M3-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 8] },
    contentFn: ({ a }) => `(x - ${a})²를 전개하면 x² - ?x + ${a * a}입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => 2 * a,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => -a,
      ({ a }) => -(2 * a),
    ],
    explanationFn: ({ a }, ans) =>
      `완전제곱식 공식: (x - a)² = x² - 2ax + a²\n(x - ${a})² = x² - 2 × ${a} × x + ${a}² = x² - ${ans}x + ${a * a}\n\n흔한 실수: 중간 항의 부호를 반대로 하지 않도록 주의`,
  },
  {
    id: 'm3-comp-12a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra',
    conceptId: 'M3-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 9] },
    contentFn: ({ a }) => `(x + ${a})(x - ${a}) = x² - ?입니다. ?에 들어갈 수는?`,
    answerFn: ({ a }) => a * a,
    distractorFns: [
      ({ a }) => a,
      ({ a }) => 2 * a,
      ({ a }) => a * a + 1,
    ],
    explanationFn: ({ a }, ans) =>
      `합차 공식: (a + b)(a - b) = a² - b²\n(x + ${a})(x - ${a}) = x² - ${a}² = x² - ${ans}`,
  },
  {
    id: 'm3-comp-12b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'algebra',
    conceptId: 'M3-ALG-01',
    pattern: '',
    paramRanges: { a: [1, 6], b: [2, 7] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `(x + ${a})(x + ${b})를 전개할 때 x의 계수는?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a - b,
      ({ a, b }) => 2 * (a + b),
    ],
    explanationFn: ({ a, b }, ans) =>
      `전개 공식: (x + a)(x + b) = x² + (a + b)x + ab\n(x + ${a})(x + ${b}) = x² + (${a} + ${b})x + ${a * b} = x² + ${ans}x + ${a * b}`,
  },

  // Lv.13: 이차방정식 풀이
  {
    id: 'm3-comp-13a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 6] },
    constraints: ({ a, b }) => a !== b && a > 0 && b > 0,
    contentFn: ({ a, b }) => `x² - ${a + b}x + ${a * b} = 0에서 두 근의 합은?`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => -(a + b),
      ({ a, b }) => a * b,
      ({ a, b }) => a - b,
    ],
    explanationFn: ({ a, b }, ans) =>
      `인수분해하면 (x - ${a})(x - ${b}) = 0\nx = ${a} 또는 x = ${b}\n두 근의 합 = ${a} + ${b} = ${ans}\n\n근의 공식에 의해: 두 근의 합 = -b/a = -(-${a + b})/1 = ${ans}`,
  },
  {
    id: 'm3-comp-13b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
    pattern: '',
    paramRanges: { a: [1, 7], b: [1, 16] },
    constraints: ({ b }) => {
      const sqrt = Math.sqrt(b)
      return sqrt === Math.floor(sqrt) && sqrt > 0
    },
    contentFn: ({ a, b }) => `(x - ${a})² = ${b} 형태의 방정식을 풀면 x = ${a} ± ?입니다. ?에 들어갈 수는?`,
    answerFn: ({ b }) => Math.sqrt(b),
    distractorFns: [
      ({ b }) => b,
      ({ b }) => b / 2,
      ({ b }) => Math.sqrt(b) + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `완전제곱식을 이용한 풀이\n(x - ${a})² = ${b}\nx - ${a} = ±√${b} = ±${ans}\nx = ${a} ± ${ans}`,
  },

  // Lv.14: 통계 (분산, 표준편차)
  {
    id: 'm3-comp-14a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'data',
    conceptId: 'M3-STA-01',
    pattern: '',
    paramRanges: { a: [1, 4], b: [1, 4], c: [1, 4], d: [1, 4] },
    constraints: ({ a, b, c, d }) => {
      // 평균이 정수가 되도록
      return (a + b + c + d) % 4 === 0
    },
    contentFn: ({ a, b, c, d }) => {
      const mean = (a + b + c + d) / 4
      return `자료 ${a}, ${b}, ${c}, ${d}의 평균이 ${mean}일 때, 분산은? (각 편차의 제곱: ${(a - mean) ** 2}, ${(b - mean) ** 2}, ${(c - mean) ** 2}, ${(d - mean) ** 2})`
    },
    answerFn: ({ a, b, c, d }) => {
      const mean = (a + b + c + d) / 4
      const variance = ((a - mean) ** 2 + (b - mean) ** 2 + (c - mean) ** 2 + (d - mean) ** 2) / 4
      return variance
    },
    distractorFns: [
      ({ a, b, c, d }) => {
        const mean = (a + b + c + d) / 4
        return (a - mean) ** 2 + (b - mean) ** 2 + (c - mean) ** 2 + (d - mean) ** 2
      },
      ({ a, b, c, d }) => {
        const mean = (a + b + c + d) / 4
        return Math.abs(a - mean) + Math.abs(b - mean) + Math.abs(c - mean) + Math.abs(d - mean)
      },
      ({ a, b, c, d }) => (a + b + c + d) / 4,
    ],
    explanationFn: ({ a, b, c, d }, ans) => {
      const mean = (a + b + c + d) / 4
      const dev = [a, b, c, d].map(x => x - mean)
      return `1단계: 평균 계산 = (${a} + ${b} + ${c} + ${d}) / 4 = ${mean}\n` +
        `2단계: 편차 계산 = [${dev.join(', ')}]\n` +
        `3단계: 편차 제곱 = [${dev.map(x => x ** 2).join(', ')}]\n` +
        `4단계: 분산 = 편차 제곱의 평균 = ${ans}\n\n` +
        `흔한 실수: 편차의 합을 구하지 않고 편차 제곱의 평균을 구해야 함`
    },
  },
  {
    id: 'm3-comp-14b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'data',
    conceptId: 'M3-STA-01',
    pattern: '',
    paramRanges: { a: [1, 16] },
    constraints: ({ a }) => {
      const sqrt = Math.sqrt(a)
      return sqrt === Math.floor(sqrt)
    },
    contentFn: ({ a }) => `어떤 자료의 분산이 ${a}일 때, 표준편차는?`,
    answerFn: ({ a }) => Math.sqrt(a),
    distractorFns: [
      ({ a }) => a,
      ({ a }) => a / 2,
      ({ a }) => a * 2,
    ],
    explanationFn: ({ a }, ans) =>
      `표준편차 = √(분산)\n표준편차 = √${a} = ${ans}`,
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
      `제곱근의 정의: a² = b일 때, a를 b의 제곱근이라 함\n${ans}² = ${a}이므로 제곱근 ${a}의 양수는 ${ans}입니다.`,
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
      `${a}의 제곱근은 ±${ans}입니다.\n절댓값은 양수이므로 ${ans}입니다.`,
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
      `무리수의 정의: 분수로 나타낼 수 없는 무한소수\n${ans}는 제곱근이 정수가 아닌 무리수입니다.\n\n참고: √4 = 2 (유리수), 0.333... = 1/3 (유리수), 22/7 (유리수)`,
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
      `√${a}는 완전제곱수가 아니므로 ${ans}입니다.`,
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
      return `인수분해: 다항식을 인수의 곱으로 나타내기\n합이 ${a + b}, 곱이 ${a * b}인 두 수: ${min}, ${max}\nx² + ${a + b}x + ${a * b} = (x + ${min})(x + ${max})`
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
    conceptId: 'M3-ALG-03',
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
      return `인수분해하면\nx² - ${a + b}x + ${a * b} = (x - ${a})(x - ${b}) = 0\nx = ${a} 또는 x = ${b}\n두 근의 합 = ${a} + ${b} = ${ans}`
    },
  },
  {
    id: 'm3-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
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
      `(x - ${a})(x - ${b}) = 0의 두 근은 ${a}, ${b}\n두 근의 곱 = ${a} × ${b} = ${ans}\n\n근의 공식에 의해: 두 근의 곱 = c/a`,
  },

  // Lv.5: 이차방정식 (근의 공식)
  {
    id: 'm3-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
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
      `근의 공식에 의해 판별식 D = b² - 4ac\nax² + bx + c = 0에서 a = 1, b = ${b}, c = ${c}\nD = ${b}² - 4 × 1 × ${c} = ${b * b} - ${4 * c} = ${ans}\n\n흔한 실수: -4ac의 부호를 잘못 계산하지 않도록 주의`,
  },
  {
    id: 'm3-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'algebra',
    conceptId: 'M3-ALG-03',
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
      `판별식 D = b² - 4ac\nD = ${b}² - 4 × ${a} × ${c} = ${b * b} - ${4 * a * c} = ${ans}\n\n판별식의 의미: D > 0 (서로 다른 두 실근), D = 0 (중근), D < 0 (실근 없음)`,
  },

  // Lv.6: 이차함수 y = ax²
  {
    id: 'm3-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func',
    conceptId: 'M3-FUNC-01',
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
      `이차함수의 함숫값 계산\ny = ${a} × (${b})² = ${a} × ${b * b} = ${ans}`,
  },
  {
    id: 'm3-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func',
    conceptId: 'M3-FUNC-01',
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
      `y = ${a} × (${b})² = ${a} × ${b * b} = ${ans}\n\n주의: 음수를 제곱하면 양수가 됨`,
  },

  // Lv.7: 이차함수 그래프 (꼭짓점, 축)
  {
    id: 'm3-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M3-FUNC-01',
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
      `이차함수의 표준형: y = a(x - p)² + q\n꼭짓점은 (p, q)이므로 x좌표는 p = ${b}\n\n주의: (x - p) 형태에서 부호를 바꾸면 p입니다.`,
  },
  {
    id: 'm3-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'func',
    conceptId: 'M3-FUNC-01',
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
      `이차함수의 축은 꼭짓점을 지나는 수직선\n축의 방정식: x = ${b}`,
    questionType: 'multiple_choice',
  },

  // ========== Phase A: Curriculum corrections ==========

  // Lv.8: 삼각비 (Phase A1 - improved explanation for 3,4,5 triangle)
  {
    id: 'm3-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'M3-GEO-01',
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
        '삼각비의 정의: sin θ = 높이/빗변\nsin θ = 3/5\n\n흔한 실수: 분자와 분모를 반대로 쓰지 않도록 주의',
        'cos θ = 밑변/빗변\ncos θ = 4/5',
        'tan θ = 높이/밑변\ntan θ = 3/4 = sin θ / cos θ',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.8b: 특수각 삼각비 (Phase A1 - NEW special angles)
  {
    id: 'm3-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'M3-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 8] },
    contentFn: ({ variant }) => {
      const questions = [
        'sin 30°의 값은?',
        'sin 45°의 값은?',
        'sin 60°의 값은?',
        'cos 30°의 값은?',
        'cos 45°의 값은?',
        'cos 60°의 값은?',
        'tan 30°의 값은?',
        'tan 45°의 값은?',
        'tan 60°의 값은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['1/2', '√2/2', '√3/2', '√3/2', '√2/2', '1/2', '√3/3', '1', '√3']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['√3/2', '1/2', '1/2', '1/2', '√3/2', '√3/2', '1', '√3/3', '√3/2'][variant]!,
      ({ variant }) => ['1', '√3/2', '√2/2', '√2/2', '1/2', '√2/2', '√3', '√3', '1'][variant]!,
      ({ variant }) => ['√2/2', '1', '1', '1', '1', '1', '√2/2', '√2/2', '√2/2'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '특수각 30°의 삼각비\nsin 30° = 1/2\n(1:2:√3 삼각형에서 높이/빗변)',
        '특수각 45°의 삼각비\nsin 45° = √2/2\n(1:1:√2 직각이등변삼각형)',
        'sin 60° = √3/2\n(1:2:√3 삼각형)',
        'cos 30° = √3/2\n(밑변/빗변)',
        'cos 45° = √2/2\n(직각이등변삼각형)',
        'cos 60° = 1/2\n\n참고: sin 30° = cos 60°',
        'tan 30° = √3/3 = 1/√3\n(높이/밑변)',
        'tan 45° = 1\n(높이 = 밑변)',
        'tan 60° = √3\n\n참고: tan 60° = sin 60° / cos 60° = (√3/2) / (1/2) = √3',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.9: 원주각 (Phase A2 - REPLACED 원의 접선 with 원주각)
  {
    id: 'm3-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo',
    conceptId: 'M3-GEO-02',
    pattern: '',
    paramRanges: { a: [20, 140], variant: [0, 1] },
    constraints: ({ a }) => a % 10 === 0 && a !== 90,
    contentFn: ({ a, variant }) => {
      if (variant === 0) {
        return `원에서 중심각이 ${a}°일 때, 같은 호에 대한 원주각은 몇 도인가?`
      } else {
        return `원에서 원주각이 ${a}°일 때, 같은 호에 대한 중심각은 몇 도인가?`
      }
    },
    answerFn: ({ a, variant }) => {
      if (variant === 0) return a / 2
      return 2 * a
    },
    distractorFns: [
      ({ a, variant }) => variant === 0 ? a : a / 2,
      ({ a, variant }) => variant === 0 ? a * 2 : a * 4,
      ({ a, variant }) => variant === 0 ? a - 10 : a + 10,
    ],
    explanationFn: ({ a, variant }, ans) => {
      if (variant === 0) {
        return `원주각의 정리: 원주각은 같은 호에 대한 중심각의 절반\n원주각 = 중심각 / 2 = ${a}° / 2 = ${ans}°`
      } else {
        return `원주각의 정리: 중심각은 같은 호에 대한 원주각의 2배\n중심각 = 원주각 × 2 = ${a}° × 2 = ${ans}°`
      }
    },
  },

  // Lv.9b: 반원에 대한 원주각 (Phase A2)
  {
    id: 'm3-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo',
    conceptId: 'M3-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '원에서 지름에 대한 원주각의 크기는?',
        '반원에 대한 원주각은 몇 도인가?',
        '원에서 중심각이 180°일 때 원주각은?',
      ]
      return questions[variant]!
    },
    answerFn: () => 90,
    distractorFns: [
      () => 180,
      () => 45,
      () => 60,
    ],
    explanationFn: (_, ans) =>
      `반원에 대한 원주각의 정리\n반원(지름)에 대한 원주각 = ${ans}° (직각)\n\n증명: 중심각 180°의 절반 = 90°`,
    questionType: 'multiple_choice',
  },

  // Lv.10: 복합 응용
  {
    id: 'm3-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-FUNC-01',
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
      `이차함수의 최댓값/최솟값\ny = ${a}(x - ${b})² + ${signedStr(c)}는 a = ${a} > 0이므로 아래로 볼록한 포물선\n꼭짓점 (${b}, ${c})에서 최솟값 = ${ans}`,
  },
  {
    id: 'm3-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'algebra',
    conceptId: 'M3-FUNC-01',
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
      `y = ${a}(x - ${b})² + ${signedStr(c)}는 a = ${a} < 0이므로 위로 볼록한 포물선\n꼭짓점 (${b}, ${c})에서 최댓값 = ${ans}`,
  },

  // ========== Phase B: New concept templates ==========

  // Lv.11: 특수각 삼각비 혼합 (Phase B3)
  {
    id: 'm3-conc-11a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo',
    conceptId: 'M3-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        'sin 30° + cos 60°의 값은?',
        'sin 45° × cos 45°의 값은?',
        'sin 60° × cos 30°의 값은?',
        'tan 30° × tan 60°의 값은?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['1', '1/2', '3/4', '1']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['1/2', '1', '√3/2', '√3'][variant]!,
      ({ variant }) => ['√3/2', '√2', '1/2', '√3/3'][variant]!,
      ({ variant }) => ['√3', '√2/2', '1', '3'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        'sin 30° = 1/2, cos 60° = 1/2\nsin 30° + cos 60° = 1/2 + 1/2 = 1\n\n참고: sin 30° = cos 60° (여각 관계)',
        'sin 45° = √2/2, cos 45° = √2/2\nsin 45° × cos 45° = (√2/2) × (√2/2) = 2/4 = 1/2',
        'sin 60° = √3/2, cos 30° = √3/2\nsin 60° × cos 30° = (√3/2) × (√3/2) = 3/4',
        'tan 30° = √3/3, tan 60° = √3\ntan 30° × tan 60° = (√3/3) × √3 = 3/3 = 1',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // Lv.12: 원주각 개념 (Phase B4)
  {
    id: 'm3-conc-12a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo',
    conceptId: 'M3-GEO-02',
    pattern: '',
    paramRanges: { a: [30, 80], variant: [0, 2] },
    constraints: ({ a }) => a % 10 === 0,
    contentFn: ({ a, variant }) => {
      const questions = [
        `원에서 같은 호 AB에 대한 원주각이 ${a}°일 때, 다른 점에서 본 호 AB에 대한 원주각은?`,
        `원에서 호 AB에 대한 원주각 ∠ACB = ${a}°일 때, 같은 호에 대한 원주각 ∠ADB는?`,
        `원 위의 서로 다른 두 점에서 같은 호를 보는 원주각이 각각 ${a}°와 x°일 때, x의 값은?`,
      ]
      return questions[variant]!
    },
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => 2 * a,
      ({ a }) => a / 2,
      ({ a }) => 180 - a,
    ],
    explanationFn: ({ a }) =>
      `같은 호에 대한 원주각의 정리\n같은 호에 대한 원주각의 크기는 모두 같습니다.\n따라서 답은 ${a}°`,
  },

  // Lv.13: 이차함수 일반형→표준형 (Phase B6)
  {
    id: 'm3-conc-13a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'func',
    conceptId: 'M3-FUNC-01',
    pattern: '',
    paramRanges: { a: [1, 3], b: [2, 10], c: [1, 15] },
    constraints: ({ b }) => b % 2 === 0,
    contentFn: ({ a, b, c }) => `이차함수 y = ${a}x² + ${b}x + ${c}의 꼭짓점의 x좌표는?`,
    answerFn: ({ b, a }) => -(b / (2 * a)),
    distractorFns: [
      ({ b, a }) => b / (2 * a),
      ({ b }) => -b,
      ({ b }) => b,
    ],
    explanationFn: ({ a, b }) =>
      `일반형 y = ax² + bx + c에서 꼭짓점의 x좌표 공식\nx = -b/(2a) = -${b}/(2 × ${a}) = ${-(b / (2 * a))}\n\n이후 y좌표를 구하려면 이 x값을 대입하면 됩니다.`,
  },

  // Lv.14: 상관관계 (Phase B7)
  {
    id: 'm3-conc-14a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'data',
    conceptId: 'M3-STA-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        'x의 값이 증가할 때 y의 값도 증가하는 경향이 있으면 무슨 상관관계인가?',
        'x의 값이 증가할 때 y의 값은 감소하는 경향이 있으면 무슨 상관관계인가?',
        'x와 y 사이에 뚜렷한 경향이 없으면 무슨 상관관계인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['양의 상관관계', '음의 상관관계', '상관관계 없음']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => ['음의 상관관계', '양의 상관관계', '양의 상관관계'][variant]!,
      ({ variant }) => ['상관관계 없음', '상관관계 없음', '음의 상관관계'][variant]!,
      ({ variant }) => ['역의 상관관계', '정비례', '반비례'][variant]!,
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '양의 상관관계: x가 증가하면 y도 증가하는 경향\n예: 공부 시간과 성적',
        '음의 상관관계: x가 증가하면 y는 감소하는 경향\n예: 결석 일수와 성적',
        '상관관계 없음: x와 y 사이에 뚜렷한 관계가 없음\n예: 키와 성적',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },
]

export const middle3Templates: QuestionTemplate[] = [...comp, ...conc]
