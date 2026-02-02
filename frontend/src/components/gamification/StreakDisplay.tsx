// 스트릭 표시 컴포넌트

import { motion } from 'framer-motion'

interface StreakDisplayProps {
  streak: number
  showLabel?: boolean
}

export function StreakDisplay({ streak, showLabel = true }: StreakDisplayProps) {
  const getStreakInfo = () => {
    if (streak >= 30) return { emoji: '👑', color: 'from-yellow-400 to-orange-500', label: '전설' }
    if (streak >= 14) return { emoji: '💎', color: 'from-blue-400 to-purple-500', label: '다이아' }
    if (streak >= 7) return { emoji: '🔥', color: 'from-orange-400 to-red-500', label: '불꽃' }
    if (streak >= 3) return { emoji: '⚡', color: 'from-yellow-400 to-yellow-600', label: '번개' }
    return { emoji: '✨', color: 'from-gray-400 to-gray-500', label: '시작' }
  }

  const { emoji, color, label } = getStreakInfo()

  if (streak === 0) return null

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`inline-flex items-center gap-2 rounded-full bg-gradient-to-r ${color} px-4 py-2 text-white shadow-lg`}
    >
      <span className="text-xl">{emoji}</span>
      <div className="text-center">
        <div className="text-lg font-bold">{streak}일</div>
        {showLabel && <div className="text-xs opacity-80">{label}</div>}
      </div>
    </motion.div>
  )
}

// 스트릭 배지 (작은 버전)
export function StreakBadge({ streak }: { streak: number }) {
  if (streak < 3) return null

  const getBadge = () => {
    if (streak >= 30) return { icon: '👑', bg: 'bg-yellow-100', text: 'text-yellow-700' }
    if (streak >= 14) return { icon: '💎', bg: 'bg-blue-100', text: 'text-blue-700' }
    if (streak >= 7) return { icon: '🔥', bg: 'bg-orange-100', text: 'text-orange-700' }
    return { icon: '⚡', bg: 'bg-yellow-100', text: 'text-yellow-700' }
  }

  const { icon, bg, text } = getBadge()

  return (
    <span className={`inline-flex items-center gap-1 rounded-full ${bg} px-2 py-1 text-xs font-medium ${text}`}>
      {icon} {streak}일
    </span>
  )
}

// 스트릭 캘린더 (주간 표시)
export function StreakCalendar({ activeDays }: { activeDays: boolean[] }) {
  const dayLabels = ['일', '월', '화', '수', '목', '금', '토']

  return (
    <div className="flex justify-center gap-1">
      {dayLabels.map((day, index) => (
        <div key={day} className="text-center">
          <div className="mb-1 text-xs text-gray-500">{day}</div>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: index * 0.05 }}
            className={`h-8 w-8 rounded-lg ${
              activeDays[index]
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-400'
            } flex items-center justify-center text-sm font-medium`}
          >
            {activeDays[index] ? '✓' : '·'}
          </motion.div>
        </div>
      ))}
    </div>
  )
}
