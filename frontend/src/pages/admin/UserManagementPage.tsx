// 계정 관리 페이지 (관리자/마스터 전용)

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../../lib/api'
import { useAuthStore } from '../../store/authStore'
import type { UserRole, Grade, PaginatedResponse } from '../../types'

interface UserListItem {
  id: string
  login_id: string
  name: string
  role: UserRole
  grade?: Grade
  class_id?: string
  created_at: string
}

const ROLE_CONFIG: Record<UserRole, { label: string; color: string }> = {
  master: { label: '마스터', color: 'bg-red-100 text-red-700' },
  admin: { label: '관리자', color: 'bg-orange-100 text-orange-700' },
  teacher: { label: '강사', color: 'bg-blue-100 text-blue-700' },
  student: { label: '학생', color: 'bg-green-100 text-green-700' },
}

const GRADE_OPTIONS: { value: Grade; label: string; disabled?: boolean }[] = [
  { value: 'elementary_1', label: '초등 1학년', disabled: true },
  { value: 'elementary_2', label: '초등 2학년', disabled: true },
  { value: 'elementary_3', label: '초등 3학년' },
  { value: 'elementary_4', label: '초등 4학년' },
  { value: 'elementary_5', label: '초등 5학년' },
  { value: 'elementary_6', label: '초등 6학년' },
  { value: 'middle_1', label: '중등 1학년' },
  { value: 'middle_2', label: '중등 2학년' },
  { value: 'middle_3', label: '중등 3학년' },
  { value: 'high_1', label: '고등 1학년' },
]

