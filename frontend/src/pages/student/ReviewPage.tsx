// 복습 페이지 - 틀렸던 문제 다시 풀기

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import { MathText } from '../../components/common/MathText'
import type { QuestionOption } from '../../types'

interface WrongQuestion {
  question: {
    id: string
    concept_id: string
    question_type: string
    difficulty: string
    content: string
    options?: QuestionOption[]
    correct_answer: string
    explanation: string
    points: number
  }
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

  const getDifficultyLabel = (d: number | string) => {
    const lv = typeof d === 'number' ? d : parseInt(d, 10) || 5
    return `Lv.${lv}`
  }

  const getDifficultyColor = (d: number | string) => {
    const lv = typeof d === 'number' ? d : parseInt(d, 10) || 5
    if (lv <= 2) return 'bg-green-100 text-green-700'
    if (lv <= 4) return 'bg-emerald-100 text-emerald-700'
    if (lv <= 6) return 'bg-yellow-100 text-yellow-700'
    if (lv <= 8) return 'bg-orange-100 text-orange-700'
    return 'bg-red-100 text-red-700'
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
                  className="overflow-hidden rounded-2xl bg-white shadow-sm"
                >
                  {/* 문제 헤더 */}
                  <div className="border-b border-gray-100 px-4 py-3 sm:px-6 sm:py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600">
                          {index + 1}
                        </span>
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${getDifficultyColor(item.question.difficulty)}`}>
                          {getDifficultyLabel(item.question.difficulty)}
                        </span>
                      </div>
                      <span className="text-sm text-red-500 font-medium">
                        {item.wrong_count}회 오답
                      </span>
                    </div>
                  </div>

                  {/* 문제 내용 */}
                  <div className="px-4 py-3 sm:px-6 sm:py-4">
                    <p className="mb-4 text-lg font-medium text-gray-900">
                      <MathText text={item.question.content} />
                    </p>

                    {/* 선택지 */}
                    {item.question.options && (
                      <div className="space-y-2">
                        {item.question.options.map((opt) => {
                          const isThisSelected = selected === opt.label
                          const isThisCorrect = opt.label === item.question.correct_answer
                          const wasLastWrong = opt.label === item.last_selected_answer

                          let optionClass = 'border-gray-200 hover:border-primary-300 cursor-pointer'

                          if (isRevealed) {
                            if (isThisCorrect) {
                              optionClass = 'border-green-500 bg-green-50'
                            } else if (isThisSelected && !isCorrect) {
                              optionClass = 'border-red-500 bg-red-50'
                            } else {
                              optionClass = 'border-gray-200 opacity-50'
                            }
                          } else if (isThisSelected) {
                            optionClass = 'border-primary-500 bg-primary-50'
                          }

                          return (
                            <button
                              key={opt.id}
                              onClick={() => handleSelect(qId, opt.label)}
                              disabled={isRevealed}
                              className={`flex w-full items-center gap-3 rounded-xl border-2 p-3 text-left transition-all min-h-[3rem] ${optionClass}`}
                            >
                              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gray-100 text-sm font-bold text-gray-600">
                                {opt.label}
                              </span>
                              <span className="text-gray-800 leading-relaxed"><MathText text={opt.text} /></span>
                              {isRevealed && isThisCorrect && (
                                <span className="ml-auto text-green-600 font-medium text-sm">정답</span>
                              )}
                              {!isRevealed && wasLastWrong && (
                                <span className="ml-auto text-xs text-gray-400">지난번 선택</span>
                              )}
                            </button>
                          )
                        })}
                      </div>
                    )}

                    {/* 확인 버튼 */}
                    {!isRevealed && (
                      <div className="mt-4 text-center">
                        <button
                          onClick={() => handleReveal(qId)}
                          disabled={!selected}
                          className="btn-primary px-6 py-2 disabled:opacity-50"
                        >
                          정답 확인
                        </button>
                      </div>
                    )}

                    {/* 결과 & 해설 */}
                    <AnimatePresence>
                      {isRevealed && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="mt-4"
                        >
                          <div className={`rounded-xl p-4 ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
                            <p className={`font-semibold ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                              {isCorrect ? '🎉 정답!' : '❌ 오답'}
                            </p>
                            <p className="mt-2 text-sm text-gray-700">
                              <span className="font-medium">해설:</span> <MathText text={item.question.explanation} />
                            </p>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
