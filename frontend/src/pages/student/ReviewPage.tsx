// 복습 페이지 - 틀렸던 문제 다시 풀기

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import { QuestionCard } from '../../components/test/QuestionCard'
import type { Question } from '../../types'

interface WrongQuestion {
  question: Question
  wrong_count: number
  last_selected_answer: string
  last_attempted_at: string
}

interface ReviewData {
  items: WrongQuestion[]
  total: number
}

export function ReviewPage() {
  const [data, setData] = useState<ReviewData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [revealedIds, setRevealedIds] = useState<Set<string>>(new Set())
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({})

  useEffect(() => {
    fetchWrongQuestions()
  }, [])

  const fetchWrongQuestions = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<{ success: boolean; data: ReviewData }>(
        '/api/v1/tests/review/wrong-questions'
      )
      setData(response.data.data)
    } catch {
      setError('오답 목록을 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSelect = (questionId: string, answer: string) => {
    if (revealedIds.has(questionId)) return
    setSelectedAnswers((prev) => ({ ...prev, [questionId]: answer }))
  }

  const handleReveal = (questionId: string) => {
    setRevealedIds((prev) => new Set(prev).add(questionId))
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">오답 목록을 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error}</p>
          <button onClick={fetchWrongQuestions} className="btn-primary px-4 py-2">
            다시 시도
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-4 sm:py-8">
      <div className="container mx-auto px-3 sm:px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 sm:mb-8"
        >
          <h1 className="text-xl sm:text-2xl font-bold text-gray-900">복습하기</h1>
          <p className="text-gray-600">
            틀렸던 문제를 다시 풀어보세요 ({data?.total ?? 0}문제)
          </p>
        </motion.div>

        {!data || data.total === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="rounded-2xl bg-white p-8 text-center shadow-sm"
          >
            <div className="mb-4 text-5xl">🎉</div>
            <h2 className="mb-2 text-xl font-semibold text-gray-900">완벽해요!</h2>
            <p className="text-gray-600">틀린 문제가 없습니다. 계속 이 페이스를 유지하세요!</p>
          </motion.div>
        ) : (
          <div className="space-y-6">
            {data.items.map((item, index) => {
              const qId = item.question.id
              const isRevealed = revealedIds.has(qId)
              const selected = selectedAnswers[qId]
              const isCorrect = selected === item.question.correct_answer

              return (
                <motion.div
                  key={qId}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <QuestionCard
                    question={item.question}
                    questionNumber={index + 1}
                    selectedAnswer={selected || null}
                    onSelectAnswer={(ans) => handleSelect(qId, ans)}
                    disabled={isRevealed}
                    isCorrect={isCorrect}
                    showExplanation={isRevealed}
                    previousAnswer={item.last_selected_answer}
                    headerRight={
                      <span className="text-sm text-red-500 font-medium whitespace-nowrap">
                        {item.wrong_count}회 오답
                      </span>
                    }
                  />

                  {/* 확인 버튼 */}
                  {!isRevealed && (
                    <div className="mt-4 text-center">
                      <button
                        onClick={() => handleReveal(qId)}
                        disabled={!selected}
                        className="btn-primary px-6 py-2 disabled:opacity-50 transition-all hover:-translate-y-0.5 shadow-sm"
                      >
                        정답 확인
                      </button>
                    </div>
                  )}
                </motion.div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
