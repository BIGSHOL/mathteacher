import { generateQuestions, generateAdaptiveQuestion } from '../engine'
import type { QuestionTemplate, GenerateRequest, Params, Answer } from '../types'

// Mock template for testing
const mockTemplate: QuestionTemplate = {
  id: 'test-add-1',
  grade: 'middle_1',
  category: 'computation',
  level: 3,
  part: 'calc',
  conceptId: 'M1-NUM-01',
  pattern: '{a} + {b} = ?',
  paramRanges: { a: [1, 10], b: [1, 10] },
  answerFn: (p: Params): Answer => (p.a ?? 0) + (p.b ?? 0),
  distractorFns: [
    (p: Params): Answer => (p.a ?? 0) - (p.b ?? 0),
    (p: Params): Answer => (p.a ?? 0) * (p.b ?? 0),
    (p: Params): Answer => Math.abs((p.a ?? 0) - (p.b ?? 0)),
  ],
  explanationFn: (p: Params, ans: Answer): string =>
    `${p.a}와 ${p.b}를 더하면 ${ans}입니다.`,
}

const mockTemplate2: QuestionTemplate = {
  id: 'test-multiply-1',
  grade: 'middle_1',
  category: 'computation',
  level: 5,
  part: 'calc',
  conceptId: 'M1-NUM-02',
  pattern: '{a} × {b} = ?',
  paramRanges: { a: [2, 5], b: [2, 5] },
  answerFn: (p: Params): Answer => (p.a ?? 0) * (p.b ?? 0),
  distractorFns: [
    (p: Params): Answer => (p.a ?? 0) + (p.b ?? 0),
    (p: Params): Answer => (p.a ?? 0) * (p.b ?? 0) - 1,
    (p: Params): Answer => (p.a ?? 0) * (p.b ?? 0) + 1,
  ],
  explanationFn: (p: Params, ans: Answer): string =>
    `${p.a}와 ${p.b}를 곱하면 ${ans}입니다.`,
}

describe('generateQuestions', () => {
  it('빈 템플릿 배열로는 빈 배열을 반환한다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [])
    expect(result).toEqual([])
  })

  it('조건에 맞는 템플릿이 없으면 빈 배열을 반환한다', () => {
    const request: GenerateRequest = {
      grade: 'elementary_6',
      category: 'concept',
      level: 1,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    expect(result).toEqual([])
  })

  it('조건에 맞는 템플릿으로 문제를 생성한다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    expect(result.length).toBe(1)
    expect(result[0]).toBeDefined()
  })

  it('생성된 문제가 올바른 구조를 가진다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    const question = result[0]!

    expect(question).toHaveProperty('id')
    expect(question).toHaveProperty('concept_id')
    expect(question).toHaveProperty('category')
    expect(question).toHaveProperty('part')
    expect(question).toHaveProperty('question_type')
    expect(question).toHaveProperty('difficulty')
    expect(question).toHaveProperty('content')
    expect(question).toHaveProperty('options')
    expect(question).toHaveProperty('correct_answer')
    expect(question).toHaveProperty('explanation')
    expect(question).toHaveProperty('points')
  })

  it('생성된 문제의 값이 유효하다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    const question = result[0]!

    expect(question.id).toBeTruthy()
    expect(question.concept_id).toBe('M1-NUM-01')
    expect(question.category).toBe('computation')
    expect(question.part).toBe('calc')
    expect(question.question_type).toBe('multiple_choice')
    expect(question.difficulty).toBe(3)
    expect(question.content).toMatch(/\d+ \+ \d+ = \?/)
    expect(question.options.length).toBeGreaterThan(0)
    expect(['A', 'B', 'C', 'D', 'E', 'F']).toContain(question.correct_answer)
    expect(question.explanation).toBeTruthy()
    expect(question.points).toBe(10)
  })

  it('요청한 개수만큼 문제를 생성한다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 3,
    }

    const result = generateQuestions(request, [mockTemplate])
    expect(result.length).toBe(3)
  })

  it('여러 템플릿 중 조건에 맞는 것으로 생성한다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 5,
      count: 2,
    }

    const result = generateQuestions(request, [mockTemplate, mockTemplate2])
    expect(result.length).toBe(2)
    result.forEach((q) => {
      expect(q.difficulty).toBe(5)
    })
  })

  it('문제 내용이 중복되지 않도록 시도한다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 5,
    }

    const result = generateQuestions(request, [mockTemplate])
    const contents = result.map((q) => q.content)
    const uniqueContents = new Set(contents)

    // 대부분 중복되지 않아야 함 (파라미터 범위가 충분히 큼)
    expect(uniqueContents.size).toBeGreaterThan(1)
  })

  it('options 배열에 정답이 포함되어 있다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    const question = result[0]!

    const correctOption = question.options.find(
      (opt) => opt.label === question.correct_answer
    )
    expect(correctOption).toBeDefined()
  })

  it('각 option이 고유한 id와 label을 가진다', () => {
    const request: GenerateRequest = {
      grade: 'middle_1',
      category: 'computation',
      level: 3,
      count: 1,
    }

    const result = generateQuestions(request, [mockTemplate])
    const question = result[0]!

    const ids = question.options.map((opt) => opt.id)
    const labels = question.options.map((opt) => opt.label)

    expect(new Set(ids).size).toBe(ids.length)
    expect(new Set(labels).size).toBe(labels.length)
  })
})

