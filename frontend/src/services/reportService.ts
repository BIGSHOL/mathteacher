/**
 * 문제 신고 API 서비스.
 */

import api from '../lib/api'

export type ReportType = 'wrong_answer' | 'wrong_options' | 'question_error' | 'other'
export type ReportStatus = 'pending' | 'resolved' | 'dismissed'

export interface QuestionReport {
  id: string
  question_id: string
  question_content: string | null
  reporter_id: string
  reporter_name: string | null
  report_type: ReportType
  comment: string
  status: ReportStatus
  admin_response: string | null
  resolved_by: string | null
  reviewer_name: string | null
  resolved_at: string | null
  created_at: string
  updated_at: string
}

interface ApiResponse<T> {
  success: boolean
  data: T
}

interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/** 문제 신고 등록 */
export async function createQuestionReport(data: {
  question_id: string
  report_type: ReportType
  comment: string
}): Promise<QuestionReport> {
  const res = await api.post<ApiResponse<QuestionReport>>(
    '/api/v1/question-reports',
    data,
  )
  return res.data.data
}

/** 신고 목록 조회 (관리자용) */
export async function getQuestionReports(params: {
  status?: ReportStatus
  page?: number
  page_size?: number
}): Promise<PaginatedResponse<QuestionReport>> {
  const res = await api.get<ApiResponse<PaginatedResponse<QuestionReport>>>(
    '/api/v1/question-reports',
    { params },
  )
  return res.data.data
}

/** 신고 처리 (관리자용) */
export async function resolveQuestionReport(
  id: string,
  data: { status: 'resolved' | 'dismissed'; admin_response?: string },
): Promise<QuestionReport> {
  const res = await api.patch<ApiResponse<QuestionReport>>(
    `/api/v1/question-reports/${id}/resolve`,
    data,
  )
  return res.data.data
}
