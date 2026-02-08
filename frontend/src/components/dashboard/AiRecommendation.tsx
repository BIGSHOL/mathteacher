import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import { Link } from 'react-router-dom'

interface Question {
    id: string
    content: string
    difficulty: string
    concept_id: string
}

interface Weakness {
    concept_id: string
    concept_name: string
    mastery_score: number
    reason: string
}

export function AiRecommendation() {
    const [questions, setQuestions] = useState<Question[]>([])
    const [weaknesses, setWeaknesses] = useState<Weakness[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const { data } = await api.get('/ai-learning/recommendations?count=3')
                setQuestions(data.data.questions)
                setWeaknesses(data.data.weaknesses)
            } catch (error) {
                console.error('Failed to fetch AI recommendations:', error)
            } finally {
                setLoading(false)
            }
        }

        fetchData()
    }, [])

    if (loading) return (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-full flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
        </div>
    )

    return (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-full flex flex-col relative overflow-hidden">
            {/* Background Decor */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-primary-50 rounded-full blur-3xl opacity-50 -mr-10 -mt-10 pointer-events-none" />

            <div className="flex justify-between items-center mb-6 relative z-10">
                <div>
                    <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                        🤖 AI 맞춤 추천
                        <span className="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full">BETA</span>
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">취약점을 분석하여 엄선했습니다.</p>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto pr-1 custom-scrollbar relative z-10">
                {weaknesses.length > 0 && (
                    <div className="mb-6 bg-red-50 rounded-xl p-4 border border-red-100">
                        <h3 className="text-sm font-bold text-red-800 mb-2 flex items-center gap-1">
                            ⚠️ 집중 보완 필요
                        </h3>
                        <div className="space-y-2">
                            {weaknesses.map((w) => (
                                <div key={w.concept_id} className="flex justify-between items-center text-sm">
                                    <span className="text-gray-700 font-medium">{w.concept_name}</span>
                                    <span className="text-red-600 font-bold">{w.mastery_score}점</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {questions.length > 0 ? (
                    <div className="space-y-3">
                        <h3 className="text-sm font-bold text-gray-700 mb-2">추천 문제</h3>
                        {questions.map((q, idx) => (
                            <motion.div
                                key={q.id}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className="group relative bg-gray-50 hover:bg-white border border-gray-100 hover:border-primary-200 rounded-xl p-4 transition-all hover:shadow-md cursor-pointer"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-xs font-bold text-primary-600 bg-primary-50 px-2 py-0.5 rounded">
                                        문제 {idx + 1}
                                    </span>
                                    <span className={`text-xs px-2 py-0.5 rounded font-medium ${q.difficulty === 'high' ? 'bg-red-100 text-red-600' :
                                        q.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                                            'bg-green-100 text-green-600'
                                        }`}>
                                        {q.difficulty === 'high' ? '상' : q.difficulty === 'medium' ? '중' : '하'}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-800 line-clamp-2 mb-2 font-medium">
                                    {q.content}
                                </p>
                                <div className="text-xs text-gray-400 group-hover:text-primary-500 transition-colors text-right">
                                    클릭해서 풀기 →
                                </div>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-8 text-gray-500 text-sm">
                        추천할 문제가 없습니다.<br />
                        먼저 테스트를 진행해보세요!
                    </div>
                )}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 relative z-10">
                <Link
                    to="/tests"
                    className="block w-full py-3 bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-700 hover:to-indigo-700 text-white rounded-xl font-bold text-center shadow-lg shadow-primary-200 transition-all active:scale-95"
                >
                    AI 트레이닝 시작하기 🚀
                </Link>
            </div>
        </div>
    )
}
