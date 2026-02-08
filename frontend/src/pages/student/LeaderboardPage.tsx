import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import api from '../../lib/api'
import { RankingItem } from '../../types'
import { useAuthStore } from '../../store/authStore'

export function LeaderboardPage() {
    const { user } = useAuthStore()
    const [activeTab, setActiveTab] = useState<'all' | 'grade'>('all')
    const [rankings, setRankings] = useState<RankingItem[]>([])
    const [myRank, setMyRank] = useState<RankingItem | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchRankings()
    }, [activeTab])

    const fetchRankings = async () => {
        try {
            setIsLoading(true)
            const gradeParam = activeTab === 'grade' && user?.grade ? user.grade : undefined

            const [listRes, myRes] = await Promise.all([
                api.get<{ success: boolean; data: RankingItem[] }>('/api/v1/stats/ranking', {
                    params: { grade: gradeParam, limit: 50 }
                }),
                api.get<{ success: boolean; data: RankingItem | null }>('/api/v1/stats/ranking/me', {
                    params: { grade: gradeParam }
                })
            ])

            setRankings(listRes.data.data)
            setMyRank(myRes.data.data)
        } catch (err) {
            console.error('Failed to fetch rankings:', err)
        } finally {
            setIsLoading(false)
        }
    }

    const getMedal = (rank: number) => {
        if (rank === 1) return '🥇'
        if (rank === 2) return '🥈'
        if (rank === 3) return '🥉'
        return null
    }

    return (
        <div className="min-h-screen bg-gray-50 py-4 sm:py-8">
            <div className="container mx-auto max-w-2xl px-4">
                <div className="mb-6 text-center">
                    <h1 className="text-2xl font-bold text-gray-900">명예의 전당</h1>
                    <p className="text-gray-600 mt-1">학습 열정이 넘치는 학생들을 만나보세요!</p>
                </div>

                {/* 탭 */}
                <div className="mb-6 flex rounded-xl bg-white p-1 shadow-sm">
                    <button
                        onClick={() => setActiveTab('all')}
                        className={clsx(
                            'flex-1 rounded-lg py-2.5 text-sm font-semibold transition-all',
                            activeTab === 'all'
                                ? 'bg-primary-500 text-white shadow-md'
                                : 'text-gray-500 hover:bg-gray-50'
                        )}
                    >
                        전체 랭킹
                    </button>
                    <button
                        onClick={() => setActiveTab('grade')}
                        className={clsx(
                            'flex-1 rounded-lg py-2.5 text-sm font-semibold transition-all',
                            activeTab === 'grade'
                                ? 'bg-primary-500 text-white shadow-md'
                                : 'text-gray-500 hover:bg-gray-50'
                        )}
                        disabled={!user?.grade}
                    >
                        {user?.grade ? '우리 학년' : '학년 정보 없음'}
                    </button>
                </div>

                {/* 내 랭킹 (상단 고정) */}
                {myRank && (
                    <motion.div
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        className="mb-6 sticky top-4 z-10"
                    >
                        <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 p-4 text-white shadow-lg">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 text-xl font-bold backdrop-blur-sm">
                                        {myRank.rank}
                                    </div>
                                    <div>
                                        <div className="font-bold text-lg">나 ({myRank.name})</div>
                                        <div className="text-indigo-100 text-sm">Lv.{myRank.level}</div>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="text-2xl font-black font-math">{myRank.total_xp.toLocaleString()} XP</div>
                                    {activeTab === 'grade' && <div className="text-xs text-indigo-200">같은 학년 중</div>}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* 랭킹 리스트 */}
                <div className="rounded-2xl bg-white shadow-sm overflow-hidden">
                    {isLoading ? (
                        <div className="p-8 text-center text-gray-500">
                            <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
                            랭킹을 불러오는 중...
                        </div>
                    ) : rankings.length > 0 ? (
                        <div className="divide-y divide-gray-100">
                            {rankings.map((item, index) => (
                                <motion.div
                                    key={item.user_id}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    className={clsx(
                                        'flex items-center justify-between p-4 transition-colors',
                                        item.user_id === user?.id ? 'bg-primary-50' : 'hover:bg-gray-50'
                                    )}
                                >
                                    <div className="flex items-center gap-4">
                                        <div className={clsx(
                                            "flex h-8 w-8 items-center justify-center rounded-full font-bold",
                                            item.rank <= 3 ? "text-xl" : "bg-gray-100 text-gray-500 text-sm"
                                        )}>
                                            {getMedal(item.rank) || item.rank}
                                        </div>
                                        <div>
                                            <div className="font-medium text-gray-900 flex items-center gap-1.5">
                                                {item.name}
                                                {item.user_id === user?.id && <span className="text-[10px] bg-primary-100 text-primary-600 px-1.5 rounded-full">ME</span>}
                                            </div>
                                            <div className="text-xs text-gray-500">Lv.{item.level}</div>
                                        </div>
                                    </div>
                                    <div className="font-math font-bold text-gray-700">
                                        {item.total_xp.toLocaleString()} <span className="text-xs font-normal text-gray-400">XP</span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    ) : (
                        <div className="p-8 text-center text-gray-500">
                            아직 랭킹 정보가 없습니다.
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
