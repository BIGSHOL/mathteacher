import { useState, useEffect } from 'react'
import api from '../../lib/api'

interface Mission {
    id: string
    type: string
    title: string
    target_count: number
    current_count: number
    is_completed: boolean
    is_claimed: boolean
    reward_xp: number
}

export function MissionWidget() {
    const [missions, setMissions] = useState<Mission[]>([])
    const [loading, setLoading] = useState(true)

    const fetchMissions = async () => {
        try {
            const { data } = await api.get('/missions/')
            setMissions(data.data)
        } catch (error) {
            console.error('Failed to fetch missions:', error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchMissions()
    }, [])

    const handleClaim = async (mission: Mission) => {
        if (!mission.is_completed || mission.is_claimed) return

        try {
            await api.post(`/missions/${mission.id}/claim`)
            // 로컬 상태 업데이트
            setMissions(prev =>
                prev.map(m =>
                    m.id === mission.id ? { ...m, is_claimed: true } : m
                )
            )
            // TODO: 전역 XP 상태 업데이트 (AuthStore 등) - 여기선 생략하고 새로고침 유도 or Toast
            // 간단한 알림
            alert(`${mission.reward_xp} XP를 획득했습니다!`)
            window.location.reload() // XP 갱신을 위해 리로드 (임시)
        } catch (error) {
            console.error('Failed to claim reward:', error)
        }
    }

    if (loading) return <div className="animate-pulse h-40 bg-gray-100 rounded-xl" />

    return (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                    📅 오늘의 미션
                </h2>
                <span className="text-sm text-gray-500">
                    매일 자정 초기화
                </span>
            </div>

            <div className="space-y-3">
                {missions.map(mission => (
                    <div
                        key={mission.id}
                        className={`relative flex items-center justify-between p-4 rounded-xl border transition-all ${mission.is_completed
                            ? mission.is_claimed
                                ? 'bg-gray-50 border-gray-100 opacity-60'
                                : 'bg-primary-50 border-primary-100 shadow-sm'
                            : 'bg-white border-gray-100'
                            }`}
                    >
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="font-medium text-gray-900">
                                    {mission.title}
                                </span>
                                {mission.is_completed && !mission.is_claimed && (
                                    <span className="px-2 py-0.5 text-xs font-bold text-primary-600 bg-white rounded-full border border-primary-100">
                                        완료!
                                    </span>
                                )}
                            </div>
                            <div className="flex items-center gap-2 text-xs text-gray-500">
                                <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden max-w-[100px]">
                                    <div
                                        className={`h-full rounded-full ${mission.is_completed ? 'bg-primary-500' : 'bg-gray-300'
                                            }`}
                                        style={{
                                            width: `${Math.min(
                                                (mission.current_count / mission.target_count) * 100,
                                                100
                                            )}%`,
                                        }}
                                    />
                                </div>
                                <span>
                                    {mission.current_count}/{mission.target_count}
                                </span>
                            </div>
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="text-sm font-bold text-amber-500">
                                +{mission.reward_xp} XP
                            </span>
                            <button
                                onClick={() => handleClaim(mission)}
                                disabled={!mission.is_completed || mission.is_claimed}
                                className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${mission.is_claimed
                                    ? 'bg-gray-100 text-gray-400 cursor-default'
                                    : mission.is_completed
                                        ? 'bg-primary-500 text-white hover:bg-primary-600 shadow-md animate-bounce-sm'
                                        : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                    }`}
                            >
                                {mission.is_claimed ? '수령완료' : '받기'}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
