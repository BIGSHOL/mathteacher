// 문제 생성 엔진 코어

import type { QuestionOption } from '../../types'
import type { GenerateRequest, GeneratedQuestion, Params, QuestionTemplate } from './types'
import { answerToString, makeDistractors } from './distractors'
import { generateParams, shuffle, uuid } from './utils/random'

const LABELS = ['A', 'B', 'C', 'D', 'E', 'F']

/** 패턴 문자열에서 {param} 치환 */
function interpolate(pattern: string, params: Params): string {
  return pattern.replace(/\{(\w+)\}/g, (_, key) => {
    const val = params[key]
    return val !== undefined ? `${val}` : `{${key}}`
  })
}

/** 단일 문제 생성 */
function generateOne(template: QuestionTemplate): GeneratedQuestion {
  const params = generateParams(
    template.paramRanges,
    template.constraints
  )

  // 정답 계산
  const answer = template.answerFn(params)
  const correctStr = answerToString(answer)

  // 문제 내용
  const content = template.contentFn
    ? template.contentFn(params)
    : interpolate(template.pattern, params)

  // 풀이 설명
  const explanation = template.explanationFn(params, answer)

  // 오답 보기 생성
  const distractorStrs = makeDistractors(
    params,
    answer,
    template.distractorFns,
    3
  )

  // 보기 조립 + 셔플
  const allAnswers = shuffle([correctStr, ...distractorStrs])
  const options: QuestionOption[] = allAnswers.map((text, i) => ({
    id: `${i + 1}`,
    label: LABELS[i]!,
    text,
  }))

  // 정답 라벨 찾기
  const correctOption = options.find((o) => o.text === correctStr)
  const correctLabel = correctOption?.label ?? 'A'

  return {
    id: uuid(),
    concept_id: template.conceptId,
    category: template.category,
    part: template.part,
    question_type: template.questionType ?? 'multiple_choice',
    difficulty: template.level,
    content,
    options,
    correct_answer: correctLabel,
    explanation,
    points: template.points ?? 10,
  }
}

/**
 * 문제 생성 메인 함수.
 * 주어진 조건에 맞는 템플릿을 찾아 문제를 생성한다.
 */
export function generateQuestions(
  request: GenerateRequest,
  templates: QuestionTemplate[]
): GeneratedQuestion[] {
  const { grade, category, level, count = 1 } = request

  // 조건에 맞는 템플릿 필터링
  const matching = templates.filter(
    (t) => t.grade === grade && t.category === category && t.level === level
  )

  if (matching.length === 0) {
    return []
  }

  const results: GeneratedQuestion[] = []
  const usedContents = new Set<string>()

  for (let i = 0; i < count; i++) {
    // 최대 10번 시도하여 중복 문제 방지
    let question: GeneratedQuestion | null = null
    for (let attempt = 0; attempt < 10; attempt++) {
      const template = matching[Math.floor(Math.random() * matching.length)]!
      const q = generateOne(template)
      if (!usedContents.has(q.content)) {
        usedContents.add(q.content)
        question = q
        break
      }
    }
    if (question) {
      results.push(question)
    }
  }

  return results
}

/**
 * 적응형 테스트용 문제 생성.
 * 현재 레벨에서 시작하여, 정답/오답에 따라 다음 레벨을 조절.
 */
export function generateAdaptiveQuestion(
  grade: string,
  category: string,
  currentLevel: number,
  templates: QuestionTemplate[]
): GeneratedQuestion | null {
  const clamped = Math.max(1, Math.min(10, currentLevel))
  const results = generateQuestions(
    {
      grade: grade as GenerateRequest['grade'],
      category: category as GenerateRequest['category'],
      level: clamped,
    },
    templates
  )
  return results[0] ?? null
}
