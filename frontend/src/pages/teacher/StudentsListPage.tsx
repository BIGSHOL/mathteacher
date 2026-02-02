// 강사용 학생 목록 페이지

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import type { StudentStatsSummary, PaginatedResponse, Grade } from '../../types'
import { StreakBadge } from '../../components/gamification/StreakDisplay'

export function StudentsListPage() {
  const [students, setStudents] = useState<StudentStatsSummary[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [gradeFilter, setGradeFilter] = useState<Grade | ''>('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchStudents()
  }, [page, gradeFilter])

  const fetchStudents = async () => {
    try {
      setIsLoading(true)
      setError('')

      const params = new URLSearchParams({
        page: page.toString(),
        page_size: '20',
      })
      if (gradeFilter) {
        params.append('grade', gradeFilter)
      }

      const response = await api.get<{ success: boolean; data: PaginatedResponse<StudentStatsSummary> }>(
        `/api/v1/stats/students?${params}`
      )

      setStudents(response.data.data.items)
      setTotalPages(response.data.data.total_pages)
    } catch {
      setError('학생 목록을 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const filteredStudents = students.filter((student) =>
    student.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const gradeOptions: { value: Grade | ''; label: string }[] = [
    { value: '', label: '전체 학년' },
    { value: 'elementary_1', label: '초등 1학년' },
    { value: 'elementary_2', label: '초등 2학년' },
    { value: 'elementary_3', label: '초등 3학년' },
    { value: 'elementary_4', label: '초등 4학년' },
    { value: 'elementary_5', label: '초등 5학년' },
    { value: 'elementary_6', label: '초등 6학년' },
    { value: 'middle_1', label: '중등 1학년' },
    { value: 'middle_2', label: '중등 2학년' },
    { value: 'middle_3', label: '중등 3학년' },
    { value: 'high_1', label: '고등 1학년' },
  ]

  const formatGrade = (grade: Grade): string => {
    const gradeMap: Record<Grade, string> = {
      elementary_1: '초1',
      elementary_2: '초2',
      elementary_3: '초3',
      elementary_4: '초4',
      elementary_5: '초5',
      elementary_6: '초6',
      middle_1: '중1',
      middle_2: '중2',
      middle_3: '중3',
      high_1: '고1',
    }
    return gradeMap[grade] || grade
  }

  const formatLastActivity = (dateStr: string | null): string => {
    if (!dateStr) return '활동 없음'
    const date = new Date(dateStr)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return '오늘'
    if (diffDays === 1) return '어제'
    if (diffDays < 7) return `${diffDays}일 전`
    return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })
  }

  if (isLoading && students.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">학생 목록을 불러오는 중...</p>
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
          <h1 className="text-2xl font-bold text-gray-900">학생 관리</h1>
          <p className="text-gray-600">담당 학생들의 학습 현황을 확인하세요</p>
        </motion.div>

        {/* 필터 & 검색 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex gap-4">
            <select
              value={gradeFilter}
              onChange={(e) => {
                setGradeFilter(e.target.value as Grade | '')
                setPage(1)
              }}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              {gradeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="relative">
            <input
              type="text"
              placeholder="이름으로 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 sm:w-64"
            />
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              🔍
            </span>
          </div>
        </motion.div>

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 p-4 text-red-600">{error}</div>
        )}

        {/* 학생 목록 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="overflow-hidden rounded-2xl bg-white shadow-sm"
        >
          {filteredStudents.length === 0 ? (
            <div className="p-8 text-center">
              <div className="mb-4 text-4xl">👥</div>
              <p className="text-gray-600">
                {searchQuery ? '검색 결과가 없습니다.' : '담당 학생이 없습니다.'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-600">학생</th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-600">학년/반</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">레벨</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">XP</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">정답률</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">테스트</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">스트릭</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">최근 활동</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredStudents.map((student, index) => (
                    <motion.tr
                      key={student.user_id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="cursor-pointer hover:bg-gray-50"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white font-medium">
                            {student.name.charAt(0)}
                          </div>
                          <span className="font-medium text-gray-900">{student.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div>
                          <span className="text-gray-900">{formatGrade(student.grade)}</span>
                          {student.class_name && (
                            <span className="ml-2 text-sm text-gray-500">{student.class_name}</span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="inline-flex items-center rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-700">
                          Lv.{student.level}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="font-medium text-gray-900">{student.total_xp.toLocaleString()}</span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span
                          className={`font-medium ${
                            student.accuracy_rate >= 80
                              ? 'text-green-600'
                              : student.accuracy_rate >= 60
                              ? 'text-yellow-600'
                              : 'text-red-600'
                          }`}
                        >
                          {student.accuracy_rate}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center text-gray-600">
                        {student.tests_completed}개
                      </td>
                      <td className="px-6 py-4 text-center">
                        <StreakBadge streak={student.current_streak} />
                      </td>
                      <td className="px-6 py-4 text-center text-sm text-gray-500">
                        {formatLastActivity(student.last_activity_at)}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>

        {/* 페이지네이션 */}
        {totalPages > 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-6 flex items-center justify-center gap-2"
          >
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              이전
            </button>
            <div className="flex gap-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = Math.max(1, Math.min(page - 2, totalPages - 4)) + i
                if (pageNum > totalPages) return null
                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`rounded-lg px-4 py-2 text-sm font-medium ${
                      page === pageNum
                        ? 'bg-primary-500 text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {pageNum}
                  </button>
                )
              })}
            </div>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              다음
            </button>
          </motion.div>
        )}
      </div>
    </div>
  )
}
