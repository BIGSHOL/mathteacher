import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useAuthStore } from '../store/authStore'
import { Link } from 'react-router-dom'
import api from '../lib/api'

interface QuotaProgress {
  daily_quota: number
  correct_today: number
  quota_remaining: number
  accumulated_quota: number
  quota_met: boolean
  carry_over: boolean
}

interface StudentStats {
  today_solved: number
  current_streak: number
  max_streak: number
  level: number
  total_xp: number
  quota: QuotaProgress | null
}

export function DashboardPage() {
  const user = useAuthStore((state) => state.user)
  const [stats, setStats] = useState<StudentStats | null>(null)

  const [statsError, setStatsError] = useState(false)

  useEffect(() => {
    api.get<{ success: boolean; data: StudentStats }>('/api/v1/stats/me', { timeout: 10000 })
      .then((res) => setStats(res.data.data))
      .catch(() => setStatsError(true))
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

        {/* 할당량 프로그레스 */}
        {stats?.quota && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-6"
          >
            <QuotaCard quota={stats.quota} />
          </motion.div>
        )}

        {/* 통계 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
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

function QuotaCard({ quota }: { quota: QuotaProgress }) {
  const target = quota.carry_over ? quota.accumulated_quota : quota.daily_quota
  const progress = Math.min(100, Math.round((quota.correct_today / target) * 100))

  return (
    <div className={`card p-5 border-2 ${quota.quota_met ? 'border-green-300 bg-green-50' : 'border-blue-200 bg-white'}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-xl">{quota.quota_met ? '\u2705' : '\uD83C\uDFAF'}</span>
          <span className="font-semibold text-gray-900">
            {quota.quota_met ? '\uC624\uB298 \uBAA9\uD45C \uB2EC\uC131!' : '\uC624\uB298 \uBAA9\uD45C'}
          </span>
        </div>
        <span className="text-sm text-gray-500">
          {quota.carry_over && quota.accumulated_quota > quota.daily_quota
            ? `(\uB204\uC801 ${quota.accumulated_quota}\uBB38\uC81C)`
            : `\uB9E4\uC77C ${quota.daily_quota}\uBB38\uC81C`}
        </span>
      </div>

      <div className="flex items-end justify-between mb-2">
        <span className="text-3xl font-bold text-gray-900">
          {quota.correct_today}<span className="text-lg text-gray-400">/{target}</span>
        </span>
        <span className="text-sm font-medium text-gray-500">{progress}%</span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-3">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className={`h-3 rounded-full ${quota.quota_met ? 'bg-green-500' : 'bg-blue-500'}`}
        />
      </div>

      {!quota.quota_met && quota.quota_remaining > 0 && (
        <p className="text-sm text-gray-500 mt-2">
          \uC815\uB2F5 <span className="font-semibold text-blue-600">{quota.quota_remaining}\uBB38\uC81C</span> \uB0A8\uC558\uC5B4\uC694
        </p>
      )}
    </div>
  )
}
