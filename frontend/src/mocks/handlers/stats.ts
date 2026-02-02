// 통계 API Mock 핸들러 - 실제 시도 데이터에서 통계 계산

import { http, HttpResponse } from 'msw'
import { currentAttempts, masteryAlerts } from './test'
import { mockAttempts, mockConcepts, getQuestionById } from '../data/questions'
import { findUserById } from '../data/users'

function parseToken(token: string): { userId: string } | null {
  const match = token.match(/mock_(access|refresh)_token_([^_]+)_/)
  if (match) {
    return { userId: match[2] as string }
  }
  return null
}

export const statsHandlers = [
  // GET /api/v1/stats/me
  http.get('/api/v1/stats/me', ({ request }) => {
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

    const token = authHeader.replace('Bearer ', '')
    const parsed = parseToken(token)
    if (!parsed) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'INVALID_TOKEN', message: '유효하지 않은 토큰입니다.' },
        },
        { status: 401 }
      )
    }

    const user = findUserById(parsed.userId)
    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'USER_NOT_FOUND', message: '사용자를 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    // 완료된 시도 수집 (currentAttempts + mockAttempts)
    const completedAttempts = [
      ...Array.from(currentAttempts.values()).filter(
        (a) => a.student_id === parsed.userId && a.completed_at
      ),
      ...mockAttempts.filter(
        (a) => a.student_id === parsed.userId && a.completed_at
      ),
    ]

    const totalTests = completedAttempts.length
    const totalQuestions = completedAttempts.reduce((sum, a) => sum + a.total_count, 0)
    const correctAnswers = completedAttempts.reduce((sum, a) => sum + a.correct_count, 0)
    const accuracyRate = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0

    // 평균 풀이 시간 (시도당 시간에서 추정)
    const totalTimeSeconds = completedAttempts.reduce((sum, a) => {
      if (a.completed_at && a.started_at) {
        const start = new Date(a.started_at).getTime()
        const end = new Date(a.completed_at).getTime()
        return sum + (end - start) / 1000
      }
      return sum
    }, 0)
    const avgTimePerQuestion = totalQuestions > 0
      ? Math.round((totalTimeSeconds / totalQuestions) * 10) / 10
      : 0

    // XP / 레벨: user 객체에 이미 반영된 최신 값 사용 (complete 핸들러에서 동기화됨)
    const totalXp = user.total_xp
    const level = user.level

    // 개념별 통계 계산
    const conceptStats = new Map<string, { correct: number; total: number }>()
    for (const attempt of completedAttempts) {
      const answeredMap = 'answered_questions' in attempt
        ? (attempt as { answered_questions: Set<string> }).answered_questions
        : null

      if (answeredMap) {
        for (const qId of answeredMap) {
          const q = getQuestionById(qId)
          if (!q) continue
          const stat = conceptStats.get(q.concept_id) ?? { correct: 0, total: 0 }
          stat.total++
          const correctLabel = 'correctAnswerMap' in attempt
            ? (attempt as { correctAnswerMap: Map<string, string> }).correctAnswerMap.get(qId)
            : undefined
          if (correctLabel) {
            // 상세 정보 없으므로 attempt 전체 정답률로 추정
          }
          conceptStats.set(q.concept_id, stat)
        }
      }
    }

    // 개념별 정답률 (시도 기반 추정)
    const weakConcepts = mockConcepts
      .filter(() => accuracyRate < 80)
      .slice(0, 2)
      .map((c) => ({
        concept_id: c.id,
        concept_name: c.name,
        total_questions: Math.ceil(totalQuestions / mockConcepts.length),
        correct_count: Math.ceil(correctAnswers / mockConcepts.length),
        accuracy_rate: Math.max(0, accuracyRate - Math.floor(Math.random() * 20)),
      }))

    const strongConcepts = mockConcepts
      .filter(() => accuracyRate >= 60)
      .slice(0, 2)
      .map((c) => ({
        concept_id: c.id,
        concept_name: c.name,
        total_questions: Math.ceil(totalQuestions / mockConcepts.length),
        correct_count: Math.ceil(correctAnswers / mockConcepts.length),
        accuracy_rate: Math.min(100, accuracyRate + Math.floor(Math.random() * 15)),
      }))

    // 트랙별 통계 (연산 / 개념)
    const compQuestions = Math.ceil(totalQuestions * 0.55)
    const compCorrect = Math.ceil(correctAnswers * 0.5)
    const concQuestions = totalQuestions - compQuestions
    const concCorrect = correctAnswers - compCorrect

    return HttpResponse.json({
      success: true,
      data: {
        user_id: user.id,
        total_tests: totalTests,
        total_questions: totalQuestions,
        correct_answers: correctAnswers,
        accuracy_rate: accuracyRate,
        average_time_per_question: avgTimePerQuestion,
        current_streak: user.current_streak,
        max_streak: Math.max(user.current_streak, 7),
        level,
        total_xp: totalXp,
        weak_concepts: accuracyRate < 100 ? weakConcepts : [],
        strong_concepts: strongConcepts,
        computation_stats: {
          total_questions: compQuestions,
          correct_answers: compCorrect,
          accuracy_rate: compQuestions > 0 ? Math.round((compCorrect / compQuestions) * 100) : 0,
        },
        concept_stats: {
          total_questions: concQuestions,
          correct_answers: concCorrect,
          accuracy_rate: concQuestions > 0 ? Math.round((concCorrect / concQuestions) * 100) : 0,
        },
      },
    })
  }),

  // GET /api/v1/stats/dashboard (강사용)
  http.get('/api/v1/stats/dashboard', ({ request }) => {
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

    return HttpResponse.json({
      success: true,
      data: {
        today: {
          active_students: currentAttempts.size > 0 ? 1 : 0,
          tests_completed: Array.from(currentAttempts.values()).filter((a) => a.completed_at).length,
          questions_answered: Array.from(currentAttempts.values()).reduce(
            (sum, a) => sum + a.answered_questions.size,
            0
          ),
          average_accuracy: 85,
        },
        this_week: {
          active_students: 2,
          tests_completed: mockAttempts.length + Array.from(currentAttempts.values()).filter((a) => a.completed_at).length,
          accuracy_trend: [78, 82, 85, 80, 88, 92, 85],
        },
        alerts: [...masteryAlerts],
      },
    })
  }),

  // GET /api/v1/stats/students (강사용)
  http.get('/api/v1/stats/students', ({ request }) => {
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

    const student1 = findUserById('student-1')
    const student2 = findUserById('student-2')

    return HttpResponse.json({
      success: true,
      data: {
        items: [
          {
            user_id: 'student-1',
            name: student1?.name ?? '김철수',
            grade: 'middle_1',
            class_name: '1반',
            level: student1?.level ?? 3,
            total_xp: student1?.total_xp ?? 450,
            accuracy_rate: 85,
            tests_completed: mockAttempts.filter((a) => a.student_id === 'student-1').length,
            current_streak: student1?.current_streak ?? 5,
            last_activity_at: new Date().toISOString(),
          },
          {
            user_id: 'student-2',
            name: student2?.name ?? '이영희',
            grade: 'middle_1',
            class_name: '1반',
            level: student2?.level ?? 5,
            total_xp: student2?.total_xp ?? 820,
            accuracy_rate: 92,
            tests_completed: 8,
            current_streak: student2?.current_streak ?? 12,
            last_activity_at: new Date().toISOString(),
          },
        ],
        total: 2,
        page: 1,
        page_size: 10,
        total_pages: 1,
      },
    })
  }),

  // PUT /api/v1/students/:studentId/grade (학년 승급)
  http.put('/api/v1/students/:studentId/grade', async ({ params, request }) => {
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

    const studentId = params.studentId as string
    const user = findUserById(studentId)
    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'NOT_FOUND', message: '학생을 찾을 수 없습니다.' },
        },
        { status: 404 }
      )
    }

    // 다음 학년 매핑
    const gradeMap: Record<string, string> = {
      elementary_1: 'elementary_2', elementary_2: 'elementary_3',
      elementary_3: 'elementary_4', elementary_4: 'elementary_5',
      elementary_5: 'elementary_6', elementary_6: 'middle_1',
      middle_1: 'middle_2', middle_2: 'middle_3',
      middle_3: 'high_1',
    }

    const currentGrade = user.grade ?? 'middle_1'
    const nextGrade = gradeMap[currentGrade]
    if (!nextGrade) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'MAX_GRADE', message: '이미 최고 학년입니다.' },
        },
        { status: 400 }
      )
    }

    // 학년 승급 + 레벨 5로 리셋
    ;(user as unknown as Record<string, unknown>).grade = nextGrade
    user.level = 5

    // 해당 학생의 마스터 알림 제거
    const alertIndex = masteryAlerts.findIndex((a) => a.student_id === studentId)
    if (alertIndex !== -1) {
      masteryAlerts.splice(alertIndex, 1)
    }

    return HttpResponse.json({
      success: true,
      data: {
        student_id: studentId,
        new_grade: nextGrade,
        new_level: 5,
        message: `${user.name} 학생이 ${nextGrade}로 승급되었습니다.`,
      },
    })
  }),
]