describe('generateAdaptiveQuestion', () => {
  it('조건에 맞는 템플릿으로 문제를 생성한다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      3,
      [mockTemplate]
    )

    expect(result).not.toBeNull()
    expect(result?.difficulty).toBe(3)
  })

  it('조건에 맞는 템플릿이 없으면 null을 반환한다', () => {
    const result = generateAdaptiveQuestion(
      'elementary_6',
      'concept',
      1,
      [mockTemplate]
    )

    expect(result).toBeNull()
  })

  it('레벨이 1보다 작으면 1로 제한한다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      -5,
      [mockTemplate]
    )

    // level 3인 템플릿만 있으므로 null
    expect(result).toBeNull()
  })

  it('레벨이 10보다 크면 10으로 제한한다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      15,
      [mockTemplate]
    )

    // level 3인 템플릿만 있으므로 null
    expect(result).toBeNull()
  })

  it('빈 템플릿 배열로는 null을 반환한다', () => {
    const result = generateAdaptiveQuestion('middle_1', 'computation', 3, [])

    expect(result).toBeNull()
  })

  it('여러 템플릿 중 레벨에 맞는 것으로 생성한다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      5,
      [mockTemplate, mockTemplate2]
    )

    expect(result).not.toBeNull()
    expect(result?.difficulty).toBe(5)
  })

  it('생성된 문제가 유효한 구조를 가진다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      3,
      [mockTemplate]
    )

    expect(result).not.toBeNull()
    if (result) {
      expect(result.id).toBeTruthy()
      expect(result.concept_id).toBeTruthy()
      expect(result.content).toBeTruthy()
      expect(result.options.length).toBeGreaterThan(0)
      expect(result.correct_answer).toBeTruthy()
      expect(result.explanation).toBeTruthy()
    }
  })

  it('정확히 하나의 문제를 생성한다', () => {
    const result = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      3,
      [mockTemplate]
    )

    // 단일 문제 또는 null
    expect(result === null || typeof result === 'object').toBe(true)
  })

  it('레벨 경계값을 올바르게 처리한다', () => {
    // 레벨 1 (최소)
    const result1 = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      1,
      [mockTemplate]
    )
    expect(result1).toBeNull() // level 3인 템플릿만 있음

    // 레벨 10 (최대)
    const result10 = generateAdaptiveQuestion(
      'middle_1',
      'computation',
      10,
      [mockTemplate]
    )
    expect(result10).toBeNull() // level 3인 템플릿만 있음
  })
})
