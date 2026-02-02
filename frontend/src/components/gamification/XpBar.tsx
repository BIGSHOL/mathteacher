// XP 바 컴포넌트

import { motion } from 'framer-motion'

// 레벨별 필요 XP (백엔드와 동일)
const LEVEL_XP_REQUIREMENTS: Record<number, number> = {
  1: 0,
  2: 100,
  3: 250,
  4: 450,
  5: 700,
  6: 1000,
  7: 1400,
  8: 1900,
  9: 2500,
  10: 3200,
}

interface XpBarProps {
  level: number
  totalXp: number
  showLabel?: boolean
}

export function XpBar({ level, totalXp, showLabel = true }: XpBarProps) {
  const currentLevelXp = LEVEL_XP_REQUIREMENTS[level] || 0
  const nextLevelXp = LEVEL_XP_REQUIREMENTS[level + 1] || currentLevelXp + 500
  const xpInCurrentLevel = totalXp - currentLevelXp
  const xpNeededForNextLevel = nextLevelXp - currentLevelXp
  const progress = Math.min((xpInCurrentLevel / xpNeededForNextLevel) * 100, 100)

  return (
    <div className="w-full">
      {showLabel && (
        <div className="mb-1 flex items-center justify-between text-sm">
          <span className="font-medium text-gray-700">Lv.{level}</span>
          <span className="text-gray-500">
            {xpInCurrentLevel} / {xpNeededForNextLevel} XP
          </span>
        </div>
      )}
      <div className="h-3 overflow-hidden rounded-full bg-gray-200">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="h-full rounded-full bg-gradient-to-r from-levelup to-purple-600"
        />
      </div>
    </div>
  )
}

// 컴팩트 버전
export function XpBadge({ level, totalXp }: { level: number; totalXp: number }) {
  return (
    <div className="inline-flex items-center gap-2 rounded-full bg-purple-100 px-3 py-1">
      <span className="font-bold text-purple-700">Lv.{level}</span>
      <span className="text-sm text-purple-500">{totalXp} XP</span>
    </div>
  )
}
