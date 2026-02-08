/**
 * 문제 생성 → 백엔드 DB 저장 파이프라인.
 *
 * 프론트엔드 QuestionTemplate에서 paramRanges 내 랜덤 파라미터를 생성하여
 * 완성된 문제를 백엔드 questions 테이블에 저장합니다.
 */

import api from '../lib/api'
import type { GeneratedQuestion } from './questionGenerator/types'

/** 백엔드 QuestionCreate 스키마에 대응하는 요청 타입 */
interface QuestionCreatePayload {
  concept_id: string
  category: 'computation' | 'concept' | 'fill_in_blank'
  part: 'calc' | 'algebra' | 'func' | 'geo' | 'data' | 'word'
  question_type: 'multiple_choice' | 'short_answer'
  difficulty: number
  content: string
  options: { id: string; label: string; text: string }[] | null
  correct_answer: string
  explanation: string
  points: number
  prerequisite_concept_ids?: string[] | null
}

/** 백엔드 응답 타입 */
interface QuestionResponse {
  id: string
  concept_id: string
  category: string
  part: string
  question_type: string
  difficulty: number
  content: string
  options: { id: string; label: string; text: string }[] | null
  correct_answer: string
  explanation: string
  points: number
  prerequisite_concept_ids: string[] | null
}

interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/** GeneratedQuestion → QuestionCreatePayload 변환 */
function toPayload(q: GeneratedQuestion): QuestionCreatePayload {
  return {
    concept_id: q.concept_id,
    category: q.category,
    part: q.part,
    question_type: q.question_type,
    difficulty: q.difficulty,
    content: q.content,
    options: q.options,
    correct_answer: q.correct_answer,
    explanation: q.explanation,
    points: q.points,
  }
}

/**
 * 단일 문제를 백엔드에 저장합니다.
 */
export async function saveQuestion(
  question: GeneratedQuestion,
): Promise<QuestionResponse> {
  const { data } = await api.post<ApiResponse<QuestionResponse>>(
    '/api/v1/questions',
    toPayload(question),
  )
  return data.data
}

/**
 * 문제 일괄 저장 (최대 100건).
 * 프론트에서 generateQuestions()로 생성한 문제 배열을 한 번에 저장합니다.
 */
export async function saveQuestionsBatch(
  questions: GeneratedQuestion[],
): Promise<QuestionResponse[]> {
  const { data } = await api.post<ApiResponse<QuestionResponse[]>>(
    '/api/v1/questions/batch',
    questions.map(toPayload),
  )
  return data.data
}

/**
 * 개념 ID로 문제 목록을 조회합니다.
 */
export async function getQuestionsByConcept(
  conceptId: string,
): Promise<QuestionResponse[]> {
  const { data } = await api.get<ApiResponse<QuestionResponse[]>>(
    `/api/v1/questions/by-concept/${conceptId}`,
  )
  return data.data
}

/**
 * 필터링된 문제 목록을 페이지네이션으로 조회합니다.
 */
export async function listQuestions(params: {
  concept_id?: string
  grade?: string
  category?: string
  part?: string
  difficulty?: number
  page?: number
  page_size?: number
}): Promise<PaginatedResponse<QuestionResponse>> {
  const { data } = await api.get<ApiResponse<PaginatedResponse<QuestionResponse>>>(
    '/api/v1/questions',
    { params },
  )
  return data.data
}

/**
 * 문제 통계를 조회합니다 (개념별 문제 수).
 */
export async function getQuestionStats(): Promise<{
  total: number
  by_concept: Record<string, number>
}> {
  const { data } = await api.get<ApiResponse<{ total: number; by_concept: Record<string, number> }>>(
    '/api/v1/questions/stats',
  )
  return data.data
}

// ─────────────────────────────────────────────
// AI 문제 대량 생성 (마스터 전용)
// ─────────────────────────────────────────────

/** AI 문제 생성 요청 */
export async function generateQuestionsAI(params: {
  concept_id: string
  count?: number
  question_type?: string
  difficulty_min?: number
  difficulty_max?: number
  granular_config?: { question_type: string; difficulty: number; count: number }[]
}): Promise<{ generated: Record<string, unknown>[]; count: number }> {
  const { data } = await api.post<
    ApiResponse<{ generated: Record<string, unknown>[]; count: number }>
  >('/api/v1/admin/generate-questions', params)
  return data.data
}

/** 생성된 문제 저장 */
export async function saveGeneratedQuestions(
  questions: Record<string, unknown>[],
): Promise<{ saved_count: number }> {
  const { data } = await api.post<ApiResponse<{ saved_count: number }>>(
    '/api/v1/admin/save-generated-questions',
    { questions },
  )
  return data.data
}

/** MC에서 FB 빈칸 문제 파생 */
export async function deriveFillBlank(params: {
  concept_id: string
  max_per_mc: number
}): Promise<{
  source_mc_count: number
  derived_fb_count: number
  derived_questions: Record<string, unknown>[]
}> {
  const { data } = await api.post<
    ApiResponse<{
      source_mc_count: number
      derived_fb_count: number
      derived_questions: Record<string, unknown>[]
    }>
  >('/api/v1/admin/derive-fill-blank', params)
  return data.data
}
