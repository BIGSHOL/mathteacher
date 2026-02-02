// 강사 대시보드 페이지

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import type { DashboardStats, StudentStatsSummary, PaginatedResponse } from '../../types'

export function DashboardPage() {
  const navigate = useNavigate()
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null)
  const [students, setStudents] = useState<StudentStatsSummary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setIsLoading(true)
      setError('')

      const [dashboardRes, studentsRes] = await Promise.all([
        api.get<{ success: boolean; data: DashboardStats }>('/api/v1/stats/dashboard'),
        api.get<{ success: boolean; data: PaginatedResponse<StudentStatsSummary> }>(
          '/api/v1/stats/students?page_size=10'
        ),
      ])

      setDashboardStats(dashboardRes.data.data)
      setStudents(studentsRes.data.data.items)
    } catch {
      setError('데이터를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">대시보드를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error}</p>
          <button onClick={fetchData} className="btn-primary px-4 py-2">
            다시 시도
          </button>
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
          <h1 className="text-2xl font-bold text-gray-900">대시보드</h1>
          <p className="text-gray-600">학습 현황을 한눈에 확인하세요</p>
        </motion.div>

        {/* 오늘 통계 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">오늘</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              icon="👥"
              label="활동 학생"
              value={dashboardStats?.today.active_students || 0}
              suffix="명"
              color="blue"
            />
            <StatCard
              icon="📝"
              label="완료 테스트"
              value={dashboardStats?.today.tests_completed || 0}
              suffix="개"
              color="green"
            />
            <StatCard
              icon="✏️"
              label="풀이 문제"
              value={dashboardStats?.today.questions_answered || 0}
              suffix="문제"
              color="purple"
            />
            <StatCard
              icon="🎯"
              label="평균 정답률"
              value={dashboardStats?.today.average_accuracy || 0}
              suffix="%"
              color="orange"
            />
          </div>
        </motion.div>

        {/* 이번 주 통계 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">이번 주</h2>
          <div className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-2xl bg-white p-6 shadow-sm">
              <div className="mb-4 flex items-center justify-between">
                <span className="text-gray-600">활동 학생</span>
                <span className="text-2xl font-bold text-primary-600">
                  {dashboardStats?.this_week.active_students || 0}명
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">완료 테스트</span>
                <span className="text-2xl font-bold text-green-600">
                  {dashboardStats?.this_week.tests_completed || 0}개
                </span>
              </div>
            </div>

            {/* 정답률 트렌드 차트 */}
            <div className="rounded-2xl bg-white p-6 shadow-sm">
              <h3 className="mb-4 font-medium text-gray-700">7일간 정답률 추이</h3>
              <AccuracyTrendChart trend={dashboardStats?.this_week.accuracy_trend || []} />
            </div>
          </div>
        </motion.div>

        {/* 알림 */}
        {dashboardStats?.alerts && dashboardStats.alerts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-8"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">관심 필요 학생</h2>
            <div className="space-y-2">
              {dashboardStats.alerts.map((alert, index) => (
                <AlertCard key={index} alert={alert} />
              ))}
            </div>
          </motion.div>
        )}

        {/* 학생 목록 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">학생 현황</h2>
            <button
              onClick={() => navigate('/teacher/students')}
              className="text-sm text-primary-600 hover:text-primary-700"
            >
              전체 보기 →
            </button>
          </div>
          <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">이름</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">학년</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">레벨</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">정답률</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">스트릭</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">테스트</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {students.map((student) => (
                    <StudentRow key={student.user_id} student={student} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>
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
  color: 'blue' | 'green' | 'purple' | 'orange'
}

function StatCard({ icon, label, value, suffix, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600',
  }

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <div className={`mb-3 inline-flex h-12 w-12 items-center justify-center rounded-xl ${colorClasses[color]}`}>
        <span className="text-2xl">{icon}</span>
      </div>
      <p className="mb-1 text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-bold text-gray-900">
        {value}
        <span className="ml-1 text-sm font-normal text-gray-500">{suffix}</span>
      </p>
    </div>
  )
}

// 정답률 트렌드 차트 컴포넌트
function AccuracyTrendChart({ trend }: { trend: number[] }) {
  const days = ['일', '월', '화', '수', '목', '금', '토']
  const today = new Date().getDay()
  const orderedDays = [...days.slice(today - 6), ...days.slice(0, today + 1)].slice(-7)
  const maxValue = Math.max(...trend, 100)

  return (
    <div className="flex h-32 items-end justify-between gap-2">
      {trend.map((value, index) => (
        <div key={index} className="flex flex-1 flex-col items-center">
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: `${(value / maxValue) * 100}%` }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
            className="w-full min-h-[4px] rounded-t bg-primary-500"
            title={`${value}%`}
          />
          <span className="mt-2 text-xs text-gray-500">{orderedDays[index]}</span>
        </div>
      ))}
    </div>
  )
}

// 알림 카드 컴포넌트
interface AlertCardProps {
  alert: {
    type: string
    student_name: string
    message: string
  }
}

function AlertCard({ alert }: AlertCardProps) {
  const getAlertIcon = () => {
    switch (alert.type) {
      case 'inactive':
        return '😴'
      case 'low_accuracy':
        return '📉'
      case 'struggling':
        return '😓'
      default:
        return '⚠️'
    }
  }

  return (
    <div className="flex items-center gap-4 rounded-xl bg-yellow-50 p-4">
      <span className="text-2xl">{getAlertIcon()}</span>
      <div>
        <p className="font-medium text-gray-900">{alert.student_name}</p>
        <p className="text-sm text-gray-600">{alert.message}</p>
      </div>
    </div>
  )
}

// 학생 행 컴포넌트
function StudentRow({ student }: { student: StudentStatsSummary }) {
  const getStreakBadge = () => {
    if (student.current_streak >= 30) return { icon: '👑', color: 'text-yellow-600' }
    if (student.current_streak >= 14) return { icon: '💎', color: 'text-blue-600' }
    if (student.current_streak >= 7) return { icon: '🔥', color: 'text-orange-600' }
    if (student.current_streak >= 3) return { icon: '⚡', color: 'text-yellow-600' }
    return { icon: '', color: '' }
  }

  const streak = getStreakBadge()

  return (
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-medium text-primary-700">
            {student.name.charAt(0)}
          </div>
          <span className="font-medium text-gray-900">{student.name}</span>
        </div>
      </td>
      <td className="px-4 py-3 text-gray-600">{student.grade}</td>
      <td className="px-4 py-3">
        <span className="inline-flex items-center rounded-full bg-purple-100 px-2 py-1 text-xs font-medium text-purple-700">
          Lv.{student.level}
        </span>
      </td>
      <td className="px-4 py-3">
        <span className={`font-medium ${student.accuracy_rate >= 80 ? 'text-green-600' : student.accuracy_rate >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
          {student.accuracy_rate}%
        </span>
      </td>
      <td className="px-4 py-3">
        {student.current_streak > 0 && (
          <span className={`${streak.color}`}>
            {streak.icon} {student.current_streak}일
          </span>
        )}
      </td>
      <td className="px-4 py-3 text-gray-600">{student.tests_completed}개</td>
    </tr>
  )
}
