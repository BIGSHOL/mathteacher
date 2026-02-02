// 템플릿 레지스트리
// 모든 학년의 템플릿을 한 곳에서 관리

import type { QuestionTemplate } from '../types'
import type { Grade, QuestionCategory } from '../../../types'
import { elementary1Templates } from './elementary1'
import { elementary2Templates } from './elementary2'
import { elementary3Templates } from './elementary3'
import { elementary4Templates } from './elementary4'
import { elementary5Templates } from './elementary5'
import { elementary6Templates } from './elementary6'
import { middle1Templates } from './middle1'
import { middle2Templates } from './middle2'
import { middle3Templates } from './middle3'
import { high1Templates } from './high1'

/** 전체 템플릿 목록 */
const ALL_TEMPLATES: QuestionTemplate[] = [
  ...elementary1Templates,
  ...elementary2Templates,
  ...elementary3Templates,
  ...elementary4Templates,
  ...elementary5Templates,
  ...elementary6Templates,
  ...middle1Templates,
  ...middle2Templates,
  ...middle3Templates,
  ...high1Templates,
]

/** 조건에 맞는 템플릿 조회 */
export function getTemplates(
  grade?: Grade,
  category?: QuestionCategory,
  level?: number
): QuestionTemplate[] {
  return ALL_TEMPLATES.filter((t) => {
    if (grade && t.grade !== grade) return false
    if (category && t.category !== category) return false
    if (level !== undefined && t.level !== level) return false
    return true
  })
}

/** 특정 학년에서 사용 가능한 레벨 범위 조회 */
export function getAvailableLevels(
  grade: Grade,
  category: QuestionCategory
): number[] {
  const levels = new Set<number>()
  for (const t of ALL_TEMPLATES) {
    if (t.grade === grade && t.category === category) {
      levels.add(t.level)
    }
  }
  return Array.from(levels).sort((a, b) => a - b)
}

/** 지원하는 학년 목록 */
export function getSupportedGrades(): Grade[] {
  const grades = new Set<Grade>()
  for (const t of ALL_TEMPLATES) {
    grades.add(t.grade)
  }
  return Array.from(grades)
}

export { ALL_TEMPLATES }
