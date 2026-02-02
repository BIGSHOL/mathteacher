// 학생 내 통계 페이지

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import { XpBar } from '../../components/gamification/XpBar'
import { StreakDisplay } from '../../components/gamification/StreakDisplay'
import type { StudentStats } from '../../types'

export function MyStatsPage() {
  const [stats, setStats] = useState<StudentStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setIsLoading(true)
      setError('')

      const response = await api.get<{ success: boolean; data: StudentStats }>(
        '/api/v1/stats/me'
      )
      setStats(response.data.data)
    } catch {
      setError('통계를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">통계를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error}</p>
          <button onClick={fetchStats} className="btn-primary px-4 py-2">
            다시 시도
          </button>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 text-4xl">📊</div>
          <p className="text-gray-600">아직 학습 기록이 없습니다.</p>
          <p className="text-sm text-gray-500">테스트를 풀면 통계가 표시됩니다.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-2xl font-bold text-gray-900">내 학습 통계</h1>
          <p className="text-gray-600">나의 학습 현황을 확인해보세요</p>
        </motion.div>

        {/* 레벨 & 스트릭 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 grid gap-4 md:grid-cols-2"
        >
          {/* 레벨 카드 */}
          <div className="rounded-2xl bg-gradient-to-br from-purple-500 to-purple-700 p-6 text-white">
            <div className="mb-4 flex items-center justify-between">
              <span className="text-lg font-medium opacity-90">레벨</span>
              <span className="text-4xl font-black">Lv.{stats.level}</span>
            </div>
            <XpBar level={stats.level} totalXp={stats.total_xp} showLabel />
            <p className="mt-2 text-sm opacity-75">
              총 {stats.total_xp.toLocaleString()} XP
            </p>
          </div>

          {/* 스트릭 카드 */}
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <span className="text-lg font-medium text-gray-700">연속 학습</span>
              <StreakDisplay streak={stats.current_streak} />
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">최대 연속</span>
              <span className="font-medium text-gray-900">{stats.max_streak}일</span>
            </div>
          </div>
        </motion.div>

        {/* 학습 통계 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">학습 현황</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              icon="📝"
              label="완료 테스트"
              value={stats.total_tests}
              suffix="개"
            />
            <StatCard
              icon="✏️"
              label="풀이 문제"
              value={stats.total_questions}
              suffix="문제"
            />
            <StatCard
              icon="✅"
              label="정답 수"
              value={stats.correct_answers}
              suffix="개"
            />
            <StatCard
              icon="🎯"
              label="정답률"
              value={stats.accuracy_rate}
              suffix="%"
              highlight
            />
          </div>
        </motion.div>

        {/* 평균 풀이 시간 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8 rounded-2xl bg-white p-6 shadow-sm"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">평균 풀이 시간</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats.average_time_per_question}초
                <span className="ml-2 text-sm font-normal text-gray-500">/ 문제당</span>
              </p>
            </div>
            <div className="text-4xl">⏱️</div>
          </div>
        </motion.div>

        {/* 취약 개념 */}
        {stats.weak_concepts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mb-8"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              더 연습이 필요한 개념
            </h2>
            <div className="space-y-3">
              {stats.weak_concepts.map((concept) => (
                <ConceptBar
                  key={concept.concept_id}
                  name={concept.concept_name}
                  accuracy={concept.accuracy_rate}
                  color="red"
                />
              ))}
            </div>
          </motion.div>
        )}

        {/* 강점 개념 */}
        {stats.strong_concepts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">잘하는 개념</h2>
            <div className="space-y-3">
              {stats.strong_concepts.map((concept) => (
                <ConceptBar
                  key={concept.concept_id}
                  name={concept.concept_name}
                  accuracy={concept.accuracy_rate}
                  color="green"
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

// 통계 카드 컴포넌트
interface StatCardProps {
  icon: string
  label: string
  value: number
  suffix: string
  highlight?: boolean
}

function StatCard({ icon, label, value, suffix, highlight }: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <div className="mb-3 text-3xl">{icon}</div>
      <p className="mb-1 text-sm text-gray-600">{label}</p>
      <p
        className={`text-2xl font-bold ${
          highlight ? 'text-primary-600' : 'text-gray-900'
        }`}
      >
        {value}
        <span className="ml-1 text-sm font-normal text-gray-500">{suffix}</span>
      </p>
    </div>
  )
}

// 개념 막대 컴포넌트
interface ConceptBarProps {
  name: string
  accuracy: number
  color: 'red' | 'green'
}

function ConceptBar({ name, accuracy, color }: ConceptBarProps) {
  const bgColor = color === 'red' ? 'bg-red-100' : 'bg-green-100'
  const barColor = color === 'red' ? 'bg-red-500' : 'bg-green-500'
  const textColor = color === 'red' ? 'text-red-600' : 'text-green-600'

  return (
    <div className={`rounded-xl ${bgColor} p-4`}>
      <div className="mb-2 flex items-center justify-between">
        <span className="font-medium text-gray-900">{name}</span>
        <span className={`font-bold ${textColor}`}>{accuracy}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-white/50">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${accuracy}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className={`h-full rounded-full ${barColor}`}
        />
      </div>
    </div>
  )
}
