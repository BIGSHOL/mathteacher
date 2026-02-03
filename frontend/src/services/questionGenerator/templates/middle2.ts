// 중2 (middle_2) 연산 + 개념 템플릿 Lv.1~10 + 추가 템플릿
// Phase A: 교육과정 정합성 수정 (중3 내용 제거, 중2 내용으로 대체)
// Phase B: 신규 템플릿 18개 추가
// Phase C: 해설 및 오답 개선

import type { QuestionTemplate } from '../types'
import type { ProblemPart } from '../../../types'
import { signedStr } from '../utils/math'

const G = 'middle_2' as const

// ============================
// 연산(computation) Lv.1~10 + 추가
// ============================

const comp: QuestionTemplate[] = [
  // Lv.1: 단항식 × 단항식
  {
    id: 'm2-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-01',
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
      `단항식의 곱셈에서 지수법칙 a^m × a^n = a^(m+n)을 사용합니다.\n` +
      `${a}x^${b} × ${c}x^${d} = (${a} × ${c})x^${b + d} = ${ans}x^${b + d}\n` +
      `계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-01',
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
      `지수법칙에 의해 x^${b} × x^${d} = x^${b + d}입니다.\n` +
      `${a}x^${b} × ${c}x^${d} = ${a * c}x^${ans}\n` +
      `지수는 ${ans}입니다.\n` +
      `※ 주의: 지수는 더하고, 계수는 곱합니다.`,
  },

  // Lv.2: 단항식 ÷ 단항식
  {
    id: 'm2-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-01',
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
      return `단항식의 나눗셈에서 지수법칙 a^m ÷ a^n = a^(m-n)을 사용합니다.\n` +
        `${coef}x^${exp} ÷ ${c}x^${d} = (${coef} ÷ ${c})x^${exp - d} = ${a}x^${b}\n` +
        `계수는 ${a}입니다.`
    },
  },

  // Lv.3: 다항식 + 다항식
  {
    id: 'm2-comp-3a',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
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
      `다항식의 덧셈은 동류항끼리 모아서 계산합니다.\n` +
      `(${a}x + ${b}) + (${c}x + ${d}) = (${a} + ${c})x + (${b} + ${d}) = ${ans}x + ${b + d}\n` +
      `x의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-3b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
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
      `다항식의 덧셈에서 상수항끼리 더합니다.\n` +
      `(${a}x + ${b}) + (${c}x + ${d}) = ${a + c}x + (${b} + ${d}) = ${a + c}x + ${ans}\n` +
      `상수항은 ${ans}입니다.`,
  },

  // Lv.4: 다항식 - 다항식
  {
    id: 'm2-comp-4a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
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
      `다항식의 뺄셈은 괄호를 풀 때 부호를 바꿔서 계산합니다.\n` +
      `(${a}x + ${b}) - (${c}x + ${d}) = ${a}x + ${b} - ${c}x - ${d}\n` +
      `= (${a} - ${c})x + (${b} - ${d}) = ${ans}x + ${b - d}\n` +
      `x의 계수는 ${ans}입니다.\n` +
      `※ 주의: 괄호 앞의 음수는 괄호 안의 모든 항의 부호를 바꿉니다.`,
  },

  // Lv.5: 단항식 × 다항식
  {
    id: 'm2-comp-5a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
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
      `분배법칙을 사용하여 전개합니다.\n` +
      `${a}(${b}x + ${c}) = ${a} × ${b}x + ${a} × ${c} = ${ans}x + ${a * c}\n` +
      `x의 계수는 ${ans}입니다.`,
  },
  {
    id: 'm2-comp-5b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-02',
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
      `분배법칙으로 괄호를 풉니다.\n` +
      `${a}(${b}x + ${c}) = ${a * b}x + ${a} × ${c} = ${a * b}x + ${ans}\n` +
      `상수항은 ${ans}입니다.`,
  },

  // Lv.6: 일차부등식 풀이 (Phase A 수정: 중3 곱셈공식 제거)
  {
    id: 'm2-comp-6a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 10], c: [5, 20] },
    constraints: ({ a, b, c }) => (c - b) % a === 0 && c > b,
    contentFn: ({ a, b, c }) => `${a}x + ${b} > ${c}를 풀면? (x > ? 형태로 답하시오)`,
    answerFn: ({ a, b, c }) => (c - b) / a,
    distractorFns: [
      ({ a, b, c }) => (c + b) / a,
      ({ a, b, c }) => (c - b) / a + 1,
      ({ a, b, c }) => (c - b) / a - 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `일차부등식을 푸는 단계:\n` +
      `1. 양변에서 ${b}를 빼면: ${a}x > ${c - b}\n` +
      `2. 양변을 ${a}로 나누면: x > ${ans}\n` +
      `※ 양수로 나누면 부등호 방향은 바뀌지 않습니다.`,
  },
  {
    id: 'm2-comp-6b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 5], b: [1, 10], c: [5, 20] },
    constraints: ({ a, b, c }) => (b - c) % a === 0 && b > c,
    contentFn: ({ a, b, c }) => `-${a}x + ${b} < ${c}를 풀면? (x > ? 형태로 답하시오)`,
    answerFn: ({ a, b, c }) => (b - c) / a,
    distractorFns: [
      ({ a, b, c }) => (c - b) / a,
      ({ a, b, c }) => -(b - c) / a,
      ({ a, b, c }) => (b - c) / a + 1,
    ],
    explanationFn: ({ a, b, c }, ans) =>
      `음수 계수가 있는 일차부등식:\n` +
      `1. 양변에서 ${b}를 빼면: -${a}x < ${c - b}\n` +
      `2. 양변을 -${a}로 나누면: x > ${ans}\n` +
      `※ 주의: 음수로 나누거나 곱하면 부등호 방향이 바뀝니다!`,
  },

  // Lv.7: 순환소수 → 분수 변환 (Phase A 수정: 중3 곱셈공식 제거)
  {
    id: 'm2-comp-7a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'M2-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 9] },
    contentFn: ({ a }) => `0.${a}${a}${a}... (순환마디: ${a})를 분수로 나타내면? (분자만 답하시오, 분모는 9)`,
    answerFn: ({ a }) => a,
    distractorFns: [
      ({ a }) => a * 11,
      ({ a }) => a + 1,
      ({ a }) => a - 1,
    ],
    explanationFn: ({ a }, ans) =>
      `순환소수를 분수로 변환:\n` +
      `x = 0.${a}${a}${a}...라고 하면\n` +
      `10x = ${a}.${a}${a}${a}...\n` +
      `10x - x = ${a}\n` +
      `9x = ${a}\n` +
      `x = ${ans}/9\n` +
      `※ 순환마디가 1자리면 분모는 9입니다.`,
  },
  {
    id: 'm2-comp-7b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'M2-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 9], b: [1, 9] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `0.${a}${b}${a}${b}... (순환마디: ${a}${b})를 분수로 나타내면? (분자만 답하시오, 분모는 99)`,
    answerFn: ({ a, b }) => a * 10 + b,
    distractorFns: [
      ({ a, b }) => (a * 10 + b) * 11,
      ({ a, b }) => a + b,
      ({ a, b }) => a * 10 + b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `순환소수를 분수로 변환:\n` +
      `x = 0.${a}${b}${a}${b}...라고 하면\n` +
      `100x = ${a}${b}.${a}${b}${a}${b}...\n` +
      `100x - x = ${a}${b}\n` +
      `99x = ${a}${b}\n` +
      `x = ${ans}/99\n` +
      `※ 순환마디가 2자리면 분모는 99입니다.`,
  },

  // Lv.8: 유한소수 판별 + 지수법칙 (Phase A 수정: 중3 곱셈공식 제거)
  {
    id: 'm2-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'M2-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 20], b: [2, 12] },
    constraints: ({ b }) => {
      // b가 2 또는 5의 거듭제곱이 아닌 경우
      const factors: number[] = []
      let temp = b
      for (let i = 2; i <= temp; i++) {
        while (temp % i === 0) {
          if (!factors.includes(i)) factors.push(i)
          temp = temp / i
        }
      }
      // 2와 5 이외의 소인수가 있는지 확인
      return factors.some(f => f !== 2 && f !== 5)
    },
    contentFn: ({ a, b }) => `기약분수 ${a}/${b}가 유한소수가 되려면 분모 ${b}의 소인수가 2와 5뿐이어야 합니다. 유한소수가 되나요? (예/아니오)`,
    answerFn: ({ b }) => {
      let temp = b
      while (temp % 2 === 0) temp = temp / 2
      while (temp % 5 === 0) temp = temp / 5
      return temp === 1 ? '예' : '아니오'
    },
    distractorFns: [
      ({ b }) => {
        let temp = b
        while (temp % 2 === 0) temp = temp / 2
        while (temp % 5 === 0) temp = temp / 5
        return temp === 1 ? '아니오' : '예'
      },
      () => '조건부',
      () => '알 수 없음',
    ],
    explanationFn: ({ b }) => {
      let temp = b
      const factors: number[] = []
      for (let i = 2; i <= temp; i++) {
        while (temp % i === 0) {
          factors.push(i)
          temp = temp / i
        }
      }
      const hasOnly2And5 = factors.every(f => f === 2 || f === 5)
      return `유한소수 판별:\n` +
        `${b}의 소인수분해: ${b} = ${factors.join(' × ')}\n` +
        `${hasOnly2And5 ? '2와 5뿐이므로 유한소수입니다.' : '2와 5 이외의 소인수가 있으므로 순환소수입니다.'}\n` +
        `※ 기약분수가 유한소수 ⟺ 분모의 소인수가 2, 5뿐`
    },
  },
  {
    id: 'm2-comp-8b',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-01',
    pattern: '',
    paramRanges: { a: [2, 6], b: [2, 5] },
    contentFn: ({ a, b }) => `a^${a} × a^${b} = a^? (물음표는?)`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `지수법칙 응용:\n` +
      `a^m × a^n = a^(m+n)\n` +
      `a^${a} × a^${b} = a^${ans}\n` +
      `※ 같은 밑을 가진 거듭제곱의 곱셈은 지수를 더합니다.`,
  },

  // Lv.9: 연립방정식 계산 (대입법)
  {
    id: 'm2-comp-9a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법으로 연립방정식을 풉니다.\n` +
      `x + y = ${a} ... ①\n` +
      `x - y = ${b} ... ②\n` +
      `① + ②: 2x = ${a + b}\n` +
      `x = ${ans}\n` +
      `※ y를 소거하기 위해 두 식을 더했습니다.`,
  },
  {
    id: 'm2-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법으로 y를 구합니다.\n` +
      `x + y = ${a} ... ①\n` +
      `x - y = ${b} ... ②\n` +
      `① - ②: 2y = ${a - b}\n` +
      `y = ${ans}\n` +
      `※ x를 소거하기 위해 ①에서 ②를 뺐습니다.`,
  },

  // Lv.10: 연립방정식 계산 (가감법)
  {
    id: 'm2-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법을 사용합니다.\n` +
      `${a}x + y = ${c} ... ①\n` +
      `${a}x - y = ${d} ... ②\n` +
      `① - ②: 2y = ${c - d}\n` +
      `y = ${ans}\n` +
      `※ ${a}x 항이 소거되도록 뺄셈을 했습니다.`,
  },
  {
    id: 'm2-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법으로 x를 구합니다.\n` +
      `${a}x + y = ${c} ... ①\n` +
      `${a}x - y = ${d} ... ②\n` +
      `① + ②: ${2 * a}x = ${c + d}\n` +
      `x = ${ans}\n` +
      `※ y항이 소거되도록 덧셈을 했습니다.`,
  },

  // ============================
  // Phase B: 신규 연산 템플릿 추가
  // ============================

  // B1: 유리수와 순환소수
  {
    id: 'm2-comp-11a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'M2-NUM-01',
    pattern: '',
    paramRanges: { a: [1, 20], b: [2, 8], c: [2, 8] },
    constraints: ({ b, c }) => b !== c,
    contentFn: ({ a, b, c }) => `기약분수 ${a}/(2^${b} × 5^${c})는 유한소수인가요? (예/아니오)`,
    answerFn: () => '예',
    distractorFns: [
      () => '아니오',
      () => '순환소수',
      () => '알 수 없음',
    ],
    explanationFn: ({ b, c }) =>
      `유한소수 조건 확인:\n` +
      `분모 = 2^${b} × 5^${c}\n` +
      `분모의 소인수가 2와 5뿐이므로 유한소수입니다.\n` +
      `※ 기약분수 a/b가 유한소수 ⟺ b = 2^m × 5^n (m, n은 음이 아닌 정수)`,
  },
  {
    id: 'm2-comp-11b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'M2-NUM-01',
    pattern: '',
    paramRanges: { a: [2, 9], b: [1, 9] },
    constraints: ({ a, b }) => a !== b,
    contentFn: ({ a, b }) => `1.${a}${b}${b}${b}... (순환마디: ${b})를 기약분수로 나타내면? (분자는?)`,
    answerFn: ({ a, b }) => {
      // 1.abb... = 1 + 0.abb... = 1 + (ab-a)/90 = (90 + ab - a)/90
      const ab = a * 10 + b
      const num = 90 + ab - a
      // 기약분수로 만들기 위해 gcd 계산
      const gcd = (x: number, y: number): number => y === 0 ? x : gcd(y, x % y)
      const g = gcd(num, 90)
      return num / g
    },
    distractorFns: [
      ({ a, b }) => a * 10 + b,
      ({ a, b }) => {
        const ab = a * 10 + b
        return 90 + ab - a
      },
      ({ a, b }) => a * 100 + b * 10 + b,
    ],
    explanationFn: ({ a, b }, ans) => {
      const ab = a * 10 + b
      const num = 90 + ab - a
      const gcd = (x: number, y: number): number => y === 0 ? x : gcd(y, x % y)
      const g = gcd(num, 90)
      const denom = 90 / g
      return `혼합 순환소수를 분수로:\n` +
        `x = 1.${a}${b}${b}${b}...라고 하면\n` +
        `10x = ${a}${b}.${b}${b}${b}...\n` +
        `100x = ${ab}${b}.${b}${b}${b}...\n` +
        `100x - 10x = ${ab}${b} - ${a}${b}\n` +
        `90x = ${num}\n` +
        `x = ${num}/90 = ${ans}/${denom} (기약분수)\n` +
        `※ 순환마디가 시작하기 전에 ${a}가 있으므로 혼합 순환소수입니다.`
    },
  },

  // B4: 피타고라스 정리
  {
    id: 'm2-comp-12a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-02',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9] },
    constraints: ({ a, b }) => {
      const cSquared = a * a + b * b
      const c = Math.sqrt(cSquared)
      return Number.isInteger(c) && c <= 15
    },
    contentFn: ({ a, b }) => `직각삼각형에서 두 변의 길이가 ${a}, ${b}일 때 빗변의 길이는?`,
    answerFn: ({ a, b }) => Math.sqrt(a * a + b * b),
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => Math.sqrt(a * a + b * b) + 1,
      ({ a, b }) => Math.sqrt(a * a + b * b) - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `피타고라스 정리를 사용합니다.\n` +
      `빗변을 c라 하면: a² + b² = c²\n` +
      `${a}² + ${b}² = c²\n` +
      `${a * a} + ${b * b} = c²\n` +
      `c² = ${a * a + b * b}\n` +
      `c = ${ans}\n` +
      `※ 직각삼각형에서 빗변의 제곱 = 다른 두 변의 제곱의 합`,
  },
  {
    id: 'm2-comp-12b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-02',
    pattern: '',
    paramRanges: { c: [5, 13], a: [3, 8] },
    constraints: ({ c, a }) => {
      const bSquared = c * c - a * a
      const b = Math.sqrt(bSquared)
      return bSquared > 0 && Number.isInteger(b) && b > a
    },
    contentFn: ({ c, a }) => `직각삼각형에서 빗변이 ${c}, 한 변이 ${a}일 때 나머지 변의 길이는?`,
    answerFn: ({ c, a }) => Math.sqrt(c * c - a * a),
    distractorFns: [
      ({ c, a }) => c - a,
      ({ c, a }) => Math.sqrt(c * c - a * a) + 1,
      ({ c, a }) => Math.sqrt(c * c - a * a) - 1,
    ],
    explanationFn: ({ c, a }, ans) =>
      `피타고라스 정리로 한 변 구하기:\n` +
      `나머지 변을 b라 하면: a² + b² = c²\n` +
      `${a}² + b² = ${c}²\n` +
      `b² = ${c}² - ${a}² = ${c * c} - ${a * a} = ${c * c - a * a}\n` +
      `b = ${ans}\n` +
      `※ 주의: c - a가 아니라 √(c² - a²)입니다!`,
  },
]

