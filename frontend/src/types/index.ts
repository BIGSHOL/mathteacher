// 타입 정의

export type UserRole = 'student' | 'teacher' | 'admin'

export type Grade =
  | 'elementary_1'
  | 'elementary_2'
  | 'elementary_3'
  | 'elementary_4'
  | 'elementary_5'
  | 'elementary_6'
  | 'middle_1'
  | 'middle_2'
  | 'middle_3'
  | 'high_1'

export type QuestionType = 'multiple_choice' | 'true_false' | 'short_answer'

export type Difficulty = 'easy' | 'medium' | 'hard'

// API 응답 타입
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

export interface ErrorResponse {
  success: false
  error: {
    code: string
    message: string
    details?: Record<string, string[]>
  }
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// 사용자 타입
export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  grade?: Grade
  class_id?: string
  level: number
  total_xp: number
  current_streak: number
  created_at: string
  updated_at: string
}

// 개념 타입
export interface Concept {
  id: string
  name: string
  grade: Grade
  parent_id?: string
  description: string
}

// 문제 타입
export interface QuestionOption {
  id: string
  label: string
  text: string
}

export interface Question {
  id: string
  concept_id: string
  question_type: QuestionType
  difficulty: Difficulty
  content: string
  options?: QuestionOption[]
  correct_answer: string
  explanation: string
  points: number
}

// 테스트 타입
export interface Test {
  id: string
  title: string
  description: string
  grade: Grade
  concept_ids: string[]
  question_count: number
  time_limit_minutes?: number
  is_active: boolean
  created_at: string
}

export interface AvailableTest extends Test {
  is_completed: boolean
  best_score?: number
  attempt_count: number
}

export interface TestWithQuestions extends Test {
  questions: Omit<Question, 'correct_answer'>[]
}

// 시도 타입
export interface TestAttempt {
  id: string
  test_id: string
  student_id: string
  started_at: string
  completed_at?: string
  score: number
  max_score: number
  correct_count: number
  total_count: number
  xp_earned: number
  combo_max: number
}

export interface AnswerLog {
  id: string
  attempt_id: string
  question_id: string
  selected_answer: string
  is_correct: boolean
  time_spent_seconds: number
  combo_count: number
  created_at: string
}

// 답안 제출 응답
export interface SubmitAnswerResponse {
  is_correct: boolean
  correct_answer: string
  explanation: string
  points_earned: number
  combo_count: number
  xp_earned: number
  current_score: number
  questions_remaining: number
}

// 통계 타입
export interface ConceptStat {
  concept_id: string
  concept_name: string
  total_questions: number
  correct_count: number
  accuracy_rate: number
}

export interface StudentStats {
  user_id: string
  total_tests: number
  total_questions: number
  correct_answers: number
  accuracy_rate: number
  average_time_per_question: number
  current_streak: number
  max_streak: number
  level: number
  total_xp: number
  weak_concepts: ConceptStat[]
  strong_concepts: ConceptStat[]
}

// 학생 통계 요약 (강사용)
export interface StudentStatsSummary {
  user_id: string
  name: string
  grade: Grade
  class_name: string
  level: number
  total_xp: number
  accuracy_rate: number
  tests_completed: number
  current_streak: number
  last_activity_at: string
}

// 대시보드 통계 (강사용)
export interface DashboardStats {
  today: {
    active_students: number
    tests_completed: number
    questions_answered: number
    average_accuracy: number
  }
  this_week: {
    active_students: number
    tests_completed: number
    accuracy_trend: number[]
  }
  alerts: DashboardAlert[]
}

export interface DashboardAlert {
  type: 'low_accuracy' | 'inactive' | 'struggling'
  student_id: string
  student_name: string
  message: string
}
