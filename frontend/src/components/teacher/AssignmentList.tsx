import { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { ko } from 'date-fns/locale'
import api from '../../lib/api'
import type { Assignment } from '../../types'

interface AssignmentListProps {
    studentId: string
    onRefresh?: () => void
}

export function AssignmentList({ studentId, onRefresh }: AssignmentListProps) {
    const [assignments, setAssignments] = useState<Assignment[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchAssignments()
    }, [studentId])

    const fetchAssignments = async () => {
        setLoading(true)
        setError(null)
        try {
            const res = await api.get<{ success: boolean; data: Assignment[] }>(
                `/api/v1/assignments/students/${studentId}`
            )
            setAssignments(res.data.data)
        } catch {
            setError('과제 목록을 불러오는데 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    const handleDelete = async (id: string) => {
        if (!confirm('정말 삭제하시겠습니까?')) return

        try {
            await api.delete(`/api/v1/assignments/${id}`)
            fetchAssignments()
            if (onRefresh) onRefresh()
        } catch {
            alert('과제 삭제에 실패했습니다.')
        }
    }

    if (loading) return <div className="text-center py-4">로딩 중...</div>
    if (error) return <div className="text-center py-4 text-red-500">{error}</div>

    if (assignments.length === 0) {
        return <div className="text-center py-8 text-gray-500">등록된 과제가 없습니다.</div>
    }

    return (
        <div className="space-y-3">
            {assignments.map((assignment) => (
                <div
                    key={assignment.id}
                    className={`flex items-start justify-between rounded-lg border p-4 transition-colors ${assignment.is_completed ? 'bg-green-50 border-green-100' : 'bg-white border-gray-100'
                        }`}
                >
                    <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                            <span
                                className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${assignment.assignment_type === 'chapter'
                                        ? 'bg-blue-100 text-blue-800'
                                        : assignment.assignment_type === 'review'
                                            ? 'bg-purple-100 text-purple-800'
                                            : 'bg-gray-100 text-gray-800'
                                    }`}
                            >
                                {assignment.assignment_type === 'chapter'
                                    ? '단원 학습'
                                    : assignment.assignment_type === 'review'
                                        ? '오답 복습'
                                        : '기타'}
                            </span>
                            <h4 className="font-semibold text-gray-900">{assignment.title}</h4>
                        </div>
                        {assignment.description && (
                            <p className="text-sm text-gray-600 mb-2">{assignment.description}</p>
                        )}
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                            <span className="flex items-center gap-1">
                                📅 생성일: {format(new Date(assignment.created_at), 'PPP', { locale: ko })}
                            </span>
                            {assignment.due_date && (
                                <span className="flex items-center gap-1 text-red-500">
                                    ⏰ 기한: {format(new Date(assignment.due_date), 'PPP', { locale: ko })}
                                </span>
                            )}
                        </div>
                    </div>

                    <div className="flex items-center gap-3 ml-4">
                        {assignment.is_completed ? (
                            <div className="text-center">
                                <svg className="h-6 w-6 text-green-500 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span className="text-xs text-green-600 font-medium">완료</span>
                            </div>
                        ) : (
                            <div className="text-center">
                                <svg className="h-6 w-6 text-gray-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span className="text-xs text-gray-400">미완료</span>
                            </div>
                        )}

                        <button
                            onClick={() => handleDelete(assignment.id)}
                            className="rounded-full p-1 text-gray-400 hover:bg-red-50 hover:text-red-500 transition-colors"
                            title="삭제"
                        >
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                        </button>
                    </div>
                </div>
            ))}
        </div>
    )
}
