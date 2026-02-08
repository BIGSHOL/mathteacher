// 재도전 힌트 박스 컴포넌트

import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import type { RetryHint } from '../../types'

interface HintBoxProps {
    hint: RetryHint
    className?: string
}

/**
 * 재도전 시 보여주는 힌트 박스
 * - level 1: 관련 개념 힌트 (💡)
 * - level 2: 풀이 방향 힌트 (📖)
 * - level 3: 확장 힌트 (📚)
 */
export function HintBox({ hint, className }: HintBoxProps) {
    const getStyles = () => {
        switch (hint.level) {
            case 1:
                return {
                    bg: 'bg-blue-50 border-blue-200',
                    icon: '💡',
                    title: '관련 개념을 떠올려보세요',
                }
            case 2:
                return {
                    bg: 'bg-amber-50 border-amber-200',
                    icon: '📖',
                    title: '풀이 방향 힌트',
                }
            case 3:
            default:
                return {
                    bg: 'bg-purple-50 border-purple-200',
                    icon: '📚',
                    title: '추가 힌트',
                }
        }
    }

    const styles = getStyles()

    return (
        <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={clsx(
                'rounded-xl border-2 p-4',
                styles.bg,
                className
            )}
        >
            <div className="flex items-start gap-3">
                <span className="text-2xl">{styles.icon}</span>
                <div className="flex-1">
                    <p className="font-medium text-gray-800 mb-1">{styles.title}</p>
                    <p className="text-gray-700 text-sm">{hint.message}</p>
                </div>
            </div>
        </motion.div>
    )
}

interface FocusCheckAlertProps {
    message: string
    className?: string
}

/**
 * 집중 체크 이동 알림
 */
export function FocusCheckAlert({ message, className }: FocusCheckAlertProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={clsx(
                'rounded-xl border-2 border-orange-300 bg-orange-50 p-4',
                className
            )}
        >
            <div className="flex items-center gap-3">
                <span className="text-2xl">⚠️</span>
                <div>
                    <p className="font-medium text-orange-800">집중 체크에 추가됨</p>
                    <p className="text-sm text-orange-700">{message}</p>
                </div>
            </div>
        </motion.div>
    )
}

interface RetryBadgeProps {
    retryCount: number
    retryQueueCount: number
}

/**
 * 재도전 상태 뱃지 (남은 재도전 문제 수 표시)
 */
export function RetryBadge({ retryCount, retryQueueCount }: RetryBadgeProps) {
    if (retryQueueCount === 0) return null

    return (
        <div className="flex items-center gap-2 text-sm">
            <span className="rounded-full bg-amber-100 px-3 py-1 text-amber-700 font-medium">
                🔄 재도전 {retryQueueCount}문제
            </span>
            {retryCount > 0 && (
                <span className="text-gray-500">
                    (이 문제 {retryCount}회 오답)
                </span>
            )}
        </div>
    )
}
