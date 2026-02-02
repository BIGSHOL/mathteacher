// 피드백 모달 컴포넌트

import { motion, AnimatePresence } from 'framer-motion'

interface FeedbackModalProps {
  isOpen: boolean
  isCorrect: boolean
  correctAnswer: string
  explanation: string
  pointsEarned: number
  comboCount: number
  isLastQuestion: boolean
  onNext: () => void
}

export function FeedbackModal({
  isOpen,
  isCorrect,
  correctAnswer,
  explanation,
  pointsEarned,
  comboCount,
  isLastQuestion,
  onNext,
}: FeedbackModalProps) {
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
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 50 }}
            className="fixed inset-x-4 bottom-0 z-50 mx-auto max-w-lg overflow-hidden rounded-t-3xl bg-white shadow-2xl md:bottom-auto md:top-1/2 md:-translate-y-1/2 md:rounded-3xl"
          >
            {/* 헤더 */}
            <div
              className={`p-6 text-center ${
                isCorrect ? 'bg-correct text-white' : 'bg-incorrect text-white'
              }`}
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', duration: 0.5 }}
                className="mb-2 text-6xl"
              >
                {isCorrect ? '🎉' : '😢'}
              </motion.div>
              <h2 className="text-2xl font-bold">{isCorrect ? '정답!' : '아쉬워요'}</h2>

              {/* 콤보 & 점수 */}
              {isCorrect && (
                <div className="mt-4 flex justify-center gap-4">
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
                </div>
              )}
            </div>

            {/* 내용 */}
            <div className="p-6">
              {/* 정답 표시 (오답일 때) */}
              {!isCorrect && (
                <div className="mb-4 rounded-xl bg-gray-100 p-4">
                  <div className="text-sm text-gray-500">정답</div>
                  <div className="text-lg font-bold text-gray-900">{correctAnswer}</div>
                </div>
              )}

              {/* 해설 */}
              {explanation && (
                <div className="mb-6">
                  <div className="mb-2 text-sm font-medium text-gray-500">해설</div>
                  <p className="text-gray-700">{explanation}</p>
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
    <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
      <div className="mb-4 text-center text-6xl">😢</div>
      <h3 className="mb-4 text-center text-2xl font-bold text-incorrect">아쉬워요</h3>
      <div className="rounded-xl bg-gray-100 p-4">
        <div className="mb-2 text-sm text-gray-500">정답: {correctAnswer}</div>
        {explanation && <p className="text-gray-700">{explanation}</p>}
      </div>
    </motion.div>
  )
}
