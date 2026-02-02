// 테스트 풀이 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import { QuestionCard } from '../../components/test/QuestionCard'
import { FeedbackModal } from '../../components/test/FeedbackModal'
import { ProgressBar } from '../../components/test/ProgressBar'
import { ComboDisplay } from '../../components/test/ComboDisplay'
import type { Question, SubmitAnswerResponse } from '../../types'

interface AttemptDetail {
  attempt_id: string
  test: {
    id: string
    title: string
    questions: Question[]
  }
}

export function TestPlayPage() {
  const { attemptId } = useParams<{ attemptId: string }>()
  const navigate = useNavigate()

  const [attemptDetail, setAttemptDetail] = useState<AttemptDetail | null>(null)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [feedbackData, setFeedbackData] = useState<SubmitAnswerResponse | null>(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [score, setScore] = useState(0)
  const [combo, setCombo] = useState(0)
  const [startTime, setStartTime] = useState<number>(Date.now())
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (attemptId) {
      fetchAttemptDetail()
    }
  }, [attemptId])

  const fetchAttemptDetail = async () => {
    try {
      setIsLoading(true)
      // 시도 정보 조회
      const response = await api.get<{ success: boolean; data: AttemptDetail }>(
        `/api/v1/tests/attempts/${attemptId}`
      )
      setAttemptDetail(response.data.data)
    } catch {
      setError('테스트 정보를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSelectAnswer = (answer: string) => {
    if (!showFeedback) {
      setSelectedAnswer(answer)
    }
  }

  const handleSubmitAnswer = async () => {
    if (!attemptId || !selectedAnswer || !attemptDetail) return

    const currentQuestion = attemptDetail.test.questions[currentIndex]
    if (!currentQuestion) return

    const timeSpent = Math.floor((Date.now() - startTime) / 1000)

    try {
      setIsSubmitting(true)
      const response = await api.post<{ success: boolean; data: SubmitAnswerResponse }>(
        `/api/v1/tests/attempts/${attemptId}/submit`,
        {
          question_id: currentQuestion.id,
          selected_answer: selectedAnswer,
          time_spent_seconds: timeSpent,
        }
      )

      const result = response.data.data
      setFeedbackData(result)
      setScore(result.current_score)
      setCombo(result.combo_count)
      setShowFeedback(true)
    } catch {
      setError('답안 제출에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleNextQuestion = () => {
    if (!attemptDetail) return

    const isLastQuestion = currentIndex >= attemptDetail.test.questions.length - 1

    if (isLastQuestion) {
      // 테스트 완료
      completeTest()
    } else {
      // 다음 문제
      setCurrentIndex((prev) => prev + 1)
      setSelectedAnswer(null)
      setFeedbackData(null)
      setShowFeedback(false)
      setStartTime(Date.now())
    }
  }

  const completeTest = async () => {
    if (!attemptId) return

    try {
      await api.post(`/api/v1/tests/attempts/${attemptId}/complete`)
      navigate(`/test/result/${attemptId}`)
    } catch {
      setError('테스트 완료에 실패했습니다.')
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">문제를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error || !attemptDetail) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error || '테스트를 찾을 수 없습니다.'}</p>
          <button onClick={() => navigate('/tests')} className="btn-primary px-4 py-2">
            목록으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  const currentQuestion = attemptDetail.test.questions[currentIndex]
  const totalQuestions = attemptDetail.test.questions.length
  const isLastQuestion = currentIndex >= totalQuestions - 1

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="sticky top-0 z-10 bg-white shadow-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <h1 className="text-lg font-semibold text-gray-900">
              {attemptDetail.test.title}
            </h1>
            <div className="flex items-center gap-4">
              <ComboDisplay combo={combo} />
              <div className="text-sm font-medium text-gray-600">
                점수: <span className="text-primary-500">{score}</span>
              </div>
            </div>
          </div>
          <ProgressBar current={currentIndex + 1} total={totalQuestions} />
        </div>
      </header>

      {/* 문제 */}
      <main className="container mx-auto px-4 py-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            {currentQuestion && (
              <QuestionCard
                question={currentQuestion}
                questionNumber={currentIndex + 1}
                selectedAnswer={selectedAnswer}
                onSelectAnswer={handleSelectAnswer}
                disabled={showFeedback}
              />
            )}
          </motion.div>
        </AnimatePresence>

        {/* 제출 버튼 */}
        {!showFeedback && (
          <div className="mt-6 text-center">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSubmitAnswer}
              disabled={!selectedAnswer || isSubmitting}
              className="btn-primary px-8 py-3 text-lg disabled:opacity-50"
            >
              {isSubmitting ? '제출 중...' : '정답 확인'}
            </motion.button>
          </div>
        )}
      </main>

      {/* 피드백 모달 */}
      <FeedbackModal
        isOpen={showFeedback}
        isCorrect={feedbackData?.is_correct ?? false}
        correctAnswer={feedbackData?.correct_answer ?? ''}
        explanation={feedbackData?.explanation ?? ''}
        pointsEarned={feedbackData?.points_earned ?? 0}
        comboCount={feedbackData?.combo_count ?? 0}
        isLastQuestion={isLastQuestion}
        onNext={handleNextQuestion}
      />
    </div>
  )
}
