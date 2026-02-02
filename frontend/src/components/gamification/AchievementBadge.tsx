// 업적 배지 컴포넌트

import { motion } from 'framer-motion'

interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  earned: boolean
  earnedAt?: string
}

interface AchievementBadgeProps {
  achievement: Achievement
  size?: 'sm' | 'md' | 'lg'
}

export function AchievementBadge({ achievement, size = 'md' }: AchievementBadgeProps) {
  const sizeClasses = {
    sm: 'w-12 h-12 text-xl',
    md: 'w-16 h-16 text-2xl',
    lg: 'w-20 h-20 text-3xl',
  }

  return (
    <motion.div
      whileHover={{ scale: 1.1 }}
      className="text-center"
    >
      <div
        className={`mx-auto mb-2 flex items-center justify-center rounded-full ${sizeClasses[size]} ${
          achievement.earned
            ? 'bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg'
            : 'bg-gray-200'
        }`}
      >
        <span className={achievement.earned ? '' : 'grayscale opacity-50'}>
          {achievement.icon}
        </span>
      </div>
      <div className={`text-xs font-medium ${achievement.earned ? 'text-gray-900' : 'text-gray-400'}`}>
        {achievement.name}
      </div>
    </motion.div>
  )
}

// 업적 목록
export function AchievementList({ achievements }: { achievements: Achievement[] }) {
  return (
    <div className="grid grid-cols-4 gap-4 sm:grid-cols-6">
      {achievements.map((achievement) => (
        <AchievementBadge key={achievement.id} achievement={achievement} size="sm" />
      ))}
    </div>
  )
}

// 업적 획득 알림
interface AchievementUnlockProps {
  isOpen: boolean
  achievement: Achievement
  onClose: () => void
}

export function AchievementUnlock({ isOpen, achievement, onClose }: AchievementUnlockProps) {
  if (!isOpen) return null

  return (
    <motion.div
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: -100, opacity: 0 }}
      className="fixed left-1/2 top-4 z-50 -translate-x-1/2"
    >
      <div className="flex items-center gap-4 rounded-2xl bg-gradient-to-r from-yellow-400 to-orange-500 px-6 py-4 text-white shadow-2xl">
        <div className="text-4xl">{achievement.icon}</div>
        <div>
          <div className="text-sm font-medium opacity-90">업적 달성!</div>
          <div className="text-lg font-bold">{achievement.name}</div>
        </div>
        <button onClick={onClose} className="ml-4 opacity-70 hover:opacity-100">
          ✕
        </button>
      </div>
    </motion.div>
  )
}

// 기본 업적 목록
export const DEFAULT_ACHIEVEMENTS: Achievement[] = [
  { id: 'first_test', name: '첫 테스트', description: '첫 번째 테스트 완료', icon: '🎯', earned: false },
  { id: 'streak_3', name: '3일 연속', description: '3일 연속 학습', icon: '⚡', earned: false },
  { id: 'streak_7', name: '7일 연속', description: '7일 연속 학습', icon: '🔥', earned: false },
  { id: 'streak_30', name: '30일 연속', description: '30일 연속 학습', icon: '👑', earned: false },
  { id: 'combo_5', name: '5콤보', description: '5연속 정답', icon: '💫', earned: false },
  { id: 'combo_10', name: '10콤보', description: '10연속 정답', icon: '🌟', earned: false },
  { id: 'perfect', name: '퍼펙트', description: '테스트 만점', icon: '💯', earned: false },
  { id: 'level_5', name: '레벨 5', description: '레벨 5 달성', icon: '🏅', earned: false },
  { id: 'level_10', name: '레벨 10', description: '레벨 10 달성', icon: '🏆', earned: false },
  { id: 'tests_10', name: '10회 테스트', description: '테스트 10회 완료', icon: '📚', earned: false },
  { id: 'tests_50', name: '50회 테스트', description: '테스트 50회 완료', icon: '📖', earned: false },
  { id: 'tests_100', name: '100회 테스트', description: '테스트 100회 완료', icon: '🎓', earned: false },
]
