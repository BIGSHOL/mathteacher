import type { QuestionTemplate } from '../types'
import type { ProblemPart } from '../../../types'

const G = 'elementary_3' as const

// Helper function for GCD
function gcdHelper(a: number, b: number): number {
  return b === 0 ? a : gcdHelper(b, a % b)
}

// ============================================================================
// COMPUTATION TEMPLATES (계산력)
// ============================================================================

const comp: QuestionTemplate[] = [
  // e3-comp-1a: 덧셈 (세로셈)
  {
    id: 'e3-comp-1a',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '세자리 + 세자리 (받아올림 있음)',
    paramRanges: { a: [100, 500], b: [200, 499] },
    constraints: (p) => p.a + p.b < 1000,
    answerFn: (p) => p.a + p.b,
    distractorFns: [
      (p) => p.a + p.b + 10,
      (p) => p.a + p.b - 10,
      (p) => p.a + p.b + 100,
    ],
    explanationFn: (p, ans) =>
      `① 일의 자리부터 차례로 더합니다\n② ${p.a} + ${p.b} = ${ans}\n③ 받아올림에 주의하세요`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-comp-1b: 덧셈 (가로셈)
  {
    id: 'e3-comp-1b',
    grade: G,
    category: 'computation',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '세자리 + 세자리 (받아올림 2번)',
    paramRanges: { a: [150, 550], b: [250, 449] },
    constraints: (p) => {
      const aOnes = p.a % 10
      const bOnes = p.b % 10
      const aTens = Math.floor(p.a / 10) % 10
      const bTens = Math.floor(p.b / 10) % 10
      return (aOnes + bOnes >= 10) && (aTens + bTens >= 10) && p.a + p.b < 1000
    },
    answerFn: (p) => p.a + p.b,
    distractorFns: [
      (p) => p.a + p.b + 11,
      (p) => p.a + p.b - 11,
      (p) => p.a + p.b + 1,
    ],
    explanationFn: (p, ans) =>
      `① 일의 자리: ${p.a % 10} + ${p.b % 10} = ${(p.a % 10) + (p.b % 10)} (받아올림 발생)\n② 십의 자리: ${Math.floor(p.a / 10) % 10} + ${Math.floor(p.b / 10) % 10} + 1 = ${Math.floor(p.a / 10) % 10 + Math.floor(p.b / 10) % 10 + 1}\n③ 최종 답: ${ans}`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-comp-2a: 뺄셈 (받아내림 1번)
  {
    id: 'e3-comp-2a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '세자리 - 세자리 (받아내림 1번)',
    paramRanges: { a: [300, 900], b: [100, 400] },
    constraints: (p) => {
      const aOnes = p.a % 10
      const bOnes = p.b % 10
      return p.a > p.b && aOnes < bOnes
    },
    answerFn: (p) => p.a - p.b,
    distractorFns: [
      (p) => p.a - p.b + 10,
      (p) => p.a - p.b - 10,
      (p) => Math.abs((p.a % 100) - (p.b % 100)) + Math.floor(p.a / 100) * 100,
    ],
    explanationFn: (p, ans) =>
      `① 일의 자리: ${p.a % 10} < ${p.b % 10}이므로 받아내림 필요\n② 십의 자리에서 1을 빌려옴\n③ ${p.a} - ${p.b} = ${ans}`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-comp-2b: 뺄셈 (받아내림 2번)
  {
    id: 'e3-comp-2b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-01',
    pattern: '세자리 - 세자리 (받아내림 2번)',
    paramRanges: { a: [500, 900], b: [200, 499] },
    constraints: (p) => {
      const aOnes = p.a % 10
      const bOnes = p.b % 10
      const aTens = Math.floor(p.a / 10) % 10
      const bTens = Math.floor(p.b / 10) % 10
      return p.a > p.b && aOnes < bOnes && aTens < bTens
    },
    answerFn: (p) => p.a - p.b,
    distractorFns: [
      (p) => p.a - p.b + 100,
      (p) => p.a - p.b - 100,
      (p) => p.a - p.b + 11,
    ],
    explanationFn: (p, ans) =>
      `① 일의 자리와 십의 자리 모두 받아내림 발생\n② 백의 자리에서 차례로 빌려옴\n③ ${p.a} - ${p.b} = ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-3a: 곱셈 (한자리 × 두자리)
  {
    id: 'e3-comp-3a',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '한자리 × 두자리',
    paramRanges: { a: [2, 9], b: [11, 25] },
    answerFn: (p) => p.a * p.b,
    distractorFns: [
      (p) => p.a * p.b + 10,
      (p) => p.a * p.b - 10,
      (p) => p.a * (p.b % 10) + p.a * Math.floor(p.b / 10),
    ],
    explanationFn: (p, ans) =>
      `① ${p.a} × ${Math.floor(p.b / 10)}0 = ${p.a * Math.floor(p.b / 10) * 10}\n② ${p.a} × ${p.b % 10} = ${p.a * (p.b % 10)}\n③ ${p.a * Math.floor(p.b / 10) * 10} + ${p.a * (p.b % 10)} = ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-3b: 곱셈 (두자리 × 한자리)
  {
    id: 'e3-comp-3b',
    grade: G,
    category: 'computation',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '두자리 × 한자리 (받아올림)',
    paramRanges: { a: [15, 35], b: [3, 9] },
    constraints: (p) => (p.a % 10) * p.b >= 10,
    answerFn: (p) => p.a * p.b,
    distractorFns: [
      (p) => p.a * p.b + p.b,
      (p) => p.a * p.b - p.b,
      (p) => (p.a % 10) * p.b + Math.floor(p.a / 10) * p.b,
    ],
    explanationFn: (p, ans) =>
      `① 일의 자리 계산: ${p.a % 10} × ${p.b} = ${(p.a % 10) * p.b}\n② 십의 자리 계산: ${Math.floor(p.a / 10)} × ${p.b} = ${Math.floor(p.a / 10) * p.b}\n③ 받아올림 주의: ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-4a: 곱셈 (두자리 × 한자리, 0 포함)
  {
    id: 'e3-comp-4a',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '두자리(0 포함) × 한자리',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: (p) => `${p.a}0 × ${p.b} = ?`,
    answerFn: (p) => p.a * 10 * p.b,
    distractorFns: [
      (p) => p.a * p.b,
      (p) => p.a * 10 * p.b + 10,
      (p) => p.a * p.b * 100,
    ],
    explanationFn: (p, ans) =>
      `① ${p.a}0 = ${p.a} × 10\n② ${p.a} × 10 × ${p.b} = ${p.a} × ${p.b} × 10\n③ ${p.a * p.b} × 10 = ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-4b: 곱셈 (세자리 × 한자리)
  {
    id: 'e3-comp-4b',
    grade: G,
    category: 'computation',
    level: 5,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '세자리 × 한자리',
    paramRanges: { a: [100, 300], b: [2, 5] },
    answerFn: (p) => p.a * p.b,
    distractorFns: [
      (p) => p.a * p.b + 100,
      (p) => p.a * p.b - 100,
      (p) => p.a + p.b * 100,
    ],
    explanationFn: (p, ans) =>
      `① 세자리 수를 분해: ${Math.floor(p.a / 100)}00 + ${Math.floor(p.a / 10) % 10}0 + ${p.a % 10}\n② 각각 ${p.b}를 곱한 후 더하기\n③ ${p.a} × ${p.b} = ${ans}`,
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-5a: 나눗셈 (나누어떨어짐)
  {
    id: 'e3-comp-5a',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '두자리 ÷ 한자리 (나누어떨어짐)',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: (p) => `${p.a * p.b} ÷ ${p.b} = ?`,
    answerFn: (p) => p.a,
    distractorFns: [
      (p) => p.a + 1,
      (p) => p.a - 1,
      (p) => p.a * p.b,
    ],
    explanationFn: (p, ans) =>
      `① ${p.a * p.b} ÷ ${p.b} = ${ans}\n② 검산: ${p.b} × ${ans} = ${p.a * p.b} ✓\n③ 나누어떨어지므로 나머지는 0`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-5b: 나눗셈 (큰 수)
  {
    id: 'e3-comp-5b',
    grade: G,
    category: 'computation',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '두자리 ÷ 한자리 (큰 수)',
    paramRanges: { a: [4, 9], b: [3, 8] },
    contentFn: (p) => `${p.a * p.b} ÷ ${p.b} = ?`,
    constraints: (p) => p.a * p.b >= 30,
    answerFn: (p) => p.a,
    distractorFns: [
      (p) => p.a + 1,
      (p) => Math.floor(p.a / 2),
      (p) => p.b,
    ],
    explanationFn: (p, ans) =>
      `① ${p.a * p.b}를 ${p.b}로 나눔\n② ${p.b} × ${ans} = ${p.a * p.b}\n③ 검산: ${p.b} × ${ans} = ${p.a * p.b} ✓`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-6a: 나눗셈 (나머지 있음)
  {
    id: 'e3-comp-6a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '두자리 ÷ 한자리 (나머지 있음)',
    paramRanges: { n: [20, 50], b: [3, 8] },
    constraints: (p) => p.n % p.b !== 0 && p.n > p.b,
    contentFn: (p) => `${p.n} ÷ ${p.b}의 나머지는?`,
    answerFn: (p) => p.n % p.b,
    distractorFns: [
      (p) => Math.floor(p.n / p.b),
      (p) => (p.n % p.b) + 1,
      (p) => p.b,
    ],
    explanationFn: (p, ans) =>
      `① ${p.n} ÷ ${p.b} = ${Math.floor(p.n / p.b)} … ${ans}\n② 검산: ${p.b} × ${Math.floor(p.n / p.b)} + ${ans} = ${p.n} ✓\n③ 나머지는 나누는 수보다 작아야 함`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-6b: 나눗셈 (몫 구하기)
  {
    id: 'e3-comp-6b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '두자리 ÷ 한자리 (몫)',
    paramRanges: { n: [25, 60], b: [4, 9] },
    constraints: (p) => p.n % p.b !== 0 && p.n > p.b,
    contentFn: (p) => `${p.n} ÷ ${p.b}의 몫은?`,
    answerFn: (p) => Math.floor(p.n / p.b),
    distractorFns: [
      (p) => Math.floor(p.n / p.b) + 1,
      (p) => p.n % p.b,
      (p) => Math.floor(p.n / p.b) - 1,
    ],
    explanationFn: (p, ans) => {
      const remainder = p.n % p.b
      return `① ${p.n} ÷ ${p.b} = ${ans} … ${remainder}\n② 검산: ${p.b} × ${ans} + ${remainder} = ${p.n} ✓\n③ 나머지 ${remainder}는 나누는 수 ${p.b}보다 작음 (규칙)`
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-7a: 분수 크기 비교
  {
    id: 'e3-comp-7a',
    grade: G,
    category: 'computation',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-10',
    pattern: '분모 같은 분수 크기 비교',
    paramRanges: { a: [1, 7], b: [2, 9], d: [3, 9] },
    constraints: (p) => p.a < p.b && p.d > Math.max(p.a, p.b),
    contentFn: (p) => `${p.a}/${p.d}와 ${p.b}/${p.d} 중 더 큰 수는?`,
    answerFn: (p) => `${p.b}/${p.d}`,
    distractorFns: [
      (p) => `${p.a}/${p.d}`,
      (p) => `${p.a + p.b}/${p.d}`,
      (p) => `${Math.max(p.a, p.b)}/${Math.min(p.a, p.b)}`,
    ],
    explanationFn: (p, _ans) =>
      `① 분모가 같은 분수는 분자가 클수록 큰 분수입니다\n② ${p.b} > ${p.a}이므로 ${p.b}/${p.d} > ${p.a}/${p.d}\n③ 흔한 실수: 분모가 크면 더 크다고 착각 (단위분수에서 분모가 클수록 작음!)`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-comp-7b: 분수 크기 비교 (부등호)
  {
    id: 'e3-comp-7b',
    grade: G,
    category: 'computation',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-10',
    pattern: '분모 같은 분수 부등호',
    paramRanges: { a: [2, 8], b: [3, 9], d: [5, 12] },
    constraints: (p) => p.a < p.b && p.d > p.b,
    contentFn: (p) => `${p.a}/${p.d} ☐ ${p.b}/${p.d}에서 ☐에 알맞은 부등호는?`,
    answerFn: () => '<',
    distractorFns: [
      () => '>',
      () => '=',
      () => '≥',
    ],
    explanationFn: (p, _ans) =>
      `① 분모가 ${p.d}로 같습니다\n② 분자를 비교: ${p.a} < ${p.b}\n③ 따라서 ${p.a}/${p.d} < ${p.b}/${p.d}`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-comp-8a: 분수 덧셈 (동분모)
  {
    id: 'e3-comp-8a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-13',
    pattern: '동분모 분수 덧셈',
    paramRanges: { a: [1, 5], b: [1, 6], d: [4, 9] },
    constraints: (p) => p.a + p.b < p.d && p.d > Math.max(p.a, p.b),
    contentFn: (p) => `${p.a}/${p.d} + ${p.b}/${p.d} = ?`,
    answerFn: (p) => `${p.a + p.b}/${p.d}`,
    distractorFns: [
      (p) => `${p.a + p.b}/${p.d * 2}`,
      (p) => `${p.a + p.b}/${p.d + p.d}`,
      (p) => {
        const gcd = gcdHelper(p.a + p.b, p.d)
        return gcd > 1 ? `${(p.a + p.b) / gcd}/${p.d / gcd}` : `${p.a + p.b + 1}/${p.d}`
      },
    ],
    explanationFn: (p, ans) =>
      `① 분모가 같으면 분자끼리만 더합니다\n② ${p.a} + ${p.b} = ${p.a + p.b}\n③ 분모는 그대로: ${ans}\n④ 흔한 실수: 분모까지 더하면 안 됨!`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-8b: 분수 덧셈 (대분수)
  {
    id: 'e3-comp-8b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-13',
    pattern: '동분모 대분수 덧셈',
    paramRanges: { x: [1, 3], a: [1, 4], y: [1, 2], b: [1, 3], d: [5, 8] },
    constraints: (p) => p.a + p.b < p.d && p.a < p.d && p.b < p.d,
    contentFn: (p) => `${p.x} ${p.a}/${p.d} + ${p.y} ${p.b}/${p.d} = ?`,
    answerFn: (p) => `${p.x + p.y} ${p.a + p.b}/${p.d}`,
    distractorFns: [
      (p) => `${p.x + p.y}/${p.d}`,
      (p) => `${p.x + p.y} ${p.a + p.b}/${p.d * 2}`,
      (p) => `${p.x + p.y + 1} ${p.a + p.b}/${p.d}`,
    ],
    explanationFn: (p, ans) =>
      `① 자연수끼리: ${p.x} + ${p.y} = ${p.x + p.y}\n② 분수끼리: ${p.a}/${p.d} + ${p.b}/${p.d} = ${p.a + p.b}/${p.d}\n③ 결과: ${ans}`,
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-9a: 분수 뺄셈 (동분모)
  {
    id: 'e3-comp-9a',
    grade: G,
    category: 'computation',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-14',
    pattern: '동분모 분수 뺄셈',
    paramRanges: { a: [3, 8], b: [1, 5], d: [6, 12] },
    constraints: (p) => p.a > p.b && p.d > p.a,
    contentFn: (p) => `${p.a}/${p.d} - ${p.b}/${p.d} = ?`,
    answerFn: (p) => `${p.a - p.b}/${p.d}`,
    distractorFns: [
      (p) => `${p.a - p.b}/${p.d * 2}`,
      (p) => `${p.a}/${p.d - p.b}`,
      (p) => {
        const gcd = gcdHelper(p.a - p.b, p.d)
        return gcd > 1 ? `${(p.a - p.b) / gcd}/${p.d / gcd}` : `${p.a - p.b - 1}/${p.d}`
      },
    ],
    explanationFn: (p, ans) =>
      `① 분모가 같으면 분자끼리만 뺍니다\n② ${p.a} - ${p.b} = ${p.a - p.b}\n③ 분모는 그대로: ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-9b: 분수 뺄셈 (대분수)
  {
    id: 'e3-comp-9b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-14',
    pattern: '동분모 대분수 뺄셈',
    paramRanges: { x: [2, 5], a: [3, 6], y: [1, 3], b: [1, 4], d: [7, 10] },
    constraints: (p) => p.x > p.y && p.a > p.b && p.a < p.d && p.b < p.d,
    contentFn: (p) => `${p.x} ${p.a}/${p.d} - ${p.y} ${p.b}/${p.d} = ?`,
    answerFn: (p) => `${p.x - p.y} ${p.a - p.b}/${p.d}`,
    distractorFns: [
      (p) => `${p.x - p.y}/${p.d}`,
      (p) => `${p.x - p.y} ${p.a - p.b}/${p.d - 1}`,
      (p) => `${p.x - p.y - 1} ${p.a - p.b}/${p.d}`,
    ],
    explanationFn: (p, ans) =>
      `① 자연수끼리: ${p.x} - ${p.y} = ${p.x - p.y}\n② 분수끼리: ${p.a}/${p.d} - ${p.b}/${p.d} = ${p.a - p.b}/${p.d}\n③ 결과: ${ans}`,
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-10a: 곱셈 응용
  {
    id: 'e3-comp-10a',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-06',
    pattern: '곱셈 응용 (배열)',
    paramRanges: { x: [3, 8], y: [4, 9] },
    contentFn: (p) => `한 줄에 ${p.y}개씩 ${p.x}줄로 놓인 사과의 총 개수는?`,
    answerFn: (p) => p.x * p.y,
    distractorFns: [
      (p) => p.x + p.y,
      (p) => p.x * p.y + p.x,
      (p) => p.x * p.y - 1,
    ],
    explanationFn: (p, ans) =>
      `① 한 줄에 ${p.y}개씩 ${p.x}줄\n② ${p.x} × ${p.y} = ${ans}\n③ 곱셈은 같은 수를 여러 번 더하는 것`,
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-10b: 나눗셈 응용
  {
    id: 'e3-comp-10b',
    grade: G,
    category: 'computation',
    level: 10,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '나눗셈 응용 (똑같이 나누기)',
    paramRanges: { total: [20, 56], n: [3, 8] },
    constraints: (p) => p.total % p.n !== 0 && p.total > p.n,
    contentFn: (p) => `사탕 ${p.total}개를 ${p.n}명에게 똑같이 나누면 한 명당 몇 개씩 받고 몇 개가 남는가? (한 명당)`,
    answerFn: (p) => Math.floor(p.total / p.n),
    distractorFns: [
      (p) => p.total % p.n,
      (p) => Math.floor(p.total / p.n) + 1,
      (p) => p.n,
    ],
    explanationFn: (p, ans) => {
      const remainder = p.total % p.n
      return `① ${p.total} ÷ ${p.n} = ${ans} … ${remainder}\n② 한 명당 ${ans}개씩 받고 ${remainder}개가 남습니다\n③ 검산: ${p.n} × ${ans} + ${remainder} = ${p.total} ✓`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-11a: 가분수→대분수 변환 (NEW)
  {
    id: 'e3-comp-11a',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-11',
    pattern: '가분수를 대분수로',
    paramRanges: { a: [5, 15], b: [2, 6] },
    constraints: (p) => p.a > p.b && p.a % p.b !== 0,
    contentFn: (p) => `${p.a}/${p.b}을 대분수로 나타내면?`,
    answerFn: (p) => {
      const quotient = Math.floor(p.a / p.b)
      const remainder = p.a % p.b
      return `${quotient} ${remainder}/${p.b}`
    },
    distractorFns: [
      (p) => {
        const quotient = Math.floor(p.a / p.b) + 1
        const remainder = p.a % p.b
        return `${quotient} ${remainder}/${p.b}`
      },
      (p) => {
        const quotient = Math.floor(p.a / p.b)
        const remainder = p.a % p.b
        return `${remainder} ${quotient}/${p.b}`
      },
      (p) => `${Math.floor(p.a / p.b)}`,
    ],
    explanationFn: (p, ans) => {
      const quotient = Math.floor(p.a / p.b)
      const remainder = p.a % p.b
      return `① ${p.a} ÷ ${p.b} = ${quotient} … ${remainder}\n② 몫 ${quotient}이 자연수 부분, 나머지 ${remainder}가 분자\n③ 결과: ${ans}`
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-11b: 대분수→가분수 변환 (NEW)
  {
    id: 'e3-comp-11b',
    grade: G,
    category: 'computation',
    level: 7,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-12',
    pattern: '대분수를 가분수로',
    paramRanges: { a: [1, 5], b: [1, 5], c: [2, 7] },
    constraints: (p) => p.b < p.c,
    contentFn: (p) => `${p.a} ${p.b}/${p.c}을 가분수로 나타내면?`,
    answerFn: (p) => `${p.a * p.c + p.b}/${p.c}`,
    distractorFns: [
      (p) => `${p.a + p.b}/${p.c}`,
      (p) => `${p.a * p.c}/${p.c}`,
      (p) => `${p.a * p.b}/${p.c}`,
    ],
    explanationFn: (p, ans) =>
      `① ${p.a} × ${p.c} = ${p.a * p.c}\n② ${p.a * p.c} + ${p.b} = ${p.a * p.c + p.b}\n③ 결과: ${ans}`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-comp-12a: 소수 덧셈 (NEW)
  {
    id: 'e3-comp-12a',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-17',
    pattern: '소수 한자리 덧셈',
    paramRanges: { a: [1, 9], b: [1, 9], c: [1, 9], d: [1, 9] },
    constraints: (p) => (p.a * 10 + p.b) + (p.c * 10 + p.d) < 200,
    contentFn: (p) => `${p.a}.${p.b} + ${p.c}.${p.d} = ?`,
    answerFn: (p) => {
      const sum = (p.a * 10 + p.b) + (p.c * 10 + p.d)
      return `${Math.floor(sum / 10)}.${sum % 10}`
    },
    distractorFns: [
      (p) => `${p.a + p.c}.${p.b + p.d}`,
      (p) => {
        const sum = (p.a * 10 + p.b) + (p.c * 10 + p.d)
        return `${Math.floor(sum / 10) + 1}.${sum % 10}`
      },
      (p) => {
        const sum = (p.a * 10 + p.b) + (p.c * 10 + p.d)
        return `${sum % 10}.${Math.floor(sum / 10)}`
      },
    ],
    explanationFn: (p, ans) => {
      const decimalSum = p.b + p.d
      const carry = Math.floor(decimalSum / 10)
      return `① 소수점을 맞춰 세로로 씁니다\n② 0.${p.b} + 0.${p.d} = ${decimalSum >= 10 ? '1.' + (decimalSum % 10) : '0.' + decimalSum}\n③ ${p.a} + ${p.c}${carry > 0 ? ' + ' + carry : ''} = ${p.a + p.c + carry}\n④ 최종 답: ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-comp-12b: 소수 뺄셈 (NEW)
  {
    id: 'e3-comp-12b',
    grade: G,
    category: 'computation',
    level: 9,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-17',
    pattern: '소수 한자리 뺄셈',
    paramRanges: { a: [2, 9], b: [1, 9], c: [1, 8], d: [1, 9] },
    constraints: (p) => (p.a * 10 + p.b) > (p.c * 10 + p.d),
    contentFn: (p) => `${p.a}.${p.b} - ${p.c}.${p.d} = ?`,
    answerFn: (p) => {
      const diff = (p.a * 10 + p.b) - (p.c * 10 + p.d)
      return `${Math.floor(diff / 10)}.${diff % 10}`
    },
    distractorFns: [
      (p) => `${p.a - p.c}.${Math.abs(p.b - p.d)}`,
      (p) => {
        const diff = (p.a * 10 + p.b) - (p.c * 10 + p.d)
        return `${Math.floor(diff / 10) + 1}.${diff % 10}`
      },
      (p) => {
        const diff = (p.a * 10 + p.b) - (p.c * 10 + p.d)
        return `${Math.floor(diff / 10) - 1}.${diff % 10}`
      },
    ],
    explanationFn: (p, ans) => {
      const borrow = p.b < p.d ? 1 : 0
      return `① 소수점을 맞춰 세로로 씁니다\n② 소수 부분: ${p.b < p.d ? `${p.b} < ${p.d}이므로 받아내림` : `${p.b} - ${p.d} = ${p.b - p.d}`}\n③ 자연수 부분: ${p.a}${borrow > 0 ? ' - 1' : ''} - ${p.c} = ${p.a - borrow - p.c}\n④ 최종 답: ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },
]

// ============================================================================
// CONCEPT TEMPLATES (개념이해)
// ============================================================================

const conc: QuestionTemplate[] = [
  // e3-conc-1a: 분수 개념
  {
    id: 'e3-conc-1a',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '분수 읽기',
    paramRanges: { a: [1, 7], b: [2, 9] },
    constraints: (p) => p.a < p.b,
    contentFn: (p) => `${p.a}/${p.b}를 바르게 읽은 것은?`,
    answerFn: (p) => {
      const denominators = ['', '', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십']
      const numerators = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
      return `${denominators[p.b]}분의 ${numerators[p.a]}`
    },
    distractorFns: [
      (p) => {
        const denominators = ['', '', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십']
        const numerators = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
        return `${numerators[p.a]}분의 ${denominators[p.b]}`
      },
      (p) => `${p.a}분의 ${p.b}`,
      (p) => `${p.b}분의 ${p.a}`,
    ],
    explanationFn: (p, ans) =>
      `① 분수는 분모를 먼저 읽고 분자를 나중에 읽습니다\n② ${p.a}/${p.b} → ${ans}\n③ 분모가 전체를 나눈 개수, 분자가 그 중 선택한 개수`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-1b: 분수 쓰기
  {
    id: 'e3-conc-1b',
    grade: G,
    category: 'concept',
    level: 1,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-08',
    pattern: '분수 쓰기',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '전체를 4로 나눈 것 중 1을 분수로 나타내면?',
        '전체를 5로 나눈 것 중 3을 분수로 나타내면?',
        '사분의 일을 기호로 나타내면?',
        '오분의 삼을 기호로 나타내면?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['1/4', '3/5', '1/4', '3/5']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['4/1', '5/3', '4/1', '5/3']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['1/3', '3/4', '1/3', '3/4']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['4', '5', '4', '5']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 전체를 4로 나눈 것 → 분모 4\n② 그 중 1 → 분자 1\n③ 답: 1/4',
        '① 전체를 5로 나눈 것 → 분모 5\n② 그 중 3 → 분자 3\n③ 답: 3/5',
        '① 사분의 일 = 4로 나눈 것 중 1\n② 분모 4, 분자 1\n③ 답: 1/4',
        '① 오분의 삼 = 5로 나눈 것 중 3\n② 분모 5, 분자 3\n③ 답: 3/5',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-2a: 분수 크기 비교 개념
  {
    id: 'e3-conc-2a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-10',
    pattern: '분모 같은 분수 크기 비교 원리',
    paramRanges: { variant: [0, 2] },
    contentFn: (p) => {
      const questions = [
        '분모가 같은 분수를 비교할 때, 어느 것을 비교하면 되는가?',
        '3/7과 5/7 중 큰 것은?',
        '분모가 같은 분수에서 분자가 크면 전체적으로 어떻게 되는가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['분자', '5/7', '크다']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['분모', '3/7', '작다']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['분자와 분모 모두', '같다', '같다']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['알 수 없다', '비교 불가', '알 수 없다']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 분모가 같으면 전체를 나눈 크기가 같습니다\n② 따라서 분자만 비교하면 됩니다\n③ 분자가 클수록 큰 분수',
        '① 분모가 7로 같습니다\n② 분자 비교: 5 > 3\n③ 따라서 5/7 > 3/7',
        '① 분모가 같으면 한 조각의 크기가 같습니다\n② 분자가 크면 조각 개수가 많습니다\n③ 따라서 전체가 더 큽니다',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-2b: 진분수 개념
  {
    id: 'e3-conc-2b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-10',
    pattern: '진분수 판별',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '분자가 분모보다 작은 분수를 무엇이라 하는가?',
        '다음 중 진분수는? 2/3, 5/3, 7/7, 8/5',
        '진분수의 값은 항상 얼마보다 작은가?',
        '3/5는 어떤 종류의 분수인가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['진분수', '2/3', '1', '진분수']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['가분수', '5/3', '0', '가분수']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['대분수', '7/7', '분모', '대분수']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['자연수', '8/5', '분자', '자연수']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 분자 < 분모인 분수\n② 이를 진분수라 합니다\n③ 예: 1/2, 2/5, 3/7',
        '① 진분수는 분자 < 분모\n② 2/3: 2 < 3 ✓\n③ 나머지는 모두 분자 ≥ 분모',
        '① 진분수는 분자 < 분모\n② 따라서 값이 항상 1보다 작습니다\n③ 예: 1/2 = 0.5, 3/4 = 0.75',
        '① 3/5: 분자 3 < 분모 5\n② 분자가 분모보다 작음\n③ 따라서 진분수입니다',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-3a: 곱셈 원리
  {
    id: 'e3-conc-3a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-02',
    pattern: '곱셈의 의미',
    paramRanges: { a: [3, 7], b: [4, 9] },
    contentFn: (p) => `${p.a} × ${p.b}의 의미로 맞는 것은?`,
    answerFn: (p) => `${p.a}를 ${p.b}번 더한 것`,
    distractorFns: [
      (p) => `${p.b}를 ${p.a}번 뺀 것`,
      (p) => `${p.a}와 ${p.b}를 더한 것`,
      (p) => `${p.a}를 ${p.b}로 나눈 것`,
    ],
    explanationFn: (p, _ans) =>
      `① 곱셈은 같은 수를 여러 번 더하는 것\n② ${p.a} × ${p.b} = ${p.a} + ${p.a} + ... (${p.b}번)\n③ 또는 ${p.b}를 ${p.a}번 더한 것과 같음 (교환법칙)`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-3b: 곱셈표
  {
    id: 'e3-conc-3b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-02',
    pattern: '곱셈표 활용',
    paramRanges: { a: [2, 9], b: [2, 9] },
    contentFn: (p) => `${p.a}단에서 ${p.a} × ${p.b}는?`,
    answerFn: (p) => p.a * p.b,
    distractorFns: [
      (p) => p.a * p.b + p.a,
      (p) => p.a * p.b - p.a,
      (p) => p.a + p.b,
    ],
    explanationFn: (p, ans) =>
      `① ${p.a}단: ${p.a} × 1, ${p.a} × 2, ${p.a} × 3, ...\n② ${p.a} × ${p.b} = ${ans}\n③ 곱셈표를 외우면 빠르게 계산 가능`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-4a: 나눗셈 원리
  {
    id: 'e3-conc-4a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '나눗셈의 의미',
    paramRanges: { total: [12, 36], n: [3, 6] },
    constraints: (p) => p.total % p.n === 0,
    contentFn: (p) => `${p.total}개를 ${p.n}명에게 똑같이 나누면 한 명당 몇 개?`,
    answerFn: (p) => p.total / p.n,
    distractorFns: [
      (p) => p.total / p.n + 1,
      (p) => p.total - p.n,
      (p) => p.n,
    ],
    explanationFn: (p, ans) =>
      `① 나눗셈은 똑같이 나누는 것\n② ${p.total} ÷ ${p.n} = ${ans}\n③ ${p.n}명이 각각 ${ans}개씩 받음`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-4b: 나눗셈과 곱셈 관계
  {
    id: 'e3-conc-4b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-04',
    pattern: '나눗셈 검산 (곱셈)',
    paramRanges: { a: [4, 9], b: [3, 8] },
    contentFn: (p) => `${p.a * p.b} ÷ ${p.b}의 검산 방법은?`,
    answerFn: (p) => `${p.b} × ${p.a} = ${p.a * p.b}`,
    distractorFns: [
      (p) => `${p.a * p.b} - ${p.b} = ${p.a * p.b - p.b}`,
      (p) => `${p.a} + ${p.b} = ${p.a + p.b}`,
      (p) => `${p.a * p.b} ÷ ${p.a} = ${p.b}`,
    ],
    explanationFn: (p, _ans) =>
      `① 나눗셈 검산은 곱셈으로\n② ${p.a * p.b} ÷ ${p.b} = ${p.a}\n③ 검산: ${p.b} × ${p.a} = ${p.a * p.b} ✓`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-5a: 길이 단위
  {
    id: 'e3-conc-5a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-03',
    pattern: '길이 단위 환산 (km, m)',
    paramRanges: { x: [1, 5], y: [100, 900] },
    constraints: (p) => p.y % 100 === 0,
    contentFn: (p) => `${p.x}km ${p.y}m는 모두 몇 m인가?`,
    answerFn: (p) => p.x * 1000 + p.y,
    distractorFns: [
      (p) => p.x * 100 + p.y,
      (p) => p.x * 1000,
      (p) => p.x + p.y,
    ],
    explanationFn: (p, ans) =>
      `① 1km = 1000m\n② ${p.x}km = ${p.x * 1000}m\n③ ${p.x * 1000}m + ${p.y}m = ${ans}m`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-5b: 길이 단위 환산 (mm)
  {
    id: 'e3-conc-5b',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-03',
    pattern: '길이 단위 환산 (cm, mm)',
    paramRanges: { x: [2, 15], y: [10, 90] },
    constraints: (p) => p.y % 10 === 0,
    contentFn: (p) => `${p.x}cm ${p.y}mm는 모두 몇 mm인가?`,
    answerFn: (p) => p.x * 10 + p.y,
    distractorFns: [
      (p) => p.x * 100 + p.y,
      (p) => p.x + p.y,
      (p) => p.x * 10,
    ],
    explanationFn: (p, ans) =>
      `① 1cm = 10mm\n② ${p.x}cm = ${p.x * 10}mm\n③ ${p.x * 10}mm + ${p.y}mm = ${ans}mm`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-6a: 무게 단위
  {
    id: 'e3-conc-6a',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-04',
    pattern: '무게 단위 환산 (kg, g)',
    paramRanges: { x: [1, 8], y: [100, 900] },
    constraints: (p) => p.y % 100 === 0,
    contentFn: (p) => `${p.x}kg ${p.y}g은 모두 몇 g인가?`,
    answerFn: (p) => p.x * 1000 + p.y,
    distractorFns: [
      (p) => p.x * 100 + p.y,
      (p) => p.x + p.y,
      (p) => p.x * 1000,
    ],
    explanationFn: (p, ans) =>
      `① 1kg = 1000g\n② ${p.x}kg = ${p.x * 1000}g\n③ ${p.x * 1000}g + ${p.y}g = ${ans}g`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-6b: 무게 비교
  {
    id: 'e3-conc-6b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-04',
    pattern: '무게 비교',
    paramRanges: { a: [2, 5], b: [200, 800], c: [2, 5], d: [300, 900] },
    constraints: (p) => p.a * 1000 + p.b !== p.c * 1000 + p.d,
    contentFn: (p) => `${p.a}kg ${p.b}g과 ${p.c}kg ${p.d}g 중 더 무거운 것은?`,
    answerFn: (p) => {
      const w1 = p.a * 1000 + p.b
      const w2 = p.c * 1000 + p.d
      return w1 > w2 ? `${p.a}kg ${p.b}g` : `${p.c}kg ${p.d}g`
    },
    distractorFns: [
      (p) => {
        const w1 = p.a * 1000 + p.b
        const w2 = p.c * 1000 + p.d
        return w1 <= w2 ? `${p.a}kg ${p.b}g` : `${p.c}kg ${p.d}g`
      },
      () => '같다',
      (p) => `${Math.max(p.a, p.c)}kg ${Math.max(p.b, p.d)}g`,
    ],
    explanationFn: (p, ans) => {
      const w1 = p.a * 1000 + p.b
      const w2 = p.c * 1000 + p.d
      return `① ${p.a}kg ${p.b}g = ${w1}g\n② ${p.c}kg ${p.d}g = ${w2}g\n③ ${w1}g ${w1 > w2 ? '>' : '<'} ${w2}g이므로 ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-7a: 시각과 시간
  {
    id: 'e3-conc-7a',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-05',
    pattern: '시각과 시간의 차이',
    paramRanges: { variant: [0, 2] },
    contentFn: (p) => {
      const questions = [
        '시계가 가리키는 한 시점을 무엇이라 하는가?',
        '시각과 시각 사이의 길이를 무엇이라 하는가?',
        '\'3시 30분\'은 시각인가 시간인가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['시각', '시간', '시각']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['시간', '시각', '시간']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['시', '초', '분']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['분', '시', '초']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 시각: 특정한 한 시점\n② 예: 3시, 오후 2시 30분\n③ 시간: 시각과 시각 사이의 길이',
        '① 시간: 시각과 시각 사이의 길이\n② 예: 1시간 30분 동안\n③ 시각: 특정한 한 시점',
        '① 3시 30분은 특정한 한 시점\n② 따라서 시각입니다\n③ 시간은 "~동안"처럼 길이를 나타냄',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-7b: 시간 단위
  {
    id: 'e3-conc-7b',
    grade: G,
    category: 'concept',
    level: 7,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-05',
    pattern: '시간 단위 환산',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '1시간은 몇 분인가?',
        '1분은 몇 초인가?',
        '120분은 몇 시간인가?',
        '180초는 몇 분인가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['60', '60', '2', '3']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['100', '100', '1', '2']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['10', '10', '12', '18']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['24', '24', '120', '180']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 1시간 = 60분\n② 시간은 60진법을 사용\n③ 1시간 30분 = 90분',
        '① 1분 = 60초\n② 시간은 60진법을 사용\n③ 2분 30초 = 150초',
        '① 1시간 = 60분\n② 120분 ÷ 60 = 2시간\n③ 또는 120분 = 60분 + 60분 = 1시간 + 1시간',
        '① 1분 = 60초\n② 180초 ÷ 60 = 3분\n③ 또는 180초 = 60초 × 3',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-8a: 원 개념
  {
    id: 'e3-conc-8a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-02',
    pattern: '원의 구성 요소',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '원의 중심에서 원 위의 한 점까지의 선분을 무엇이라 하는가?',
        '원 위의 두 점을 이은 선분 중 원의 중심을 지나는 것을 무엇이라 하는가?',
        '지름은 반지름의 몇 배인가?',
        '컴퍼스로 원을 그릴 때 변하지 않는 길이는?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['반지름', '지름', '2', '반지름']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['지름', '반지름', '1', '지름']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['현', '현', '3', '중심']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['호', '호', '4', '원둘레']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 원의 중심 → 원 위의 점\n② 이 선분을 반지름이라 합니다\n③ 같은 원의 모든 반지름은 길이가 같음',
        '① 원 위의 두 점을 이은 선분 = 현\n② 그 중 원의 중심을 지나는 것 = 지름\n③ 지름은 가장 긴 현',
        '① 지름 = 반지름 × 2\n② 지름은 반지름의 2배\n③ 반지름 = 지름 ÷ 2',
        '① 컴퍼스의 침과 연필 사이 거리 = 반지름\n② 이 길이가 변하지 않아야 원을 그릴 수 있음\n③ 반지름이 같으면 같은 크기의 원',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-8b: 원 그리기
  {
    id: 'e3-conc-8b',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-02',
    pattern: '원 그리기 방법',
    paramRanges: { n: [3, 8] },
    contentFn: (p) => `반지름이 ${p.n}cm인 원을 그리려면 컴퍼스를 몇 cm로 벌려야 하는가?`,
    answerFn: (p) => p.n,
    distractorFns: [
      (p) => p.n * 2,
      (p) => p.n + 1,
      (p) => p.n - 1,
    ],
    explanationFn: (p, ans) =>
      `① 컴퍼스의 침과 연필 사이 거리 = 반지름\n② 반지름 ${p.n}cm인 원\n③ 컴퍼스를 ${ans}cm로 벌림`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-9a: 들이 단위
  {
    id: 'e3-conc-9a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-06',
    pattern: '들이 단위 환산 (L, mL)',
    paramRanges: { x: [1, 5], y: [100, 900] },
    constraints: (p) => p.y % 100 === 0,
    contentFn: (p) => `${p.x}L ${p.y}mL는 모두 몇 mL인가?`,
    answerFn: (p) => p.x * 1000 + p.y,
    distractorFns: [
      (p) => p.x * 100 + p.y,
      (p) => p.x + p.y,
      (p) => p.x * 1000,
    ],
    explanationFn: (p, ans) =>
      `① 1L = 1000mL\n② ${p.x}L = ${p.x * 1000}mL\n③ ${p.x * 1000}mL + ${p.y}mL = ${ans}mL`,
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-9b: 들이 비교
  {
    id: 'e3-conc-9b',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-06',
    pattern: '들이 비교',
    paramRanges: { a: [1, 4], b: [200, 800], c: [1, 4], d: [300, 900] },
    constraints: (p) => p.a * 1000 + p.b !== p.c * 1000 + p.d,
    contentFn: (p) => `${p.a}L ${p.b}mL와 ${p.c}L ${p.d}mL 중 더 많은 것은?`,
    answerFn: (p) => {
      const v1 = p.a * 1000 + p.b
      const v2 = p.c * 1000 + p.d
      return v1 > v2 ? `${p.a}L ${p.b}mL` : `${p.c}L ${p.d}mL`
    },
    distractorFns: [
      (p) => {
        const v1 = p.a * 1000 + p.b
        const v2 = p.c * 1000 + p.d
        return v1 <= v2 ? `${p.a}L ${p.b}mL` : `${p.c}L ${p.d}mL`
      },
      () => '같다',
      (p) => `${Math.max(p.a, p.c)}L ${Math.max(p.b, p.d)}mL`,
    ],
    explanationFn: (p, ans) => {
      const v1 = p.a * 1000 + p.b
      const v2 = p.c * 1000 + p.d
      return `① ${p.a}L ${p.b}mL = ${v1}mL\n② ${p.c}L ${p.d}mL = ${v2}mL\n③ ${v1}mL ${v1 > v2 ? '>' : '<'} ${v2}mL이므로 ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-10a: 표와 그래프
  {
    id: 'e3-conc-10a',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'data' as ProblemPart,
    conceptId: 'E3-STA-01',
    pattern: '표 읽기',
    paramRanges: { a: [5, 12], b: [3, 10], c: [7, 15] },
    contentFn: (p) => `좋아하는 과일 조사 결과 - 사과: ${p.a}명, 바나나: ${p.b}명, 포도: ${p.c}명. 가장 많이 좋아하는 과일은?`,
    answerFn: (p) => {
      const max = Math.max(p.a, p.b, p.c)
      if (max === p.a) return '사과'
      if (max === p.b) return '바나나'
      return '포도'
    },
    distractorFns: [
      (p) => {
        const min = Math.min(p.a, p.b, p.c)
        if (min === p.a) return '사과'
        if (min === p.b) return '바나나'
        return '포도'
      },
      (p) => {
        const vals = [p.a, p.b, p.c]
        vals.sort((x, y) => x - y)
        const mid = vals[1]
        if (mid === p.a) return '사과'
        if (mid === p.b) return '바나나'
        return '포도'
      },
      () => '같다',
    ],
    explanationFn: (p, ans) => {
      const max = Math.max(p.a, p.b, p.c)
      return `① 사과: ${p.a}명, 바나나: ${p.b}명, 포도: ${p.c}명\n② 가장 큰 수는 ${max}명\n③ 따라서 ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-10b: 그래프 해석
  {
    id: 'e3-conc-10b',
    grade: G,
    category: 'concept',
    level: 10,
    part: 'data' as ProblemPart,
    conceptId: 'E3-STA-01',
    pattern: '그림그래프 해석',
    paramRanges: { x: [2, 5], y: [0, 9] },
    contentFn: (p) => `그림그래프에서 큰 그림 1개는 10을 나타냅니다. 큰 그림 ${p.x}개와 작은 그림 ${p.y}개는 모두 얼마를 나타내는가?`,
    answerFn: (p) => p.x * 10 + p.y,
    distractorFns: [
      (p) => p.x + p.y,
      (p) => p.x * 10,
      (p) => p.x * p.y,
    ],
    explanationFn: (p, ans) =>
      `① 큰 그림 1개 = 10\n② 큰 그림 ${p.x}개 = ${p.x * 10}\n③ 작은 그림 ${p.y}개 = ${p.y}\n④ 합계 = ${ans}`,
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-11a: 단위분수 비교 (NEW)
  {
    id: 'e3-conc-11a',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-09',
    pattern: '단위분수 크기 비교',
    paramRanges: { a: [2, 6], b: [3, 9] },
    constraints: (p) => p.a !== p.b && p.a < p.b,
    contentFn: (p) => `1/${p.a}과 1/${p.b} 중 큰 것은?`,
    answerFn: (p) => `1/${p.a}`,
    distractorFns: [
      (p) => `1/${p.b}`,
      (p) => `1/${p.a + p.b}`,
      (p) => `${p.a}/${p.b}`,
    ],
    explanationFn: (p, _ans) =>
      `① 단위분수는 분자가 모두 1입니다\n② 분모가 작을수록 한 조각이 크므로 1/${p.a} > 1/${p.b}\n③ 흔한 실수: 분모가 클수록 크다고 착각하기 쉽습니다`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-11b: 단위분수 개념 (NEW)
  {
    id: 'e3-conc-11b',
    grade: G,
    category: 'concept',
    level: 2,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-09',
    pattern: '단위분수 개념',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '분자가 1인 분수를 무엇이라 하는가?',
        '단위분수 1/4는 전체를 몇으로 나눈 것 중 하나인가?',
        '1/3과 1/5 중 큰 것은?',
        '단위분수가 아닌 것은? (보기: 1/2, 2/3, 1/7, 1/10)',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['단위분수', '4', '1/3', '2/3']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['진분수', '1', '1/5', '1/2']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['가분수', '2', '같다', '1/7']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['자연수', '8', '비교 불가', '1/10']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 분자가 1인 분수를 단위분수라 합니다\n② 예: 1/2, 1/3, 1/4, 1/5\n③ 전체를 똑같이 나눈 것 중 하나',
        '① 1/4는 전체를 4로 나눈 것 중 1\n② 분모가 나눈 개수\n③ 단위분수는 기본 단위',
        '① 1/3과 1/5는 모두 단위분수\n② 분모가 작을수록 크므로 1/3 > 1/5\n③ 3조각 vs 5조각 → 3조각이 더 큼',
        '① 단위분수는 분자가 1\n② 2/3은 분자가 2이므로 단위분수가 아님\n③ 나머지는 모두 분자가 1',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-12a: 가분수 판별 (NEW)
  {
    id: 'e3-conc-12a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-11',
    pattern: '가분수 판별',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '분자가 분모보다 크거나 같은 분수를 무엇이라 하는가?',
        '다음 중 가분수는? 2/3, 5/3, 1/4, 3/7',
        '7/4는 어떤 종류의 분수인가?',
        '가분수의 특징은?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['가분수', '5/3', '가분수', '분자 ≥ 분모']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['진분수', '2/3', '진분수', '분자 < 분모']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['대분수', '1/4', '대분수', '자연수 + 분수']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['단위분수', '3/7', '단위분수', '분자 = 1']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 분자 ≥ 분모인 분수를 가분수라 합니다\n② 예: 5/3, 7/4, 9/9\n③ 가분수는 1보다 크거나 같음',
        '① 가분수는 분자 ≥ 분모\n② 5/3: 5 ≥ 3 ✓\n③ 나머지는 모두 분자 < 분모 (진분수)',
        '① 7/4: 분자 7 ≥ 분모 4\n② 분자가 분모보다 큼\n③ 따라서 가분수입니다',
        '① 가분수는 분자 ≥ 분모\n② 값이 1보다 크거나 같음\n③ 대분수로 나타낼 수 있음',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-12b: 가분수→대분수 개념 (NEW)
  {
    id: 'e3-conc-12b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-11',
    pattern: '가분수를 대분수로 변환',
    paramRanges: { a: [5, 11], b: [2, 5] },
    constraints: (p) => p.a > p.b && p.a % p.b !== 0,
    contentFn: (p) => `${p.a}/${p.b}를 대분수로 나타내면?`,
    answerFn: (p) => {
      const quotient = Math.floor(p.a / p.b)
      const remainder = p.a % p.b
      return `${quotient} ${remainder}/${p.b}`
    },
    distractorFns: [
      (p) => {
        const quotient = Math.floor(p.a / p.b) + 1
        const remainder = p.a % p.b
        return `${quotient} ${remainder}/${p.b}`
      },
      (p) => {
        const quotient = Math.floor(p.a / p.b)
        const remainder = p.a % p.b
        return `${remainder} ${quotient}/${p.b}`
      },
      (p) => `${Math.floor(p.a / p.b)}`,
    ],
    explanationFn: (p, ans) => {
      const quotient = Math.floor(p.a / p.b)
      const remainder = p.a % p.b
      return `① ${p.a} ÷ ${p.b} = ${quotient} … ${remainder}\n② 자연수: ${quotient}, 분수: ${remainder}/${p.b}\n③ 대분수: ${ans}`
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-13a: 대분수 개념 (NEW)
  {
    id: 'e3-conc-13a',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-12',
    pattern: '대분수 개념',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '자연수와 진분수로 이루어진 분수를 무엇이라 하는가?',
        '1 2/3은 어떤 종류의 분수인가?',
        '대분수 2 3/5에서 자연수 부분은?',
        '대분수를 가분수로 바꾸는 방법은?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['대분수', '대분수', '2', '자연수×분모+분자']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['가분수', '가분수', '3', '분자×분모+자연수']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['진분수', '진분수', '5', '자연수+분자']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['단위분수', '단위분수', '2/3', '분자÷분모']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 자연수 + 진분수 형태를 대분수라 합니다\n② 예: 1 2/3, 2 3/5, 5 1/4\n③ 진분수는 분자 < 분모',
        '① 1 2/3 = 자연수 1 + 진분수 2/3\n② 자연수와 진분수로 이루어짐\n③ 따라서 대분수입니다',
        '① 대분수 2 3/5\n② 자연수 부분은 앞의 2\n③ 분수 부분은 3/5',
        '① 대분수 → 가분수: (자연수 × 분모) + 분자\n② 예: 2 3/5 = (2×5+3)/5 = 13/5\n③ 분모는 그대로',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-13b: 대분수→가분수 개념 (NEW)
  {
    id: 'e3-conc-13b',
    grade: G,
    category: 'concept',
    level: 3,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-12',
    pattern: '대분수를 가분수로 변환',
    paramRanges: { a: [1, 4], b: [1, 5], c: [2, 7] },
    constraints: (p) => p.b < p.c,
    contentFn: (p) => `${p.a} ${p.b}/${p.c}를 가분수로 나타내면?`,
    answerFn: (p) => `${p.a * p.c + p.b}/${p.c}`,
    distractorFns: [
      (p) => `${p.a + p.b}/${p.c}`,
      (p) => `${p.a * p.c}/${p.c}`,
      (p) => `${p.a * p.b}/${p.c}`,
    ],
    explanationFn: (p, ans) =>
      `① 자연수 × 분모: ${p.a} × ${p.c} = ${p.a * p.c}\n② 결과에 분자 더하기: ${p.a * p.c} + ${p.b} = ${p.a * p.c + p.b}\n③ 분모는 그대로: ${ans}`,
    questionType: 'multiple_choice',
    points: 3,
  },

  // e3-conc-14a: 소수 0.1 개념 (NEW)
  {
    id: 'e3-conc-14a',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-15',
    pattern: '소수 0.1의 의미',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '0.1은 1을 몇으로 나눈 것 중 하나인가?',
        '0.1이 3개이면 얼마인가?',
        '1/10을 소수로 나타내면?',
        '0.7은 0.1이 몇 개인가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['10', '0.3', '0.1', '7']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['100', '0.03', '0.01', '0.7']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['2', '3', '1/10', '10']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['1', '0.13', '0.10', '70']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 0.1 = 1/10\n② 1을 10으로 나눈 것 중 1\n③ 따라서 답은 10',
        '① 0.1 × 3 = 0.3\n② 또는 1/10 + 1/10 + 1/10 = 3/10 = 0.3\n③ 0.1이 3개 = 0.3',
        '① 1/10 = 1 ÷ 10\n② 소수로 나타내면 0.1\n③ 분수 1/10 = 소수 0.1',
        '① 0.7 = 7/10\n② 7/10 = 1/10 + 1/10 + ... (7개)\n③ 0.1이 7개 = 0.7',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-14b: 소수 읽기 (NEW)
  {
    id: 'e3-conc-14b',
    grade: G,
    category: 'concept',
    level: 4,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-16',
    pattern: '소수 읽기',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '3.5를 바르게 읽은 것은?',
        '2.7을 바르게 읽은 것은?',
        '4.9를 바르게 읽은 것은?',
        '1.2를 바르게 읽은 것은?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['삼 점 오', '이 점 칠', '사 점 구', '일 점 이']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['삼점오', '이점칠', '사점구', '일점이']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['삼과 오', '이와 칠', '사와 구', '일과 이']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['삼 쉼표 오', '이 쉼표 칠', '사 쉼표 구', '일 쉼표 이']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 3.5는 "삼 점 오"로 읽습니다\n② 소수점은 "점"으로 읽음\n③ 자연수 부분과 소수 부분을 나누어 읽음',
        '① 2.7은 "이 점 칠"로 읽습니다\n② 소수점은 "점"으로 읽음\n③ 자연수 부분과 소수 부분을 나누어 읽음',
        '① 4.9는 "사 점 구"로 읽습니다\n② 소수점은 "점"으로 읽음\n③ 자연수 부분과 소수 부분을 나누어 읽음',
        '① 1.2는 "일 점 이"로 읽습니다\n② 소수점은 "점"으로 읽음\n③ 자연수 부분과 소수 부분을 나누어 읽음',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 4,
  },

  // e3-conc-15a: 선분/반직선/직선 (NEW)
  {
    id: 'e3-conc-15a',
    grade: G,
    category: 'concept',
    level: 5,
    part: 'geo' as ProblemPart,
    conceptId: 'E3-GEO-01',
    pattern: '선분, 반직선, 직선 개념',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '두 점을 곧게 이은 선을 무엇이라 하는가?',
        '한 점에서 한 방향으로 끝없이 뻗은 선은?',
        '양쪽으로 끝없이 뻗은 선은?',
        '반직선 AB와 반직선 BA는 같은가?',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['선분', '반직선', '직선', '다르다']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['반직선', '직선', '반직선', '같다']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['직선', '선분', '선분', '알 수 없다']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['곡선', '곡선', '곡선', '비교 불가']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 두 점을 곧게 이은 선 = 선분\n② 선분은 양 끝이 있음\n③ 길이를 잴 수 있음',
        '① 한 점에서 한 방향으로만 끝없이 뻗은 선 = 반직선\n② 시작점은 있지만 끝점은 없음\n③ 길이를 잴 수 없음',
        '① 양쪽으로 끝없이 뻗은 선 = 직선\n② 시작점과 끝점 모두 없음\n③ 길이를 잴 수 없음',
        '① 반직선 AB: A에서 시작해 B 방향으로\n② 반직선 BA: B에서 시작해 A 방향으로\n③ 시작점과 방향이 다르므로 다릅니다',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-15b: 시간 연산 60진법 덧셈 (NEW)
  {
    id: 'e3-conc-15b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-GEO-05',
    pattern: '시간 덧셈 (60진법)',
    paramRanges: { a: [1, 10], b: [30, 55], c: [10, 40] },
    constraints: (p) => p.b + p.c >= 60,
    contentFn: (p) => `${p.a}시 ${p.b}분 + ${p.c}분 = ?`,
    answerFn: (p) => {
      const totalMin = p.b + p.c
      const hours = p.a + Math.floor(totalMin / 60)
      const mins = totalMin % 60
      return `${hours}시 ${mins}분`
    },
    distractorFns: [
      (p) => `${p.a}시 ${p.b + p.c}분`,
      (p) => {
        const totalMin = p.b + p.c
        const hours = p.a + 1
        const mins = totalMin - 60 + 10
        return `${hours}시 ${mins}분`
      },
      (p) => {
        const totalMin = p.b + p.c
        const hours = p.a
        const mins = totalMin - 100
        return `${hours}시 ${Math.abs(mins)}분`
      },
    ],
    explanationFn: (p, ans) => {
      const totalMin = p.b + p.c
      const carry = Math.floor(totalMin / 60)
      const mins = totalMin % 60
      return `① ${p.b}분 + ${p.c}분 = ${totalMin}분\n② ${totalMin}분 = ${carry}시간 ${mins}분\n③ ${p.a}시 + ${carry}시간 = ${p.a + carry}시, ${mins}분 → ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-16b: 시간 연산 60진법 뺄셈 (NEW)
  {
    id: 'e3-conc-16b',
    grade: G,
    category: 'concept',
    level: 6,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-GEO-05',
    pattern: '시간 뺄셈 (60진법)',
    paramRanges: { a: [2, 11], b: [5, 25], c: [30, 50] },
    constraints: (p) => p.b < p.c && p.a >= 2,
    contentFn: (p) => `${p.a}시 ${p.b}분 - ${p.c}분 = ?`,
    answerFn: (p) => {
      const totalMin = p.a * 60 + p.b - p.c
      const hours = Math.floor(totalMin / 60)
      const mins = totalMin % 60
      return `${hours}시 ${mins}분`
    },
    distractorFns: [
      (p) => `${p.a}시 ${p.c - p.b}분`,
      (p) => {
        const mins = 100 - p.c + p.b
        return `${p.a - 1}시 ${mins}분`
      },
      (p) => {
        const totalMin = p.a * 60 + p.b - p.c
        const hours = Math.floor(totalMin / 60) + 1
        const mins = totalMin % 60
        return `${hours}시 ${mins}분`
      },
    ],
    explanationFn: (p, ans) => {
      return `① ${p.b}분 < ${p.c}분이므로 1시간 = 60분을 빌림\n② (${p.a - 1})시 (${p.b + 60})분 - ${p.c}분\n③ ${p.a - 1}시 ${p.b + 60 - p.c}분 = ${ans}`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-17a: 나눗셈 검산 (NEW)
  {
    id: 'e3-conc-17a',
    grade: G,
    category: 'concept',
    level: 8,
    part: 'calc' as ProblemPart,
    conceptId: 'E3-NUM-05',
    pattern: '나눗셈 검산식',
    paramRanges: { n: [15, 50], b: [3, 8] },
    constraints: (p) => p.n % p.b !== 0 && p.n > p.b,
    contentFn: (p) => `${p.n} ÷ ${p.b}의 검산식을 완성하시오. ${p.b} × □ + △ = ${p.n}에서 □는?`,
    answerFn: (p) => Math.floor(p.n / p.b),
    distractorFns: [
      (p) => Math.floor(p.n / p.b) + 1,
      (p) => p.n % p.b,
      (p) => p.b,
    ],
    explanationFn: (p, _ans) => {
      const quotient = Math.floor(p.n / p.b)
      const remainder = p.n % p.b
      return `① ${p.n} ÷ ${p.b} = ${quotient} … ${remainder}\n② 검산: 나누는 수 × 몫 + 나머지 = 나누어지는 수\n③ ${p.b} × ${quotient} + ${remainder} = ${p.n} ✓`
    },
    questionType: 'multiple_choice',
    points: 5,
  },

  // e3-conc-18a: 그림그래프 (NEW)
  {
    id: 'e3-conc-18a',
    grade: G,
    category: 'concept',
    level: 9,
    part: 'data' as ProblemPart,
    conceptId: 'E3-STA-01',
    pattern: '그림그래프 해석',
    paramRanges: { variant: [0, 3] },
    contentFn: (p) => {
      const questions = [
        '그림그래프에서 큰 그림 3개와 작은 그림 5개는 모두 얼마인가? (큰 그림 1개 = 10)',
        '그림그래프에서 큰 그림 1개가 10을 나타낼 때, 작은 그림 1개는 얼마를 나타내는가?',
        '큰 그림 4개는 얼마를 나타내는가? (큰 그림 1개 = 10)',
        '35를 큰 그림과 작은 그림으로 나타내면? (큰 그림 1개 = 10)',
      ]
      return questions[p.variant]!
    },
    answerFn: (p) => {
      const answers = ['35', '1', '40', '큰 그림 3개, 작은 그림 5개']
      return answers[p.variant]!
    },
    distractorFns: [
      (p) => {
        const d1 = ['8', '10', '4', '큰 그림 35개']
        return d1[p.variant]!
      },
      (p) => {
        const d2 = ['30', '5', '14', '큰 그림 3개, 작은 그림 50개']
        return d2[p.variant]!
      },
      (p) => {
        const d3 = ['50', '0.1', '400', '작은 그림 35개']
        return d3[p.variant]!
      },
    ],
    explanationFn: (p, _ans) => {
      const explanations = [
        '① 큰 그림 3개 = 10 × 3 = 30\n② 작은 그림 5개 = 1 × 5 = 5\n③ 합계 = 30 + 5 = 35',
        '① 큰 그림 1개 = 10\n② 작은 그림은 큰 그림의 1/10\n③ 작은 그림 1개 = 1',
        '① 큰 그림 1개 = 10\n② 큰 그림 4개 = 10 × 4\n③ = 40',
        '① 35 = 30 + 5\n② 30 = 큰 그림 3개\n③ 5 = 작은 그림 5개',
      ]
      return explanations[p.variant]!
    },
    questionType: 'multiple_choice',
    points: 5,
  },
]

// ============================================================================
// EXPORT
// ============================================================================

export const elementary3Templates: QuestionTemplate[] = [...comp, ...conc]
