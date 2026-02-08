import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { fireAchievement } from '../../utils/confetti'
import { AchievementEarned } from '../../types'

interface AchievementToastProps {
    achievements: AchievementEarned[]
    onComplete?: () => void
}

export function AchievementToast({ achievements, onComplete }: AchievementToastProps) {
    const [currentIndex, setCurrentIndex] = useState(0)
    const [isVisible, setIsVisible] = useState(false)

    useEffect(() => {
        if (achievements.length > 0) {
            // showNext 로직을 useEffect 내부로 이동하거나 의존성 해결
            // 여기서는 간단히 초기화 로직만 수행
            setCurrentIndex(0)
        }
    }, [achievements])

    useEffect(() => {
        if (currentIndex < achievements.length) {
            setIsVisible(true)

            // 토스트 표시 시점에 폭죽 발사
            fireAchievement()

            const timer1 = setTimeout(() => {
                setIsVisible(false)
            }, 3000)

            const timer2 = setTimeout(() => {
                setCurrentIndex(prev => {
                    const next = prev + 1
                    if (next >= achievements.length && onComplete) {
                        onComplete()
                    }
                    return next
                })
            }, 3500)

            return () => {
                clearTimeout(timer1)
                clearTimeout(timer2)
            }
        }
    }, [currentIndex, achievements, onComplete])

    const currentAchievement = achievements[currentIndex]

    if (!currentAchievement) return null

    return (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    initial={{ opacity: 0, y: 50, scale: 0.8 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.5 } }}
                    className="fixed bottom-24 left-1/2 z-50 -translate-x-1/2 transform"
                >
                    <div className="flex w-80 flex-col items-center rounded-2xl bg-gradient-to-r from-yellow-400 to-orange-500 p-1 shadow-2xl">
                        <div className="flex w-full flex-col items-center rounded-xl bg-white p-4 text-center">
                            <div className="mb-2 text-4xl animate-bounce">{currentAchievement.icon}</div>
                            <h3 className="text-lg font-bold text-gray-900">업적 달성!</h3>
                            <div className="text-xl font-black text-orange-500 mb-1">{currentAchievement.name}</div>
                            <p className="text-sm text-gray-500">{currentAchievement.description}</p>
                        </div>
                    </div>
                    {/* Confetti effect local to toast could be added here if needed */}
                </motion.div>
            )}
        </AnimatePresence>
    )
}
