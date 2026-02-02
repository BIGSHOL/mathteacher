// ===========================
// 공통 타입 정의
// ===========================

// 사용자 역할
export type UserRole = 'student' | 'teacher' | 'admin'

// 학년
export type Grade = 'elementary_1' | 'elementary_2' | 'elementary_3' | 'elementary_4' | 'elementary_5' | 'elementary_6' | 'middle_1' | 'middle_2' | 'middle_3' | 'high_1'

// 문제 유형
export type QuestionType = 'multiple_choice' | 'true_false' | 'short_answer'

// 난이도
export type Difficulty = 'easy' | 'medium' | 'hard'

// ===========================
// 기본 응답 타입
// ===========================

export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface ErrorResponse {
  success: false
  error: {
    code: string
    message: string
    details?: Record<string, string[]>
  }
}

// ===========================
// 사용자 관련 타입
// ===========================

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

export interface Class {
  id: string
  name: string
  teacher_id: string
  grade: Grade
  created_at: string
}

// ===========================
// 테스트 관련 타입
// ===========================

export interface Concept {
  id: string
  name: string
  grade: Grade
  parent_id?: string
  description: string
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

export interface QuestionOption {
  id: string
  label: string
  text: string
}

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

export interface TestWithQuestions extends Test {
  questions: Question[]
}

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

// ===========================
// 게이미피케이션 타입
// ===========================

export interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  condition_type: 'streak' | 'level' | 'score' | 'combo'
  condition_value: number
}

export interface UserAchievement {
  id: string
  user_id: string
  achievement_id: string
  earned_at: string
}

export interface DailyStreak {
  user_id: string
  date: string
  tests_completed: number
  questions_answered: number
}

// ===========================
// 통계 타입
// ===========================

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

export interface ConceptStat {
  concept_id: string
  concept_name: string
  total_questions: number
  correct_count: number
  accuracy_rate: number
}

export interface ClassStats {
  class_id: string
  student_count: number
  average_accuracy: number
  average_level: number
  tests_completed_today: number
  weak_concepts: ConceptStat[]
}
