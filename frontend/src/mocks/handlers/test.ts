// 테스트 API Mock 핸들러

import { http, HttpResponse } from 'msw'
import {
  mockTests,
  mockAttempts,
  getTestById,
  getQuestionsForTest,
  getQuestionById,
} from '../data/questions'
import { findUserById } from '../data/users'
import { generateAdaptiveQuestion, ALL_TEMPLATES } from '../../services/questionGenerator'
import type { QuestionCategory, QuestionOption } from '../../types'

// 레벨별 필요 XP (백엔드와 동일)
const LEVEL_XP: Record<number, number> = {
  1: 0, 2: 100, 3: 250, 4: 450, 5: 700,
  6: 1000, 7: 1400, 8: 1900, 9: 2500, 10: 3200,
}

function getLevelForXp(totalXp: number): number {
  let level = 1
  for (const [lv, xp] of Object.entries(LEVEL_XP)) {
    if (totalXp >= xp) level = Number(lv)
  }
  return Math.min(level, 10)
}

function parseTokenUserId(token: string): string | null {
  const match = token.match(/mock_(access|refresh)_token_([^_]+)_/)
  return match ? match[2]! : null
}

const LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

function shuffleOptions(options: QuestionOption[], correctLabel: string) {
  const shuffled = [...options].sort(() => Math.random() - 0.5)
  const relabeled = shuffled.map((opt, i) => ({ ...opt, label: LABELS[i]! }))
  const originalCorrect = options.find((o) => o.label === correctLabel)
  const newCorrect = relabeled.find((o) => o.id === originalCorrect?.id)
  return { options: relabeled, correctLabel: newCorrect?.label ?? correctLabel }
}

// 현재 진행 중인 시도 저장 (stats 핸들러에서도 참조)
export const currentAttempts = new Map<
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
    correctAnswerMap: Map<string, string>
    shuffledQuestions: Record<string, unknown>[]
    // 적응형 연습 전용 필드
    is_adaptive: boolean
    grade: string
    category: string
    current_difficulty: number
    testTitle: string
    generatedAnswerMap: Map<string, { correct_answer: string; explanation: string; points: number }>
    lastAnswerCorrect: boolean | null
  }
>()

