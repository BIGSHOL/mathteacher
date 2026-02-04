import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuthStore } from '../../store/authStore'
import api from '../../lib/api'
import type { DailyTestRecord, DailyTestTodayResponse, PaginatedResponse } from '../../types'

const CATEGORY_CONFIG: Record<string, { icon: string; gradient: string; border: string }> = {
  concept: { icon: '📚', gradient: 'from-blue-50 to-sky-50', border: 'border-l-blue-400' },
  computation: { icon: '🧮', gradient: 'from-rose-50 to-pink-50', border: 'border-l-rose-400' },
  fill_in_blank: { icon: '✏️', gradient: 'from-violet-50 to-purple-50', border: 'border-l-violet-400' },
}

export function DailyLabPage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const [todayData, setTodayData] = useState<DailyTestTodayResponse | null>(null)
  const [history, setHistory] = useState<DailyTestRecord[]>([])
  const [historyTotal, setHistoryTotal] = useState(0)
  const [historyPage, setHistoryPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [starting, setStarting] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [todayRes, historyRes] = await Promise.all([
        api.get<{ success: boolean; data: DailyTestTodayResponse }>('/api/v1/daily-tests/today'),
        api.get<{ success: boolean; data: PaginatedResponse<DailyTestRecord> }>('/api/v1/daily-tests/history?page=1&page_size=30'),
      ])
      setTodayData(todayRes.data.data)
      setHistory(historyRes.data.data.items)
      setHistoryTotal(historyRes.data.data.total)
    } catch {
      // 에러 무시
    } finally {
      setLoading(false)
    }
  }

  const loadMoreHistory = async () => {
    const nextPage = historyPage + 1
    try {
      const res = await api.get<{ success: boolean; data: PaginatedResponse<DailyTestRecord> }>(
        `/api/v1/daily-tests/history?page=${nextPage}&page_size=30`
      )
      setHistory((prev) => [...prev, ...res.data.data.items])
      setHistoryPage(nextPage)
    } catch {
      // 에러 무시
    }
  }

  const handleCardClick = async (record: DailyTestRecord) => {
    if (record.status === 'completed' && record.attempt_id) {
      navigate(`/test/result/${record.attempt_id}`)
      return
    }

    if (record.status === 'in_progress' && record.attempt_id) {
      navigate(`/test/play/${record.attempt_id}`)
      return
    }

    // pending → 시작
    setStarting(record.id)
    try {
      const res = await api.post<{ success: boolean; data: { attempt_id: string } }>(
        `/api/v1/daily-tests/${record.id}/start`
      )
      navigate(`/test/play/${res.data.data.attempt_id}`)
    } catch {
      setStarting(null)
    }
  }

  // 날짜별 그룹핑
  const historyByDate = history.reduce<Record<string, DailyTestRecord[]>>((acc, record) => {
    if (!acc[record.date]) acc[record.date] = []
    acc[record.date]?.push(record)
    return acc
  }, {})

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr + 'T00:00:00')
    const month = date.getMonth() + 1
    const day = date.getDate()
    const weekDays = ['일', '월', '화', '수', '목', '금', '토']
    const weekDay = weekDays[date.getDay()]
    return `${month}/${day} (${weekDay})`
  }

  const completedToday = todayData?.tests.filter((t) => t.status === 'completed').length ?? 0
  const totalToday = todayData?.tests.length ?? 3

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                오늘의 수학
              </h1>
              <p className="text-gray-500 text-sm mt-1">
                {user?.name}님 | {todayData?.date}
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">오늘 진행</div>
              <div className="text-xl font-bold text-primary-600">
                {completedToday}/{totalToday}
              </div>
            </div>
          </div>
        </motion.div>

        {/* 오늘의 카테고리 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-3 gap-3 mb-8"
        >
          {todayData?.tests.map((record) => (
            <CategoryCard
              key={record.id}
              record={record}
              isStarting={starting === record.id}
              onClick={() => handleCardClick(record)}
            />
          ))}
        </motion.div>

        {/* 지난 기록 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-lg font-semibold text-gray-900 mb-4">학습 히스토리</h2>

          {Object.keys(historyByDate).length === 0 ? (
            <div className="card p-8 text-center text-gray-400">
              아직 학습 기록이 없습니다
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(historyByDate).map(([date, records]) => (
                <HistoryDateRow key={date} date={date} records={records} formatDate={formatDate} />
              ))}

              {history.length < historyTotal && (
                <button
                  onClick={loadMoreHistory}
                  className="w-full rounded-lg border border-gray-200 bg-white py-3 text-sm text-gray-500 hover:bg-gray-50"
                >
                  더 보기
                </button>
              )}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

// ------------------------------------------------------------------
// 하위 컴포넌트
// ------------------------------------------------------------------

function CategoryCard({
  record,
  isStarting,
  onClick,
}: {
  record: DailyTestRecord
  isStarting: boolean
  onClick: () => void
}) {
  const config = CATEGORY_CONFIG[record.category] ?? CATEGORY_CONFIG.concept
  const isCompleted = record.status === 'completed'
  const isInProgress = record.status === 'in_progress'

  const accuracy =
    isCompleted && record.correct_count != null && record.total_count
      ? Math.round((record.correct_count / record.total_count) * 100)
      : null

  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      onClick={onClick}
      disabled={isStarting}
      className={`
        relative flex flex-col items-center rounded-2xl border-l-4 p-4 text-center
        bg-gradient-to-br ${config?.gradient ?? 'from-blue-50 to-sky-50'} ${config?.border ?? 'border-l-blue-400'}
        transition-shadow hover:shadow-md
        ${isCompleted ? 'opacity-90' : ''}
        ${isStarting ? 'animate-pulse' : ''}
      `}
    >
      <span className="text-3xl mb-2">{config?.icon ?? '📚'}</span>
      <span className="text-sm font-semibold text-gray-800">{record.category_label}</span>

      {isCompleted && accuracy !== null ? (
        <span className={`mt-1 text-lg font-bold ${accuracy >= 80 ? 'text-green-600' : accuracy >= 50 ? 'text-yellow-600' : 'text-red-500'}`}>
          {accuracy}%
        </span>
      ) : isInProgress ? (
        <span className="mt-1 text-xs font-medium text-blue-500">이어서 풀기</span>
      ) : (
        <span className="mt-1 text-xs text-gray-400">{record.question_count}문제</span>
      )}

      {isCompleted && (
        <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-green-500 text-[10px] text-white">
          ✓
        </span>
      )}
    </motion.button>
  )
}

function HistoryDateRow({
  date,
  records,
  formatDate,
}: {
  date: string
  records: DailyTestRecord[]
  formatDate: (d: string) => string
}) {
  return (
    <div className="card flex items-center gap-3 px-4 py-3">
      <span className="text-sm font-medium text-gray-500 w-20 shrink-0">
        {formatDate(date)}
      </span>
      <div className="flex flex-1 gap-2">
        {records.map((r) => {
          const config = CATEGORY_CONFIG[r.category] ?? CATEGORY_CONFIG.concept
          const isCompleted = r.status === 'completed'
          const accuracy =
            isCompleted && r.correct_count != null && r.total_count
              ? Math.round((r.correct_count / r.total_count) * 100)
              : null

          return (
            <div
              key={r.id}
              className={`flex items-center gap-1 rounded-lg px-2 py-1 text-xs ${
                isCompleted ? 'bg-gray-100' : 'bg-gray-50 text-gray-300'
              }`}
            >
              <span className="text-sm">{config?.icon ?? '📚'}</span>
              {accuracy !== null ? (
                <span className={`font-semibold ${accuracy >= 80 ? 'text-green-600' : accuracy >= 50 ? 'text-yellow-600' : 'text-red-500'}`}>
                  {accuracy}%
                </span>
              ) : (
                <span className="text-gray-300">-</span>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
