// 카운트다운 타이머 컴포넌트 - 원형 SVG + 시각적 압박

import { useEffect, useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

/** 남은 10초부터 재생되는 긴장감 사운드 (10초 길이) */
const timerSound = new Audio('/sounds/timer.mp3')
timerSound.volume = 0.5

interface CountdownTimerProps {
  /** 제한시간 (초) */
  totalSeconds: number
  /** 타이머 활성 여부 */
  isRunning: boolean
  /** 시간 초과 콜백 */
  onTimeUp: () => void
  /** 남은 시간 콜백 (초) */
  onTick?: (remaining: number) => void
}

const RADIUS = 28
const CIRCUMFERENCE = 2 * Math.PI * RADIUS
/** 사운드 시작 임계값 (초) */
const SOUND_THRESHOLD = 10

export function CountdownTimer({
  totalSeconds,
  isRunning,
  onTimeUp,
  onTick,
}: CountdownTimerProps) {
  const [remaining, setRemaining] = useState(totalSeconds)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const onTimeUpRef = useRef(onTimeUp)
  onTimeUpRef.current = onTimeUp
  const soundPlayingRef = useRef(false)

  // totalSeconds 변경 시 리셋
  useEffect(() => {
    setRemaining(totalSeconds)
    // 타이머 리셋 시 사운드도 정지
    timerSound.pause()
    timerSound.currentTime = 0
    soundPlayingRef.current = false
  }, [totalSeconds])

  useEffect(() => {
    if (!isRunning) {
      if (intervalRef.current) clearInterval(intervalRef.current)
      // 타이머 정지 시 사운드도 정지
      timerSound.pause()
      timerSound.currentTime = 0
      soundPlayingRef.current = false
      return
    }

    intervalRef.current = setInterval(() => {
      setRemaining((prev) => {
        const next = prev - 1
        if (next <= 0) {
          if (intervalRef.current) clearInterval(intervalRef.current)
          timerSound.pause()
          timerSound.currentTime = 0
          soundPlayingRef.current = false
          onTimeUpRef.current()
          return 0
        }
        return next
      })
    }, 1000)

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [isRunning])

  // 남은 시간 10초 이하 → 사운드 재생 시작
  useEffect(() => {
    if (remaining <= SOUND_THRESHOLD && remaining > 0 && isRunning && !soundPlayingRef.current) {
      timerSound.currentTime = 0
      timerSound.play().catch(() => {})
      soundPlayingRef.current = true
    }
  }, [remaining, isRunning])

  // 컴포넌트 언마운트 시 사운드 정리
  useEffect(() => {
    return () => {
      timerSound.pause()
      timerSound.currentTime = 0
      soundPlayingRef.current = false
    }
  }, [])

  useEffect(() => {
    onTick?.(remaining)
  }, [remaining])

  const progress = remaining / totalSeconds
  const strokeDashoffset = CIRCUMFERENCE * (1 - progress)

  // 색상: 초록(>50%) → 노랑(25~50%) → 빨강(<25%)
  const getColor = () => {
    if (progress > 0.5) return '#10b981'  // emerald-500
    if (progress > 0.25) return '#f59e0b' // amber-500
    return '#ef4444'                       // red-500
  }

  // 위험 단계
  const isDanger = progress <= 0.25
  const isCritical = remaining <= 3 && remaining > 0

  return (
    <div className="relative flex items-center">
      <motion.div
        animate={
          isDanger
            ? { scale: [1, 1.08, 1], transition: { repeat: Infinity, duration: 0.8 } }
            : { scale: 1 }
        }
        className="relative"
      >
        <svg width="64" height="64" viewBox="0 0 64 64">
          {/* 배경 원 */}
          <circle
            cx="32"
            cy="32"
            r={RADIUS}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="4"
          />
          {/* 진행 원 */}
          <circle
            cx="32"
            cy="32"
            r={RADIUS}
            fill="none"
            stroke={getColor()}
            strokeWidth="4"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={strokeDashoffset}
            transform="rotate(-90 32 32)"
            style={{ transition: 'stroke-dashoffset 0.3s linear, stroke 0.3s' }}
          />
        </svg>
        {/* 중앙 숫자 */}
        <div className="absolute inset-0 flex items-center justify-center">
          <AnimatePresence mode="wait">
            <motion.span
              key={remaining}
              initial={{ scale: 1.3, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              transition={{ duration: 0.15 }}
              className={`text-lg font-bold tabular-nums ${
                isDanger ? 'text-red-500' : progress <= 0.5 ? 'text-amber-600' : 'text-gray-700'
              }`}
            >
              {remaining}
            </motion.span>
          </AnimatePresence>
        </div>
      </motion.div>

      {/* 시간 초과 임박 경고 */}
      <AnimatePresence>
        {isCritical && (
          <motion.span
            initial={{ opacity: 0, x: -5 }}
            animate={{ opacity: [0.5, 1, 0.5], x: 0 }}
            exit={{ opacity: 0 }}
            transition={{ repeat: Infinity, duration: 0.5 }}
            className="ml-1 text-xs font-bold text-red-500"
          >
            급해!
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  )
}