// 마스터 알림 저장소 (stats 핸들러에서 참조)
export const masteryAlerts: Array<{
  type: 'mastery'
  student_id: string
  student_name: string
  message: string
  current_grade: string
  recommended_grade: string
}> = []

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

  // POST /api/v1/tests/:testId/start (기존 고정형 테스트)
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

    const correctAnswerMap = new Map<string, string>()
    const shuffledQuestions = questions.map((q) => {
      if (q.options) {
        const { options, correctLabel } = shuffleOptions(q.options, q.correct_answer)
        correctAnswerMap.set(q.id, correctLabel)
        return { ...q, options, correct_answer: correctLabel }
      }
      correctAnswerMap.set(q.id, q.correct_answer)
      return q
    })

    const questionsWithoutAnswers = shuffledQuestions.map(
      ({ correct_answer, ...q }) => q
    ) as Record<string, unknown>[]

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
      correctAnswerMap,
      shuffledQuestions: questionsWithoutAnswers,
      // 고정형은 적응형 아님
      is_adaptive: false,
      grade: test.grade,
      category: test.category ?? '',
      current_difficulty: 5,
      testTitle: test.title,
      generatedAnswerMap: new Map<string, { correct_answer: string; explanation: string; points: number }>(),
      lastAnswerCorrect: null,
    }
    currentAttempts.set(attemptId, attempt)

    return HttpResponse.json(
      {
        success: true,
        data: {
          attempt_id: attemptId,
          test: {
            ...test,
            questions: questionsWithoutAnswers,
          },
          started_at: attempt.started_at,
        },
      },
      { status: 201 }
    )
  }),

  // POST /api/v1/practice/start (엔진 기반 적응형 연습)
  http.post('/api/v1/practice/start', async ({ request }) => {
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
      grade: string
      category: QuestionCategory
      count: number
      starting_difficulty: number
    }

    const { grade, category, count = 10, starting_difficulty = 5 } = body

    // 엔진으로 첫 문제 생성
    const firstQuestion = generateAdaptiveQuestion(
      grade,
      category,
      starting_difficulty,
      ALL_TEMPLATES
    )

    if (!firstQuestion) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'NO_TEMPLATES',
            message: `${grade} / ${category} / Lv.${starting_difficulty} 템플릿이 없습니다.`,
          },
        },
        { status: 404 }
      )
    }

    const attemptId = `practice-${Date.now()}`
    const categoryLabel = category === 'computation' ? '연산' : '개념'
    const testTitle = `${categoryLabel} 빠른 연습 (Lv.${starting_difficulty})`

    // 정답 저장
    const generatedAnswerMap = new Map<string, { correct_answer: string; explanation: string; points: number }>()
    generatedAnswerMap.set(firstQuestion.id, {
      correct_answer: firstQuestion.correct_answer,
      explanation: firstQuestion.explanation,
      points: firstQuestion.points,
    })

    // 정답 제외한 문제
    const { correct_answer: _ca, explanation: _ex, ...questionWithoutAnswer } = firstQuestion

    const attempt = {
      id: attemptId,
      test_id: `practice-test-${Date.now()}`,
      student_id: 'student-1',
      started_at: new Date().toISOString(),
      completed_at: null,
      score: 0,
      max_score: count * 10,
      correct_count: 0,
      total_count: count,
      xp_earned: 0,
      combo_count: 0,
      combo_max: 0,
      answered_questions: new Set<string>(),
      correctAnswerMap: new Map<string, string>(),
      shuffledQuestions: [questionWithoutAnswer] as Record<string, unknown>[],
      // 적응형 필드
      is_adaptive: true,
      grade,
      category,
      current_difficulty: starting_difficulty,
      testTitle,
      generatedAnswerMap,
      lastAnswerCorrect: null,
    }
    currentAttempts.set(attemptId, attempt)

    return HttpResponse.json(
      {
        success: true,
        data: {
          attempt_id: attemptId,
          test: {
            id: attempt.test_id,
            title: testTitle,
            is_adaptive: true,
            questions: [questionWithoutAnswer],
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

    // 정답 확인: 엔진 생성 문제는 generatedAnswerMap, 기존 문제는 correctAnswerMap + getQuestionById
    let correctAnswer: string
    let explanation: string
    let questionPoints: number

    const generatedInfo = attempt.generatedAnswerMap.get(body.question_id)
    if (generatedInfo) {
      // 엔진 생성 문제
      correctAnswer = generatedInfo.correct_answer
      explanation = generatedInfo.explanation
      questionPoints = generatedInfo.points
    } else {
      // 기존 고정형 문제
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
      correctAnswer = attempt.correctAnswerMap.get(body.question_id) ?? question.correct_answer
      explanation = question.explanation
      questionPoints = question.points
    }

    const isCorrect = body.selected_answer === correctAnswer
    // 시간 초과 판별 (빈 문자열 제출 = 시간 초과)
    const isTimeUp = body.selected_answer === ''
    attempt.answered_questions.add(body.question_id)
    attempt.lastAnswerCorrect = isCorrect

    // 시간 보너스: 빠르게 풀수록 높은 보너스 (정답 && 시간 초과 아닐 때만)
    let timeBonus = 0
    if (isCorrect && !isTimeUp) {
      const timeLimit = attempt.category === 'computation' ? 20 : 60
      const remainingRatio = Math.max(0, 1 - body.time_spent_seconds / timeLimit)
      // 최대 보너스: questionPoints의 50%
      timeBonus = Math.floor(questionPoints * 0.5 * remainingRatio)
    }

    let pointsEarned = 0
    if (isCorrect) {
      attempt.correct_count++
      attempt.combo_count++
      attempt.combo_max = Math.max(attempt.combo_max, attempt.combo_count)

      // 콤보 보너스 계산
      let comboMultiplier = 1
      if (attempt.combo_count >= 5) comboMultiplier = 2
      else if (attempt.combo_count >= 3) comboMultiplier = 1.5

      pointsEarned = Math.floor(questionPoints * comboMultiplier) + timeBonus
      attempt.score += pointsEarned
      attempt.xp_earned += Math.floor(pointsEarned * 0.5)
    } else {
      attempt.combo_count = 0
    }

    // 적응형: 난이도 조절 (시간 초과도 오답과 동일하게 난이도 하락)
    if (attempt.is_adaptive) {
      if (isCorrect) {
        attempt.current_difficulty = Math.min(10, attempt.current_difficulty + 1)
      } else {
        attempt.current_difficulty = Math.max(1, attempt.current_difficulty - 1)
      }
    }

    const questionsRemaining =
      attempt.total_count - attempt.answered_questions.size

    return HttpResponse.json({
      success: true,
      data: {
        is_correct: isCorrect,
        correct_answer: correctAnswer,
        explanation,
        points_earned: pointsEarned,
        time_bonus: timeBonus,
        combo_count: attempt.combo_count,
        xp_earned: attempt.xp_earned,
        current_score: attempt.score,
        questions_remaining: questionsRemaining,
        next_difficulty: attempt.is_adaptive ? attempt.current_difficulty : undefined,
      },
    })
  }),

  // POST /api/v1/tests/attempts/:attemptId/next (적응형 다음 문제)
  http.post('/api/v1/tests/attempts/:attemptId/next', ({ params, request }) => {
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

    const questionsAnswered = attempt.answered_questions.size
    const questionsRemaining = attempt.total_count - questionsAnswered

    // 모든 문제를 풀었으면 완료
    if (questionsRemaining <= 0) {
      return HttpResponse.json({
        success: true,
        data: {
          question: null,
          current_difficulty: attempt.current_difficulty,
          questions_answered: questionsAnswered,
          questions_remaining: 0,
          is_complete: true,
        },
      })
    }

    // 엔진으로 다음 문제 생성
    const nextQuestion = generateAdaptiveQuestion(
      attempt.grade,
      attempt.category,
      attempt.current_difficulty,
      ALL_TEMPLATES
    )

    if (!nextQuestion) {
      // 해당 난이도에 템플릿이 없으면 완료 처리
      return HttpResponse.json({
        success: true,
        data: {
          question: null,
          current_difficulty: attempt.current_difficulty,
          questions_answered: questionsAnswered,
          questions_remaining: questionsRemaining,
          is_complete: true,
        },
      })
    }

    // 정답 저장
    attempt.generatedAnswerMap.set(nextQuestion.id, {
      correct_answer: nextQuestion.correct_answer,
      explanation: nextQuestion.explanation,
      points: nextQuestion.points,
    })

    // 정답 제외
    const { correct_answer: _ca, explanation: _ex, ...questionWithoutAnswer } = nextQuestion

    // 문제 목록에 추가
    attempt.shuffledQuestions.push(questionWithoutAnswer as Record<string, unknown>)

    return HttpResponse.json({
      success: true,
      data: {
        question: questionWithoutAnswer,
        current_difficulty: attempt.current_difficulty,
        questions_answered: questionsAnswered,
        questions_remaining: questionsRemaining - 1,
        is_complete: false,
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

    // 사용자 데이터로 게이미피케이션 계산
    const token = authHeader.replace('Bearer ', '')
    const userId = parseTokenUserId(token)
    const user = userId ? findUserById(userId) : null

    const oldLevel = user?.level ?? 1
    const oldTotalXp = user?.total_xp ?? 0
    const newTotalXp = oldTotalXp + attempt.xp_earned
    const calculatedLevel = getLevelForXp(newTotalXp)
    const levelUp = calculatedLevel > oldLevel

    // 레벨다운 체크 (적응형만, 정답률 < 30% && 갭 >= 2 && 레벨 > 1)
    let levelDown = false
    let levelDownAction: string = 'none'
    let levelDownDefense: number | null = user ? 3 : null
    let finalLevel = levelUp ? calculatedLevel : oldLevel

    if (attempt.is_adaptive && attempt.total_count > 0) {
      const accuracy = attempt.correct_count / attempt.total_count
      const gap = oldLevel - attempt.current_difficulty

      if (accuracy >= 0.6 && levelDownDefense !== null && levelDownDefense < 3) {
        // 실드 회복
        levelDownDefense = Math.min((levelDownDefense ?? 0) + 1, 3)
        levelDownAction = 'defense_restored'
      } else if (accuracy < 0.3 && gap >= 2 && oldLevel > 1) {
        // 심각한 실패 → 실드 소모 또는 레벨다운
        if (levelDownDefense && levelDownDefense > 0) {
          levelDownDefense -= 1
          levelDownAction = 'defense_consumed'
        } else {
          finalLevel = Math.max(oldLevel - 1, 1)
          levelDownDefense = 3
          levelDownAction = 'level_down'
          levelDown = true
        }
      }
    }

    // 마스터 판정: 적응형 + Lv.9~10 도달 + 정답률 70% 이상
    let masteryAchieved = false
    if (attempt.is_adaptive && attempt.total_count > 0) {
      const accuracy = attempt.correct_count / attempt.total_count
      if (attempt.current_difficulty >= 9 && accuracy >= 0.7) {
        masteryAchieved = true
        // 마스터 알림 저장 (stats 핸들러에서 참조)
        const gradeMap: Record<string, string> = {
          elementary_1: 'elementary_2', elementary_2: 'elementary_3',
          elementary_3: 'elementary_4', elementary_4: 'elementary_5',
          elementary_5: 'elementary_6', elementary_6: 'middle_1',
          middle_1: 'middle_2', middle_2: 'middle_3',
          middle_3: 'high_1',
        }
        const nextGrade = gradeMap[attempt.grade]
        if (nextGrade && user) {
          masteryAlerts.push({
            type: 'mastery' as const,
            student_id: attempt.student_id,
            student_name: user.name,
            message: `${user.name} 학생이 ${attempt.grade} Lv.10을 마스터했습니다!`,
            current_grade: attempt.grade,
            recommended_grade: nextGrade,
          })
        }
      }
    }

    // 스트릭 업데이트 (항상 +1)
    const currentStreak = (user?.current_streak ?? 0) + 1

    // mock user 데이터 동기화 (메모리)
    if (user) {
      user.total_xp = newTotalXp
      user.level = levelDown ? finalLevel : (levelUp ? calculatedLevel : user.level)
      user.current_streak = currentStreak
    }

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
        level_up: levelUp && !levelDown,
        level_down: levelDown,
        new_level: (levelUp || levelDown) ? finalLevel : null,
        xp_earned: attempt.xp_earned,
        total_xp: newTotalXp,
        current_streak: currentStreak,
        achievements_earned: [],
        level_down_defense: levelDownDefense,
        level_down_action: levelDownAction,
        mastery_achieved: masteryAchieved || undefined,
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
      const questions = test
        ? getQuestionsForTest(test.id).map(({ correct_answer, ...q }) => q)
        : []
      return HttpResponse.json({
        success: true,
        data: {
          attempt: existingAttempt,
          answers: [],
          test: test ? { ...test, questions } : test,
        },
      })
    }

    // 테스트 정보: mockTests에서 찾거나 적응형이면 가상 테스트 생성
    const staticTest = getTestById(attempt.test_id)
    const test = staticTest
      ? { ...staticTest, questions: attempt.shuffledQuestions }
      : {
          id: attempt.test_id,
          title: attempt.testTitle,
          description: `${attempt.category === 'computation' ? '연산' : '개념'} 적응형 연습`,
          grade: attempt.grade,
          category: attempt.category,
          concept_ids: [],
          question_count: attempt.total_count,
          is_active: true,
          is_adaptive: attempt.is_adaptive,
          created_at: attempt.started_at,
          questions: attempt.shuffledQuestions,
        }

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
          is_adaptive: attempt.is_adaptive,
          current_difficulty: attempt.is_adaptive ? attempt.current_difficulty : undefined,
          category: attempt.category || undefined,
        },
        answers: [],
        test,
      },
    })
  }),
]
