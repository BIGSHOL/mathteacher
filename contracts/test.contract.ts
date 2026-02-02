// ===========================
// 테스트 API 계약
// ===========================

import type {
  Test,
  TestWithQuestions,
  TestAttempt,
  AnswerLog,
  Question,
  ApiResponse,
  PaginatedResponse,
  ErrorResponse,
  Grade,
} from './types'

// ===========================
// GET /api/v1/tests/available
// ===========================

export interface GetAvailableTestsParams {
  grade?: Grade
  page?: number
  page_size?: number
}

export interface AvailableTest extends Test {
  is_completed: boolean
  best_score?: number
  attempt_count: number
}

export type GetAvailableTestsResponse = PaginatedResponse<AvailableTest>

export type GetAvailableTestsResult = ApiResponse<GetAvailableTestsResponse> | ErrorResponse

/**
 * 풀 수 있는 테스트 목록 조회
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: student
 *
 * 쿼리 파라미터:
 * - grade: 학년 필터 (선택)
 * - page: 페이지 번호 (기본: 1)
 * - page_size: 페이지 크기 (기본: 10, 최대: 50)
 *
 * 성공 (200):
 * - 테스트 목록 + 페이지네이션
 */

// ===========================
// GET /api/v1/tests/{test_id}
// ===========================

export interface GetTestDetailParams {
  test_id: string
}

export type GetTestDetailResponse = TestWithQuestions

export type GetTestDetailResult = ApiResponse<GetTestDetailResponse> | ErrorResponse

/**
 * 테스트 상세 조회 (문제 포함)
 *
 * 헤더: Authorization: Bearer {access_token}
 *
 * 성공 (200):
 * - 테스트 정보 + 문제 목록
 * - 문제의 correct_answer는 포함되지 않음 (채점 시에만 확인)
 *
 * 실패:
 * - 404: 테스트를 찾을 수 없음
 */

// ===========================
// POST /api/v1/tests/{test_id}/start
// ===========================

export interface StartTestParams {
  test_id: string
}

export interface StartTestResponse {
  attempt_id: string
  test: TestWithQuestions
  started_at: string
}

export type StartTestResult = ApiResponse<StartTestResponse> | ErrorResponse

/**
 * 테스트 시작 (새 시도 생성)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: student
 *
 * 성공 (201):
 * - 새 TestAttempt 생성
 * - 문제 목록 반환 (correct_answer 제외)
 *
 * 실패:
 * - 404: 테스트를 찾을 수 없음
 */

// ===========================
// POST /api/v1/tests/attempts/{attempt_id}/submit
// ===========================

export interface SubmitAnswerParams {
  attempt_id: string
}

export interface SubmitAnswerRequest {
  question_id: string
  selected_answer: string
  time_spent_seconds: number
}

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

export type SubmitAnswerResult = ApiResponse<SubmitAnswerResponse> | ErrorResponse

/**
 * 답안 제출 (문제별 즉시 채점)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: student
 *
 * 성공 (200):
 * - 즉시 채점 결과
 * - 정답 여부, 해설, 점수, 콤보
 *
 * 실패:
 * - 400: 이미 답안 제출됨
 * - 404: 시도 또는 문제를 찾을 수 없음
 */

// ===========================
// POST /api/v1/tests/attempts/{attempt_id}/complete
// ===========================

export interface CompleteTestParams {
  attempt_id: string
}

export interface CompleteTestResponse {
  attempt: TestAttempt
  answers: AnswerLog[]
  level_up: boolean
  new_level?: number
  xp_earned: number
  achievements_earned: string[]
}

export type CompleteTestResult = ApiResponse<CompleteTestResponse> | ErrorResponse

/**
 * 테스트 완료
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: student
 *
 * 성공 (200):
 * - 최종 결과 요약
 * - 레벨업 정보
 * - 획득 업적
 *
 * 실패:
 * - 400: 이미 완료된 시도
 * - 404: 시도를 찾을 수 없음
 */

// ===========================
// GET /api/v1/tests/attempts/{attempt_id}
// ===========================

export interface GetAttemptParams {
  attempt_id: string
}

export interface GetAttemptResponse {
  attempt: TestAttempt
  answers: AnswerLog[]
  test: Test
}

export type GetAttemptResult = ApiResponse<GetAttemptResponse> | ErrorResponse

/**
 * 테스트 시도 결과 조회
 *
 * 헤더: Authorization: Bearer {access_token}
 *
 * 성공 (200):
 * - 시도 정보 + 답안 기록
 *
 * 실패:
 * - 404: 시도를 찾을 수 없음
 */

// ===========================
// 강사용 API
// ===========================

// GET /api/v1/tests (강사용 전체 목록)
export interface GetAllTestsParams {
  grade?: Grade
  is_active?: boolean
  page?: number
  page_size?: number
}

export type GetAllTestsResponse = PaginatedResponse<Test>

// POST /api/v1/tests (테스트 생성)
export interface CreateTestRequest {
  title: string
  description: string
  grade: Grade
  concept_ids: string[]
  question_ids: string[]
  time_limit_minutes?: number
}

export type CreateTestResponse = Test

// PATCH /api/v1/tests/{test_id} (테스트 수정)
export interface UpdateTestRequest {
  title?: string
  description?: string
  is_active?: boolean
  question_ids?: string[]
}

export type UpdateTestResponse = Test
