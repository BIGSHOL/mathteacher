// 학생 내 통계 페이지

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import { XpBar } from '../../components/gamification/XpBar'
import { useAuthStore } from '../../store/authStore'
import type { StudentStats, TrackStats, Grade } from '../../types'

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

export function MyStatsPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<StudentStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const gradeLabel = user?.grade ? GRADE_LABELS[user.grade] : null

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

  const accuracyLabel =
    stats.accuracy_rate >= 80
      ? { text: '우수', badge: 'bg-white/20' }
      : stats.accuracy_rate >= 60
        ? { text: '보통', badge: 'bg-white/20' }
        : { text: '도전', badge: 'bg-white/20' }

  return (
    <div className="min-h-screen bg-gray-50 py-6 sm:py-8">
      <div className="container mx-auto max-w-6xl px-4 space-y-6">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-1">
            <span className="text-3xl">📊</span>
            <h1 className="text-3xl font-bold text-gray-900">내 학습 통계</h1>
            {gradeLabel && (
              <span className="rounded-full bg-primary-100 px-3 py-1 text-sm font-semibold text-primary-700">
                {gradeLabel}
              </span>
            )}
          </div>
          <p className="text-gray-500 ml-12">나의 학습 현황을 확인하고 성장해보세요</p>
        </motion.div>

        {/* 레벨 & 스트릭 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid gap-4 md:grid-cols-2"
        >
          {/* 레벨 카드 */}
          <div className="rounded-2xl bg-gradient-to-br from-purple-500 via-purple-600 to-purple-700 p-6 text-white shadow-lg">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <span className="text-sm font-medium opacity-75">현재 레벨</span>
                <p className="font-math text-5xl font-black mt-1">Lv.{stats.level}</p>
              </div>
              <div className="text-right">
                <span className="text-xs opacity-75">총 획득 XP</span>
                <p className="font-math text-2xl font-bold">{stats.total_xp.toLocaleString()}</p>
              </div>
            </div>
            <XpBar level={stats.level} totalXp={stats.total_xp} showLabel={false} />
          </div>

          {/* 스트릭 카드 */}
          <div className="rounded-2xl bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 p-6 text-white shadow-lg">
            <div className="mb-3 flex items-center justify-between">
              <span className="text-sm font-medium opacity-75">연속 학습 스트릭</span>
              <span className="text-3xl">🔥</span>
            </div>
            <div className="mb-4">
              <p className="font-math text-5xl font-black">{stats.current_streak}</p>
              <p className="text-sm opacity-90 mt-1">일 연속 학습 중!</p>
            </div>
            <div className="flex items-center justify-between border-t border-white/20 pt-3 text-sm">
              <span className="opacity-75">최대 기록</span>
              <span className="font-math text-lg font-bold">{stats.max_streak}일</span>
            </div>
          </div>
        </motion.div>

        {/* 학습 통계 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">학습 현황</h2>
          <div className="grid gap-4 grid-cols-2 lg:grid-cols-3">
            {/* 정답률 카드 - 강조 */}
            <div className="col-span-2 lg:col-span-1 lg:row-span-2 flex flex-col items-center justify-center rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 p-8 text-white shadow-lg text-center">
              <div className="text-5xl mb-3">🎯</div>
              <p className="text-sm font-medium opacity-75 mb-2">정답률</p>
              <p className="font-math text-6xl font-black mb-3">{stats.accuracy_rate}%</p>
              <span className={`inline-block px-4 py-1.5 ${accuracyLabel.badge} rounded-full text-sm font-medium`}>
                {accuracyLabel.text}
              </span>
            </div>

            <StatCard icon="📝" label="완료 테스트" value={stats.total_tests} suffix="개" />
            <StatCard icon="✏️" label="풀이 문제" value={stats.total_questions} suffix="문제" />
            <StatCard icon="✅" label="정답 수" value={stats.correct_answers} suffix="개" />
            <StatCard
              icon="⏱️"
              label="평균 풀이 시간"
              value={stats.average_time_per_question}
              suffix="초"
            />
          </div>
        </motion.div>

        {/* 트랙별 정답률 (연산 / 개념) */}
        {(stats.computation_stats || stats.concept_stats) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">트랙별 성적</h2>
            <div className="grid gap-4 grid-cols-2">
              {stats.computation_stats && (
                <TrackCard
                  icon="🧮"
                  label="연산"
                  stats={stats.computation_stats}
                  color="blue"
                />
              )}
              {stats.concept_stats && (
                <TrackCard
                  icon="📚"
                  label="개념"
                  stats={stats.concept_stats}
                  color="emerald"
                />
              )}
            </div>
          </motion.div>
        )}

        {/* 취약 개념 */}
        {stats.weak_concepts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              📚 더 연습이 필요한 개념
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
            transition={{ delay: 0.4 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">⭐ 잘하는 개념</h2>
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
}

function StatCard({ icon, label, value, suffix }: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="mb-3 text-3xl">{icon}</div>
      <p className="mb-1 text-sm text-gray-600">{label}</p>
      <p className="font-math text-3xl font-bold tabular-nums text-gray-900">
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

// 트랙별 통계 카드
interface TrackCardProps {
  icon: string
  label: string
  stats: TrackStats
  color: 'blue' | 'emerald'
}

function TrackCard({ icon, label, stats: trackStats, color }: TrackCardProps) {
  const gradients = {
    blue: 'from-blue-400 to-blue-600',
    emerald: 'from-emerald-400 to-emerald-600',
  }
  const bgColors = {
    blue: 'bg-blue-50',
    emerald: 'bg-emerald-50',
  }
  const textColors = {
    blue: 'text-blue-700',
    emerald: 'text-emerald-700',
  }

  return (
    <div className={`rounded-2xl ${bgColors[color]} p-5 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">{icon}</span>
        <span className={`font-semibold ${textColors[color]}`}>{label}</span>
      </div>
      <p className={`font-math text-4xl font-black ${textColors[color]} mb-2`}>
        {trackStats.accuracy_rate}%
      </p>
      <p className="text-sm text-gray-500 mb-3">
        {trackStats.correct_answers}/{trackStats.total_questions} 정답
      </p>
      <div className="h-2.5 overflow-hidden rounded-full bg-white/70 shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${trackStats.accuracy_rate}%` }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full bg-gradient-to-r ${gradients[color]}`}
        />
      </div>
    </div>
  )
}

function ConceptBar({ name, accuracy, color }: ConceptBarProps) {
  const bgColor = color === 'red' ? 'bg-red-50' : 'bg-green-50'
  const barColor =
    color === 'red'
      ? 'bg-gradient-to-r from-red-400 to-red-600'
      : 'bg-gradient-to-r from-green-400 to-green-600'
  const textColor = color === 'red' ? 'text-red-600' : 'text-green-600'

  return (
    <div className={`rounded-xl ${bgColor} p-5 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="mb-3 flex items-center justify-between">
        <span className="font-semibold text-gray-900">{name}</span>
        <span className={`font-math text-xl font-bold ${textColor}`}>{accuracy}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-white/70 shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${accuracy}%` }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full ${barColor}`}
        />
      </div>
    </div>
  )
}
