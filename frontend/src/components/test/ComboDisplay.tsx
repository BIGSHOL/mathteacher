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

  return (
    <AnimatePresence>
      <motion.div
        key={combo}
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 1.5, opacity: 0 }}
        className={`flex items-center gap-1 rounded-full bg-gradient-to-r ${getComboColor()} px-3 py-1 text-sm font-bold text-white shadow-lg`}
      >
        <span>{getComboEmoji()}</span>
        <span>{combo}콤보</span>
      </motion.div>
    </AnimatePresence>
  )
}

// 대형 콤보 표시 (레벨업 등 특별한 상황)
export function ComboDisplayLarge({ combo }: ComboDisplayProps) {
  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ type: 'spring', damping: 10 }}
      className="text-center"
    >
      <div className="mb-2 text-5xl">🔥</div>
      <div className="text-4xl font-black text-combo">{combo}</div>
      <div className="text-lg font-bold text-gray-600">콤보!</div>
    </motion.div>
  )
}
