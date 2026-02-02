// 콤보 표시 컴포넌트

import { motion, AnimatePresence } from 'framer-motion'

interface ComboDisplayProps {
  combo: number
}

export function ComboDisplay({ combo }: ComboDisplayProps) {
  if (combo < 2) return null

  const getComboColor = () => {
    if (combo >= 10) return 'from-purple-500 to-pink-500'
    if (combo >= 5) return 'from-orange-500 to-red-500'
    return 'from-yellow-500 to-orange-500'
  }

  const getComboEmoji = () => {
    if (combo >= 10) return '🔥🔥🔥'
    if (combo >= 5) return '🔥🔥'
    return '🔥'
  }

  const getComboGlow = () => {
    if (combo >= 10) return 'combo-glow-10'
    if (combo >= 5) return 'combo-glow-5'
    return ''
  }

  const getComboText = () => {
    if (combo >= 10) return '무적모드!'
    if (combo >= 5) return '대단해요!'
    return `${combo}콤보`
  }

  return (
    <AnimatePresence>
      <motion.div
        key={combo}
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{
          scale: [1, combo >= 5 ? 1.1 : 1, 1],
          opacity: 1
        }}
        exit={{ scale: 1.5, opacity: 0 }}
        transition={{
          scale: { duration: 0.3, times: [0, 0.5, 1] }
        }}
        className={`flex items-center gap-1 rounded-full bg-gradient-to-r ${getComboColor()} px-3 py-1 text-sm font-bold text-white shadow-lg ${getComboGlow()}`}
      >
        <span>{getComboEmoji()}</span>
        <span className="font-math">{getComboText()}</span>
        {combo >= 10 && (
          <motion.span
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ repeat: Infinity, duration: 0.5 }}
          >
            ⚡
          </motion.span>
        )}
      </motion.div>
    </AnimatePresence>
  )
}

// 대형 콤보 표시 (레벨업 등 특별한 상황)
export function ComboDisplayLarge({ combo }: ComboDisplayProps) {
  const getSpecialMessage = () => {
    if (combo >= 10) return '무적모드!'
    if (combo >= 5) return '대단해요!'
    return '콤보!'
  }

  const getGlowClass = () => {
    if (combo >= 10) return 'combo-glow-10'
    if (combo >= 5) return 'combo-glow-5'
    return ''
  }

  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ type: 'spring', damping: 10 }}
      className={`text-center rounded-2xl p-4 ${getGlowClass()}`}
    >
      <motion.div
        className="mb-2 text-5xl"
        animate={combo >= 5 ? { scale: [1, 1.2, 1] } : {}}
        transition={{ repeat: Infinity, duration: 1 }}
      >
        {combo >= 10 ? '🔥⚡🔥' : combo >= 5 ? '🔥🔥' : '🔥'}
      </motion.div>
      <div className="text-4xl font-black text-combo font-math">{combo}</div>
      <div className="text-lg font-bold text-gray-600">{getSpecialMessage()}</div>
    </motion.div>
  )
}

// 화면 테두리 글로우 오버레이 (콤보 5+ 일 때 사용)
export function ComboGlowOverlay({ combo }: ComboDisplayProps) {
  if (combo < 5) return null

  const glowColor = combo >= 10
    ? 'rgba(139, 92, 246, 0.3)' // 퍼플
    : 'rgba(249, 115, 22, 0.3)' // 오렌지

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="pointer-events-none fixed inset-0 z-30"
      style={{
        boxShadow: `inset 0 0 100px ${glowColor}, inset 0 0 200px ${glowColor}`
      }}
    />
  )
}
