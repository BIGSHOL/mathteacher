// 타입 정의

export type UserRole = 'student' | 'teacher' | 'admin' | 'master'

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

export type QuestionType = 'multiple_choice' | 'true_false' | 'short_answer' | 'fill_in_blank'

/** 문제 카테고리 (트랙): 연산(computation) / 개념(concept) / 빈칸(fill_in_blank) */
export type QuestionCategory = 'computation' | 'concept' | 'fill_in_blank'

/** 문제 파트 (6개 영역) */
export type ProblemPart = 'calc' | 'algebra' | 'func' | 'geo' | 'data' | 'word'

/** 난이도 1~10 (1: 가장 쉬움, 10: 가장 어려움). 학년별 × 트랙별 독립 운영 */
export type Difficulty = number

// 집중 체크 항목 타입
export interface FocusCheckItem {
  id: string
  question_id: string
  question_content: string
  concept_name: string
  wrong_count: number
  created_at: string
}

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
  login_id: string
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
  category: QuestionCategory
  part: ProblemPart
  parent_id?: string
  prerequisite_ids?: string[]
  description: string
}

// 문제 타입
export interface QuestionOption {
  id: string
  label: string
  text: string
}

export interface BlankConfig {
  display_content: string
  blank_answers: Record<string, { answer: string; position: number }>
  original_content: string
}

export interface Question {
  id: string
  concept_id: string
  concept_name?: string
  category: QuestionCategory
  part: ProblemPart
  question_type: QuestionType
  difficulty: Difficulty
  content: string
  options?: QuestionOption[]
  correct_answer: string
  explanation: string
  points: number
  prerequisite_concept_ids?: string[]
  blank_config?: BlankConfig
}

// 테스트 타입
export interface Test {
  id: string
  title: string
  description: string
  grade: Grade
  category?: QuestionCategory
  test_type?: string  // concept, cumulative, semester_final, grade_final
  semester?: number   // 학기 종합시험의 경우 학기 번호
  concept_ids: string[]
  question_count: number
  time_limit_minutes?: number
  is_active: boolean
  is_adaptive: boolean
  created_at: string
}

export interface AvailableTest extends Test {
  is_completed: boolean
  best_score?: number
  attempt_count: number
  difficulty?: number  // 평균 난이도 1~10
}

export interface TestWithQuestions extends Test {
  questions: (Omit<Question, 'correct_answer'> & { correct_answer?: string })[]
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
  is_adaptive: boolean
  current_difficulty?: number
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
  time_bonus: number
  combo_count: number
  xp_earned: number
  current_score: number
  questions_remaining: number
  next_difficulty?: number
  error_type?: string
  suggestion?: string
  // 재도전 관련 필드 (일일 테스트용)
  retry_scheduled?: boolean  // 재도전 예정 여부
  retry_count?: number  // 이 문제에서 틀린 횟수
  retry_queue_count?: number  // 재도전 대기 문제 수
  hint?: RetryHint | null  // 재도전 힌트 정보
  moved_to_focus_check?: boolean  // 집중 체크로 이동 여부
  focus_check_message?: string  // 집중 체크 안내 메시지
}

// 재도전 힌트 타입
export interface RetryHint {
  level: number  // 1, 2, 3
  type: 'concept' | 'direction' | 'extended'
  message: string
  concept_id?: string
}

// 적응형 다음 문제 응답
export interface NextQuestionResponse {
  question: Omit<Question, 'correct_answer'> | null
  current_difficulty: number
  questions_answered: number
  questions_remaining: number
  is_complete: boolean
}

// 테스트 완료 응답
export type LevelDownAction = 'none' | 'defense_consumed' | 'defense_restored' | 'level_down'

export interface AchievementEarned {
  id: string
  name: string
  description: string
  icon: string
  earned_at: string
}

export interface CompleteTestResult {
  level_up: boolean
  level_down: boolean
  new_level: number | null
  xp_earned: number
  total_xp: number | null
  current_streak: number | null
  achievements_earned?: AchievementEarned[]
  level_down_defense: number | null
  level_down_action: LevelDownAction | null
  mastery_achieved?: boolean
}

// 통계 타입
export interface ConceptStat {
  concept_id: string
  concept_name: string
  total_questions: number
  correct_count: number
  accuracy_rate: number
}

export interface TrackStats {
  total_questions: number
  correct_answers: number
  accuracy_rate: number
  average_time?: number
}

export interface ReviewStatsInfo {
  pending_count: number
  in_progress_count: number
  graduated_count: number
}

export interface DailyActivityItem {
  date: string
  tests_completed: number
  questions_answered: number
  accuracy_rate: number
}

export interface RecentTestItem {
  test_id: string
  test_title: string
  score: number
  max_score: number
  accuracy_rate: number
  completed_at: string
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
  today_solved: number
  weak_concepts: ConceptStat[]
  strong_concepts: ConceptStat[]
  computation_stats?: TrackStats
  concept_stats?: TrackStats
  type_stats?: Record<string, TrackStats>
  daily_activity?: DailyActivityItem[]
  recent_tests?: RecentTestItem[]
  review_stats?: ReviewStatsInfo
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
  type: 'low_accuracy' | 'inactive' | 'struggling' | 'mastery'
  student_id: string
  student_name: string
  message: string
  current_grade?: Grade
  recommended_grade?: Grade
}

// 일일 테스트 타입
export type DailyTestCategory = 'concept' | 'computation' | 'fill_in_blank'

export interface DailyTestRecord {
  id: string
  date: string
  category: DailyTestCategory
  category_label: string
  status: 'pending' | 'in_progress' | 'completed'
  test_id: string
  attempt_id?: string
  score?: number
  max_score?: number
  correct_count?: number
  total_count?: number
  completed_at?: string
  question_count: number
}

export interface DailyTestTodayResponse {
  date: string
  tests: DailyTestRecord[]
}

// 단원 진행 상황 타입
export interface ChapterProgressItem {
  chapter_id: string
  chapter_number: number
  semester: number
  name: string
  description: string
  is_unlocked: boolean
  overall_progress: number
  is_completed: boolean
  final_test_score: number | null
  teacher_approved: boolean
}

// 과제 타입
export interface Assignment {
  id: string
  student_id: string
  assignment_type: 'chapter' | 'review' | 'custom'
  reference_id?: string
  title: string
  description?: string
  due_date?: string
  is_completed: boolean
  completed_at?: string
  created_at: string
}

export interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  earned_at: string
}

export interface RankingItem {
  rank: number
  user_id: string
  name: string
  level: number
  total_xp: number
  grade: string | null
}
