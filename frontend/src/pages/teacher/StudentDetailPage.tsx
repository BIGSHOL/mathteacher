// 강사용 학생 상세 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import type { Grade } from '../../types'

interface ConceptStat {
  concept_id: string
  concept_name: string
  total_questions: number
  correct_count: number
  accuracy_rate: number
}

interface RecentTest {
  test_id: string
  test_title: string
  score: number
  max_score: number
  accuracy_rate: number
  completed_at: string
}

interface DailyActivity {
  date: string
  tests_completed: number
  questions_answered: number
  accuracy_rate: number
}

interface StudentDetail {
  user_id: string
  name: string
  email: string
  grade: Grade
  class_name: string
  total_tests: number
  total_questions: number
  correct_answers: number
  accuracy_rate: number
  average_time_per_question: number
  current_streak: number
  max_streak: number
  level: number
  total_xp: number
  weak_concepts: ConceptStat[]
  strong_concepts: ConceptStat[]
  recent_tests: RecentTest[]
  daily_activity: DailyActivity[]
}

const formatGrade = (grade: Grade): string => {
  const gradeMap: Record<string, string> = {
    elementary_1: '초등 1학년', elementary_2: '초등 2학년', elementary_3: '초등 3학년',
    elementary_4: '초등 4학년', elementary_5: '초등 5학년', elementary_6: '초등 6학년',
    middle_1: '중등 1학년', middle_2: '중등 2학년', middle_3: '중등 3학년',
    high_1: '고등 1학년',
  }
  return gradeMap[grade] || grade
}

export function StudentDetailPage() {
  const { studentId } = useParams<{ studentId: string }>()
  const navigate = useNavigate()
  const [data, setData] = useState<StudentDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (studentId) fetchDetail()
  }, [studentId])

  const fetchDetail = async () => {
    try {
      setIsLoading(true)
      const res = await api.get<{ success: boolean; data: StudentDetail }>(
        `/api/v1/stats/students/${studentId}`
      )
      setData(res.data.data)
    } catch {
      setError('학생 정보를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error || '학생을 찾을 수 없습니다.'}</p>
          <button onClick={() => navigate('/teacher/students')} className="btn-primary px-4 py-2">
            목록으로
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* 뒤로가기 */}
        <button
          onClick={() => navigate('/teacher/students')}
          className="mb-6 text-sm text-gray-500 hover:text-gray-700"
        >
          &larr; 학생 목록으로
        </button>

        {/* 프로필 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 rounded-2xl bg-white p-6 shadow-sm"
        >
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-2xl font-bold text-white">
              {data.name.charAt(0)}
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{data.name}</h1>
              <p className="text-gray-500">{data.email}</p>
              <div className="mt-1 flex items-center gap-3 text-sm text-gray-600">
                <span>{formatGrade(data.grade)}</span>
                <span>{data.class_name}</span>
                <span className="rounded-full bg-purple-100 px-2 py-0.5 text-xs font-medium text-purple-700">
                  Lv.{data.level}
                </span>
                <span className="text-xs text-gray-400">{data.total_xp.toLocaleString()} XP</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* 핵심 지표 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4"
        >
          <StatCard label="총 테스트" value={`${data.total_tests}회`} />
          <StatCard label="정답률" value={`${data.accuracy_rate}%`} color={data.accuracy_rate >= 80 ? 'green' : data.accuracy_rate >= 60 ? 'yellow' : 'red'} />
          <StatCard label="평균 풀이 시간" value={`${data.average_time_per_question.toFixed(1)}초`} />
          <StatCard label="최대 스트릭" value={`${data.max_streak}회`} />
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* 취약 개념 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">취약 개념</h2>
            {data.weak_concepts.length === 0 ? (
              <p className="text-sm text-gray-500">취약 개념이 없습니다.</p>
            ) : (
              <div className="space-y-3">
                {data.weak_concepts.map((c) => (
                  <div key={c.concept_id} className="flex items-center justify-between">
                    <span className="text-sm text-gray-800">{c.concept_name}</span>
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-gray-200">
                        <div
                          className="h-full rounded-full bg-red-400"
                          style={{ width: `${c.accuracy_rate}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-red-600">{c.accuracy_rate}%</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>

          {/* 강점 개념 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">강점 개념</h2>
            {data.strong_concepts.length === 0 ? (
              <p className="text-sm text-gray-500">아직 데이터가 없습니다.</p>
            ) : (
              <div className="space-y-3">
                {data.strong_concepts.map((c) => (
                  <div key={c.concept_id} className="flex items-center justify-between">
                    <span className="text-sm text-gray-800">{c.concept_name}</span>
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-gray-200">
                        <div
                          className="h-full rounded-full bg-green-400"
                          style={{ width: `${c.accuracy_rate}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-green-600">{c.accuracy_rate}%</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </div>

        {/* 최근 테스트 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-6 rounded-2xl bg-white p-6 shadow-sm"
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">최근 테스트</h2>
          {data.recent_tests.length === 0 ? (
            <p className="text-sm text-gray-500">테스트 기록이 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium text-gray-600">테스트</th>
                    <th className="px-4 py-3 text-center font-medium text-gray-600">점수</th>
                    <th className="px-4 py-3 text-center font-medium text-gray-600">정답률</th>
                    <th className="px-4 py-3 text-center font-medium text-gray-600">완료일</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {data.recent_tests.map((t) => (
                    <tr key={`${t.test_id}-${t.completed_at}`}>
                      <td className="px-4 py-3 text-gray-900">{t.test_title}</td>
                      <td className="px-4 py-3 text-center">
                        {t.score}/{t.max_score}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={t.accuracy_rate >= 80 ? 'text-green-600' : t.accuracy_rate >= 60 ? 'text-yellow-600' : 'text-red-600'}>
                          {t.accuracy_rate}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center text-gray-500">
                        {new Date(t.completed_at).toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

function StatCard({ label, value, color }: { label: string; value: string; color?: string }) {
  const colorClass = color === 'green' ? 'text-green-600' : color === 'red' ? 'text-red-600' : color === 'yellow' ? 'text-yellow-600' : 'text-gray-900'
  return (
    <div className="rounded-xl bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className={`text-2xl font-bold ${colorClass}`}>{value}</p>
    </div>
  )
}
