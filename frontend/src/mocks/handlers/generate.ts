// 문제 생성 API Mock 핸들러

import { http, HttpResponse } from 'msw'
import { generateQuestions, ALL_TEMPLATES, getAvailableLevels, getSupportedGrades } from '../../services/questionGenerator'
import type { Grade, QuestionCategory } from '../../types'

export const generateHandlers = [
  // POST /api/v1/questions/generate — 문제 동적 생성
  http.post('/api/v1/questions/generate', async ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'UNAUTHORIZED', message: '인증이 필요합니다.' },
        },
        { status: 401 }
      )
    }

    const body = (await request.json()) as {
      grade: Grade
      category: QuestionCategory
      level: number
      count?: number
    }

    if (!body.grade || !body.category || !body.level) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'BAD_REQUEST', message: 'grade, category, level은 필수입니다.' },
        },
        { status: 400 }
      )
    }

    if (body.level < 1 || body.level > 10) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'BAD_REQUEST', message: 'level은 1~10 사이여야 합니다.' },
        },
        { status: 400 }
      )
    }

    const questions = generateQuestions(
      {
        grade: body.grade,
        category: body.category,
        level: body.level,
        count: body.count ?? 5,
      },
      ALL_TEMPLATES
    )

    if (questions.length === 0) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'NO_TEMPLATES',
            message: `${body.grade} / ${body.category} / Lv.${body.level} 템플릿이 없습니다.`,
          },
        },
        { status: 404 }
      )
    }

    // 정답 제거한 버전 (학생용)
    const questionsWithoutAnswers = questions.map(
      ({ correct_answer, ...q }) => q
    )

    return HttpResponse.json({
      success: true,
      data: {
        questions: questionsWithoutAnswers,
        answers: questions.map((q) => ({
          question_id: q.id,
          correct_answer: q.correct_answer,
          explanation: q.explanation,
        })),
        meta: {
          grade: body.grade,
          category: body.category,
          level: body.level,
          count: questions.length,
        },
      },
    })
  }),

  // GET /api/v1/questions/levels — 사용 가능한 레벨 조회
  http.get('/api/v1/questions/levels', ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'UNAUTHORIZED', message: '인증이 필요합니다.' },
        },
        { status: 401 }
      )
    }

    const url = new URL(request.url)
    const grade = url.searchParams.get('grade') as Grade | null
    const category = url.searchParams.get('category') as QuestionCategory | null

    if (!grade || !category) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'BAD_REQUEST', message: 'grade와 category는 필수입니다.' },
        },
        { status: 400 }
      )
    }

    const levels = getAvailableLevels(grade, category)

    return HttpResponse.json({
      success: true,
      data: {
        grade,
        category,
        levels,
        supported_grades: getSupportedGrades(),
      },
    })
  }),
]
