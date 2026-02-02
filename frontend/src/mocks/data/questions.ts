// Mock 문제 데이터

import type { Concept, Question, Test, TestAttempt } from '../../types'

export const mockConcepts: Concept[] = [
  {
    id: 'concept-1',
    name: '정수의 덧셈과 뺄셈',
    grade: 'middle_1',
    category: 'computation',
    part: 'calc',
    description: '양수와 음수를 포함한 정수의 덧셈과 뺄셈을 학습합니다.',
  },
  {
    id: 'concept-2',
    name: '일차방정식',
    grade: 'middle_1',
    category: 'concept',
    part: 'algebra',
    description: '미지수가 하나인 일차방정식의 풀이법을 학습합니다.',
  },
  {
    id: 'concept-3',
    name: '좌표평면',
    grade: 'middle_1',
    category: 'concept',
    part: 'func',
    description: '좌표평면 위의 점의 위치를 나타내는 방법을 학습합니다.',
  },
]

export const mockQuestions: Question[] = [
  {
    id: 'q1',
    concept_id: 'concept-1',
    category: 'computation',
    part: 'calc',
    question_type: 'multiple_choice',
    difficulty: 5,
    content: '(-3) + 5 의 값은?',
    options: [
      { id: '1', label: 'A', text: '2' },
      { id: '2', label: 'B', text: '-2' },
      { id: '3', label: 'C', text: '8' },
      { id: '4', label: 'D', text: '-8' },
    ],
    correct_answer: 'A',
    explanation: '(-3) + 5 = 5 - 3 = 2 입니다.',
    points: 10,
  },
  {
    id: 'q2',
    concept_id: 'concept-1',
    category: 'computation',
    part: 'calc',
    question_type: 'multiple_choice',
    difficulty: 5,
    content: '(-7) - (-4) 의 값은?',
    options: [
      { id: '1', label: 'A', text: '-11' },
      { id: '2', label: 'B', text: '-3' },
      { id: '3', label: 'C', text: '3' },
      { id: '4', label: 'D', text: '11' },
    ],
    correct_answer: 'B',
    explanation: '(-7) - (-4) = -7 + 4 = -3 입니다.',
    points: 10,
  },
  {
    id: 'q3',
    concept_id: 'concept-2',
    category: 'concept',
    part: 'algebra',
    question_type: 'multiple_choice',
    difficulty: 6,
    content: '다음 중 일차방정식인 것은?',
    options: [
      { id: '1', label: 'A', text: 'x + 3' },
      { id: '2', label: 'B', text: '2x - 1 = 5' },
      { id: '3', label: 'C', text: 'x² = 4' },
      { id: '4', label: 'D', text: 'x + y = 3' },
    ],
    correct_answer: 'B',
    explanation:
      '일차방정식은 미지수가 1개이고 차수가 1인 등식입니다. 2x - 1 = 5만 이 조건을 만족합니다.',
    points: 10,
  },
  {
    id: 'q4',
    concept_id: 'concept-2',
    category: 'concept',
    part: 'algebra',
    question_type: 'multiple_choice',
    difficulty: 7,
    content: "일차방정식의 풀이에서 '이항'이란?",
    options: [
      { id: '1', label: 'A', text: '등호 양변에 같은 수를 더하는 것' },
      { id: '2', label: 'B', text: '항을 등호의 반대편으로 부호를 바꿔 옮기는 것' },
      { id: '3', label: 'C', text: '미지수끼리 모으는 것' },
      { id: '4', label: 'D', text: '양변을 같은 수로 나누는 것' },
    ],
    correct_answer: 'B',
    explanation:
      '이항이란 등식에서 한 항을 부호를 바꾸어 반대편으로 옮기는 것입니다.',
    points: 10,
  },
  {
    id: 'q5',
    concept_id: 'concept-3',
    category: 'concept',
    part: 'func',
    question_type: 'multiple_choice',
    difficulty: 6,
    content:
      '좌표평면에서 x좌표가 양수이고 y좌표가 음수인 점은 어느 사분면에 위치하는가?',
    options: [
      { id: '1', label: 'A', text: '제1사분면' },
      { id: '2', label: 'B', text: '제2사분면' },
      { id: '3', label: 'C', text: '제3사분면' },
      { id: '4', label: 'D', text: '제4사분면' },
    ],
    correct_answer: 'D',
    explanation:
      '제4사분면은 x > 0, y < 0인 영역입니다. 제1사분면(+,+), 제2사분면(-,+), 제3사분면(-,-), 제4사분면(+,-)로 구분합니다.',
    points: 10,
  },
]

export const mockTests: Test[] = [
  {
    id: 'test-1',
    title: '중1 정수 기초 테스트',
    description: '정수의 덧셈과 뺄셈 기초 문제입니다.',
    grade: 'middle_1',
    category: 'computation',
    concept_ids: ['concept-1'],
    question_count: 2,
    time_limit_minutes: 10,
    is_active: true,
    is_adaptive: false,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'test-2',
    title: '중1 일차방정식 테스트',
    description: '일차방정식 풀이 연습 문제입니다.',
    grade: 'middle_1',
    category: 'concept',
    concept_ids: ['concept-2'],
    question_count: 2,
    time_limit_minutes: 15,
    is_active: true,
    is_adaptive: false,
    created_at: '2024-01-02T00:00:00Z',
  },
  {
    id: 'test-3',
    title: '중1 종합 테스트',
    description: '중1 1학기 종합 문제입니다.',
    grade: 'middle_1',
    concept_ids: ['concept-1', 'concept-2', 'concept-3'],
    question_count: 5,
    time_limit_minutes: 30,
    is_active: true,
    is_adaptive: false,
    created_at: '2024-01-03T00:00:00Z',
  },
]

export const mockAttempts: TestAttempt[] = [
  {
    id: 'attempt-1',
    test_id: 'test-1',
    student_id: 'student-1',
    started_at: '2024-01-10T10:00:00Z',
    completed_at: '2024-01-10T10:08:00Z',
    score: 20,
    max_score: 20,
    correct_count: 2,
    total_count: 2,
    xp_earned: 25,
    combo_max: 2,
    is_adaptive: false,
  },
]

export function getTestById(id: string): Test | undefined {
  return mockTests.find((test) => test.id === id)
}

export function getQuestionsForTest(testId: string): Question[] {
  const test = getTestById(testId)
  if (!test) return []

  return mockQuestions.filter((q) => test.concept_ids.includes(q.concept_id))
}

export function getQuestionById(id: string): Question | undefined {
  return mockQuestions.find((q) => q.id === id)
}
