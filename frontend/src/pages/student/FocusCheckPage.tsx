// 집중 체크 페이지 - 4회 이상 틀린 문제 복습

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import { MathText } from '../../components/common/MathText'
import { FocusCheckItem } from '../../types'

interface FocusCheckResponse {
    items: FocusCheckItem[]
    total: number
}

export function FocusCheckPage() {
    const navigate = useNavigate()
    const [items, setItems] = useState<FocusCheckItem[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState('')
    const [resolvingId, setResolvingId] = useState<string | null>(null)

    useEffect(() => {
        loadFocusCheckItems()
    }, [])

    const loadFocusCheckItems = async () => {
        try {
            setIsLoading(true)
            const response = await api.get<{ success: boolean; data: FocusCheckResponse }>(
                '/api/v1/students/me/focus-check'
            )
            setItems(response.data.data.items)
        } catch {
            setError('집중 체크 목록을 불러오는데 실패했습니다.')
        } finally {
            setIsLoading(false)
        }
    }

    const handleResolve = async (itemId: string) => {
        try {
            setResolvingId(itemId)
            await api.post(`/api/v1/students/me/focus-check/${itemId}/resolve`)
            setItems((prev) => prev.filter((item) => item.id !== itemId))
        } catch {
            alert('해결 처리에 실패했습니다.')
        } finally {
            setResolvingId(null)
        }
    }

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gray-50 py-6">
                <div className="container mx-auto px-4">
                    <div className="mb-6 flex items-center justify-between">
                        <div>
                            <div className="h-8 w-32 animate-pulse rounded bg-gray-200"></div>
                            <div className="mt-2 h-4 w-48 animate-pulse rounded bg-gray-200"></div>
                        </div>
                    </div>
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="rounded-xl bg-white p-6 shadow-sm">
                                <div className="h-20 animate-pulse rounded bg-gray-100"></div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 py-6">
            <div className="container mx-auto px-4">
                {/* 헤더 */}
                <div className="mb-6 flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">⚠️ 집중 체크</h1>
                        <p className="text-gray-600">4회 이상 틀린 문제들을 복습하세요</p>
                    </div>
                    <button
                        onClick={() => navigate(-1)}
                        className="rounded-lg bg-gray-100 px-4 py-2 text-gray-700 hover:bg-gray-200"
                    >
                        뒤로가기
                    </button>
                </div>

                {error && (
                    <div className="mb-4 rounded-lg bg-red-100 p-4 text-red-700">{error}</div>
                )}

                {/* 빈 상태 */}
                {items.length === 0 && !error && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="rounded-xl bg-white p-12 text-center shadow-sm"
                    >
                        <div className="mx-auto mb-4 text-6xl">🎉</div>
                        <h2 className="mb-2 text-xl font-bold text-gray-900">모든 문제를 해결했어요!</h2>
                        <p className="text-gray-600">집중 체크에 남은 문제가 없습니다.</p>
                    </motion.div>
                )}

                {/* 문제 목록 */}
                <div className="space-y-4">
                    <AnimatePresence>
                        {items.map((item) => (
                            <motion.div
                                key={item.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, x: -100 }}
                                className="rounded-xl bg-white p-6 shadow-sm"
                            >
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex-1">
                                        {/* 개념 배지 */}
                                        <div className="mb-2 flex items-center gap-2">
                                            <span className="rounded-full bg-orange-100 px-3 py-1 text-sm font-medium text-orange-700">
                                                {item.wrong_count}회 오답
                                            </span>
                                            {item.concept_name && (
                                                <span className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600">
                                                    {item.concept_name}
                                                </span>
                                            )}
                                        </div>

                                        {/* 문제 내용 */}
                                        <p className="text-gray-900">
                                            <MathText text={item.question_content} />
                                        </p>

                                        {/* 날짜 */}
                                        <p className="mt-2 text-xs text-gray-500">
                                            추가됨: {new Date(item.created_at).toLocaleDateString('ko-KR')}
                                        </p>
                                    </div>

                                    {/* 해결 버튼 */}
                                    <button
                                        onClick={() => handleResolve(item.id)}
                                        disabled={resolvingId === item.id}
                                        className="shrink-0 rounded-lg bg-emerald-500 px-4 py-2 text-white transition-colors hover:bg-emerald-600 disabled:opacity-50"
                                    >
                                        {resolvingId === item.id ? '처리 중...' : '✓ 해결'}
                                    </button>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    )
}
