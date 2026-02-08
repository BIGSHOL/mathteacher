import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { MathText } from '../common/MathText'
import type { TestAttempt, AnswerLog, TestWithQuestions, Question } from '../../types'

interface GetAttemptResponse {
    attempt: TestAttempt
    answers: AnswerLog[]
    test: TestWithQuestions
}

interface StudentTestDetailModalProps {
    isOpen: boolean
    onClose: () => void
    attemptId: string | null
}

export function StudentTestDetailModal({ isOpen, onClose, attemptId }: StudentTestDetailModalProps) {
    const [data, setData] = useState<GetAttemptResponse | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (isOpen && attemptId) {
            fetchAttemptDetails(attemptId)
        } else {
            setData(null)
        }
    }, [isOpen, attemptId])

    const fetchAttemptDetails = async (id: string) => {
        try {
            setLoading(true)
            setError(null)
            const response = await axios.get<{ success: boolean; data: GetAttemptResponse }>(
                `/api/v1/tests/attempts/${id}`
            )
            if (response.data.success) {
                setData(response.data.data)
            } else {
                setError('데이터를 불러오는데 실패했습니다.')
            }
        } catch (err) {
            setError('서버 오류가 발생했습니다.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (!isOpen) return null

    return createPortal(
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
                    />
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4"
                    >
                        <div className="flex max-h-[90vh] w-full max-w-4xl flex-col overflow-hidden rounded-2xl bg-white shadow-xl">
                            {/* Header */}
                            <div className="flex items-center justify-between border-b border-gray-100 bg-white px-6 py-4">
                                <div>
                                    <h2 className="text-xl font-bold text-gray-900">
                                        {loading ? '로딩 중...' : data?.test.title || '테스트 상세 분석'}
                                    </h2>
                                    {!loading && data && (
                                        <div className="mt-1 flex items-center gap-3 text-sm text-gray-500">
                                            <span>{data.attempt.score}점 / {data.attempt.max_score}점</span>
                                            <span className="h-3 w-px bg-gray-300" />
                                            <span>{new Date(data.attempt.started_at).toLocaleDateString()} 응시</span>
                                        </div>
                                    )}
                                </div>
                                <button
                                    onClick={onClose}
                                    className="rounded-full p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
                                >
                                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>

                            {/* Content */}
                            <div className="flex-1 overflow-y-auto bg-gray-50 p-6">
                                {loading ? (
                                    <div className="flex h-64 items-center justify-center">
                                        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-primary-600" />
                                    </div>
                                ) : error ? (
                                    <div className="flex h-64 items-center justify-center text-red-500">
                                        {error}
                                    </div>
                                ) : data ? (
                                    <div className="space-y-6">
                                        {data.test.questions.map((question: Omit<Question, 'correct_answer'> & { correct_answer?: string }, index: number) => {
                                            const answerLog = data.answers.find((a) => a.question_id === question.id)
                                            const isCorrect = answerLog?.is_correct ?? false

                                            return (
                                                <div key={question.id} className={`rounded-xl border bg-white p-5 shadow-sm ${isCorrect ? 'border-gray-200' : 'border-red-200 ring-1 ring-red-50'
                                                    }`}>
                                                    {/* Question Info */}
                                                    <div className="mb-4 flex items-start gap-4">
                                                        <span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-bold ${isCorrect ? 'bg-primary-50 text-primary-700' : 'bg-red-50 text-red-700'
                                                            }`}>
                                                            Q{index + 1}
                                                        </span>
                                                        <div className="flex-1">
                                                            <div className="flex items-center gap-2 text-xs font-medium text-gray-500 mb-2">
                                                                <span className="rounded bg-gray-100 px-2 py-0.5">{question.part}</span>
                                                                {question.difficulty && <span>난이도 {question.difficulty}</span>}
                                                                {question.concept_name && <span>• {question.concept_name}</span>}
                                                            </div>
                                                            <div className="text-lg font-medium text-gray-900">
                                                                <MathText text={question.content} />
                                                            </div>
                                                        </div>
                                                        <div className={`shrink-0 rounded-full px-3 py-1 text-xs font-bold ${isCorrect ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                                            }`}>
                                                            {isCorrect ? '정답' : '오답'}
                                                        </div>
                                                    </div>

                                                    {/* Answer Area */}
                                                    <div className="grid gap-4 rounded-lg bg-gray-50 p-4 md:grid-cols-2">
                                                        <div>
                                                            <div className="mb-1 text-xs font-medium text-gray-500">학생 답안</div>
                                                            <div className={`font-mono font-medium ${isCorrect ? 'text-green-700' : 'text-red-700'}`}>
                                                                <MathText text={answerLog?.selected_answer || '-'} />
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <div className="mb-1 text-xs font-medium text-gray-500">정답</div>
                                                            <div className="font-mono font-medium text-primary-700">
                                                                <MathText text={question.correct_answer || '-'} />
                                                            </div>
                                                        </div>
                                                    </div>

                                                    {/* Explanation (if incorrect or requested) */}
                                                    {question.explanation && (
                                                        <div className="mt-4 border-t border-gray-100 pt-3">
                                                            <div className="mb-1 text-xs font-medium text-gray-500">해설</div>
                                                            <div className="text-sm text-gray-700">
                                                                <MathText text={question.explanation} />
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            )
                                        })}
                                    </div>
                                ) : null}
                            </div>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>,
        document.body
    )
}
