// Mock 문제 데이터

import type { Concept, Question, Test, TestAttempt } from '../../types'

export const mockConcepts: Concept[] = [
  {
    id: 'concept-1',
    name: '정수의 덧셈과 뺄셈',
    grade: 'middle_1',
    description: '양수와 음수를 포함한 정수의 덧셈과 뺄셈을 학습합니다.',
  },
  {
    id: 'concept-2',
    name: '일차방정식',
    grade: 'middle_1',
    description: '미지수가 하나인 일차방정식의 풀이법을 학습합니다.',
  },
  {
    id: 'concept-3',
    name: '좌표평면',
    grade: 'middle_1',
    description: '좌표평면 위의 점의 위치를 나타내는 방법을 학습합니다.',
  },
]

export const mockQuestions: Question[] = [
  {
    id: 'q1',
    concept_id: 'concept-1',
    question_type: 'multiple_choice',
    difficulty: 'easy',
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
    question_type: 'multiple_choice',
    difficulty: 'medium',
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
    question_type: 'multiple_choice',
    difficulty: 'easy',
    content: 'x + 5 = 12 일 때, x의 값은?',
    options: [
      { id: '1', label: 'A', text: '5' },
      { id: '2', label: 'B', text: '7' },
      { id: '3', label: 'C', text: '12' },
      { id: '4', label: 'D', text: '17' },
    ],
    correct_answer: 'B',
    explanation: 'x = 12 - 5 = 7 입니다.',
    points: 10,
  },
  {
    id: 'q4',
    concept_id: 'concept-2',
    question_type: 'multiple_choice',
    difficulty: 'medium',
    content: '2x - 3 = 7 일 때, x의 값은?',
    options: [
      { id: '1', label: 'A', text: '2' },
      { id: '2', label: 'B', text: '5' },
      { id: '3', label: 'C', text: '7' },
      { id: '4', label: 'D', text: '10' },
    ],
    correct_answer: 'B',
    explanation: '2x = 10, x = 5 입니다.',
    points: 10,
  },
  {
    id: 'q5',
    concept_id: 'concept-3',
    question_type: 'multiple_choice',
    difficulty: 'easy',
    content: '점 (3, -2)는 어느 사분면에 있는가?',
    options: [
      { id: '1', label: 'A', text: '제1사분면' },
      { id: '2', label: 'B', text: '제2사분면' },
      { id: '3', label: 'C', text: '제3사분면' },
      { id: '4', label: 'D', text: '제4사분면' },
    ],
    correct_answer: 'D',
    explanation: 'x좌표가 양수이고 y좌표가 음수이면 제4사분면입니다.',
    points: 10,
  },
]

export const mockTests: Test[] = [
  {
    id: 'test-1',
    title: '중1 정수 기초 테스트',
    description: '정수의 덧셈과 뺄셈 기초 문제입니다.',
    grade: 'middle_1',
    concept_ids: ['concept-1'],
    question_count: 2,
    time_limit_minutes: 10,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'test-2',
    title: '중1 일차방정식 테스트',
    description: '일차방정식 풀이 연습 문제입니다.',
    grade: 'middle_1',
    concept_ids: ['concept-2'],
    question_count: 2,
    time_limit_minutes: 15,
    is_active: true,
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
