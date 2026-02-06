// 강사용 학생 상세 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import type { Grade } from '../../types'

interface ClassInfo {
  id: string
  name: string
}

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

interface ChapterProgress {
  chapter_id: string
  chapter_name: string
  chapter_number: number
  is_unlocked: boolean
  is_completed: boolean
  overall_progress: number
  concepts_mastery: Record<string, number>
}

interface TrackStats {
  total_questions: number
  correct_answers: number
  accuracy_rate: number
}

interface StudentDetail {
  user_id: string
  name: string
  login_id: string
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
  today_solved: number
  computation_stats?: TrackStats
  concept_stats?: TrackStats
  weak_concepts: ConceptStat[]
  strong_concepts: ConceptStat[]
  recent_tests: RecentTest[]
  daily_activity: DailyActivity[]
  chapter_progress: ChapterProgress[]
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

const GRADE_OPTIONS: { value: Grade; label: string }[] = [
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

export function StudentDetailPage() {
  const { studentId } = useParams<{ studentId: string }>()
  const navigate = useNavigate()
  const [data, setData] = useState<StudentDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  // 설정 관련 상태
  const [showSettings, setShowSettings] = useState(false)
  const [classes, setClasses] = useState<ClassInfo[]>([])
  const [editGrade, setEditGrade] = useState<Grade | ''>('')
  const [editClassId, setEditClassId] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [showResetHistoryModal, setShowResetHistoryModal] = useState(false)
  const [actionLoading, setActionLoading] = useState(false)
  const [actionMessage, setActionMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  // 단원 잠금 해제 관련 상태
  const [chapterActionLoading, setChapterActionLoading] = useState<string | null>(null)

  useEffect(() => {
    if (studentId) {
      fetchDetail()
      fetchClasses()
    }
  }, [studentId])

  const fetchClasses = async () => {
    try {
      const res = await api.get<{ success: boolean; data: { items: ClassInfo[] } }>('/api/v1/classes')
      setClasses(res.data.data.items || [])
    } catch {
      // 반 목록 로드 실패시 무시
    }
  }

  const fetchDetail = async () => {
    try {
      setIsLoading(true)
      const res = await api.get<{ success: boolean; data: StudentDetail }>(
        `/api/v1/stats/students/${studentId}`
      )
      const studentData = res.data.data
      setData(studentData)
      setEditGrade(studentData.grade)
      // class_id는 별도로 가져와야 함
    } catch {
      setError('학생 정보를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdateStudent = async () => {
    if (!studentId) return
    setActionLoading(true)
    setActionMessage(null)
    try {
      const updateData: { grade?: Grade; class_id?: string } = {}
      if (editGrade) updateData.grade = editGrade
      if (editClassId) updateData.class_id = editClassId

      await api.patch(`/api/v1/students/${studentId}`, updateData)
      setActionMessage({ type: 'success', text: '학생 정보가 수정되었습니다.' })
      fetchDetail()
    } catch {
      setActionMessage({ type: 'error', text: '수정에 실패했습니다.' })
    } finally {
      setActionLoading(false)
    }
  }

  const handleToggleActive = async () => {
    if (!studentId || !data) return
    setActionLoading(true)
    setActionMessage(null)
    try {
      // 현재 활성 상태의 반대로 설정 (StudentDetail에 is_active가 없으므로 별도 API 호출)
      const studentRes = await api.get<{ success: boolean; data: { is_active?: boolean } }>(`/api/v1/students/${studentId}`)
      const currentActive = studentRes.data.data.is_active !== false
      await api.patch(`/api/v1/students/${studentId}`, { is_active: !currentActive })
      setActionMessage({ type: 'success', text: currentActive ? '계정이 비활성화되었습니다.' : '계정이 활성화되었습니다.' })
    } catch {
      setActionMessage({ type: 'error', text: '상태 변경에 실패했습니다.' })
    } finally {
      setActionLoading(false)
    }
  }

  const handleResetPassword = async () => {
    if (!studentId || !newPassword) return
    setActionLoading(true)
    setActionMessage(null)
    try {
      await api.post(`/api/v1/students/${studentId}/reset-password`, { new_password: newPassword })
      setActionMessage({ type: 'success', text: '비밀번호가 초기화되었습니다.' })
      setNewPassword('')
      setShowPasswordModal(false)
    } catch {
      setActionMessage({ type: 'error', text: '비밀번호 초기화에 실패했습니다.' })
    } finally {
      setActionLoading(false)
    }
  }

  const handleResetHistory = async () => {
    if (!studentId) return
    setActionLoading(true)
    setActionMessage(null)
    try {
      await api.post(`/api/v1/students/${studentId}/reset-history`)
      setActionMessage({ type: 'success', text: '테스트 기록이 초기화되었습니다.' })
      setShowResetHistoryModal(false)
      fetchDetail()
    } catch {
      setActionMessage({ type: 'error', text: '기록 초기화에 실패했습니다.' })
    } finally {
      setActionLoading(false)
    }
  }

  const handleToggleChapterLock = async (chapterId: string, _currentlyUnlocked: boolean) => {
    if (!studentId) return
    setChapterActionLoading(chapterId)
    try {
      await api.post(`/api/v1/chapters/students/${studentId}/unlock/${chapterId}`)
      await fetchDetail()
    } catch {
      setActionMessage({ type: 'error', text: '단원 잠금 상태 변경에 실패했습니다.' })
    } finally {
      setChapterActionLoading(null)
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
    <div className="min-h-screen bg-gray-50 py-4 sm:py-8">
      <div className="container mx-auto px-3 sm:px-4">
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
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-2xl font-bold text-white">
                {data.name.charAt(0)}
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{data.name}</h1>
                <p className="text-gray-500">{data.login_id}</p>
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
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="rounded-lg bg-gray-100 p-2 text-gray-600 hover:bg-gray-200 transition-colors"
              title="학생 설정"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </motion.div>

        {/* 설정 패널 */}
        <AnimatePresence>
          {showSettings && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-6 overflow-hidden rounded-2xl bg-white shadow-sm"
            >
              <div className="border-b border-gray-100 bg-gray-50 px-6 py-4">
                <h2 className="font-semibold text-gray-900">학생 관리</h2>
              </div>
              <div className="p-6">
                {actionMessage && (
                  <div className={`mb-4 rounded-lg p-3 text-sm ${actionMessage.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                    {actionMessage.text}
                  </div>
                )}

                {/* 학년/반 변경 */}
                <div className="mb-6">
                  <h3 className="mb-3 text-sm font-medium text-gray-700">학년/반 변경</h3>
                  <div className="flex flex-wrap gap-3">
                    <select
                      value={editGrade}
                      onChange={(e) => setEditGrade(e.target.value as Grade)}
                      className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                    >
                      <option value="">학년 선택</option>
                      {GRADE_OPTIONS.map((opt) => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                      ))}
                    </select>
                    <select
                      value={editClassId}
                      onChange={(e) => setEditClassId(e.target.value)}
                      className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                    >
                      <option value="">반 선택</option>
                      {classes.map((c) => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                    <button
                      onClick={handleUpdateStudent}
                      disabled={actionLoading}
                      className="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600 disabled:opacity-50"
                    >
                      {actionLoading ? '저장 중...' : '저장'}
                    </button>
                  </div>
                </div>

                {/* 계정 관리 버튼들 */}
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={() => setShowPasswordModal(true)}
                    className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    비밀번호 초기화
                  </button>
                  <button
                    onClick={handleToggleActive}
                    disabled={actionLoading}
                    className="rounded-lg border border-yellow-300 bg-yellow-50 px-4 py-2 text-sm font-medium text-yellow-700 hover:bg-yellow-100 disabled:opacity-50"
                  >
                    계정 활성화/비활성화
                  </button>
                  <button
                    onClick={() => setShowResetHistoryModal(true)}
                    className="rounded-lg border border-red-300 bg-red-50 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-100"
                  >
                    테스트 기록 초기화
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* 비밀번호 초기화 모달 */}
        <AnimatePresence>
          {showPasswordModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
              onClick={() => setShowPasswordModal(false)}
            >
              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.95 }}
                onClick={(e) => e.stopPropagation()}
                className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl"
              >
                <h3 className="mb-4 text-lg font-semibold text-gray-900">비밀번호 초기화</h3>
                <input
                  type="text"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="새 비밀번호 (6자 이상)"
                  autoComplete="off"
                  className="mb-4 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                />
                <div className="flex justify-end gap-3">
                  <button
                    onClick={() => setShowPasswordModal(false)}
                    className="rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100"
                  >
                    취소
                  </button>
                  <button
                    onClick={handleResetPassword}
                    disabled={actionLoading || newPassword.length < 6}
                    className="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600 disabled:opacity-50"
                  >
                    {actionLoading ? '처리 중...' : '초기화'}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* 기록 초기화 확인 모달 */}
        <AnimatePresence>
          {showResetHistoryModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
              onClick={() => setShowResetHistoryModal(false)}
            >
              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.95 }}
                onClick={(e) => e.stopPropagation()}
                className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl"
              >
                <h3 className="mb-2 text-lg font-semibold text-gray-900">테스트 기록 초기화</h3>
                <p className="mb-4 text-sm text-gray-600">
                  이 작업은 되돌릴 수 없습니다. 학생의 모든 테스트 기록, 레벨, XP가 초기화됩니다.
                </p>
                <div className="flex justify-end gap-3">
                  <button
                    onClick={() => setShowResetHistoryModal(false)}
                    className="rounded-lg px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100"
                  >
                    취소
                  </button>
                  <button
                    onClick={handleResetHistory}
                    disabled={actionLoading}
                    className="rounded-lg bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600 disabled:opacity-50"
                  >
                    {actionLoading ? '처리 중...' : '초기화'}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* 핵심 지표 - 8개 카드 (2행 4열) */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4"
        >
          <StatCard label="총 테스트" value={`${data.total_tests}회`} />
          <StatCard label="정답률" value={`${data.accuracy_rate}%`} color={data.accuracy_rate >= 80 ? 'green' : data.accuracy_rate >= 60 ? 'yellow' : 'red'} />
          <StatCard label="평균 풀이 시간" value={`${(data.average_time_per_question ?? 0).toFixed(1)}초`} />
          <StatCard label="최대 스트릭" value={`${data.max_streak}일`} />
          <StatCard label="현재 레벨" value={`Lv.${data.level}`} color="purple" />
          <StatCard label="총 XP" value={`${data.total_xp.toLocaleString()} XP`} />
          <StatCard label="현재 스트릭" value={`${data.current_streak}일`} color={data.current_streak > 0 ? 'green' : undefined} />
          <StatCard label="오늘 풀이" value={`${data.today_solved}문제`} />
        </motion.div>

        {/* 단원 진행 상황 */}
        {data.chapter_progress && data.chapter_progress.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="mb-6 rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">단원 진행 상황</h2>
            <div className="space-y-3">
              {data.chapter_progress.map((chapter) => {
                const statusIcon = chapter.is_completed ? '✓' : chapter.is_unlocked ? '📖' : '🔒'
                const statusText = chapter.is_completed ? '완료' : chapter.is_unlocked ? '진행중' : '잠김'
                const statusColor = chapter.is_completed ? 'text-green-600' : chapter.is_unlocked ? 'text-blue-600' : 'text-gray-400'

                return (
                  <div key={chapter.chapter_id} className="flex items-center gap-3 rounded-lg border border-gray-200 p-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-sm font-medium ${statusColor}`}>{statusIcon}</span>
                        <span className="text-sm font-medium text-gray-800">
                          {chapter.chapter_name}
                        </span>
                        <span className={`text-xs ${statusColor}`}>({statusText})</span>
                      </div>
                      <div className="mt-2 flex items-center gap-2">
                        <div className="h-2 flex-1 overflow-hidden rounded-full bg-gray-200">
                          <div
                            className="h-full rounded-full bg-primary-500 transition-all"
                            style={{ width: `${chapter.overall_progress}%` }}
                          />
                        </div>
                        <span className="text-xs font-medium text-gray-600">{chapter.overall_progress}%</span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleToggleChapterLock(chapter.chapter_id, chapter.is_unlocked)}
                      disabled={chapterActionLoading === chapter.chapter_id}
                      className={`rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
                        chapter.is_unlocked
                          ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          : 'bg-green-100 text-green-700 hover:bg-green-200'
                      } disabled:opacity-50`}
                    >
                      {chapterActionLoading === chapter.chapter_id
                        ? '...'
                        : chapter.is_unlocked
                        ? '잠금'
                        : '해제'}
                    </button>
                  </div>
                )
              })}
            </div>
          </motion.div>
        )}

        {/* 트랙별 분석 */}
        {(data.computation_stats || data.concept_stats) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.17 }}
            className="mb-6 grid gap-4 md:grid-cols-2"
          >
            {/* 연산 트랙 */}
            {data.computation_stats && (
              <div className="rounded-2xl bg-white p-6 shadow-sm">
                <h2 className="mb-4 text-lg font-semibold text-gray-900">연산 트랙</h2>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">총 문제 수</span>
                    <span className="text-sm font-semibold text-gray-900">{data.computation_stats.total_questions}문제</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">정답 수</span>
                    <span className="text-sm font-semibold text-gray-900">{data.computation_stats.correct_answers}문제</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">정답률</span>
                    <span className={`text-sm font-semibold ${
                      data.computation_stats.accuracy_rate >= 80 ? 'text-green-600' :
                      data.computation_stats.accuracy_rate >= 60 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {data.computation_stats.accuracy_rate}%
                    </span>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-gray-200">
                    <div
                      className="h-full rounded-full bg-blue-500 transition-all"
                      style={{ width: `${data.computation_stats.accuracy_rate}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* 개념 트랙 */}
            {data.concept_stats && (
              <div className="rounded-2xl bg-white p-6 shadow-sm">
                <h2 className="mb-4 text-lg font-semibold text-gray-900">개념 트랙</h2>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">총 문제 수</span>
                    <span className="text-sm font-semibold text-gray-900">{data.concept_stats.total_questions}문제</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">정답 수</span>
                    <span className="text-sm font-semibold text-gray-900">{data.concept_stats.correct_answers}문제</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">정답률</span>
                    <span className={`text-sm font-semibold ${
                      data.concept_stats.accuracy_rate >= 80 ? 'text-green-600' :
                      data.concept_stats.accuracy_rate >= 60 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {data.concept_stats.accuracy_rate}%
                    </span>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-gray-200">
                    <div
                      className="h-full rounded-full bg-purple-500 transition-all"
                      style={{ width: `${data.concept_stats.accuracy_rate}%` }}
                    />
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}

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

        {/* 일일 활동 */}
        {data.daily_activity && data.daily_activity.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.27 }}
            className="mt-6 rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">일일 활동 (최근 7일)</h2>
            <div className="grid grid-cols-7 gap-2">
              {data.daily_activity.map((day) => {
                const date = new Date(day.date)
                const accuracyColor = day.accuracy_rate >= 80 ? 'bg-green-100 text-green-700' :
                                     day.accuracy_rate >= 60 ? 'bg-yellow-100 text-yellow-700' :
                                     day.questions_answered > 0 ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-500'

                return (
                  <div key={day.date} className={`rounded-lg p-3 text-center ${accuracyColor}`}>
                    <div className="text-xs font-medium">
                      {date.getMonth() + 1}/{date.getDate()}
                    </div>
                    <div className="mt-1 text-lg font-bold">
                      {day.questions_answered}
                    </div>
                    <div className="text-xs">
                      {day.questions_answered > 0 ? `${day.accuracy_rate}%` : '-'}
                    </div>
                  </div>
                )
              })}
            </div>
          </motion.div>
        )}

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
  const colorClass = color === 'green' ? 'text-green-600' :
                     color === 'red' ? 'text-red-600' :
                     color === 'yellow' ? 'text-yellow-600' :
                     color === 'purple' ? 'text-purple-600' : 'text-gray-900'
  return (
    <div className="rounded-xl bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className={`text-2xl font-bold ${colorClass}`}>{value}</p>
    </div>
  )
}
