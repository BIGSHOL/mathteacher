// 레벨업 모달 컴포넌트

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import confetti from 'canvas-confetti'

interface LevelUpModalProps {
  isOpen: boolean
  newLevel: number
  onClose: () => void
}

export function LevelUpModal({ isOpen, newLevel, onClose }: LevelUpModalProps) {
  useEffect(() => {
    if (isOpen) {
      // 골드 폭죽 효과
      const duration = 2000
      const end = Date.now() + duration

      const frame = () => {
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: ['#FFD700', '#FFA500', '#FF8C00'],
        })
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: ['#FFD700', '#FFA500', '#FF8C00'],
        })

        if (Date.now() < end) {
          requestAnimationFrame(frame)
        }
      }
      frame()
    }
  }, [isOpen])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 배경 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-50 bg-black/70"
          />

          {/* 모달 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.5, y: 100 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.5, y: 100 }}
            transition={{ type: 'spring', damping: 15 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
          >
            <div className="w-full max-w-sm overflow-hidden rounded-3xl bg-gradient-to-b from-purple-600 to-purple-800 p-8 text-center text-white shadow-2xl">
              {/* 별 장식 */}
              <motion.div
                initial={{ rotate: 0 }}
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 opacity-20"
              >
                {[...Array(8)].map((_, i) => (
                  <div
                    key={i}
                    className="absolute text-2xl"
                    style={{
                      top: `${Math.random() * 100}%`,
                      left: `${Math.random() * 100}%`,
                    }}
                  >
                    ⭐
                  </div>
                ))}
              </motion.div>

              {/* 콘텐츠 */}
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring' }}
              >
                <div className="mb-4 text-6xl">🎊</div>
                <h2 className="mb-2 text-2xl font-bold">레벨 업!</h2>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: [0, 1.2, 1] }}
                  transition={{ delay: 0.4, duration: 0.5 }}
                  className="mb-4 text-7xl font-black"
                >
                  Lv.{newLevel}
                </motion.div>
                <p className="mb-6 text-purple-200">축하합니다! 새로운 레벨에 도달했어요!</p>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={onClose}
                  className="rounded-full bg-white px-8 py-3 font-bold text-purple-600 shadow-lg"
                >
                  계속하기
                </motion.button>
              </motion.div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
