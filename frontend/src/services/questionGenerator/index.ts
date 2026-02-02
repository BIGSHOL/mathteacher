// 문제 생성 엔진 메인 진입점

export { generateQuestions, generateAdaptiveQuestion } from './engine'
export { getTemplates, getAvailableLevels, getSupportedGrades, ALL_TEMPLATES } from './templates'
export type {
  QuestionTemplate,
  GenerateRequest,
  GeneratedQuestion,
  Params,
  Answer,
  Fraction,
} from './types'
