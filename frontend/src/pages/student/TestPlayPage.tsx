// 테스트 풀이 페이지 (고정형 + 적응형 dual-mode)

import { useEffect, useState, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import { useAuthStore } from '../../store/authStore'
import { QuestionCard } from '../../components/test/QuestionCard'
import { FeedbackModal } from '../../components/test/FeedbackModal'
import { ProgressBar } from '../../components/test/ProgressBar'
import { ComboDisplay } from '../../components/test/ComboDisplay'
import { CountdownTimer } from '../../components/test/CountdownTimer'
import type { Question, QuestionCategory, SubmitAnswerResponse, NextQuestionResponse, CompleteTestResult } from '../../types'

/** 카테고리별 제한시간 (초) */
const TIME_LIMITS: Record<string, number> = {
  computation: 20,
  concept: 60,
}
const DEFAULT_TIME_LIMIT = 60

/** 난이도 변경 정보 */
interface DifficultyChange {
  from: number
  to: number
  direction: 'up' | 'down'
}

interface AttemptDetail {
  attempt: {
    id: string
    test_id: string
    student_id: string
    score: number
    correct_count: number
    total_count: number
    combo_max: number
    is_adaptive: boolean
    current_difficulty?: number
    category?: QuestionCategory
  }
  test: {
    id: string
    title: string
    is_adaptive: boolean
    questions: Question[]
  }
  answers: unknown[]
}

/** 난이도 숫자를 한글 라벨로 변환 */
function getDifficultyLabel(level: number): string {
  if (level <= 3) return '기초'
  if (level <= 5) return '보통'
  if (level <= 7) return '심화'
  if (level <= 9) return '고급'
  return '최고급'
}

function getDifficultyColor(level: number): string {
  if (level <= 3) return 'text-green-600 bg-green-100'
  if (level <= 5) return 'text-blue-600 bg-blue-100'
  if (level <= 7) return 'text-yellow-600 bg-yellow-100'
  if (level <= 9) return 'text-orange-600 bg-orange-100'
  return 'text-red-600 bg-red-100'
}

/** 난이도 변경 토스트 */
function DifficultyChangeToast({ change }: { change: DifficultyChange }) {
  const isUp = change.direction === 'up'

  return (
    <motion.div
      initial={{ opacity: 0, y: isUp ? 40 : -40, scale: 0.8 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: isUp ? -20 : 20, scale: 0.8 }}
      transition={{ type: 'spring', damping: 15, stiffness: 300 }}
      className="fixed left-1/2 top-20 z-[60] -translate-x-1/2"
    >
      <div
        className={`flex items-center gap-3 rounded-2xl px-6 py-4 shadow-2xl ${
          isUp
            ? 'bg-gradient-to-r from-emerald-500 to-green-500 text-white'
            : 'bg-gradient-to-r from-orange-400 to-amber-500 text-white'
        }`}
      >
        <motion.span
          initial={{ scale: 0, rotate: isUp ? -180 : 180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: 'spring', delay: 0.1, damping: 10, stiffness: 200 }}
          className="text-3xl"
        >
          {isUp ? '⬆️' : '⬇️'}
        </motion.span>
        <div className="flex flex-col">
          <span className="text-xs font-medium opacity-90">
            {isUp ? '난이도 UP!' : '난이도 DOWN'}
          </span>
          <div className="flex items-center gap-2 text-lg font-bold">
            <span>Lv.{change.from}</span>
            <motion.span
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: 0.2, duration: 0.3 }}
            >
              →
            </motion.span>
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.3, 1] }}
              transition={{ delay: 0.3, duration: 0.4 }}
              className="font-extrabold"
            >
              Lv.{change.to}
            </motion.span>
          </div>
        </div>
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', delay: 0.4, damping: 8, stiffness: 200 }}
          className="ml-1 rounded-full bg-white/25 px-3 py-1 text-xs font-bold"
        >
          {getDifficultyLabel(change.to)}
        </motion.div>
      </div>
    </motion.div>
  )
}

