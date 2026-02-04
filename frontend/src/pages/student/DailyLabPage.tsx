// 이달의 수학 - 월간 캘린더 뷰

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import { useAuthStore } from '../../store/authStore'
import api from '../../lib/api'
import type { DailyTestRecord, DailyTestTodayResponse, PaginatedResponse } from '../../types'

const CATEGORY_CONFIG: Record<string, { icon: string; gradient: string; border: string; label: string }> = {
  concept: { icon: '📚', gradient: 'from-blue-50 to-sky-50', border: 'border-l-blue-400', label: '개념' },
  computation: { icon: '🧮', gradient: 'from-rose-50 to-pink-50', border: 'border-l-rose-400', label: '연산' },
  fill_in_blank: { icon: '✏️', gradient: 'from-violet-50 to-purple-50', border: 'border-l-violet-400', label: '빈칸' },
}

const WEEKDAYS = ['일', '월', '화', '수', '목', '금', '토']

export function DailyLabPage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const [todayData, setTodayData] = useState<DailyTestTodayResponse | null>(null)
  const [history, setHistory] = useState<DailyTestRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [starting, setStarting] = useState<string | null>(null)

  const [viewYear, setViewYear] = useState(() => new Date().getFullYear())
  const [viewMonth, setViewMonth] = useState(() => new Date().getMonth())

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [todayRes, historyRes] = await Promise.all([
        api.get<{ success: boolean; data: DailyTestTodayResponse }>('/api/v1/daily-tests/today'),
        api.get<{ success: boolean; data: PaginatedResponse<DailyTestRecord> }>(
          '/api/v1/daily-tests/history?page=1&page_size=100'
        ),
      ])
      setTodayData(todayRes.data.data)
      setHistory(historyRes.data.data.items)
    } catch {
      // ignore
    } finally {
      setLoading(false)
    }
  }

  // ---- 월 이동 ----
  const goToPrevMonth = () => {
    if (viewMonth === 0) {
      setViewYear((y) => y - 1)
      setViewMonth(11)
    } else {
      setViewMonth((m) => m - 1)
    }
  }

  const goToNextMonth = () => {
    const now = new Date()
    if (viewYear === now.getFullYear() && viewMonth === now.getMonth()) return
    if (viewMonth === 11) {
      setViewYear((y) => y + 1)
      setViewMonth(0)
    } else {
      setViewMonth((m) => m + 1)
    }
  }

  const isCurrentMonth =
    viewYear === new Date().getFullYear() && viewMonth === new Date().getMonth()

  // ---- 날짜별 기록 매핑 ----
  const historyByDate: Record<string, DailyTestRecord[]> = {}
  for (const r of history) {
    if (!historyByDate[r.date]) historyByDate[r.date] = []
    historyByDate[r.date]!.push(r)
  }
  if (todayData) {
    const d = todayData.date
    if (!historyByDate[d]) historyByDate[d] = []
    // 오늘 데이터가 history에 없으면 추가
    for (const t of todayData.tests) {
      if (!historyByDate[d].some((h) => h.id === t.id)) {
        historyByDate[d].push(t)
      }
    }
  }

  // ---- 캘린더 그리드 ----
  const daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate()
  const firstDayOfWeek = new Date(viewYear, viewMonth, 1).getDay()

  const calendarDays: (number | null)[] = []
  for (let i = 0; i < firstDayOfWeek; i++) calendarDays.push(null)
  for (let d = 1; d <= daysInMonth; d++) calendarDays.push(d)
  while (calendarDays.length % 7 !== 0) calendarDays.push(null)

  const now = new Date()
  const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

  const getDateStr = (day: number) =>
    `${viewYear}-${String(viewMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`

  // ---- 이번달 통계 ----
  const monthDates = Array.from({ length: daysInMonth }, (_, i) => getDateStr(i + 1))
  const activeDays = monthDates.filter((d) => {
    const recs = historyByDate[d]
    return recs && recs.length > 0
  }).length
  const completedDays = monthDates.filter((d) => {
    const recs = historyByDate[d]
    if (!recs || recs.length === 0) return false
    return recs.every((r) => r.status === 'completed')
  }).length

  // ---- 오늘 테스트 핸들러 ----
  const handleCardClick = async (record: DailyTestRecord) => {
    if (record.status === 'completed' && record.attempt_id) {
      navigate(`/test/result/${record.attempt_id}`)
      return
    }
    // 항상 start API를 거쳐서 유효한 attempt_id 확보
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
      <div className="container mx-auto max-w-2xl px-4">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">이달의 수학</h1>
              <p className="mt-1 text-sm text-gray-500">
                {user?.name}님의 {viewMonth + 1}월 학습 현황
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">이번달 학습</div>
              <div className="text-xl font-bold text-primary-600">
                {completedDays}/{activeDays || '-'}일
              </div>
            </div>
          </div>
        </motion.div>

        {/* 오늘의 학습 카드 */}
        {isCurrentMonth && todayData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-6"
          >
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-gray-700">오늘의 학습</h2>
              <span className="text-xs text-gray-400">
                {todayData.date} · {completedToday}/{totalToday} 완료
              </span>
            </div>
            <div className="grid grid-cols-3 gap-3">
              {todayData.tests.map((record) => (
                <CategoryCard
                  key={record.id}
                  record={record}
                  isStarting={starting === record.id}
                  onClick={() => handleCardClick(record)}
                />
              ))}
            </div>
          </motion.div>
        )}

        {/* 월간 캘린더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="card p-4">
            {/* 월 이동 */}
            <div className="mb-4 flex items-center justify-between">
              <button
                onClick={goToPrevMonth}
                className="rounded-lg p-2 text-gray-500 hover:bg-gray-100"
              >
                <ChevronLeft />
              </button>
              <h3 className="text-lg font-bold text-gray-900">
                {viewYear}년 {viewMonth + 1}월
              </h3>
              <button
                onClick={goToNextMonth}
                disabled={isCurrentMonth}
                className={clsx(
                  'rounded-lg p-2',
                  isCurrentMonth
                    ? 'cursor-not-allowed text-gray-300'
                    : 'text-gray-500 hover:bg-gray-100'
                )}
              >
                <ChevronRight />
              </button>
            </div>

            {/* 요일 헤더 */}
            <div className="mb-2 grid grid-cols-7">
              {WEEKDAYS.map((wd, i) => (
                <div
                  key={wd}
                  className={clsx(
                    'py-1 text-center text-xs font-medium',
                    i === 0 ? 'text-red-400' : i === 6 ? 'text-blue-400' : 'text-gray-400'
                  )}
                >
                  {wd}
                </div>
              ))}
            </div>

            {/* 날짜 셀 */}
            <div className="grid grid-cols-7 gap-1">
              {calendarDays.map((day, idx) => {
                if (day === null) return <div key={`e-${idx}`} className="aspect-square" />

                const dateStr = getDateStr(day)
                const records = historyByDate[dateStr]
                const isToday = dateStr === todayStr
                const isFuture = new Date(dateStr + 'T23:59:59') > now && !isToday

                const completedCount =
                  records?.filter((r) => r.status === 'completed').length ?? 0
                const totalCount = records?.length ?? 0
                const allCompleted = totalCount > 0 && completedCount === totalCount
                const someActivity = totalCount > 0

                const dayOfWeek = new Date(dateStr + 'T00:00:00').getDay()

                return (
                  <div
                    key={day}
                    className={clsx(
                      'relative flex flex-col items-center justify-center rounded-lg aspect-square transition-all',
                      isToday && 'ring-2 ring-primary-400 bg-primary-50',
                      !isToday && allCompleted && 'bg-green-50',
                      !isToday && someActivity && !allCompleted && 'bg-yellow-50',
                      isFuture && 'opacity-30'
                    )}
                  >
                    <span
                      className={clsx(
                        'text-xs font-medium',
                        isToday
                          ? 'font-bold text-primary-700'
                          : dayOfWeek === 0
                            ? 'text-red-400'
                            : dayOfWeek === 6
                              ? 'text-blue-400'
                              : 'text-gray-600',
                        isFuture && 'text-gray-300'
                      )}
                    >
                      {day}
                    </span>

                    {/* 카테고리별 완료 표시 (점) */}
                    {someActivity && !isFuture && (
                      <div className="mt-0.5 flex gap-0.5">
                        {records!.map((r) => (
                          <span
                            key={r.id}
                            className={clsx(
                              'inline-block h-1.5 w-1.5 rounded-full',
                              r.status === 'completed'
                                ? 'bg-green-500'
                                : r.status === 'in_progress'
                                  ? 'bg-yellow-400'
                                  : 'bg-gray-300'
                            )}
                            title={`${CATEGORY_CONFIG[r.category]?.label ?? r.category} ${r.status === 'completed' ? '완료' : '미완료'}`}
                          />
                        ))}
                      </div>
                    )}

                    {allCompleted && (
                      <span className="absolute -right-0.5 -top-0.5 text-[8px]">✅</span>
                    )}
                  </div>
                )
              })}
            </div>

            {/* 범례 */}
            <div className="mt-4 flex items-center justify-center gap-4 text-xs text-gray-500">
              <div className="flex items-center gap-1">
                <span className="inline-block h-2 w-2 rounded-full bg-green-500" />
                <span>완료</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="inline-block h-2 w-2 rounded-full bg-yellow-400" />
                <span>진행중</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="inline-block h-2 w-2 rounded-full bg-gray-300" />
                <span>미완료</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* 월간 요약 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-4 grid grid-cols-3 gap-3"
        >
          <div className="card p-4 text-center">
            <div className="mb-1 text-2xl">📅</div>
            <div className="text-xs text-gray-500">학습일</div>
            <div className="text-lg font-bold text-gray-900">{activeDays}일</div>
          </div>
          <div className="card p-4 text-center">
            <div className="mb-1 text-2xl">✅</div>
            <div className="text-xs text-gray-500">전부 완료</div>
            <div className="text-lg font-bold text-green-600">{completedDays}일</div>
          </div>
          <div className="card p-4 text-center">
            <div className="mb-1 text-2xl">🔥</div>
            <div className="text-xs text-gray-500">완료율</div>
            <div className="text-lg font-bold text-primary-600">
              {activeDays > 0 ? Math.round((completedDays / activeDays) * 100) : 0}%
            </div>
          </div>
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
  const config = CATEGORY_CONFIG[record.category] ?? CATEGORY_CONFIG['concept']!
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
        bg-gradient-to-br ${config.gradient} ${config.border}
        transition-shadow hover:shadow-md
        ${isCompleted ? 'opacity-90' : ''}
        ${isStarting ? 'animate-pulse' : ''}
      `}
    >
      <span className="mb-2 text-3xl">{config.icon}</span>
      <span className="text-sm font-semibold text-gray-800">{record.category_label}</span>

      {isCompleted && accuracy !== null ? (
        <span
          className={`mt-1 text-lg font-bold ${accuracy >= 80 ? 'text-green-600' : accuracy >= 50 ? 'text-yellow-600' : 'text-red-500'}`}
        >
          {accuracy}%
        </span>
      ) : isInProgress ? (
        <span className="mt-1 text-xs font-medium text-blue-500">이어서 풀기</span>
      ) : (
        <span className="mt-1 text-xs text-gray-400">{record.question_count}문제</span>
      )}

      {isCompleted && (
        <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-green-500 text-[10px] text-white">
          ✓
        </span>
      )}
    </motion.button>
  )
}

function ChevronLeft() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
    </svg>
  )
}

function ChevronRight() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  )
}
