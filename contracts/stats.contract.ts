// ===========================
// 통계 API 계약
// ===========================

import type {
  StudentStats,
  ClassStats,
  ConceptStat,
  ApiResponse,
  PaginatedResponse,
  ErrorResponse,
  Grade,
} from './types'

// ===========================
// GET /api/v1/stats/me
// ===========================

export type GetMyStatsResponse = StudentStats

export type GetMyStatsResult = ApiResponse<GetMyStatsResponse> | ErrorResponse

/**
 * 내 통계 조회 (학생용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: student
 *
 * 성공 (200):
 * - 총 테스트 수, 정답률, 레벨, XP 등
 * - 취약/강점 개념
 */

// ===========================
// GET /api/v1/stats/students (강사용)
// ===========================

export interface GetStudentStatsParams {
  class_id?: string
  grade?: Grade
  sort_by?: 'name' | 'accuracy' | 'level' | 'last_activity'
  sort_order?: 'asc' | 'desc'
  page?: number
  page_size?: number
}

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

export type GetStudentStatsResponse = PaginatedResponse<StudentStatsSummary>

export type GetStudentStatsResult = ApiResponse<GetStudentStatsResponse> | ErrorResponse

/**
 * 학생 통계 목록 (강사용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher, admin
 *
 * 성공 (200):
 * - 학생별 요약 통계 목록
 * - 정렬/필터 지원
 */

// ===========================
// GET /api/v1/stats/students/{student_id} (강사용)
// ===========================

export interface GetStudentDetailParams {
  student_id: string
}

export interface StudentDetailStats extends StudentStats {
  name: string
  email: string
  grade: Grade
  class_name: string
  recent_tests: RecentTest[]
  daily_activity: DailyActivity[]
}

export interface RecentTest {
  test_id: string
  test_title: string
  score: number
  max_score: number
  accuracy_rate: number
  completed_at: string
}

export interface DailyActivity {
  date: string
  tests_completed: number
  questions_answered: number
  accuracy_rate: number
}

export type GetStudentDetailResult = ApiResponse<StudentDetailStats> | ErrorResponse

/**
 * 학생 상세 통계 (강사용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher, admin
 *
 * 성공 (200):
 * - 상세 통계 + 최근 테스트 + 일별 활동
 *
 * 실패:
 * - 403: 다른 반 학생 조회 불가 (teacher)
 * - 404: 학생을 찾을 수 없음
 */

// ===========================
// GET /api/v1/stats/class/{class_id} (강사용)
// ===========================

export interface GetClassStatsParams {
  class_id: string
}

export interface ClassDetailStats extends ClassStats {
  class_name: string
  teacher_name: string
  grade: Grade
  top_students: TopStudent[]
  concept_stats: ConceptStat[]
  daily_stats: DailyClassStat[]
}

export interface TopStudent {
  user_id: string
  name: string
  level: number
  accuracy_rate: number
}

export interface DailyClassStat {
  date: string
  active_students: number
  tests_completed: number
  average_accuracy: number
}

export type GetClassStatsResult = ApiResponse<ClassDetailStats> | ErrorResponse

/**
 * 반 통계 (강사용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher (자기 반), admin (모든 반)
 *
 * 성공 (200):
 * - 반 전체 통계
 * - 상위 학생
 * - 개념별/일별 통계
 */

// ===========================
// GET /api/v1/stats/concepts (강사용)
// ===========================

export interface GetConceptStatsParams {
  grade?: Grade
  class_id?: string
}

export interface ConceptDetailStat extends ConceptStat {
  grade: Grade
  student_count: number
  average_time_seconds: number
  difficulty_distribution: {
    easy: number
    medium: number
    hard: number
  }
}

export type GetConceptStatsResponse = ConceptDetailStat[]

export type GetConceptStatsResult = ApiResponse<GetConceptStatsResponse> | ErrorResponse

/**
 * 개념별 통계 (강사용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher, admin
 *
 * 성공 (200):
 * - 개념별 정답률, 평균 풀이 시간
 * - 취약 개념 파악용
 */

// ===========================
// GET /api/v1/stats/dashboard (강사용 대시보드)
// ===========================

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
    accuracy_trend: number[] // 7일간 정답률
  }
  alerts: DashboardAlert[]
}

export interface DashboardAlert {
  type: 'low_accuracy' | 'inactive' | 'struggling'
  student_id: string
  student_name: string
  message: string
}

export type GetDashboardStatsResult = ApiResponse<DashboardStats> | ErrorResponse

/**
 * 대시보드 요약 (강사용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher, admin
 *
 * 성공 (200):
 * - 오늘/이번주 요약
 * - 관심 필요 학생 알림
 */
