// 테스트 결과 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import confetti from 'canvas-confetti'
import api from '../../lib/api'
import type { TestAttempt, Test, AnswerLog } from '../../types'

interface AttemptResult {
  attempt: TestAttempt
  test: Test
  answers: AnswerLog[]
}

export function TestResultPage() {
  const { attemptId } = useParams<{ attemptId: string }>()
  const navigate = useNavigate()
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (attemptId) {
      fetchResult()
    }
  }, [attemptId])

  useEffect(() => {
    // 좋은 성적일 때 폭죽 효과
    if (result && getAccuracyRate() >= 80) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      })
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
                      <WrongAnswerItem key={answer.id} answer={answer} index={index + 1} />
                    ))}
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
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
}

function WrongAnswerItem({ answer, index }: WrongAnswerItemProps) {
  return (
    <div className="rounded-xl border border-red-100 bg-red-50 p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-medium text-red-700">문제 #{index}</span>
        <span className="text-sm text-gray-500">내 답: {answer.selected_answer}</span>
      </div>
      <button className="text-sm text-primary-500 hover:underline">복습하기</button>
    </div>
  )
}

