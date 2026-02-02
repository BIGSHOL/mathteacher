// 테스트 API Mock 핸들러

import { http, HttpResponse } from 'msw'
import {
  mockTests,
  mockAttempts,
  getTestById,
  getQuestionsForTest,
  getQuestionById,
} from '../data/questions'

// 현재 진행 중인 시도 저장
const currentAttempts = new Map<
  string,
  {
    id: string
    test_id: string
    student_id: string
    started_at: string
    completed_at: string | null
    score: number
    max_score: number
    correct_count: number
    total_count: number
    xp_earned: number
    combo_count: number
    combo_max: number
    answered_questions: Set<string>
  }
>()

export const testHandlers = [
  // GET /api/v1/tests/available
  http.get('/api/v1/tests/available', ({ request }) => {
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
    const grade = url.searchParams.get('grade')
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('page_size') || '10')

    let filteredTests = mockTests.filter((t) => t.is_active)
    if (grade) {
      filteredTests = filteredTests.filter((t) => t.grade === grade)
    }

    const total = filteredTests.length
    const start = (page - 1) * pageSize
    const items = filteredTests.slice(start, start + pageSize).map((test) => ({
      ...test,
      is_completed: mockAttempts.some(
        (a) => a.test_id === test.id && a.completed_at
      ),
      best_score: mockAttempts
        .filter((a) => a.test_id === test.id)
        .reduce((max, a) => Math.max(max, a.score), 0) || undefined,
      attempt_count: mockAttempts.filter((a) => a.test_id === test.id).length,
    }))

    return HttpResponse.json({
      success: true,
      data: {
        items,
        total,
        page,
        page_size: pageSize,
        total_pages: Math.ceil(total / pageSize),
      },
    })
  }),

  // GET /api/v1/tests/:testId
  http.get('/api/v1/tests/:testId', ({ params, request }) => {
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

    const test = getTestById(params.testId as string)
    if (!test) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '테스트를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    const questions = getQuestionsForTest(test.id).map(
      ({ correct_answer, ...q }) => q
    )

    return HttpResponse.json({
      success: true,
      data: {
        ...test,
        questions,
      },
    })
  }),

  // POST /api/v1/tests/:testId/start
  http.post('/api/v1/tests/:testId/start', ({ params, request }) => {
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

    const test = getTestById(params.testId as string)
    if (!test) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '테스트를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    const questions = getQuestionsForTest(test.id)
    const attemptId = `attempt-${Date.now()}`
    const maxScore = questions.reduce((sum, q) => sum + q.points, 0)

    const attempt = {
      id: attemptId,
      test_id: test.id,
      student_id: 'student-1',
      started_at: new Date().toISOString(),
      completed_at: null,
      score: 0,
      max_score: maxScore,
      correct_count: 0,
      total_count: questions.length,
      xp_earned: 0,
      combo_count: 0,
      combo_max: 0,
      answered_questions: new Set<string>(),
    }
    currentAttempts.set(attemptId, attempt)

    return HttpResponse.json(
      {
        success: true,
        data: {
          attempt_id: attemptId,
          test: {
            ...test,
            questions: questions.map(({ correct_answer, ...q }) => q),
          },
          started_at: attempt.started_at,
        },
      },
      { status: 201 }
    )
  }),

  // POST /api/v1/tests/attempts/:attemptId/submit
  http.post('/api/v1/tests/attempts/:attemptId/submit', async ({ params, request }) => {
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

    const attempt = currentAttempts.get(params.attemptId as string)
    if (!attempt) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '시도를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    const body = (await request.json()) as {
      question_id: string
      selected_answer: string
      time_spent_seconds: number
    }

    if (attempt.answered_questions.has(body.question_id)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'ALREADY_SUBMITTED',
            message: '이미 답안을 제출한 문제입니다.',
          },
        },
        { status: 400 }
      )
    }

    const question = getQuestionById(body.question_id)
    if (!question) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '문제를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    const isCorrect = body.selected_answer === question.correct_answer
    attempt.answered_questions.add(body.question_id)

    if (isCorrect) {
      attempt.correct_count++
      attempt.combo_count++
      attempt.combo_max = Math.max(attempt.combo_max, attempt.combo_count)

      // 콤보 보너스 계산
      let comboMultiplier = 1
      if (attempt.combo_count >= 5) comboMultiplier = 2
      else if (attempt.combo_count >= 3) comboMultiplier = 1.5

      const pointsEarned = Math.floor(question.points * comboMultiplier)
      attempt.score += pointsEarned
      attempt.xp_earned += Math.floor(pointsEarned * 0.5)
    } else {
      attempt.combo_count = 0
    }

    const questionsRemaining =
      attempt.total_count - attempt.answered_questions.size

    return HttpResponse.json({
      success: true,
      data: {
        is_correct: isCorrect,
        correct_answer: question.correct_answer,
        explanation: question.explanation,
        points_earned: isCorrect ? question.points : 0,
        combo_count: attempt.combo_count,
        xp_earned: attempt.xp_earned,
        current_score: attempt.score,
        questions_remaining: questionsRemaining,
      },
    })
  }),

  // POST /api/v1/tests/attempts/:attemptId/complete
  http.post('/api/v1/tests/attempts/:attemptId/complete', ({ params, request }) => {
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

    const attempt = currentAttempts.get(params.attemptId as string)
    if (!attempt) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '시도를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    if (attempt.completed_at) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'ALREADY_COMPLETED',
            message: '이미 완료된 테스트입니다.',
          },
        },
        { status: 400 }
      )
    }

    attempt.completed_at = new Date().toISOString()

    // 레벨업 체크 (간단한 로직)
    const levelUp = attempt.xp_earned >= 100
    const newLevel = levelUp ? 2 : undefined

    return HttpResponse.json({
      success: true,
      data: {
        attempt: {
          id: attempt.id,
          test_id: attempt.test_id,
          student_id: attempt.student_id,
          started_at: attempt.started_at,
          completed_at: attempt.completed_at,
          score: attempt.score,
          max_score: attempt.max_score,
          correct_count: attempt.correct_count,
          total_count: attempt.total_count,
          xp_earned: attempt.xp_earned,
          combo_max: attempt.combo_max,
        },
        answers: [],
        level_up: levelUp,
        new_level: newLevel,
        xp_earned: attempt.xp_earned,
        achievements_earned: [],
      },
    })
  }),

  // GET /api/v1/tests/attempts/:attemptId
  http.get('/api/v1/tests/attempts/:attemptId', ({ params, request }) => {
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

    const attempt = currentAttempts.get(params.attemptId as string)
    if (!attempt) {
      // 기존 시도에서 찾기
      const existingAttempt = mockAttempts.find(
        (a) => a.id === params.attemptId
      )
      if (!existingAttempt) {
        return HttpResponse.json(
          {
            success: false,
            error: { code: 'NOT_FOUND', message: '시도를 찾을 수 없습니다.' },
          },
          { status: 404 }
        )
      }

      const test = getTestById(existingAttempt.test_id)
      return HttpResponse.json({
        success: true,
        data: {
          attempt: existingAttempt,
          answers: [],
          test,
        },
      })
    }

    const test = getTestById(attempt.test_id)
    return HttpResponse.json({
      success: true,
      data: {
        attempt: {
          id: attempt.id,
          test_id: attempt.test_id,
          student_id: attempt.student_id,
          started_at: attempt.started_at,
          completed_at: attempt.completed_at,
          score: attempt.score,
          max_score: attempt.max_score,
          correct_count: attempt.correct_count,
          total_count: attempt.total_count,
          xp_earned: attempt.xp_earned,
          combo_max: attempt.combo_max,
        },
        answers: [],
        test,
      },
    })
  }),
]