// ============================
// 개념(concept) Lv.1~10 + 추가
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
        '3x² + 2x는 두 개의 단항식의 합이므로 다항식입니다.\n※ 다항식: 하나 이상의 단항식의 합',
        '5x³은 하나의 항으로 이루어져 있으므로 단항식입니다.\n※ 단항식: 수나 문자의 곱으로만 이루어진 식',
        '2x + 3y - 1은 세 개의 단항식의 합이므로 다항식입니다.\n※ 상수항(-1)도 단항식입니다.',
        '7은 하나의 항(상수항)이므로 단항식입니다.\n※ 상수도 단항식으로 볼 수 있습니다.',
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
    conceptId: 'M2-ALG-03',
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
        return `${b} > ${a}이므로 x = ${b}는 해입니다.\n※ 부등식의 해: 부등식을 참이 되게 하는 값`
      } else {
        return `${b} ≤ ${a}이므로 x = ${b}는 해가 아닙니다.\n※ ${b}는 범위 x > ${a}에 포함되지 않습니다.`
      }
    },
  },
  {
    id: 'm2-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
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
        return `${b} ≥ ${a}이므로 x = ${b}는 해입니다.\n※ ≥는 '크거나 같다'이므로 ${a}도 해에 포함됩니다.`
      } else {
        return `${b} < ${a}이므로 x = ${b}는 해가 아닙니다.\n※ ${b}는 범위 x ≥ ${a}에 포함되지 않습니다.`
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
    conceptId: 'M2-ALG-04',
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
      `대입법으로 연립방정식을 풉니다.\n` +
      `y = ${a}x ... ①\n` +
      `x + y = ${b} ... ②\n` +
      `①을 ②에 대입:\n` +
      `x + ${a}x = ${b}\n` +
      `${a + 1}x = ${b}\n` +
      `x = ${ans}\n` +
      `※ 대입법: 한 식을 다른 식에 대입하여 미지수를 소거`,
  },

  // Lv.4: 연립방정식 (가감법)
  {
    id: 'm2-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법으로 연립방정식을 풉니다.\n` +
      `x + y = ${a} ... ①\n` +
      `x - y = ${b} ... ②\n` +
      `① + ②: 2x = ${a + b}\n` +
      `x = ${ans}\n` +
      `※ 가감법: 두 식을 더하거나 빼서 한 미지수를 소거`,
  },
  {
    id: 'm2-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-04',
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
      `가감법으로 y를 구합니다.\n` +
      `x + y = ${a} ... ①\n` +
      `x - y = ${b} ... ②\n` +
      `① - ②: 2y = ${a - b}\n` +
      `y = ${ans}\n` +
      `※ x를 소거하기 위해 ①에서 ②를 뺐습니다.`,
  },

  // Lv.5: 일차함수 y = ax + b
  {
    id: 'm2-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      `일차함수의 기울기와 y절편:\n` +
      `y = ax + b에서\n` +
      `• 기울기: a (x의 계수)\n` +
      `• y절편: b (상수항)\n` +
      `y = ${a}x + ${signedStr(b)}의 기울기는 ${a}입니다.\n` +
      `※ 기울기는 x가 1 증가할 때 y의 증가량입니다.`,
  },
  {
    id: 'm2-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      `일차함수 y = ax + b에서 y절편은 b입니다.\n` +
      `y = ${a}x + ${signedStr(b)}의 y절편은 ${b}입니다.\n` +
      `※ y절편: 그래프가 y축과 만나는 점의 y좌표 (x = 0일 때 y값)`,
  },

  // Lv.6: 일차함수 그래프 해석
  {
    id: 'm2-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      `그래프가 y축과 만나는 점:\n` +
      `y축 위의 점은 x = 0입니다.\n` +
      `x = 0을 대입하면 y = ${b}\n` +
      `따라서 교점의 좌표는 (0, ${b})이고 y좌표는 ${b}입니다.\n` +
      `※ y절편과 같습니다.`,
  },
  {
    id: 'm2-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      `그래프가 x축과 만나는 점:\n` +
      `x축 위의 점은 y = 0입니다.\n` +
      `0 = ${a}x + ${signedStr(b)}\n` +
      `${a}x = ${-b}\n` +
      `x = ${ans}\n` +
      `따라서 교점의 좌표는 (${ans}, 0)이고 x좌표는 ${ans}입니다.\n` +
      `※ x절편이라고도 합니다.`,
  },

  // Lv.7: 이등변삼각형 성질 (Phase A 수정: 합동 조건은 중1이므로 교체)
  {
    id: 'm2-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { a: [20, 120] },
    constraints: ({ a }) => (180 - a) % 2 === 0 && a < 180,
    contentFn: ({ a }) => `이등변삼각형에서 꼭지각이 ${a}°일 때 한 밑각의 크기는?`,
    answerFn: ({ a }) => (180 - a) / 2,
    distractorFns: [
      ({ a }) => 180 - a,
      ({ a }) => a / 2,
      ({ a }) => (180 - a) / 2 + 5,
    ],
    explanationFn: ({ a }, ans) =>
      `이등변삼각형의 성질:\n` +
      `• 두 밑각의 크기는 같습니다.\n` +
      `• 내각의 합은 180°입니다.\n` +
      `꼭지각 + 밑각 + 밑각 = 180°\n` +
      `${a}° + 2 × (밑각) = 180°\n` +
      `2 × (밑각) = ${180 - a}°\n` +
      `밑각 = ${ans}°\n` +
      `※ 이등변삼각형: 두 변의 길이가 같은 삼각형`,
  },

  // Lv.8: 사각형 성질
  {
    id: 'm2-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
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
        '평행사변형의 성질: 대변의 길이는 같습니다.\n※ 마주보는 두 변의 길이가 같습니다.',
        '평행사변형의 성질: 대각의 크기는 같습니다.\n※ 마주보는 두 각의 크기가 같습니다.',
        '직사각형의 성질: 대각선의 길이는 같습니다.\n※ 두 대각선의 길이가 같고 서로를 이등분합니다.',
        '마름모의 성질: 대각선은 서로 수직이등분합니다.\n※ 두 대각선이 직각으로 만나고 서로를 이등분합니다.',
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
    conceptId: 'M2-STA-01',
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
      `확률 = (사건이 일어나는 경우의 수) ÷ (전체 경우의 수)\n` +
      `전체 경우의 수는 6가지입니다.\n` +
      `${a} 이하의 눈은 1, 2, ..., ${a}로 ${a}가지입니다.\n` +
      `확률 = ${a}/6 = ${ans}\n` +
      `※ 확률은 0 이상 1 이하의 값입니다.`,
  },
  {
    id: 'm2-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'M2-STA-01',
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
      `확률 계산:\n` +
      `전체 경우의 수는 6가지입니다.\n` +
      `${a}보다 큰 눈은 ${a + 1}, ${a + 2}, ..., 6으로 ${6 - a}가지입니다.\n` +
      `확률 = ${6 - a}/6 = ${ans}\n` +
      `※ 여사건의 확률: P(A) + P(A가 아닌 경우) = 1`,
  },

  // Lv.10: 복합 응용 (함수 + 방정식)
  {
    id: 'm2-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      return `두 일차함수의 교점:\n` +
        `교점에서 y값이 같으므로:\n` +
        `${a}x + ${signedStr(b)} = ${c}x + ${signedStr(d)}\n` +
        `${a}x - ${c}x = ${d} - ${b}\n` +
        `${a - c}x = ${d - b}\n` +
        `x = ${ans}\n` +
        `교점의 좌표: (${ans}, ${yVal})\n` +
        `※ 연립방정식을 풀어 교점을 구합니다.`
    },
  },
  {
    id: 'm2-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
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
      return `두 일차함수의 교점의 y좌표:\n` +
        `먼저 x좌표를 구합니다:\n` +
        `${a}x + ${signedStr(b)} = ${c}x + ${signedStr(d)}\n` +
        `x = ${xVal}\n` +
        `x = ${xVal}을 y = ${a}x + ${signedStr(b)}에 대입:\n` +
        `y = ${a} × ${xVal} + ${signedStr(b)} = ${ans}\n` +
        `※ 어느 식에 대입해도 같은 y값이 나옵니다.`
    },
  },

  // ============================
  // Phase B: 신규 개념 템플릿 추가
  // ============================

  // B2: 일차부등식 활용
  {
    id: 'm2-conc-11a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 10], c: [5, 20] },
    constraints: ({ a, b, c }) => c > b && (c - b) % a === 0,
    contentFn: ({ a, b, c }) => `${a}x - ${b} > ${c}를 만족하는 가장 작은 정수 x는?`,
    answerFn: ({ a, b, c }) => Math.floor((c + b) / a) + 1,
    distractorFns: [
      ({ a, b, c }) => (c + b) / a,
      ({ a, b, c }) => Math.floor((c + b) / a),
      ({ a, b, c }) => Math.ceil((c + b) / a),
    ],
    explanationFn: ({ a, b, c }, ans) => {
      const boundary = (c + b) / a
      return `일차부등식의 해의 범위:\n` +
        `${a}x - ${b} > ${c}\n` +
        `${a}x > ${c + b}\n` +
        `x > ${boundary}\n` +
        `가장 작은 정수는 ${boundary}보다 큰 최소 정수이므로 ${ans}입니다.\n` +
        `※ 부등호가 >이므로 ${boundary}는 포함되지 않습니다.`
    },
  },
  {
    id: 'm2-conc-11b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'algebra' as ProblemPart,
    conceptId: 'M2-ALG-03',
    pattern: '',
    paramRanges: { a: [2, 4], b: [6, 18] },
    constraints: ({ a, b }) => b % a === 0,
    contentFn: ({ a, b }) => `-${a}x < ${b}의 해는? (x > ? 또는 x < ? 형태로)`,
    answerFn: ({ a, b }) => `x > ${-b / a}`,
    distractorFns: [
      ({ a, b }) => `x < ${b / a}`,
      ({ a, b }) => `x > ${b / a}`,
      ({ a, b }) => `x < ${-b / a}`,
    ],
    explanationFn: ({ a, b }, _ans) => {
      const result = -b / a
      return `음수 계수가 있는 부등식:\n` +
        `-${a}x < ${b}\n` +
        `양변을 -${a}로 나누면:\n` +
        `x > ${result}\n` +
        `※ 중요: 음수로 나누거나 곱하면 부등호 방향이 바뀝니다!\n` +
        `< → >, > → <, ≤ → ≥, ≥ → ≤`
    },
  },

  // B3: 닮음
  {
    id: 'm2-conc-12a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-02',
    pattern: '',
    paramRanges: { variant: [0, 2] },
    contentFn: ({ variant }) => {
      const questions = [
        '두 삼각형에서 두 쌍의 대응각의 크기가 같으면 어떤 닮음 조건인가?',
        '두 삼각형에서 대응하는 두 변의 길이의 비가 같고 그 끼인각의 크기가 같으면 어떤 닮음 조건인가?',
        '두 삼각형에서 대응하는 세 변의 길이의 비가 같으면 어떤 닮음 조건인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['AA 닮음', 'SAS 닮음', 'SSS 닮음']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['SAS 닮음', 'SSS 닮음', 'AA 닮음'][variant]!),
      ({ variant }) => (['SSS 닮음', 'AA 닮음', 'SAS 닮음'][variant]!),
      () => 'AAA 닮음',
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        'AA 닮음 (Angle-Angle): 두 쌍의 대응각이 같으면 닮음입니다.\n※ 삼각형은 두 각이 같으면 나머지 한 각도 자동으로 같아집니다.',
        'SAS 닮음 (Side-Angle-Side): 두 변의 비가 같고 그 끼인각이 같으면 닮음입니다.\n※ 대응하는 두 변의 길이의 비가 같고, 그 사이각의 크기가 같아야 합니다.',
        'SSS 닮음 (Side-Side-Side): 세 변의 길이의 비가 모두 같으면 닮음입니다.\n※ 대응하는 세 변의 길이의 비가 모두 같아야 합니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },
  {
    id: 'm2-conc-12b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-02',
    pattern: '',
    paramRanges: { a: [2, 5], b: [3, 7] },
    constraints: ({ a, b }) => a < b,
    contentFn: ({ a, b }) => `두 도형의 닮음비가 ${a}:${b}일 때, 넓이의 비는?`,
    answerFn: ({ a, b }) => `${a * a}:${b * b}`,
    distractorFns: [
      ({ a, b }) => `${a}:${b}`,
      ({ a, b }) => `${a * 2}:${b * 2}`,
      ({ a, b }) => `${a * a + 1}:${b * b + 1}`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `닮음비와 넓이의 비:\n` +
      `닮음비가 a:b이면\n` +
      `• 대응하는 선분의 길이의 비 = a:b\n` +
      `• 넓이의 비 = a²:b²\n` +
      `• 부피의 비 = a³:b³\n` +
      `닮음비 ${a}:${b} → 넓이의 비 ${a}²:${b}² = ${ans}\n` +
      `※ 넓이는 길이의 제곱에 비례합니다.`,
  },

  // B4: 피타고라스 정리 개념
  {
    id: 'm2-conc-13a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-02',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9], c: [5, 13] },
    constraints: ({ a, b, c }) => a * a + b * b === c * c && a < b && b < c,
    contentFn: ({ a, b, c }) => `세 수 ${a}, ${b}, ${c}는 피타고라스 수인가요? (예/아니오)`,
    answerFn: () => '예',
    distractorFns: [
      () => '아니오',
      () => '일부만',
      () => '알 수 없음',
    ],
    explanationFn: ({ a, b, c }) =>
      `피타고라스 수 판별:\n` +
      `${a}² + ${b}² = ${a * a} + ${b * b} = ${a * a + b * b}\n` +
      `${c}² = ${c * c}\n` +
      `${a}² + ${b}² = ${c}²이므로 피타고라스 수입니다.\n` +
      `※ 피타고라스 수: a² + b² = c²를 만족하는 세 자연수 (a, b, c)\n` +
      `예: (3, 4, 5), (5, 12, 13), (8, 15, 17), ...`,
  },

  // B5: 경우의 수
  {
    id: 'm2-conc-14a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'M2-STA-01',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9] },
    contentFn: ({ a, b }) => `사건 A가 일어나는 경우가 ${a}가지, 사건 B가 일어나는 경우가 ${b}가지일 때, A 또는 B가 일어나는 경우의 수는? (A와 B는 동시에 일어나지 않음)`,
    answerFn: ({ a, b }) => a + b,
    distractorFns: [
      ({ a, b }) => a * b,
      ({ a, b }) => a + b + 1,
      ({ a, b }) => a + b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `합의 법칙:\n` +
      `두 사건 A, B가 동시에 일어나지 않을 때,\n` +
      `A 또는 B가 일어나는 경우의 수 = (A의 경우의 수) + (B의 경우의 수)\n` +
      `= ${a} + ${b} = ${ans}\n` +
      `※ '또는'은 합의 법칙 (더하기)을 사용합니다.`,
  },
  {
    id: 'm2-conc-14b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'M2-STA-01',
    pattern: '',
    paramRanges: { a: [3, 8], b: [4, 9] },
    contentFn: ({ a, b }) => `사건 A가 일어나는 경우가 ${a}가지, 그 각각에 대하여 사건 B가 일어나는 경우가 ${b}가지일 때, A 그리고 B가 잇달아 일어나는 경우의 수는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => a + b,
      ({ a, b }) => a * b + 1,
      ({ a, b }) => a * b - 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `곱의 법칙:\n` +
      `사건 A가 일어나는 경우가 m가지이고,\n` +
      `그 각각에 대하여 사건 B가 일어나는 경우가 n가지일 때,\n` +
      `A 그리고 B가 잇달아 일어나는 경우의 수 = m × n\n` +
      `= ${a} × ${b} = ${ans}\n` +
      `※ '그리고'는 곱의 법칙 (곱하기)을 사용합니다.`,
  },

  // B6: 삼각형 외심/내심
  {
    id: 'm2-conc-15a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 1] },
    contentFn: ({ variant }) => {
      const questions = [
        '삼각형의 외심은 세 꼭짓점으로부터의 거리가 어떤가?',
        '삼각형의 외심은 무엇의 교점인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['모두 같다', '세 변의 수직이등분선']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['모두 다르다', '세 중선'][variant]!),
      ({ variant }) => (['일부만 같다', '세 높이'][variant]!),
      ({ variant }) => (['알 수 없다', '세 각의 이등분선'][variant]!),
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '외심의 성질:\n삼각형의 외심은 세 꼭짓점으로부터의 거리가 모두 같습니다.\n※ 외심: 삼각형의 외접원의 중심',
        '외심의 정의:\n삼각형의 외심은 세 변의 수직이등분선이 만나는 점입니다.\n※ 외심은 외접원의 중심이므로 세 꼭짓점으로부터 거리가 같습니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },
  {
    id: 'm2-conc-15b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 1] },
    contentFn: ({ variant }) => {
      const questions = [
        '삼각형의 내심은 세 변으로부터의 거리가 어떤가?',
        '삼각형의 내심은 무엇의 교점인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['모두 같다', '세 각의 이등분선']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['모두 다르다', '세 중선'][variant]!),
      ({ variant }) => (['일부만 같다', '세 높이'][variant]!),
      ({ variant }) => (['알 수 없다', '세 변의 수직이등분선'][variant]!),
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '내심의 성질:\n삼각형의 내심은 세 변으로부터의 거리가 모두 같습니다.\n※ 내심: 삼각형의 내접원의 중심',
        '내심의 정의:\n삼각형의 내심은 세 각의 이등분선이 만나는 점입니다.\n※ 내심은 내접원의 중심이므로 세 변으로부터 거리가 같습니다.',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // B7: 사각형 성질 추가
  {
    id: 'm2-conc-16a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { a: [5, 15], b: [3, 10] },
    contentFn: ({ a, b }) => `밑변의 길이가 ${a}cm, 높이가 ${b}cm인 평행사변형의 넓이는?`,
    answerFn: ({ a, b }) => a * b,
    distractorFns: [
      ({ a, b }) => 2 * (a + b),
      ({ a, b }) => (a * b) / 2,
      ({ a, b }) => a * b + 1,
    ],
    explanationFn: ({ a, b }, ans) =>
      `평행사변형의 넓이:\n` +
      `넓이 = 밑변 × 높이\n` +
      `= ${a} × ${b}\n` +
      `= ${ans} cm²\n` +
      `※ 높이는 밑변에 수직인 거리입니다.`,
  },
  {
    id: 'm2-conc-16b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'M2-GEO-01',
    pattern: '',
    paramRanges: { variant: [0, 3] },
    contentFn: ({ variant }) => {
      const questions = [
        '다음 중 항상 평행사변형인 것은?',
        '다음 중 평행사변형이 아닌 것은?',
        '직사각형은 평행사변형인가?',
        '정사각형은 마름모인가?',
      ]
      return questions[variant]!
    },
    answerFn: ({ variant }) => {
      const answers = ['직사각형', '사다리꼴', '예', '예']
      return answers[variant]!
    },
    distractorFns: [
      ({ variant }) => (['사다리꼴', '직사각형', '아니오', '아니오'][variant]!),
      ({ variant }) => (['일반 사각형', '마름모', '조건부', '조건부'][variant]!),
      ({ variant }) => (['부채꼴', '정사각형', '알 수 없음', '알 수 없음'][variant]!),
    ],
    explanationFn: ({ variant }) => {
      const explanations = [
        '사각형의 포함관계:\n직사각형은 네 각이 모두 직각인 평행사변형입니다.\n※ 정사각형 ⊂ 직사각형, 마름모 ⊂ 평행사변형 ⊂ 사다리꼴',
        '평행사변형의 조건:\n사다리꼴은 한 쌍의 대변만 평행하므로 평행사변형이 아닙니다.\n※ 평행사변형은 두 쌍의 대변이 각각 평행해야 합니다.',
        '포함관계:\n직사각형은 네 각이 모두 직각인 평행사변형입니다.\n※ 직사각형의 모든 성질은 평행사변형의 성질을 포함합니다.',
        '포함관계:\n정사각형은 네 변의 길이가 같은 마름모입니다.\n※ 정사각형 = 직사각형 ∩ 마름모',
      ]
      return explanations[variant]!
    },
    questionType: 'multiple_choice',
  },

  // B8: 일차함수 활용
  {
    id: 'm2-conc-17a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
    pattern: '',
    paramRanges: { a: [1, 5], b: [2, 8], c: [6, 10], d: [10, 20] },
    constraints: ({ a, b, c, d }) => {
      return a !== c && (d - b) % (c - a) === 0
    },
    contentFn: ({ a, b, c, d }) => `두 점 (${a}, ${b}), (${c}, ${d})를 지나는 직선의 기울기는?`,
    answerFn: ({ a, b, c, d }) => (d - b) / (c - a),
    distractorFns: [
      ({ a, b, c, d }) => (c - a) / (d - b),
      ({ a, b, c, d }) => (d + b) / (c + a),
      ({ a, b, c, d }) => (d - b) / (c - a) + 1,
    ],
    explanationFn: ({ a, b, c, d }, ans) =>
      `두 점을 지나는 직선의 기울기:\n` +
      `기울기 = (y좌표의 증가량) / (x좌표의 증가량)\n` +
      `= (y₂ - y₁) / (x₂ - x₁)\n` +
      `= (${d} - ${b}) / (${c} - ${a})\n` +
      `= ${d - b} / ${c - a}\n` +
      `= ${ans}\n` +
      `※ 기울기는 직선의 기울어진 정도를 나타냅니다.`,
  },
  {
    id: 'm2-conc-17b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'func' as ProblemPart,
    conceptId: 'M2-FUNC-01',
    pattern: '',
    paramRanges: { a: [-5, 8], b: [-10, 10] },
    constraints: ({ a }) => a !== 0,
    contentFn: ({ a, b }) => `기울기가 ${a}이고 y절편이 ${b}인 일차함수의 식은?`,
    answerFn: ({ a, b }) => `y = ${a}x + ${signedStr(b)}`,
    distractorFns: [
      ({ a, b }) => `y = ${b}x + ${signedStr(a)}`,
      ({ a, b }) => `y = ${a}x - ${b}`,
      ({ a, b }) => `y = -${a}x + ${signedStr(b)}`,
    ],
    explanationFn: ({ a, b }, ans) =>
      `일차함수의 식:\n` +
      `y = ax + b에서\n` +
      `• a: 기울기\n` +
      `• b: y절편\n` +
      `기울기 ${a}, y절편 ${b}를 대입하면:\n` +
      `${ans}\n` +
      `※ 기울기와 y절편을 알면 일차함수의 식을 구할 수 있습니다.`,
  },
]

export const middle2Templates: QuestionTemplate[] = [...comp, ...conc]
