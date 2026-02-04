// 테스트 결과 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import confetti from 'canvas-confetti'
import api from '../../lib/api'
import { ReportQuestionModal } from '../../components/test/ReportQuestionModal'
import type { TestAttempt, Test, AnswerLog, LevelDownAction } from '../../types'

interface CompleteState {
  level_up?: boolean
  level_down?: boolean
  new_level?: number | null
  xp_earned?: number
  level_down_defense?: number | null
  level_down_action?: LevelDownAction | null
  mastery_achieved?: boolean
}

interface AttemptResult {
  attempt: TestAttempt
  test: Test
  answers: AnswerLog[]
}

export function TestResultPage() {
  const { attemptId } = useParams<{ attemptId: string }>()
  const navigate = useNavigate()
  const location = useLocation()
  const completeState = (location.state as CompleteState) || {}
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [reportQuestionId, setReportQuestionId] = useState<string | null>(null)

  useEffect(() => {
    if (attemptId) {
      fetchResult()
    }
  }, [attemptId])

  useEffect(() => {
    if (!result) return
    const accuracy = getAccuracyRate()

    // 전문 정답 → perfect 효과음
    if (accuracy === 100) {
      const perfectSound = new Audio('/sounds/perfect.mp3')
      perfectSound.play().catch(() => {})
    }

    // 레벨업 효과음
    if (completeState.level_up) {
      const lvlupSound = new Audio('/sounds/lvlup.mp3')
      lvlupSound.play().catch(() => {})
    }

    // 레벨다운 효과음
    if (completeState.level_down) {
      const lvldownSound = new Audio('/sounds/lvldown.mp3')
      lvldownSound.play().catch(() => {})
    }

    // 좋은 성적일 때 폭죽 효과
    if (accuracy >= 80) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      })
    }
    // 마스터 달성 시 추가 폭죽
    if (completeState.mastery_achieved) {
      setTimeout(() => {
        confetti({ particleCount: 200, spread: 100, origin: { y: 0.4 } })
      }, 500)
      setTimeout(() => {
        confetti({ particleCount: 150, angle: 60, spread: 55, origin: { x: 0 } })
        confetti({ particleCount: 150, angle: 120, spread: 55, origin: { x: 1 } })
      }, 1000)
    }
  }, [result])

  const fetchResult = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<{ success: boolean; data: AttemptResult }>(
        `/api/v1/tests/attempts/${attemptId}`
      )
      setResult(response.data.data)
    } catch {
      setError('결과를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const getAccuracyRate = () => {
    if (!result) return 0
    return Math.round((result.attempt.correct_count / result.attempt.total_count) * 100)
  }

  const getGrade = () => {
    const rate = getAccuracyRate()
    if (rate >= 90) return { grade: 'A+', color: 'text-purple-500', emoji: '🏆' }
    if (rate >= 80) return { grade: 'A', color: 'text-primary-500', emoji: '🌟' }
    if (rate >= 70) return { grade: 'B', color: 'text-blue-500', emoji: '👍' }
    if (rate >= 60) return { grade: 'C', color: 'text-yellow-500', emoji: '💪' }
    return { grade: 'D', color: 'text-gray-500', emoji: '📚' }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">결과를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error || !result) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error || '결과를 찾을 수 없습니다.'}</p>
          <button onClick={() => navigate('/tests')} className="btn-primary px-4 py-2">
            목록으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  const { grade, color, emoji } = getGrade()
  const accuracyRate = getAccuracyRate()

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white py-8">
      <div className="container mx-auto px-4">
        {/* 결과 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mx-auto max-w-lg"
        >
          <div className="card overflow-hidden">
            {/* 헤더 */}
            <div className="bg-gradient-to-r from-primary-500 to-primary-600 p-6 text-center text-white">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', delay: 0.2 }}
                className="mb-2 text-6xl"
              >
                {emoji}
              </motion.div>
              <h1 className="text-2xl font-bold">테스트 완료!</h1>
              <p className="mt-1 text-primary-100">{result.test.title}</p>
            </div>

            {/* 점수 */}
            <div className="p-6">
              <div className="mb-6 text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', delay: 0.4 }}
                  className={`text-7xl font-black ${color}`}
                >
                  {grade}
                </motion.div>
                <div className="mt-2 text-lg text-gray-600">정답률 {accuracyRate}%</div>
              </div>

              {/* 통계 */}
              <div className="mb-6 grid grid-cols-3 gap-4">
                <StatItem
                  icon="✅"
                  label="정답"
                  value={`${result.attempt.correct_count}개`}
                  color="text-correct"
                />
                <StatItem
                  icon="❌"
                  label="오답"
                  value={`${result.attempt.total_count - result.attempt.correct_count}개`}
                  color="text-incorrect"
                />
                <StatItem
                  icon="🔥"
                  label="최대 콤보"
                  value={`${result.attempt.combo_max}`}
                  color="text-combo"
                />
              </div>

              {/* XP 획득 */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="mb-6 rounded-xl bg-levelup/10 p-4 text-center"
              >
                <div className="text-sm text-gray-600">획득한 경험치</div>
                <div className="text-2xl font-bold text-levelup">+{result.attempt.xp_earned} XP</div>
              </motion.div>

              {/* 레벨업 */}
              {completeState.level_up && completeState.new_level && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.7, type: 'spring' }}
                  className="mb-6 rounded-xl bg-yellow-50 border border-yellow-200 p-4 text-center"
                >
                  <div className="text-2xl mb-1">🎉</div>
                  <div className="text-sm font-medium text-yellow-800">레벨 업!</div>
                  <div className="text-xl font-bold text-yellow-600">Lv.{completeState.new_level}</div>
                </motion.div>
              )}

              {/* 레벨다운 방어 소모 */}
              {completeState.level_down_action === 'defense_consumed' && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="mb-6 rounded-xl bg-orange-50 border border-orange-200 p-4 text-center"
                >
                  <div className="text-2xl mb-1">🛡️</div>
                  <div className="text-sm font-medium text-orange-800">레벨다운 방어 발동!</div>
                  <div className="text-xs text-orange-600 mt-1">
                    남은 방어 횟수: {completeState.level_down_defense ?? 0}/3
                  </div>
                  <div className="text-xs text-orange-500 mt-1">
                    방어가 모두 소진되면 레벨이 하락할 수 있어요
                  </div>
                </motion.div>
              )}

              {/* 레벨다운 실행 */}
              {completeState.level_down && completeState.new_level && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.7, type: 'spring' }}
                  className="mb-6 rounded-xl bg-red-50 border border-red-200 p-4 text-center"
                >
                  <div className="text-2xl mb-1">📉</div>
                  <div className="text-sm font-medium text-red-800">레벨이 하락했어요</div>
                  <div className="text-xl font-bold text-red-600">Lv.{completeState.new_level}</div>
                  <div className="text-xs text-red-500 mt-1">
                    방어 실드가 복구되었어요 (3/3)
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    다시 열심히 풀면 레벨을 올릴 수 있어요!
                  </div>
                </motion.div>
              )}

              {/* 방어 실드 회복 */}
              {completeState.level_down_action === 'defense_restored' && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="mb-6 rounded-xl bg-green-50 border border-green-200 p-4 text-center"
                >
                  <div className="text-2xl mb-1">🛡️✨</div>
                  <div className="text-sm font-medium text-green-800">방어 실드 회복!</div>
                  <div className="text-xs text-green-600 mt-1">
                    실드: {completeState.level_down_defense ?? 0}/3
                  </div>
                </motion.div>
              )}

              {/* 마스터 달성 */}
              {completeState.mastery_achieved && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8, type: 'spring' }}
                  className="mb-6 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 p-5 text-center text-white shadow-lg"
                >
                  <div className="text-4xl mb-2">🏆</div>
                  <div className="text-lg font-bold">Lv.10 마스터!</div>
                  <div className="text-sm text-purple-100 mt-1">
                    선생님에게 승급 추천이 전달되었습니다
                  </div>
                </motion.div>
              )}

              {/* 점수 */}
              <div className="mb-6 rounded-xl bg-gray-50 p-4 text-center">
                <div className="text-sm text-gray-600">총 점수</div>
                <div className="text-3xl font-bold text-gray-900">
                  {result.attempt.score} / {result.attempt.max_score}
                </div>
              </div>

              {/* 버튼 */}
              <div className="space-y-3">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => navigate('/tests')}
                  className="btn-primary w-full py-3"
                >
                  다른 테스트 풀기
                </motion.button>
                <button
                  onClick={() => navigate('/dashboard')}
                  className="w-full py-3 text-gray-600 hover:text-gray-800"
                >
                  대시보드로 돌아가기
                </button>
              </div>
            </div>
          </div>

          {/* 오답 노트 */}
          {result.answers.some((a) => !a.is_correct) && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="mt-6"
            >
              <div className="card p-6">
                <h2 className="mb-4 text-lg font-semibold text-gray-900">오답 노트</h2>
                <div className="space-y-4">
                  {result.answers
                    .filter((a) => !a.is_correct)
                    .map((answer, index) => (
                      <WrongAnswerItem
                        key={answer.id}
                        answer={answer}
                        index={index + 1}
                        onReport={() => setReportQuestionId(answer.question_id)}
                      />
                    ))}
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* 문제 신고 모달 */}
      {reportQuestionId && (
        <ReportQuestionModal
          isOpen={!!reportQuestionId}
          questionId={reportQuestionId}
          onClose={() => setReportQuestionId(null)}
        />
      )}
    </div>
  )
}

interface StatItemProps {
  icon: string
  label: string
  value: string
  color: string
}

function StatItem({ icon, label, value, color }: StatItemProps) {
  return (
    <div className="rounded-xl bg-gray-50 p-3 text-center">
      <div className="mb-1 text-xl">{icon}</div>
      <div className="text-xs text-gray-500">{label}</div>
      <div className={`font-bold ${color}`}>{value}</div>
    </div>
  )
}

interface WrongAnswerItemProps {
  answer: AnswerLog
  index: number
  onReport: () => void
}

function WrongAnswerItem({ answer, index, onReport }: WrongAnswerItemProps) {
  return (
    <div className="rounded-xl border border-red-100 bg-red-50 p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-medium text-red-700">문제 #{index}</span>
        <span className="text-sm text-gray-500">내 답: {answer.selected_answer}</span>
      </div>
      <div className="flex items-center justify-between">
        <button className="text-sm text-primary-500 hover:underline">복습하기</button>
        <button
          onClick={onReport}
          className="flex items-center gap-1 text-xs text-gray-400 transition-colors hover:text-red-500"
        >
          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
          </svg>
          신고
        </button>
      </div>
    </div>
  )
}

