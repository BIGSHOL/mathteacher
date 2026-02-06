// 내 정보 페이지

import { motion } from 'framer-motion'
import { useAuthStore } from '../../store/authStore'
import type { Grade } from '../../types'

const GRADE_LABELS: Record<Grade, string> = {
  elementary_1: '초등 1학년',
  elementary_2: '초등 2학년',
  elementary_3: '초등 3학년',
  elementary_4: '초등 4학년',
  elementary_5: '초등 5학년',
  elementary_6: '초등 6학년',
  middle_1: '중등 1학년',
  middle_2: '중등 2학년',
  middle_3: '중등 3학년',
  high_1: '고등 1학년',
}

export function ProfilePage() {
  const { user, logout } = useAuthStore()

  if (!user) return null

  const gradeLabel = user.grade ? GRADE_LABELS[user.grade] : null

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  return (
    <div className="mx-auto max-w-lg px-4 pb-24 pt-6">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">내 정보</h1>

      {/* 프로필 카드 */}
      <div className="card mb-4 p-6">
        <div className="mb-4 flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100 text-3xl">
            👤
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">{user.name}</h2>
            <p className="text-sm text-gray-500">{user.login_id}</p>
          </div>
        </div>

        <div className="space-y-3 border-t pt-4">
          {gradeLabel && (
            <div className="flex justify-between">
              <span className="text-sm text-gray-500">학년</span>
              <span className="text-sm font-medium text-gray-900">{gradeLabel}</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">레벨</span>
            <span className="text-sm font-medium text-gray-900">Lv.{user.level}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">총 경험치</span>
            <span className="text-sm font-medium text-gray-900">{user.total_xp.toLocaleString()} XP</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">연속 출석</span>
            <span className="text-sm font-medium text-gray-900">{user.current_streak}일</span>
          </div>
        </div>
      </div>

      {/* 로그아웃 */}
      <motion.button
        whileTap={{ scale: 0.98 }}
        onClick={handleLogout}
        className="w-full rounded-xl border border-red-200 bg-white py-3 text-sm font-medium text-red-500 hover:bg-red-50"
      >
        로그아웃
      </motion.button>
    </div>
  )
}
