// AI 학습 보조 API Mock 핸들러

import { http, HttpResponse } from 'msw'

// 힌트 레벨별 템플릿
const hintTemplates: Record<number, string> = {
  1: '이 문제는 기본 개념을 활용하는 문제입니다. 문제를 다시 한번 천천히 읽어보고, 어떤 연산이 필요한지 생각해 보세요.',
  2: '문제에서 주어진 조건을 정리해 보세요. 핵심 공식이나 성질을 떠올려 보고, 단계별로 접근해 보세요. 계산 과정에서 부호와 순서에 주의하세요.',
  3: '풀이 방향을 알려드릴게요. 먼저 주어진 값을 식에 대입하고, 한 단계씩 정리해 보세요. 최종 답을 구하기 직전까지의 과정을 확인하고, 마지막 계산만 직접 해보세요.',
}

// 오답 유형별 피드백 템플릿
const errorFeedbackTemplates = [
  {
    error_type: '계산 실수',
    feedback: '계산 과정에서 작은 실수가 있었어요. 각 단계의 계산을 다시 한번 검산해 보세요.',
    suggestion: '계산할 때 중간 과정을 꼭 적어두는 습관을 들이면 실수를 줄일 수 있어요.',
  },
  {
    error_type: '부호 오류',
    feedback: '부호 처리에서 실수가 있었을 수 있어요. 음수의 덧셈, 뺄셈, 곱셈 규칙을 다시 확인해 보세요.',
    suggestion: '부호가 바뀌는 지점을 표시해두면 실수를 예방할 수 있어요.',
  },
  {
    error_type: '개념 혼동',
    feedback: '관련 개념을 다시 복습해 보면 좋겠어요. 비슷하지만 다른 개념이 헷갈릴 수 있어요.',
    suggestion: '개념 노트를 만들어 핵심 차이점을 정리해 보세요.',
  },
  {
    error_type: '문제 이해 부족',
    feedback: '문제에서 묻는 것을 정확히 파악하는 것이 중요해요. 조건을 하나씩 밑줄 치며 읽어보세요.',
    suggestion: '문제를 읽을 때 "구하는 것"과 "주어진 것"을 먼저 구분하는 연습을 해보세요.',
  },
]

export const aiHandlers = [
  // POST /api/v1/ai/hint - AI 힌트 생성
  http.post('/api/v1/ai/hint', async ({ request }) => {
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
      question_content: string
      question_type: string
      options?: string[]
      student_grade: string
      hint_level: number
    }

    const { hint_level } = body

    // 힌트 레벨 검증
    if (hint_level < 1 || hint_level > 3) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'INVALID_HINT_LEVEL', message: '힌트 레벨은 1~3이어야 합니다.' },
        },
        { status: 400 }
      )
    }

    const hintText = hintTemplates[hint_level] ?? hintTemplates[1]!

    // 약간의 지연을 시뮬레이션 (실제 AI 호출처럼)
    await new Promise((resolve) => setTimeout(resolve, 300))

    return HttpResponse.json({
      success: true,
      data: {
        hint: hintText,
        hint_level,
      },
    })
  }),

  // POST /api/v1/ai/grade-fill-blank - 유연 채점
  http.post('/api/v1/ai/grade-fill-blank', async ({ request }) => {
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
      question_content: string
      correct_answer: string
      student_answer: string
      accept_formats?: string[]
    }

    const { correct_answer, student_answer } = body

    // 간단한 유연 채점 로직
    const normalize = (s: string) =>
      s.replace(/\s+/g, '').replace(/\u00d7/g, '*').replace(/\u00f7/g, '/').toLowerCase()

    const isExactMatch = normalize(correct_answer) === normalize(student_answer)

    // 분수/소수 동치 검사 (예: 1/2 = 0.5)
    let isEquivalent = false
    if (!isExactMatch) {
      try {
        const correctNum = eval(correct_answer)
        const studentNum = eval(student_answer)
        if (
          typeof correctNum === 'number' &&
          typeof studentNum === 'number' &&
          Math.abs(correctNum - studentNum) < 0.0001
        ) {
          isEquivalent = true
        }
      } catch {
        // eval 실패 시 무시
      }
    }

    const isCorrect = isExactMatch || isEquivalent

    return HttpResponse.json({
      success: true,
      data: {
        is_correct: isCorrect,
        confidence: isExactMatch ? 1.0 : isEquivalent ? 0.9 : 0.1,
        reason: isExactMatch
          ? '정확히 일치합니다.'
          : isEquivalent
            ? '표기는 다르지만 같은 값입니다.'
            : '정답과 일치하지 않습니다.',
      },
    })
  }),

  // POST /api/v1/ai/feedback - 맞춤 피드백 생성
  http.post('/api/v1/ai/feedback', async ({ request }) => {
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

    await request.json()
    await new Promise((resolve) => setTimeout(resolve, 200))

    // 랜덤 피드백 템플릿 선택
    const template = errorFeedbackTemplates[
      Math.floor(Math.random() * errorFeedbackTemplates.length)
    ]!

    return HttpResponse.json({
      success: true,
      data: {
        feedback: template.feedback,
        error_type: template.error_type,
        suggestion: template.suggestion,
      },
    })
  }),
]