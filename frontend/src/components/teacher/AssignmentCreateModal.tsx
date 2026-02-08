import { useState } from 'react'

interface AssignmentCreateModalProps {
    isOpen: boolean
    onClose: () => void
    studentId: string
    onSuccess: () => void
}

export function AssignmentCreateModal({ isOpen, onClose, studentId, onSuccess }: AssignmentCreateModalProps) {
    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [type, setType] = useState<'chapter' | 'review' | 'custom'>('custom')
    const [dueDate, setDueDate] = useState<Date | null>(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!title.trim()) return

        setLoading(true)
        try {
            const response = await fetch('/api/v1/assignments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    student_id: studentId,
                    title,
                    description,
                    assignment_type: type,
                    due_date: dueDate ? dueDate.toISOString() : null,
                }),
            })

            if (!response.ok) throw new Error('Failed to create assignment')

            // Reset form
            setTitle('')
            setDescription('')
            setType('custom')
            setDueDate(null)

            onSuccess()
            onClose()
        } catch (error) {
            alert('과제 생성에 실패했습니다.')
        } finally {
            setLoading(false)
        }
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="fixed inset-0 bg-black/25" onClick={onClose} />

            <div className="relative z-10 w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 shadow-xl">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium leading-6 text-gray-900">
                        과제 부여
                    </h3>
                    <button
                        onClick={onClose}
                        className="rounded-full p-1 hover:bg-gray-100"
                    >
                        <svg className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="mt-4 space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            과제 유형
                        </label>
                        <select
                            value={type}
                            onChange={(e) => setType(e.target.value as 'chapter' | 'review' | 'custom')}
                            className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        >
                            <option value="custom">기타 (직접 입력)</option>
                            <option value="chapter">단원 학습</option>
                            <option value="review">오답 복습</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            제목 <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                            placeholder="예: 3단원 복습 및 문제풀이"
                            className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            설명 (선택)
                        </label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            rows={3}
                            placeholder="숙제에 대한 상세 설명을 입력하세요."
                            className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            기한 (선택)
                        </label>
                        <input
                            type="date"
                            value={dueDate ? dueDate.toISOString().split('T')[0] : ''}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDueDate(e.target.value ? new Date(e.target.value) : null)}
                            min={new Date().toISOString().split('T')[0]}
                            className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        />
                    </div>

                    <div className="mt-6 flex justify-end gap-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                        >
                            취소
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50"
                        >
                            {loading ? '생성 중...' : '생성'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
