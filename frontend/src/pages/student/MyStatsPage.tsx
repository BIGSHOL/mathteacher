// 학생 내 통계 페이지

import { useEffect, useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import api from '../../lib/api'
import { XpBar } from '../../components/gamification/XpBar'
import { useAuthStore } from '../../store/authStore'
import type { StudentStats, TrackStats, Grade, ChapterProgressItem } from '../../types'

/** 레벨별 아이콘 & 칭호 (15레벨 체계) */
function getLevelMeta(level: number): { icon: string; title: string } {
  if (level <= 1) return { icon: '🌱', title: '새싹' }
  if (level <= 2) return { icon: '🌿', title: '성장' }
  if (level <= 3) return { icon: '🛡️', title: '수호자' }
  if (level <= 4) return { icon: '⚔️', title: '전사' }
  if (level <= 5) return { icon: '🔮', title: '마법사' }
  if (level <= 6) return { icon: '🦅', title: '독수리' }
  if (level <= 7) return { icon: '💎', title: '다이아' }
  if (level <= 8) return { icon: '🐉', title: '드래곤' }
  if (level <= 9) return { icon: '👑', title: '왕관' }
  if (level <= 10) return { icon: '🏆', title: '챔피언' }
  if (level <= 11) return { icon: '⚡', title: '번개' }
  if (level <= 12) return { icon: '🌟', title: '별빛' }
  if (level <= 13) return { icon: '🔱', title: '신화' }
  if (level <= 14) return { icon: '🌀', title: '초월' }
  return { icon: '💠', title: '전설' }
}

/**
 * 스트릭 불꽃 색상 테마
 * 기본(1~29일): 붉은 불꽃 (주황~빨강)
 * 히든 30일+: 파란 불꽃
 * 히든 100일+: 흰색 불꽃
 * 히든 300일+: 검은 불꽃
 */
function getFlameTheme(streak: number) {
  if (streak >= 300) return {
    hueBase: 270,       // 보라-검정 기조
    gradient: (hue: number) =>
      `linear-gradient(to top, hsl(${hue},30%,15%) 0%, hsl(${hue},40%,20%) 30%, hsl(280,50%,25%) 60%, rgba(40,0,60,0.3) 85%, transparent 100%)`,
    core: 'linear-gradient(to top, rgba(180,140,255,0.5) 0%, rgba(100,50,180,0.3) 40%, transparent 100%)',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(80,0,120,${g}) 0%, rgba(40,0,80,${g * 0.5}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #c4b5fd, #7c3aed)',
    sparkShadow: '0 0 3px 1px rgba(124,58,237,0.6)',
    label: '암흑',
  }
  if (streak >= 100) return {
    hueBase: 210,
    gradient: (hue: number) =>
      `linear-gradient(to top, hsl(${hue},10%,90%) 0%, hsl(${hue},15%,85%) 30%, hsl(220,20%,80%) 60%, rgba(220,220,240,0.3) 85%, transparent 100%)`,
    core: 'linear-gradient(to top, rgba(255,255,255,0.8) 0%, rgba(200,210,255,0.5) 40%, transparent 100%)',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(200,210,255,${g}) 0%, rgba(180,190,240,${g * 0.5}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #ffffff, #c7d2fe)',
    sparkShadow: '0 0 4px 2px rgba(200,210,255,0.8)',
    label: '백염',
  }
  if (streak >= 30) return {
    hueBase: 210,
    gradient: (hue: number) =>
      `linear-gradient(to top, hsl(${hue},100%,55%) 0%, hsl(${hue + 10},95%,50%) 30%, hsl(${hue + 20},90%,45%) 60%, rgba(0,100,255,0.3) 85%, transparent 100%)`,
    core: 'linear-gradient(to top, rgba(180,220,255,0.6) 0%, rgba(100,180,255,0.4) 40%, transparent 100%)',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(60,130,255,${g}) 0%, rgba(30,80,200,${g * 0.5}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #93c5fd, #3b82f6)',
    sparkShadow: '0 0 3px 1px rgba(59,130,246,0.6)',
    label: '청염',
  }
  return {
    hueBase: 20,
    gradient: (hue: number) =>
      `linear-gradient(to top, hsl(${hue},100%,55%) 0%, hsl(${hue + 15},100%,50%) 30%, hsl(${hue + 30},95%,45%) 60%, rgba(255,80,0,0.3) 85%, transparent 100%)`,
    core: 'linear-gradient(to top, #fff8 0%, #ffd54f88 40%, transparent 100%)',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(255,120,0,${g}) 0%, rgba(255,60,0,${g * 0.5}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #ffe082, #ff9800)',
    sparkShadow: '0 0 3px 1px rgba(255,150,0,0.6)',
    label: null,
  }
}

/**
 * 스트릭 불꽃 애니메이션 컴포넌트
 * streak 1~2: 약한 불씨 / 3~5: 중간 / 6~10: 강함 / 11+: 최대
 * 30일+: 파란 불꽃 / 100일+: 흰 불꽃 / 300일+: 검은 불꽃
 */
function StreakFire({ streak }: { streak: number }) {
  const intensity = streak <= 0 ? 0 : streak <= 2 ? 1 : streak <= 5 ? 2 : streak <= 10 ? 3 : 4
  const theme = getFlameTheme(streak)

  const config = useMemo(() => {
    switch (intensity) {
      case 0: return { flames: 0, size: 0, speed: 0, sparks: 0, glow: 0 }
      case 1: return { flames: 1, size: 24, speed: 2.5, sparks: 0, glow: 0 }
      case 2: return { flames: 3, size: 30, speed: 1.8, sparks: 2, glow: 0.15 }
      case 3: return { flames: 5, size: 36, speed: 1.2, sparks: 4, glow: 0.3 }
      case 4: return { flames: 7, size: 44, speed: 0.8, sparks: 7, glow: 0.5 }
      default: return { flames: 1, size: 24, speed: 2.5, sparks: 0, glow: 0 }
    }
  }, [intensity])

  const flameData = useMemo(() =>
    Array.from({ length: config.flames }, (_, i) => ({
      id: i,
      xOff: (i - (config.flames - 1) / 2) * (intensity <= 1 ? 0 : intensity <= 2 ? 6 : 5),
      heightRatio: i === Math.floor(config.flames / 2) ? 1 : 0.6 + Math.random() * 0.3,
      delay: i * 0.12,
      hue: theme.hueBase + (i % 3) * 10,
    })),
    [config.flames, intensity, theme.hueBase]
  )

  const sparkData = useMemo(() =>
    Array.from({ length: config.sparks }, (_, i) => ({
      id: i,
      x: -12 + Math.random() * 24,
      delay: i * 0.3 + Math.random() * 0.5,
      duration: 0.8 + Math.random() * 0.6,
      size: 2 + Math.random() * 2,
    })),
    [config.sparks]
  )

  if (intensity === 0) {
    return (
      <div className="flex items-center justify-center" style={{ width: 56, height: 56 }}>
        <div className="h-3 w-3 rounded-full bg-orange-300/40" />
      </div>
    )
  }

  const containerH = config.size + 20

  return (
    <div className="relative flex items-end justify-center" style={{ width: 60, height: containerH }}>
      {/* 히든 불꽃 라벨 */}
      {theme.label && (
        <motion.div
          className="absolute -top-1 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-full bg-white/20 px-1.5 py-0.5 text-[9px] font-bold backdrop-blur-sm"
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {theme.label}
        </motion.div>
      )}

      {/* 글로우 이펙트 */}
      {config.glow > 0 && (
        <motion.div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 rounded-full"
          style={{
            width: config.size * 1.5,
            height: config.size * 0.5,
            background: theme.glowColor(config.glow),
            filter: `blur(${2 + intensity * 2}px)`,
          }}
          animate={{ opacity: [0.6, 1, 0.6], scaleX: [0.9, 1.1, 0.9] }}
          transition={{ duration: config.speed * 0.8, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}

      {/* 불꽃 레이어 */}
      {flameData.map((f) => {
        const h = config.size * f.heightRatio
        const w = h * 0.55
        return (
          <motion.div
            key={f.id}
            className="absolute bottom-0"
            style={{
              left: `calc(50% + ${f.xOff}px)`,
              width: w,
              height: h,
              transform: 'translateX(-50%)',
              borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
              background: theme.gradient(f.hue),
              filter: `blur(${intensity <= 1 ? 1.5 : 1}px)`,
            }}
            animate={{
              scaleX: [1, intensity <= 1 ? 1.05 : 1.15, 0.9, 1],
              scaleY: [1, intensity <= 1 ? 1.03 : 1.12, 0.95, 1],
              x: [0, (f.id % 2 === 0 ? 2 : -2) * (intensity <= 1 ? 0.5 : 1), 0],
              rotate: [0, f.id % 2 === 0 ? 3 : -3, 0],
            }}
            transition={{
              duration: config.speed,
              repeat: Infinity,
              delay: f.delay,
              ease: 'easeInOut',
            }}
          />
        )
      })}

      {/* 중심 밝은 코어 */}
      <motion.div
        className="absolute bottom-0 left-1/2 -translate-x-1/2"
        style={{
          width: config.size * 0.3,
          height: config.size * 0.45,
          borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%',
          background: theme.core,
          filter: 'blur(2px)',
        }}
        animate={{
          scaleY: [1, 1.1, 0.95, 1],
          opacity: [0.7, 1, 0.7],
        }}
        transition={{ duration: config.speed * 0.7, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* 스파크 파티클 */}
      {sparkData.map((s) => (
        <motion.div
          key={`spark-${s.id}`}
          className="absolute rounded-full"
          style={{
            width: s.size,
            height: s.size,
            left: `calc(50% + ${s.x}px)`,
            bottom: config.size * 0.4,
            background: theme.sparkBg,
            boxShadow: theme.sparkShadow,
          }}
          animate={{
            y: [0, -(20 + intensity * 10), -(35 + intensity * 15)],
            x: [0, s.x > 0 ? 6 : -6, s.x > 0 ? 10 : -10],
            opacity: [1, 0.7, 0],
            scale: [1, 0.7, 0.3],
          }}
          transition={{
            duration: s.duration,
            repeat: Infinity,
            delay: s.delay,
            ease: 'easeOut',
          }}
        />
      ))}
    </div>
  )
}

const GRADE_LABELS: Record<Grade, string> = {
  elementary_1: '초등 1학년',
  elementary_2: '초등 2학년',
  elementary_3: '초등 3학년',
  elementary_4: '초등 4학년',
  elementary_5: '초등 5학년',
  elementary_6: '초등 6학년',
  middle_1: '중등 1학년',
  middle_2: '중등 2학년',
  middle_3: '중등 3학년',
  high_1: '고등 1학년',
  high_2: '고등 2학년',
}

export function MyStatsPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<StudentStats | null>(null)
  const [chapters, setChapters] = useState<ChapterProgressItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const gradeLabel = user?.grade ? GRADE_LABELS[user.grade] : null

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setIsLoading(true)
      setError('')

      const [statsRes, chaptersRes] = await Promise.all([
        api.get<{ success: boolean; data: StudentStats }>('/api/v1/stats/me'),
        api.get<{ success: boolean; data: ChapterProgressItem[] }>('/api/v1/chapters/progress').catch(() => null),
      ])
      setStats(statsRes.data.data)
      if (chaptersRes?.data?.data) {
        setChapters(chaptersRes.data.data)
      }
    } catch {
      setError('통계를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">통계를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error}</p>
          <button onClick={fetchStats} className="btn-primary px-4 py-2">
            다시 시도
          </button>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 text-4xl">📊</div>
          <p className="text-gray-600">아직 학습 기록이 없습니다.</p>
          <p className="text-sm text-gray-500">테스트를 풀면 통계가 표시됩니다.</p>
        </div>
      </div>
    )
  }

  const accuracyLabel =
    stats.accuracy_rate >= 80
      ? { text: '우수', badge: 'bg-white/20' }
      : stats.accuracy_rate >= 60
        ? { text: '보통', badge: 'bg-white/20' }
        : { text: '도전', badge: 'bg-white/20' }

  return (
    <div className="min-h-screen bg-gray-50 py-6 sm:py-8">
      <div className="container mx-auto max-w-6xl px-4 space-y-6">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3 mb-1">
            <span className="text-3xl">📊</span>
            <h1 className="text-3xl font-bold text-gray-900">내 학습 통계</h1>
            {gradeLabel && (
              <span className="rounded-full bg-primary-100 px-3 py-1 text-sm font-semibold text-primary-700">
                {gradeLabel}
              </span>
            )}
          </div>
          <p className="text-gray-500 ml-12">나의 학습 현황을 확인하고 성장해보세요</p>
        </motion.div>

        {/* 레벨 & 스트릭 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid gap-4 md:grid-cols-2"
        >
          {/* 레벨 카드 */}
          <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 via-purple-600 to-purple-700 p-6 text-white shadow-lg">
            {/* 레벨 아이콘 배경 */}
            <motion.div
              className="pointer-events-none absolute -right-4 -top-4 select-none opacity-15"
              animate={{ rotate: [0, 5, -5, 0], scale: [1, 1.05, 1] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              style={{ fontSize: 100 }}
            >
              {getLevelMeta(stats.level).icon}
            </motion.div>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium opacity-75">현재 레벨</span>
                  <span className="rounded-full bg-white/20 px-2 py-0.5 text-xs font-bold">
                    {getLevelMeta(stats.level).icon} {getLevelMeta(stats.level).title}
                  </span>
                </div>
                <p className="font-math text-5xl font-black mt-1">Lv.{stats.level}</p>
              </div>
              <div className="text-right">
                <span className="text-xs opacity-75">총 획득 XP</span>
                <p className="font-math text-2xl font-bold">{stats.total_xp.toLocaleString()}</p>
              </div>
            </div>
            <XpBar level={stats.level} totalXp={stats.total_xp} showLabel={false} />
          </div>

          {/* 스트릭 카드 */}
          <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 p-6 text-white shadow-lg">
            <div className="mb-3 flex items-center justify-between">
              <span className="text-sm font-medium opacity-75">연속 학습 스트릭</span>
              <StreakFire streak={stats.current_streak} />
            </div>
            <div className="mb-4">
              <p className="font-math text-5xl font-black">{stats.current_streak}</p>
              <p className="text-sm opacity-90 mt-1">일 연속 학습 중!</p>
            </div>
            <div className="flex items-center justify-between border-t border-white/20 pt-3 text-sm">
              <span className="opacity-75">최대 기록</span>
              <span className="font-math text-lg font-bold">{stats.max_streak}일</span>
            </div>
          </div>
        </motion.div>

        {/* 학습 통계 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="mb-4 text-lg font-semibold text-gray-900">학습 현황</h2>
          <div className="grid gap-4 grid-cols-2 lg:grid-cols-3">
            {/* 정답률 카드 - 강조 */}
            <div className="col-span-2 lg:col-span-1 lg:row-span-2 flex flex-col items-center justify-center rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 p-8 text-white shadow-lg text-center">
              <div className="text-5xl mb-3">🎯</div>
              <p className="text-sm font-medium opacity-75 mb-2">정답률</p>
              <p className="font-math text-6xl font-black mb-3">{stats.accuracy_rate}%</p>
              <span className={`inline-block px-4 py-1.5 ${accuracyLabel.badge} rounded-full text-sm font-medium`}>
                {accuracyLabel.text}
              </span>
            </div>

            <StatCard icon="📝" label="완료 테스트" value={stats.total_tests} suffix="개" />
            <StatCard icon="✏️" label="풀이 문제" value={stats.total_questions} suffix="문제" />
            <StatCard icon="✅" label="정답 수" value={stats.correct_answers} suffix="개" />
            <StatCard
              icon="⏱️"
              label="평균 풀이 시간"
              value={stats.average_time_per_question}
              suffix="초"
            />
          </div>
        </motion.div>

        {/* 트랙별 정답률 (연산 / 개념) */}
        {(stats.computation_stats || stats.concept_stats) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">트랙별 성적</h2>
            <div className="grid gap-4 grid-cols-2">
              {stats.computation_stats && (
                <TrackCard
                  icon="🧮"
                  label="연산"
                  stats={stats.computation_stats}
                  color="blue"
                />
              )}
              {stats.concept_stats && (
                <TrackCard
                  icon="📚"
                  label="개념"
                  stats={stats.concept_stats}
                  color="emerald"
                />
              )}
            </div>
          </motion.div>
        )}

        {/* 단원 진행 상황 */}
        {chapters.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.28 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">단원 진행 상황</h2>
            <div className="space-y-3">
              {chapters.map((ch) => (
                <ChapterRow key={ch.chapter_id} chapter={ch} />
              ))}
            </div>
          </motion.div>
        )}

        {/* 취약 개념 */}
        {stats.weak_concepts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              📚 더 연습이 필요한 개념
            </h2>
            <div className="space-y-3">
              {stats.weak_concepts.map((concept) => (
                <ConceptBar
                  key={concept.concept_id}
                  name={concept.concept_name}
                  accuracy={concept.accuracy_rate}
                  color="red"
                />
              ))}
            </div>
          </motion.div>
        )}

        {/* 강점 개념 */}
        {stats.strong_concepts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h2 className="mb-4 text-lg font-semibold text-gray-900">⭐ 잘하는 개념</h2>
            <div className="space-y-3">
              {stats.strong_concepts.map((concept) => (
                <ConceptBar
                  key={concept.concept_id}
                  name={concept.concept_name}
                  accuracy={concept.accuracy_rate}
                  color="green"
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

// 통계 카드 컴포넌트
interface StatCardProps {
  icon: string
  label: string
  value: number
  suffix: string
}

function StatCard({ icon, label, value, suffix }: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="mb-3 text-3xl">{icon}</div>
      <p className="mb-1 text-sm text-gray-600">{label}</p>
      <p className="font-math text-3xl font-bold tabular-nums text-gray-900">
        {value}
        <span className="ml-1 text-sm font-normal text-gray-500">{suffix}</span>
      </p>
    </div>
  )
}

// 개념 막대 컴포넌트
interface ConceptBarProps {
  name: string
  accuracy: number
  color: 'red' | 'green'
}

// 트랙별 통계 카드
interface TrackCardProps {
  icon: string
  label: string
  stats: TrackStats
  color: 'blue' | 'emerald'
}

function TrackCard({ icon, label, stats: trackStats, color }: TrackCardProps) {
  const gradients = {
    blue: 'from-blue-400 to-blue-600',
    emerald: 'from-emerald-400 to-emerald-600',
  }
  const bgColors = {
    blue: 'bg-blue-50',
    emerald: 'bg-emerald-50',
  }
  const textColors = {
    blue: 'text-blue-700',
    emerald: 'text-emerald-700',
  }

  return (
    <div className={`rounded-2xl ${bgColors[color]} p-5 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">{icon}</span>
        <span className={`font-semibold ${textColors[color]}`}>{label}</span>
      </div>
      <p className={`font-math text-4xl font-black ${textColors[color]} mb-2`}>
        {trackStats.accuracy_rate}%
      </p>
      <p className="text-sm text-gray-500 mb-3">
        {trackStats.correct_answers}/{trackStats.total_questions} 정답
      </p>
      <div className="h-2.5 overflow-hidden rounded-full bg-white/70 shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${trackStats.accuracy_rate}%` }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full bg-gradient-to-r ${gradients[color]}`}
        />
      </div>
    </div>
  )
}

function ConceptBar({ name, accuracy, color }: ConceptBarProps) {
  const bgColor = color === 'red' ? 'bg-red-50' : 'bg-green-50'
  const barColor =
    color === 'red'
      ? 'bg-gradient-to-r from-red-400 to-red-600'
      : 'bg-gradient-to-r from-green-400 to-green-600'
  const textColor = color === 'red' ? 'text-red-600' : 'text-green-600'

  return (
    <div className={`rounded-xl ${bgColor} p-5 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="mb-3 flex items-center justify-between">
        <span className="font-semibold text-gray-900">{name}</span>
        <span className={`font-math text-xl font-bold ${textColor}`}>{accuracy}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-white/70 shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${accuracy}%` }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full ${barColor}`}
        />
      </div>
    </div>
  )
}

// 단원 진행 상황 행
function ChapterRow({ chapter: ch }: { chapter: ChapterProgressItem }) {
  const isLocked = !ch.is_unlocked
  const progress = ch.overall_progress

  return (
    <div
      className={clsx(
        'rounded-xl p-4 shadow-sm transition-shadow hover:shadow-md',
        isLocked ? 'bg-gray-100 opacity-60' : ch.is_completed ? 'bg-green-50' : 'bg-white'
      )}
    >
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">
            {isLocked ? '🔒' : ch.is_completed ? '✅' : '📖'}
          </span>
          <span className={clsx('font-semibold', isLocked ? 'text-gray-400' : 'text-gray-900')}>
            {ch.name}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {ch.is_completed && ch.final_test_score != null && (
            <span className="text-xs font-medium text-green-600">
              최종 {ch.final_test_score}점
            </span>
          )}
          {ch.teacher_approved && (
            <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
              승인됨
            </span>
          )}
          {!isLocked && !ch.is_completed && (
            <span className="font-math text-sm font-bold text-primary-600">{progress}%</span>
          )}
        </div>
      </div>
      {!isLocked && (
        <div className="h-2.5 overflow-hidden rounded-full bg-gray-200">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className={clsx(
              'h-full rounded-full',
              ch.is_completed
                ? 'bg-gradient-to-r from-green-400 to-green-600'
                : 'bg-gradient-to-r from-primary-400 to-primary-600'
            )}
          />
        </div>
      )}
      {isLocked && (
        <p className="text-xs text-gray-400">이전 단원을 완료하면 해금됩니다</p>
      )}
    </div>
  )
}
