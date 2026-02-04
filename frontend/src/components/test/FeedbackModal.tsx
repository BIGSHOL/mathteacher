// 피드백 모달 컴포넌트

import { useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const correctSound = new Audio('/sounds/correct.mp3')
const wrongSound = new Audio('/sounds/wrong.mp3')

interface FeedbackModalProps {
  isOpen: boolean
  isCorrect: boolean
  correctAnswer: string
  explanation: string
  pointsEarned: number
  timeBonus?: number
  comboCount: number
  isLastQuestion: boolean
  isTimeUp?: boolean
  /** 시간초과/오답 시 다음 난이도 (하락 경고 표시용) */
  nextDifficulty?: number
  /** 현재 난이도 (하락 경고 비교용) */
  currentDifficulty?: number
  /** 빈칸 채우기 부분 점수 정보 */
  correctCount?: number
  totalBlanks?: number
  /** AI 오류 유형 (오답 시) */
  errorType?: string
  /** AI 학습 제안 (오답 시) */
  suggestion?: string
  onNext: () => void
}

export function FeedbackModal({
  isOpen,
  isCorrect,
  correctAnswer,
  explanation,
  pointsEarned,
  timeBonus = 0,
  comboCount,
  isLastQuestion,
  isTimeUp = false,
  nextDifficulty,
  currentDifficulty,
  correctCount,
  totalBlanks,
  errorType,
  suggestion,
  onNext,
}: FeedbackModalProps) {
  const prevOpen = useRef(false)

  useEffect(() => {
    if (isOpen && !prevOpen.current) {
      const sound = isCorrect ? correctSound : wrongSound
      sound.currentTime = 0
      sound.play().catch(() => {})
    }
    prevOpen.current = isOpen
  }, [isOpen, isCorrect])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 배경 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/50"
          />

          {/* 모달 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 50 }}
            animate={{
              opacity: 1,
              scale: 1,
              y: 0,
              // 오답일 때 흔들림 효과
              x: isCorrect ? 0 : [0, -10, 10, -10, 10, -5, 5, 0]
            }}
            exit={{ opacity: 0, scale: 0.9, y: 50 }}
            transition={{
              type: 'spring',
              duration: 0.5,
              x: { duration: 0.5, ease: 'easeInOut' }
            }}
            className="fixed inset-x-4 bottom-0 z-50 mx-auto max-w-lg overflow-hidden rounded-t-3xl bg-white shadow-2xl md:bottom-auto md:top-1/2 md:-translate-y-1/2 md:rounded-3xl"
          >
            {/* 헤더 */}
            <div
              className={`p-6 text-center ${
                isTimeUp ? 'bg-gray-700 text-white' : isCorrect ? 'bg-correct text-white' : 'bg-incorrect text-white'
              }`}
            >
              <motion.div
                initial={{ scale: 0, rotate: isCorrect ? 0 : -10 }}
                animate={{
                  scale: 1,
                  rotate: isCorrect ? 0 : [0, -5, 5, -5, 5, 0]
                }}
                transition={{ type: 'spring', duration: 0.5 }}
                className="mb-2 text-6xl"
              >
                {isTimeUp ? '⏰' : isCorrect ? '🎉' : '😢'}
              </motion.div>
              <h2 className="text-2xl font-bold">
                {isTimeUp ? '시간 초과!' : isCorrect ? '정답!' : '아쉬워요'}
              </h2>

              {/* 콤보 & 점수 & 시간보너스 */}
              {isCorrect && (
                <div className="mt-4 flex flex-wrap justify-center gap-3">
                  {comboCount > 1 && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="rounded-full bg-white/20 px-4 py-1"
                    >
                      <span className="font-bold">{comboCount}</span> 콤보!
                    </motion.div>
                  )}
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.1 }}
                    className="rounded-full bg-white/20 px-4 py-1"
                  >
                    +<span className="font-bold">{pointsEarned}</span>점
                  </motion.div>
                  {timeBonus > 0 && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.2 }}
                      className="rounded-full bg-yellow-400/30 px-4 py-1"
                    >
                      +<span className="font-bold">{timeBonus}</span> 시간 보너스
                    </motion.div>
                  )}
                </div>
              )}
            </div>

            {/* 내용 */}
            <div className="p-6">
              {/* 시간초과/오답 시 난이도 하락 경고 */}
              {!isCorrect && nextDifficulty !== undefined && currentDifficulty !== undefined && nextDifficulty < currentDifficulty && (
                <motion.div
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mb-4 rounded-xl bg-red-50 border border-red-200 p-3 text-center"
                >
                  <span className="text-red-600 font-semibold text-sm">
                    📉 난이도 하락: Lv.{currentDifficulty} → Lv.{nextDifficulty}
                  </span>
                  {isTimeUp && (
                    <p className="text-xs text-red-500 mt-1">시간 안에 풀지 못하면 난이도가 내려갑니다!</p>
                  )}
                </motion.div>
              )}

              {/* 정답 표시 (오답일 때) */}
              {!isCorrect && (
                <div className="mb-4 rounded-xl bg-gray-100 p-4">
                  <div className="text-sm text-gray-500">정답</div>
                  <div className="text-lg font-bold text-gray-900">{correctAnswer}</div>
                </div>
              )}

              {/* 빈칸 채우기 부분 점수 */}
              {correctCount !== undefined && totalBlanks !== undefined && totalBlanks > 0 && (
                <div className="mb-4 rounded-xl bg-blue-50 border border-blue-200 p-4">
                  <div className="text-sm text-gray-600 mb-1">빈칸 정답 현황</div>
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold text-blue-600">{correctCount}</span>
                      <span className="text-gray-600"> / {totalBlanks}</span>
                      <span className="ml-2 text-sm text-gray-500">정답</span>
                    </div>
                    <div className="text-sm text-gray-600">
                      부분 점수: <span className="font-semibold text-blue-600">{pointsEarned}점</span>
                    </div>
                  </div>
                </div>
              )}

              {/* 해설 */}
              {explanation && (
                <div className="mb-6">
                  <div className="mb-2 text-sm font-medium text-gray-500">해설</div>
                  <p className="text-gray-700">{explanation}</p>
                </div>
              )}

              {/* AI 분석 (오답 시) */}
              {!isCorrect && (errorType || suggestion) && (
                <div className="mb-6 rounded-xl border border-blue-200 bg-blue-50 p-4">
                  {errorType && (
                    <div className="mb-2 flex items-center gap-2">
                      <span className="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-600">
                        {errorType}
                      </span>
                    </div>
                  )}
                  {suggestion && (
                    <p className="text-sm text-blue-700">{suggestion}</p>
                  )}
                </div>
              )}

              {/* 다음 버튼 */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onNext}
                className="btn-primary w-full py-4 text-lg"
              >
                {isLastQuestion ? '결과 보기' : '다음 문제'}
              </motion.button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

