/** 문제 유형 + 카테고리별 제한시간 (초) */
export function getTimeLimit(questionType?: string, category?: string): number {
  if (questionType === 'fill_in_blank') {
    return category === 'computation' ? 30 : 45
  }
  // multiple_choice, true_false, short_answer 등
  return category === 'computation' ? 20 : 30
}

/** 카테고리 기준 평균 제한시간 (초) - 테스트 전체 시간 추정용 */
export function getAverageTimeLimit(category?: string): number {
  return category === 'computation' ? 25 : 35
}
