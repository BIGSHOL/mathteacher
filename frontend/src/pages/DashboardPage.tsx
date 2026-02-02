import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useAuthStore } from '../store/authStore'
import { Link } from 'react-router-dom'
import api from '../lib/api'

interface StudentStats {
  today_solved: number
  current_streak: number
  max_streak: number
  level: number
  total_xp: number
}

export function DashboardPage() {
  const user = useAuthStore((state) => state.user)
  const [stats, setStats] = useState<StudentStats | null>(null)

  useEffect(() => {
    api.get<{ success: boolean; data: StudentStats }>('/api/v1/stats/me')
      .then((res) => setStats(res.data.data))
      .catch(() => {})
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-2xl font-bold text-gray-900">대시보드</h1>
          <p className="text-gray-600">{user?.name || '학생'}님, 오늘도 열심히 공부해요!</p>
        </motion.div>

        {/* 통계 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
        >
          <StatCard label="오늘 학습" value={`${stats?.today_solved ?? 0}문제`} icon="📝" />
          <StatCard label="연속 정답" value={`${stats?.current_streak ?? user?.current_streak ?? 0}회`} icon="🔥" color="streak" />
          <StatCard label="현재 레벨" value={`Lv.${stats?.level ?? user?.level ?? 1}`} icon="⭐" color="level" />
          <StatCard label="최고 콤보" value={`${stats?.max_streak ?? 0}`} icon="💫" color="combo" />
        </motion.div>

        {/* 학습 메뉴 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">학습하기</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <LearningCard
              title="개념 테스트"
              description="수학 개념을 테스트하고 이해도를 확인해보세요"
              icon="📚"
              href="/practice?category=concept"
            />
            <LearningCard
              title="연산 연습"
              description="빠른 연산 능력을 키워보세요"
              icon="🧮"
              href="/practice?category=computation"
            />
            <LearningCard
              title="복습하기"
              description="틀렸던 문제를 다시 풀어보세요"
              icon="🔄"
              href="/review"
            />
          </div>
        </motion.div>
      </div>
    </div>
  )
}

interface StatCardProps {
  label: string
  value: string
  icon: string
  color?: 'combo' | 'streak' | 'level'
}

function StatCard({ label, value, icon, color }: StatCardProps) {
  const colorClasses = {
    combo: 'bg-amber-50 border-amber-200',
    streak: 'bg-red-50 border-red-200',
    level: 'bg-purple-50 border-purple-200',
  }

  return (
    <div className={`card p-4 border ${color ? colorClasses[color] : 'border-gray-100'}`}>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}

interface LearningCardProps {
  title: string
  description: string
  icon: string
  href: string
}

function LearningCard({ title, description, icon, href }: LearningCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Link
        to={href}
        className="card p-6 block cursor-pointer hover:border-primary-200"
      >
        <div className="text-3xl mb-3">{icon}</div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{description}</p>
      </Link>
    </motion.div>
  )
}