// 정답 피드백 컴포넌트 (별도 사용)
export function CorrectFeedback({ points, combo }: { points: number; combo: number }) {
  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      className="text-center"
    >
      <div className="mb-4 text-6xl">🎉</div>
      <h3 className="mb-2 text-2xl font-bold text-correct">정답!</h3>
      <div className="flex justify-center gap-4">
        <span className="badge-combo">+{points}점</span>
        {combo > 1 && <span className="badge-streak">{combo}콤보!</span>}
      </div>
    </motion.div>
  )
}

// 오답 피드백 컴포넌트 (별도 사용)
export function IncorrectFeedback({
  correctAnswer,
  explanation,
}: {
  correctAnswer: string
  explanation: string
}) {
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0, x: 0 }}
      animate={{
        scale: 1,
        opacity: 1,
        x: [0, -8, 8, -8, 8, -4, 4, 0] // 흔들림 효과
      }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-4 text-center text-6xl">😢</div>
      <h3 className="mb-4 text-center text-2xl font-bold text-incorrect">아쉬워요</h3>
      <div className="rounded-xl bg-red-50 border border-red-200 p-4">
        <div className="mb-2 flex items-center gap-2 text-sm text-gray-500">
          {/* 에러 아이콘 */}
          <svg className="h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          정답
        </div>
        <div className="text-lg font-bold text-gray-900 font-math">{correctAnswer}</div>
        {explanation && <p className="mt-2 text-gray-700">{explanation}</p>}
      </div>
    </motion.div>
  )
}