export function TestPlayPage() {
  const { attemptId } = useParams<{ attemptId: string }>()
  const navigate = useNavigate()
  const { user, setUser } = useAuthStore()

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

  // 적응형 전용 상태
  const [currentDifficulty, setCurrentDifficulty] = useState<number>(6)
  const [questionsAnswered, setQuestionsAnswered] = useState(0)
  const [isFetchingNext, setIsFetchingNext] = useState(false)
  const [difficultyChange, setDifficultyChange] = useState<DifficultyChange | null>(null)
  const difficultyChangeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // 타이머 상태
  const [timerKey, setTimerKey] = useState(0)
  const [isTimeUp, setIsTimeUp] = useState(false)

  const isAdaptive = attemptDetail?.attempt.is_adaptive ?? false
  const totalQuestions = attemptDetail?.attempt.total_count ?? 0
  const category = attemptDetail?.attempt.category
  const timeLimit = category ? (TIME_LIMITS[category] ?? DEFAULT_TIME_LIMIT) : DEFAULT_TIME_LIMIT

  // 클린업
  useEffect(() => {
    return () => {
      if (difficultyChangeTimer.current) clearTimeout(difficultyChangeTimer.current)
    }
  }, [])

  useEffect(() => {
    if (attemptId) {
      fetchAttemptDetail()
    }
  }, [attemptId])

  const fetchAttemptDetail = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<{ success: boolean; data: AttemptDetail }>(
        `/api/v1/tests/attempts/${attemptId}`
      )
      const data = response.data.data
      setAttemptDetail(data)

      if (data.attempt.is_adaptive && data.attempt.current_difficulty) {
        setCurrentDifficulty(data.attempt.current_difficulty)
      }
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

  const currentQuestion: Question | undefined = attemptDetail?.test.questions[currentIndex]

  /** 답안 제출 (시간초과 시 빈 답 전송) */
  const submitAnswer = useCallback(async (answer: string) => {
    if (!attemptId || !currentQuestion) return

    const timeSpent = Math.floor((Date.now() - startTime) / 1000)

    try {
      setIsSubmitting(true)
      const response = await api.post<{ success: boolean; data: SubmitAnswerResponse }>(
        `/api/v1/tests/attempts/${attemptId}/submit`,
        {
          question_id: currentQuestion.id,
          selected_answer: answer,
          time_spent_seconds: timeSpent,
        }
      )

      const result = response.data.data
      setFeedbackData(result)
      setScore(result.current_score)
      setCombo(result.combo_count)
      setShowFeedback(true)

      if (isAdaptive) {
        setQuestionsAnswered((prev) => prev + 1)
        if (result.next_difficulty != null && result.next_difficulty !== currentDifficulty) {
          const direction = result.next_difficulty > currentDifficulty ? 'up' : 'down'
          setDifficultyChange({ from: currentDifficulty, to: result.next_difficulty, direction })

          if (difficultyChangeTimer.current) clearTimeout(difficultyChangeTimer.current)
          difficultyChangeTimer.current = setTimeout(() => setDifficultyChange(null), 2500)

          setCurrentDifficulty(result.next_difficulty)
        }
      }
    } catch {
      setError('답안 제출에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }, [attemptId, currentQuestion, startTime, isAdaptive, currentDifficulty])

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer) return
    await submitAnswer(selectedAnswer)
  }

  /** 시간 초과 처리 */
  const handleTimeUp = useCallback(() => {
    if (showFeedback || isSubmitting) return
    setIsTimeUp(true)
    submitAnswer(selectedAnswer ?? '')
  }, [showFeedback, isSubmitting, selectedAnswer, submitAnswer])

  const completeTest = useCallback(async () => {
    if (!attemptId) return

    try {
      const response = await api.post<{ success: boolean; data: CompleteTestResult }>(
        `/api/v1/tests/attempts/${attemptId}/complete`
      )
      const completeData = response.data.data

      // 헤더의 사용자 정보 동기화
      if (user) {
        setUser({
          ...user,
          level: completeData.new_level ?? user.level,
          total_xp: completeData.total_xp ?? user.total_xp,
          current_streak: completeData.current_streak ?? user.current_streak,
        })
      }

      navigate(`/test/result/${attemptId}`, {
        state: {
          level_up: completeData.level_up,
          level_down: completeData.level_down,
          new_level: completeData.new_level,
          xp_earned: completeData.xp_earned,
          level_down_defense: completeData.level_down_defense,
          level_down_action: completeData.level_down_action,
          mastery_achieved: completeData.mastery_achieved,
        },
      })
    } catch {
      setError('테스트 완료에 실패했습니다.')
    }
  }, [attemptId, navigate, user, setUser])

  const handleNextQuestion = useCallback(async () => {
    if (!attemptDetail || !attemptId) return

    if (isAdaptive) {
      if (questionsAnswered >= totalQuestions) {
        completeTest()
        return
      }

      try {
        setIsFetchingNext(true)
        const response = await api.post<{ success: boolean; data: NextQuestionResponse }>(
          `/api/v1/tests/attempts/${attemptId}/next`
        )
        const nextData = response.data.data

        if (nextData.is_complete || !nextData.question) {
          completeTest()
          return
        }

        setCurrentDifficulty(nextData.current_difficulty)

        setAttemptDetail((prev) => {
          if (!prev) return prev
          return {
            ...prev,
            test: {
              ...prev.test,
              questions: [...prev.test.questions, nextData.question as Question],
            },
          }
        })
        setCurrentIndex((prev) => prev + 1)
        setSelectedAnswer(null)
        setFeedbackData(null)
        setShowFeedback(false)
        setIsTimeUp(false)
        setStartTime(Date.now())
        setTimerKey((prev) => prev + 1)
      } catch {
        setError('다음 문제를 불러오는데 실패했습니다.')
      } finally {
        setIsFetchingNext(false)
      }
    } else {
      const isLast = currentIndex >= attemptDetail.test.questions.length - 1
      if (isLast) {
        completeTest()
      } else {
        setCurrentIndex((prev) => prev + 1)
        setSelectedAnswer(null)
        setFeedbackData(null)
        setShowFeedback(false)
        setIsTimeUp(false)
        setStartTime(Date.now())
        setTimerKey((prev) => prev + 1)
      }
    }
  }, [attemptDetail, attemptId, isAdaptive, currentIndex, questionsAnswered, totalQuestions, completeTest])

  // 진행률 계산
  const progressCurrent = isAdaptive ? questionsAnswered + 1 : currentIndex + 1
  const progressTotal = isAdaptive ? totalQuestions : (attemptDetail?.test.questions.length ?? 0)
  const isLastQuestion = isAdaptive
    ? questionsAnswered + 1 >= totalQuestions
    : currentIndex >= (attemptDetail?.test.questions.length ?? 0) - 1

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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="sticky top-0 z-10 bg-white shadow-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <h1 className="text-lg font-semibold text-gray-900">
                {attemptDetail.test.title}
              </h1>
              {isAdaptive && (
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${getDifficultyColor(currentDifficulty)}`}
                >
                  Lv.{currentDifficulty} {getDifficultyLabel(currentDifficulty)}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3">
              {/* 카운트다운 타이머 */}
              {category && !isFetchingNext && (
                <CountdownTimer
                  key={timerKey}
                  totalSeconds={timeLimit}
                  isRunning={!showFeedback && !isSubmitting}
                  onTimeUp={handleTimeUp}
                />
              )}
              <ComboDisplay combo={combo} />
              <div className="text-sm font-medium text-gray-600">
                점수: <span className="text-primary-500">{score}</span>
              </div>
            </div>
          </div>
          <ProgressBar current={progressCurrent} total={progressTotal} />
        </div>
      </header>

      {/* 문제 */}
      <main className="container mx-auto px-4 py-6">
        {isFetchingNext ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
              <p className="text-gray-500">다음 문제 준비 중...</p>
            </div>
          </div>
        ) : (
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
                  questionNumber={progressCurrent}
                  selectedAnswer={selectedAnswer}
                  onSelectAnswer={handleSelectAnswer}
                  disabled={showFeedback}
                />
              )}
            </motion.div>
          </AnimatePresence>
        )}

        {/* 제출 버튼 */}
        {!showFeedback && !isFetchingNext && (
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
        timeBonus={feedbackData?.time_bonus ?? 0}
        comboCount={feedbackData?.combo_count ?? 0}
        isLastQuestion={isLastQuestion}
        isTimeUp={isTimeUp}
        nextDifficulty={isAdaptive && difficultyChange ? difficultyChange.to : undefined}
        currentDifficulty={isAdaptive && difficultyChange ? difficultyChange.from : undefined}
        onNext={handleNextQuestion}
      />

      {/* 난이도 변경 토스트 */}
      <AnimatePresence>
        {difficultyChange && <DifficultyChangeToast change={difficultyChange} />}
      </AnimatePresence>
    </div>
  )
}