export function UserManagementPage() {
  const { user: currentUser, logout } = useAuthStore()
  const [users, setUsers] = useState<UserListItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [roleFilter, setRoleFilter] = useState<UserRole | ''>('')
  const [searchQuery, setSearchQuery] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingUser, setEditingUser] = useState<UserListItem | null>(null)
  const [isResetting, setIsResetting] = useState(false)
  const [isUpdatingChapters, setIsUpdatingChapters] = useState(false)
  const [adminMessage, setAdminMessage] = useState('')

  useEffect(() => {
    fetchUsers()
  }, [roleFilter])

  const fetchUsers = async () => {
    try {
      setIsLoading(true)
      setError('')

      const params = new URLSearchParams()
      if (roleFilter) {
        params.append('role', roleFilter)
      }

      const response = await api.get<{ success: boolean; data: PaginatedResponse<UserListItem> }>(
        `/api/v1/admin/users?${params}`
      )

      setUsers(response.data.data.items)
    } catch {
      setError('사용자 목록을 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const filteredUsers = users.filter((u) =>
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.login_id.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getCreatableRoles = (): { value: UserRole; label: string }[] => {
    if (currentUser?.role === 'master') {
      return [
        { value: 'admin', label: '관리자' },
        { value: 'teacher', label: '강사' },
        { value: 'student', label: '학생' },
      ]
    }
    if (currentUser?.role === 'admin') {
      return [
        { value: 'teacher', label: '강사' },
        { value: 'student', label: '학생' },
      ]
    }
    return []
  }

  const formatDate = (dateStr: string): string => {
    return new Date(dateStr).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const handleResetDB = async () => {
    if (!confirm('정말 DB를 완전 초기화하시겠습니까?\n\n모든 사용자/테스트 기록이 삭제되고 시드 데이터가 재생성됩니다.\n이 작업은 되돌릴 수 없습니다.')) return
    if (!confirm('마지막 확인: 진짜 초기화할까요?')) return

    setIsResetting(true)
    setAdminMessage('')
    try {
      const res = await api.post<{ success: boolean; message: string }>('/api/v1/admin/reset-db')
      setAdminMessage(res.data.message || 'DB 초기화 완료!')
      // DB 초기화 후 로그아웃 (세션 무효화됨)
      setTimeout(() => {
        logout()
        window.location.href = '/login'
      }, 2000)
    } catch {
      setAdminMessage('DB 초기화 실패. 서버 로그를 확인하세요.')
    } finally {
      setIsResetting(false)
    }
  }

  const handleUpdateChapters = async () => {
    setIsUpdatingChapters(true)
    setAdminMessage('')
    try {
      const res = await api.post<{ success: boolean; message: string; data: { updated_chapters: number } }>('/api/v1/admin/update-chapters')
      setAdminMessage(res.data.message || `${res.data.data.updated_chapters}개 챕터 업데이트`)
    } catch {
      setAdminMessage('챕터 업데이트 실패.')
    } finally {
      setIsUpdatingChapters(false)
    }
  }

  if (isLoading && users.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">사용자 목록을 불러오는 중...</p>
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
          className="mb-8 flex items-center justify-between"
        >
          <div>
            <h1 className="text-2xl font-bold text-gray-900">계정 관리</h1>
            <p className="text-gray-600">사용자 계정을 관리하고 새 계정을 생성하세요</p>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setShowCreateModal(true)}
            className="rounded-xl bg-primary-500 px-5 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-primary-600"
          >
            + 새 계정 만들기
          </motion.button>
        </motion.div>

        {/* DB 관리 (마스터/관리자) */}
        {(currentUser?.role === 'master' || currentUser?.role === 'admin') && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4"
          >
            <h3 className="mb-3 text-sm font-semibold text-red-800">DB 관리</h3>
            {adminMessage && (
              <div className="mb-3 rounded-lg bg-white p-3 text-sm text-gray-700">
                {adminMessage}
              </div>
            )}
            <div className="flex flex-wrap gap-3">
              <button
                onClick={handleUpdateChapters}
                disabled={isUpdatingChapters}
                className="rounded-lg bg-orange-500 px-4 py-2 text-sm font-medium text-white hover:bg-orange-600 disabled:opacity-50"
              >
                {isUpdatingChapters ? '업데이트 중...' : '챕터 concept_ids 업데이트'}
              </button>
              {currentUser?.role === 'master' && (
                <button
                  onClick={handleResetDB}
                  disabled={isResetting}
                  className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
                >
                  {isResetting ? '초기화 중...' : 'DB 전체 초기화 (위험)'}
                </button>
              )}
            </div>
            <p className="mt-2 text-xs text-red-600">
              챕터 업데이트: concept_ids만 갱신 (안전) | DB 초기화: 모든 데이터 삭제 후 재생성
            </p>
          </motion.div>
        )}

        {/* 필터 & 검색 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex gap-4">
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value as UserRole | '')}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="">전체 역할</option>
              <option value="master">마스터</option>
              <option value="admin">관리자</option>
              <option value="teacher">강사</option>
              <option value="student">학생</option>
            </select>
          </div>

          <div className="relative">
            <input
              type="text"
              placeholder="이름 또는 아이디로 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 sm:w-72"
            />
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              🔍
            </span>
          </div>
        </motion.div>

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 p-4 text-red-600">{error}</div>
        )}

        {/* 사용자 목록 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="overflow-hidden rounded-2xl bg-white shadow-sm"
        >
          {filteredUsers.length === 0 ? (
            <div className="p-8 text-center">
              <div className="mb-4 text-5xl">👤</div>
              <h2 className="mb-2 text-xl font-semibold text-gray-900">
                {searchQuery ? '검색 결과 없음' : '사용자 없음'}
              </h2>
              <p className="text-gray-600">
                {searchQuery ? '검색 결과가 없습니다.' : '등록된 사용자가 없습니다.'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-600">이름</th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-600">아이디</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">역할</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">학년</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">가입일</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-600">관리</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredUsers.map((user, index) => (
                    <motion.tr
                      key={user.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.03 }}
                      className="hover:bg-gray-50"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white font-medium">
                            {user.name.charAt(0)}
                          </div>
                          <span className="font-medium text-gray-900">{user.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-gray-600">{user.login_id}</td>
                      <td className="px-6 py-4 text-center">
                        <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${ROLE_CONFIG[user.role].color}`}>
                          {ROLE_CONFIG[user.role].label}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center text-gray-600">
                        {user.grade
                          ? GRADE_OPTIONS.find((g) => g.value === user.grade)?.label.replace(/\s\d학년/, '') || '-'
                          : '-'}
                      </td>
                      <td className="px-6 py-4 text-center text-sm text-gray-500">
                        {formatDate(user.created_at)}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={() => setEditingUser(user)}
                          className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-200"
                        >
                          편집
                        </button>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>

        <div className="mt-4 text-center text-sm text-gray-500">
          총 {filteredUsers.length}명
        </div>
      </div>

      {/* 계정 생성 모달 */}
      <AnimatePresence>
        {showCreateModal && (
          <CreateUserModal
            creatableRoles={getCreatableRoles()}
            onClose={() => setShowCreateModal(false)}
            onCreated={() => {
              setShowCreateModal(false)
              fetchUsers()
            }}
          />
        )}
      </AnimatePresence>

      {/* 계정 편집 모달 */}
      <AnimatePresence>
        {editingUser && (
          <EditUserModal
            user={editingUser}
            creatableRoles={getCreatableRoles()}
            onClose={() => setEditingUser(null)}
            onUpdated={() => {
              setEditingUser(null)
              fetchUsers()
            }}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

// 계정 생성 모달
interface CreateUserModalProps {
  creatableRoles: { value: UserRole; label: string }[]
  onClose: () => void
  onCreated: () => void
}

function CreateUserModal({ creatableRoles, onClose, onCreated }: CreateUserModalProps) {
  const [name, setName] = useState('')
  const [loginId, setLoginId] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<UserRole>(creatableRoles[0]?.value || 'student')
  const [grade, setGrade] = useState<Grade | ''>('')
  const [classId, setClassId] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError('')

    try {
      await api.post('/api/v1/auth/register', {
        name,
        login_id: loginId,
        password,
        role,
        ...(role === 'student' && grade ? { grade } : {}),
        ...(role === 'student' && classId ? { class_id: classId } : {}),
      })
      onCreated()
    } catch {
      setError('계정 생성에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      {/* 오버레이 */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="fixed inset-0 z-50 bg-black/50"
      />

      {/* 모달 */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
          <h2 className="mb-6 text-xl font-bold text-gray-900">새 계정 만들기</h2>

          <form onSubmit={handleSubmit} className="space-y-4" autoComplete="off">
            {error && (
              <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
            )}

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">이름</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="홍길동"
                required
                autoComplete="off"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">아이디</label>
              <input
                type="text"
                value={loginId}
                onChange={(e) => setLoginId(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="아이디를 입력하세요"
                required
                autoComplete="off"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">비밀번호</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="••••••••"
                required
                minLength={6}
                autoComplete="new-password"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">역할</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as UserRole)}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                {creatableRoles.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
              </select>
            </div>

            {role === 'student' && (
              <>
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">학년</label>
                  <select
                    value={grade}
                    onChange={(e) => setGrade(e.target.value as Grade | '')}
                    className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    <option value="">선택하세요</option>
                    {GRADE_OPTIONS.map((g) => (
                      <option key={g.value} value={g.value} disabled={g.disabled}>
                        {g.label}{g.disabled ? ' (준비중)' : ''}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">반 (선택)</label>
                  <input
                    type="text"
                    value={classId}
                    onChange={(e) => setClassId(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                    placeholder="예: 1반"
                  />
                </div>
              </>
            )}

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 rounded-xl border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                취소
              </button>
              <motion.button
                type="submit"
                disabled={isSubmitting}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 rounded-xl bg-primary-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-primary-600 disabled:opacity-50"
              >
                {isSubmitting ? '생성 중...' : '계정 생성'}
              </motion.button>
            </div>
          </form>
        </div>
      </motion.div>
    </>
  )
}

// 계정 편집 모달
interface EditUserModalProps {
  user: UserListItem
  creatableRoles: { value: UserRole; label: string }[]
  onClose: () => void
  onUpdated: () => void
}

function EditUserModal({ user, creatableRoles, onClose, onUpdated }: EditUserModalProps) {
  const [name, setName] = useState(user.name)
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<UserRole>(user.role)
  const [grade, setGrade] = useState<Grade | ''>(user.grade || '')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError('')
    setSuccess('')

    try {
      const payload: Record<string, unknown> = {}
      if (name !== user.name) payload.name = name
      if (role !== user.role) payload.role = role
      if (password) payload.password = password
      if (role === 'student' && grade && grade !== user.grade) payload.grade = grade

      if (Object.keys(payload).length === 0) {
        setError('변경된 내용이 없습니다.')
        setIsSubmitting(false)
        return
      }

      await api.put(`/api/v1/admin/users/${user.id}`, payload)
      setSuccess('수정 완료!')
      setTimeout(() => onUpdated(), 800)
    } catch {
      setError('계정 수정에 실패했습니다.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="fixed inset-0 z-50 bg-black/50"
      />

      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
          <h2 className="mb-6 text-xl font-bold text-gray-900">계정 수정</h2>
          <p className="mb-4 text-sm text-gray-500">아이디: {user.login_id}</p>

          <form onSubmit={handleSubmit} className="space-y-4" autoComplete="off">
            {error && (
              <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
            )}
            {success && (
              <div className="rounded-lg bg-green-50 p-3 text-sm text-green-600">{success}</div>
            )}

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">이름</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                required
                autoComplete="off"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                비밀번호 변경 <span className="text-gray-400">(빈칸이면 유지)</span>
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                placeholder="새 비밀번호"
                minLength={6}
                autoComplete="new-password"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">역할</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as UserRole)}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                {creatableRoles.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
                {/* 현재 역할이 목록에 없으면 표시 */}
                {!creatableRoles.find((r) => r.value === user.role) && (
                  <option value={user.role}>
                    {ROLE_CONFIG[user.role]?.label || user.role}
                  </option>
                )}
              </select>
            </div>

            {role === 'student' && (
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">학년</label>
                <select
                  value={grade}
                  onChange={(e) => setGrade(e.target.value as Grade | '')}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="">선택하세요</option>
                  {GRADE_OPTIONS.map((g) => (
                    <option key={g.value} value={g.value} disabled={g.disabled}>
                      {g.label}{g.disabled ? ' (준비중)' : ''}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 rounded-xl border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                취소
              </button>
              <motion.button
                type="submit"
                disabled={isSubmitting}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex-1 rounded-xl bg-primary-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-primary-600 disabled:opacity-50"
              >
                {isSubmitting ? '수정 중...' : '수정 완료'}
              </motion.button>
            </div>
          </form>
        </div>
      </motion.div>
    </>
  )
}
