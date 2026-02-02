// ===========================
// 인증 API 계약
// ===========================

import type { User, ApiResponse, ErrorResponse, UserRole } from './types'

// ===========================
// POST /api/v1/auth/login
// ===========================

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  user: User
  access_token: string
  refresh_token: string
  token_type: 'bearer'
  expires_in: number // seconds
}

export type LoginResult = ApiResponse<LoginResponse> | ErrorResponse

/**
 * 로그인 API
 *
 * 성공 (200):
 * - 사용자 정보 + JWT 토큰 반환
 *
 * 실패:
 * - 401: 이메일 또는 비밀번호 불일치
 * - 422: 유효하지 않은 입력
 */

// ===========================
// POST /api/v1/auth/refresh
// ===========================

export interface RefreshRequest {
  refresh_token: string
}

export interface RefreshResponse {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
  expires_in: number
}

export type RefreshResult = ApiResponse<RefreshResponse> | ErrorResponse

/**
 * 토큰 갱신 API
 *
 * 성공 (200):
 * - 새 access_token + refresh_token 반환
 *
 * 실패:
 * - 401: 유효하지 않거나 만료된 refresh_token
 */

// ===========================
// POST /api/v1/auth/logout
// ===========================

export interface LogoutRequest {
  refresh_token: string
}

export interface LogoutResponse {
  message: string
}

export type LogoutResult = ApiResponse<LogoutResponse> | ErrorResponse

/**
 * 로그아웃 API
 *
 * 성공 (200):
 * - refresh_token 무효화
 *
 * 실패:
 * - 401: 인증 필요
 */

// ===========================
// GET /api/v1/auth/me
// ===========================

export type MeResponse = User

export type MeResult = ApiResponse<MeResponse> | ErrorResponse

/**
 * 현재 사용자 정보 조회
 *
 * 헤더: Authorization: Bearer {access_token}
 *
 * 성공 (200):
 * - 현재 로그인한 사용자 정보
 *
 * 실패:
 * - 401: 인증 필요
 */

// ===========================
// POST /api/v1/auth/register (강사 전용)
// ===========================

export interface RegisterStudentRequest {
  email: string
  password: string
  name: string
  role: Extract<UserRole, 'student'>
  grade: string
  class_id: string
}

export interface RegisterTeacherRequest {
  email: string
  password: string
  name: string
  role: Extract<UserRole, 'teacher'>
}

export type RegisterRequest = RegisterStudentRequest | RegisterTeacherRequest

export interface RegisterResponse {
  user: User
  message: string
}

export type RegisterResult = ApiResponse<RegisterResponse> | ErrorResponse

/**
 * 사용자 등록 (강사/관리자 전용)
 *
 * 헤더: Authorization: Bearer {access_token}
 * 권한: teacher, admin
 *
 * 성공 (201):
 * - 생성된 사용자 정보
 *
 * 실패:
 * - 400: 이미 존재하는 이메일
 * - 401: 인증 필요
 * - 403: 권한 없음
 * - 422: 유효하지 않은 입력
 */
