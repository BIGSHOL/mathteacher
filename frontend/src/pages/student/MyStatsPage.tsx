// 학생 내 통계 페이지

import { useEffect, useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import api from '../../lib/api'
import { XpBar } from '../../components/gamification/XpBar'
import { useAuthStore } from '../../store/authStore'
import type { StudentStats, TrackStats, Grade, ChapterProgressItem, DailyActivityItem, RecentTestItem } from '../../types'

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
    hueBase: 270,
    flameStops: (hue: number) => [
      { off: '0%', color: `hsl(${hue}, 40%, 18%)` },
      { off: '30%', color: `hsl(${hue + 5}, 50%, 22%)` },
      { off: '55%', color: `hsl(280, 55%, 28%)` },
      { off: '80%', color: `hsl(285, 45%, 22%)`, opacity: 0.8 },
      { off: '100%', color: `hsl(290, 35%, 15%)`, opacity: 0.2 },
    ],
    coreBottom: '#b48cff', coreMid: '#7c3aed', coreTop: '#4c1d95',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(100,0,150,${g}) 0%, rgba(60,0,100,${g * 0.6}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #ddd6fe, #7c3aed)',
    sparkShadow: '0 0 4px 2px rgba(124,58,237,0.7)',
    label: '암흑',
  }
  if (streak >= 100) return {
    hueBase: 220,
    flameStops: (hue: number) => [
      { off: '0%', color: `hsl(${hue}, 20%, 94%)` },
      { off: '30%', color: `hsl(${hue}, 25%, 90%)` },
      { off: '55%', color: `hsl(220, 30%, 86%)` },
      { off: '80%', color: `hsl(230, 25%, 80%)`, opacity: 0.85 },
      { off: '100%', color: `hsl(240, 20%, 72%)`, opacity: 0.2 },
    ],
    coreBottom: '#ffffff', coreMid: '#e0e7ff', coreTop: '#c7d2fe',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(220,225,255,${g}) 0%, rgba(200,205,250,${g * 0.6}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #ffffff, #e0e7ff)',
    sparkShadow: '0 0 5px 2px rgba(220,225,255,0.9)',
    label: '백염',
  }
  if (streak >= 30) return {
    hueBase: 210,
    flameStops: (hue: number) => [
      { off: '0%', color: `hsl(${hue}, 100%, 58%)` },
      { off: '30%', color: `hsl(${hue + 10}, 100%, 52%)` },
      { off: '55%', color: `hsl(${hue + 20}, 95%, 46%)` },
      { off: '80%', color: `hsl(${hue + 25}, 90%, 38%)`, opacity: 0.8 },
      { off: '100%', color: `hsl(${hue + 30}, 80%, 30%)`, opacity: 0.15 },
    ],
    coreBottom: '#bfdbfe', coreMid: '#60a5fa', coreTop: '#3b82f6',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(60,130,255,${g}) 0%, rgba(30,80,200,${g * 0.6}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #dbeafe, #3b82f6)',
    sparkShadow: '0 0 4px 2px rgba(59,130,246,0.7)',
    label: '청염',
  }
  return {
    hueBase: 20,
    flameStops: (hue: number) => [
      { off: '0%', color: `hsl(${hue}, 100%, 55%)` },
      { off: '30%', color: `hsl(${hue + 12}, 100%, 50%)` },
      { off: '55%', color: `hsl(${hue + 25}, 98%, 46%)` },
      { off: '80%', color: `hsl(${hue + 30}, 92%, 38%)`, opacity: 0.8 },
      { off: '100%', color: `hsl(${hue + 35}, 80%, 30%)`, opacity: 0.15 },
    ],
    coreBottom: '#ffffff', coreMid: '#ffd54f', coreTop: '#ff9800',
    glowColor: (g: number) => `radial-gradient(ellipse, rgba(255,120,0,${g}) 0%, rgba(255,60,0,${g * 0.6}) 40%, transparent 70%)`,
    sparkBg: 'radial-gradient(circle, #fff3e0, #ff9800)',
    sparkShadow: '0 0 4px 2px rgba(255,150,0,0.7)',
    label: null,
  }
}

/**
 * 스트릭 불꽃 애니메이션 컴포넌트
 * streak 1~2: 약한 불씨 / 3~5: 중간 / 6~10: 강함 / 11+: 최대
 * 30일+: 파란 불꽃 / 100일+: 흰 불꽃 / 300일+: 검은 불꽃
 */
/** SVG 불꽃 경로 (뾰족한 꼭대기 + 넓은 바닥) */
const FLAME_PATH = 'M50 0 C50 0 62 18 68 35 C74 52 78 68 75 80 C72 90 63 98 50 100 C37 98 28 90 25 80 C22 68 26 52 32 35 C38 18 50 0 50 0Z'

function StreakFire({ streak }: { streak: number }) {
  const intensity = streak <= 0 ? 0 : streak <= 2 ? 1 : streak <= 5 ? 2 : streak <= 10 ? 3 : 4
  const theme = getFlameTheme(streak)

  const config = useMemo(() => {
    switch (intensity) {
      case 0: return { flames: 0, size: 0, speed: 0, sparks: 0, glow: 0 }
      case 1: return { flames: 1, size: 36, speed: 2.5, sparks: 0, glow: 0 }
      case 2: return { flames: 3, size: 44, speed: 1.8, sparks: 2, glow: 0.25 }
      case 3: return { flames: 5, size: 52, speed: 1.2, sparks: 4, glow: 0.45 }
      case 4: return { flames: 7, size: 60, speed: 0.8, sparks: 7, glow: 0.65 }
      default: return { flames: 1, size: 36, speed: 2.5, sparks: 0, glow: 0 }
    }
  }, [intensity])

  const flameData = useMemo(() =>
    Array.from({ length: config.flames }, (_, i) => ({
      id: i,
      xOff: (i - (config.flames - 1) / 2) * (intensity <= 1 ? 0 : intensity <= 2 ? 8 : 6),
      heightRatio: i === Math.floor(config.flames / 2) ? 1 : 0.6 + Math.random() * 0.3,
      delay: i * 0.12,
      hue: theme.hueBase + (i % 3) * 10,
    })),
    [config.flames, intensity, theme.hueBase]
  )

  const sparkData = useMemo(() =>
    Array.from({ length: config.sparks }, (_, i) => ({
      id: i,
      x: -14 + Math.random() * 28,
      delay: i * 0.3 + Math.random() * 0.5,
      duration: 0.8 + Math.random() * 0.6,
      size: 3 + Math.random() * 2,
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
    <div className="relative flex items-end justify-center" style={{ width: 76, height: containerH }}>
      {/* 히든 불꽃 라벨 */}
      {theme.label && (
        <motion.div
          className="absolute -top-2 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-full bg-white/25 px-2 py-0.5 text-[10px] font-bold backdrop-blur-sm"
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ textShadow: '0 0 4px rgba(255,255,255,0.5)' }}
        >
          {theme.label}
        </motion.div>
      )}

      {/* 글로우 이펙트 */}
      {config.glow > 0 && (
        <motion.div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 rounded-full"
          style={{
            width: config.size * 1.6,
            height: config.size * 0.5,
            background: theme.glowColor(config.glow),
            filter: `blur(${4 + intensity}px)`,
          }}
          animate={{ opacity: [0.7, 1, 0.7], scaleX: [0.9, 1.1, 0.9] }}
          transition={{ duration: config.speed * 0.8, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}

      {/* SVG 불꽃 레이어 */}
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
            }}
            animate={{
              scaleX: [1, intensity <= 1 ? 1.06 : 1.15, 0.92, 1],
              scaleY: [1, intensity <= 1 ? 1.04 : 1.12, 0.94, 1],
              x: [0, (f.id % 2 === 0 ? 2 : -2) * (intensity <= 1 ? 0.5 : 1), 0],
              rotate: [0, f.id % 2 === 0 ? 4 : -4, 0],
            }}
            transition={{
              duration: config.speed,
              repeat: Infinity,
              delay: f.delay,
              ease: 'easeInOut',
            }}
          >
            <svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height="100%">
              <defs>
                <linearGradient id={`flame-${f.id}-${streak}`} x1="0.5" y1="1" x2="0.5" y2="0">
                  {theme.flameStops(f.hue).map((s, si) => (
                    <stop key={si} offset={s.off} stopColor={s.color} stopOpacity={s.opacity ?? 1} />
                  ))}
                </linearGradient>
              </defs>
              <path d={FLAME_PATH} fill={`url(#flame-${f.id}-${streak})`} />
            </svg>
          </motion.div>
        )
      })}

      {/* 중심 밝은 코어 (SVG) */}
      <motion.div
        className="absolute bottom-0 left-1/2 -translate-x-1/2"
        style={{
          width: config.size * 0.32,
          height: config.size * 0.5,
        }}
        animate={{
          scaleY: [1, 1.08, 0.96, 1],
          opacity: [0.9, 1, 0.9],
        }}
        transition={{ duration: config.speed * 0.7, repeat: Infinity, ease: 'easeInOut' }}
      >
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height="100%">
          <defs>
            <linearGradient id={`core-${streak}`} x1="0.5" y1="1" x2="0.5" y2="0">
              <stop offset="0%" stopColor={theme.coreBottom} />
              <stop offset="40%" stopColor={theme.coreMid} stopOpacity="0.8" />
              <stop offset="100%" stopColor={theme.coreTop} stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d={FLAME_PATH} fill={`url(#core-${streak})`} />
        </svg>
      </motion.div>

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
}

export function MyStatsPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<StudentStats | null>(null)
  const [chapters, setChapters] = useState<ChapterProgressItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const gradeLabel = user?.grade ? GRADE_LABELS[user.grade] : null

  // 학기별로 단원 그룹화 (서버에서 받은 semester 필드 기반)
  const chaptersBySemester = useMemo(() => {
    const grouped = new Map<number, ChapterProgressItem[]>()

    chapters.forEach(ch => {
      const semester = ch.semester || 1
      if (!grouped.has(semester)) {
        grouped.set(semester, [])
      }
      grouped.get(semester)!.push(ch)
    })

    return Array.from(grouped.entries()).sort(([a], [b]) => a - b)
  }, [chapters])

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setIsLoading(true)
      setError('')

      const [statsRes, chaptersRes] = await Promise.all([
        api.get<{ success: boolean; data: StudentStats }>('/api/v1/stats/me'),
        api.get<{ success: boolean; data: ChapterProgressItem[] }>('/api/v1/chapters/progress', {
          params: { grade: user?.grade }
        }).catch(() => null),
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
    <div className="min-h-screen bg-gray-50 py-4 sm:py-6">
      <div className="container mx-auto max-w-5xl px-4 space-y-4">
        {/* 헤더 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-2">
            <span className="text-xl">📊</span>
            <h1 className="text-xl font-bold text-gray-900">내 학습 통계</h1>
            {gradeLabel && (
              <span className="rounded-full bg-primary-100 px-2.5 py-0.5 text-xs font-semibold text-primary-700">
                {gradeLabel}
              </span>
            )}
          </div>
        </motion.div>

        {/* 레벨 & 스트릭 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid gap-3 grid-cols-2"
        >
          {/* 레벨 카드 */}
          <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-500 via-purple-600 to-purple-700 p-4 text-white shadow-md">
            <motion.div
              className="pointer-events-none absolute -right-2 -top-2 select-none opacity-15"
              animate={{ rotate: [0, 5, -5, 0], scale: [1, 1.05, 1] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              style={{ fontSize: 64 }}
            >
              {getLevelMeta(stats.level).icon}
            </motion.div>
            <div className="flex items-center gap-1.5 mb-2">
              <span className="text-xs font-medium opacity-75">현재 레벨</span>
              <span className="rounded-full bg-white/20 px-1.5 py-0.5 text-[10px] font-bold">
                {getLevelMeta(stats.level).icon} {getLevelMeta(stats.level).title}
              </span>
            </div>
            <div className="flex items-end justify-between mb-2">
              <p className="font-math text-3xl font-black leading-none">Lv.{stats.level}</p>
              <p className="font-math text-sm font-bold opacity-80">{stats.total_xp.toLocaleString()} XP</p>
            </div>
            <XpBar level={stats.level} totalXp={stats.total_xp} showLabel={false} />
          </div>

          {/* 스트릭 카드 */}
          <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 p-4 text-white shadow-md">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-medium opacity-75">연속 학습</span>
                <p className="font-math text-3xl font-black leading-none mt-1">{stats.current_streak}</p>
                <p className="text-xs opacity-90 mt-0.5">일 연속!</p>
              </div>
              <StreakFire streak={stats.current_streak} />
            </div>
            <div className="flex items-center justify-between border-t border-white/20 pt-2 mt-2 text-xs">
              <span className="opacity-75">최대 기록</span>
              <span className="font-math text-sm font-bold">{stats.max_streak}일</span>
            </div>
          </div>
        </motion.div>

        {/* 학습 통계 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="mb-2 text-sm font-semibold text-gray-900">학습 현황</h2>
          <div className="grid gap-2.5 grid-cols-3 lg:grid-cols-5">
            {/* 정답률 카드 - 강조 */}
            <div className="flex flex-col items-center justify-center rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 p-3 text-white shadow-md text-center">
              <p className="text-[10px] font-medium opacity-75">정답률</p>
              <p className="font-math text-2xl font-black mt-0.5">{stats.accuracy_rate}%</p>
              <span className={`inline-block px-2 py-0.5 ${accuracyLabel.badge} rounded-full text-[10px] font-medium mt-1`}>
                {accuracyLabel.text}
              </span>
            </div>

            <StatCard icon="📝" label="완료 테스트" value={stats.total_tests} suffix="개" />
            <StatCard icon="✏️" label="풀이 문제" value={stats.total_questions} suffix="문제" />
            <StatCard icon="✅" label="정답 수" value={stats.correct_answers} suffix="개" />
            <StatCard
              icon="⏱️"
              label="평균 풀이"
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
            <h2 className="mb-2 text-sm font-semibold text-gray-900">트랙별 성적</h2>
            <div className="grid gap-2.5 grid-cols-2">
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

        {/* 오늘의 학습 요약 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.26 }}
        >
          <h2 className="mb-2 text-sm font-semibold text-gray-900">오늘의 학습</h2>
          <div className="grid gap-2.5 grid-cols-2">
            <div className="rounded-xl bg-gradient-to-br from-cyan-400 to-cyan-600 p-3 text-white shadow-md">
              <p className="text-[10px] font-medium opacity-75">오늘 푼 문제</p>
              <p className="font-math text-2xl font-black mt-0.5">{stats.today_solved}<span className="ml-1 text-xs font-normal opacity-80">문제</span></p>
            </div>
            {stats.review_stats && (
              <div className="rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 p-3 text-white shadow-md">
                <p className="text-[10px] font-medium opacity-75">오답 복습</p>
                <div className="flex items-end gap-2 mt-0.5">
                  <p className="font-math text-2xl font-black">{stats.review_stats.pending_count}<span className="ml-1 text-xs font-normal opacity-80">대기</span></p>
                </div>
                <div className="flex items-center gap-2 mt-1 text-[10px] opacity-90">
                  <span>진행 {stats.review_stats.in_progress_count}</span>
                  <span>|</span>
                  <span>졸업 {stats.review_stats.graduated_count}</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* 최근 7일 학습 추이 */}
        {stats.daily_activity && stats.daily_activity.length > 0 && stats.daily_activity.some(d => d.questions_answered > 0) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.28 }}
          >
            <h2 className="mb-2 text-sm font-semibold text-gray-900">최근 7일 학습 추이</h2>
            <div className="rounded-xl bg-white p-4 shadow-sm">
              <WeeklyActivityChart data={stats.daily_activity} />
            </div>
          </motion.div>
        )}

        {/* 문제 유형별 성적 */}
        {stats.type_stats && Object.keys(stats.type_stats).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="mb-2 text-sm font-semibold text-gray-900">유형별 성적</h2>
            <div className="grid gap-2.5 grid-cols-2 lg:grid-cols-4">
              {Object.entries(stats.type_stats).map(([typeKey, ts]) => (
                <TypeStatCard key={typeKey} typeKey={typeKey} stats={ts} />
              ))}
            </div>
          </motion.div>
        )}

        {/* 최근 시험 이력 */}
        {stats.recent_tests && stats.recent_tests.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.32 }}
          >
            <h2 className="mb-2 text-sm font-semibold text-gray-900">최근 시험</h2>
            <div className="space-y-1.5">
              {stats.recent_tests.slice(0, 5).map((test) => (
                <RecentTestRow key={`${test.test_id}-${test.completed_at}`} test={test} />
              ))}
            </div>
          </motion.div>
        )}

        {/* 단원 진행 상황 */}
        {chapters.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.34 }}
          >
            <h2 className="mb-2 text-sm font-semibold text-gray-900">단원 진행 상황</h2>
            <div className="space-y-4">
              {chaptersBySemester.map(([semester, semesterChapters]) => (
                <div key={semester}>
                  <h3 className="mb-2 text-xs font-medium text-gray-500">
                    {user?.grade?.startsWith('high_')
                      ? (semester === 1 ? '공통수학1' : '공통수학2')
                      : `${semester}학기`}
                  </h3>
                  <div className="space-y-2">
                    {semesterChapters.map((ch) => (
                      <ChapterRow key={ch.chapter_id} chapter={ch} />
                    ))}
                  </div>
                </div>
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
            <h2 className="mb-2 text-sm font-semibold text-gray-900">
              📚 더 연습이 필요한 개념
            </h2>
            <div className="space-y-1.5">
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
            <h2 className="mb-2 text-sm font-semibold text-gray-900">⭐ 잘하는 개념</h2>
            <div className="space-y-1.5">
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
    <div className="rounded-xl bg-white p-3 shadow-sm hover:shadow-md transition-shadow">
      <div className="text-lg mb-0.5">{icon}</div>
      <p className="text-[10px] text-gray-500 leading-tight">{label}</p>
      <p className="font-math text-lg font-bold tabular-nums text-gray-900 mt-0.5">
        {value}
        <span className="ml-0.5 text-[10px] font-normal text-gray-400">{suffix}</span>
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
    <div className={`rounded-xl ${bgColors[color]} p-3 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="flex items-center gap-1.5 mb-1.5">
        <span className="text-base">{icon}</span>
        <span className={`text-sm font-semibold ${textColors[color]}`}>{label}</span>
      </div>
      <div className="flex items-end gap-2 mb-1.5">
        <p className={`font-math text-2xl font-black ${textColors[color]}`}>
          {trackStats.accuracy_rate}%
        </p>
        <p className="text-xs text-gray-500 mb-0.5">
          {trackStats.correct_answers}/{trackStats.total_questions}
        </p>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-white/70 shadow-inner">
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
    <div className={`rounded-lg ${bgColor} px-3 py-2.5 shadow-sm`}>
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-sm font-medium text-gray-900">{name}</span>
        <span className={`font-math text-sm font-bold ${textColor}`}>{accuracy}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-white/70 shadow-inner">
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
        'rounded-lg px-3 py-2.5 shadow-sm transition-shadow hover:shadow-md',
        isLocked ? 'bg-gray-100 opacity-60' : ch.is_completed ? 'bg-green-50' : 'bg-white'
      )}
    >
      <div className="mb-1.5 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-sm">
            {isLocked ? '🔒' : ch.is_completed ? '✅' : '📖'}
          </span>
          <span className={clsx('text-sm font-medium', isLocked ? 'text-gray-400' : 'text-gray-900')}>
            {ch.name}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          {ch.is_completed && ch.final_test_score != null && (
            <span className="text-[10px] font-medium text-green-600">
              최종 {ch.final_test_score}점
            </span>
          )}
          {ch.teacher_approved && (
            <span className="rounded-full bg-green-100 px-1.5 py-0.5 text-[10px] font-medium text-green-700">
              승인됨
            </span>
          )}
          {!isLocked && !ch.is_completed && (
            <span className="font-math text-xs font-bold text-primary-600">{progress}%</span>
          )}
        </div>
      </div>
      {!isLocked && (
        <div className="h-2 overflow-hidden rounded-full bg-gray-200">
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

// 최근 7일 학습 추이 차트
const DAY_LABELS = ['일', '월', '화', '수', '목', '금', '토']

function WeeklyActivityChart({ data }: { data: DailyActivityItem[] }) {
  const maxQuestions = Math.max(...data.map(d => d.questions_answered), 1)

  return (
    <div className="space-y-3">
      {/* 막대 그래프 */}
      <div className="flex items-end justify-between gap-1" style={{ height: 100 }}>
        {data.map((d) => {
          const h = d.questions_answered > 0 ? Math.max(8, (d.questions_answered / maxQuestions) * 100) : 4
          const dayOfWeek = new Date(d.date).getDay()
          return (
            <div key={d.date} className="flex flex-1 flex-col items-center gap-1">
              {d.questions_answered > 0 && (
                <span className="text-[10px] font-bold text-gray-500">{d.questions_answered}</span>
              )}
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: h }}
                transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                className={clsx(
                  'w-full max-w-[28px] rounded-t-md',
                  d.questions_answered > 0
                    ? d.accuracy_rate >= 80 ? 'bg-gradient-to-t from-green-400 to-green-500'
                      : d.accuracy_rate >= 60 ? 'bg-gradient-to-t from-blue-400 to-blue-500'
                      : 'bg-gradient-to-t from-orange-400 to-orange-500'
                    : 'bg-gray-200'
                )}
              />
              <span className="text-[10px] text-gray-400">{DAY_LABELS[dayOfWeek]}</span>
            </div>
          )
        })}
      </div>
      {/* 범례 */}
      <div className="flex justify-center gap-3 text-[10px] text-gray-400">
        <span><span className="mr-0.5 inline-block h-2 w-2 rounded-sm bg-green-400" />80%+</span>
        <span><span className="mr-0.5 inline-block h-2 w-2 rounded-sm bg-blue-400" />60%+</span>
        <span><span className="mr-0.5 inline-block h-2 w-2 rounded-sm bg-orange-400" />60% 미만</span>
      </div>
    </div>
  )
}

// 문제 유형별 통계 카드
const TYPE_LABELS: Record<string, { icon: string; label: string }> = {
  multiple_choice: { icon: '🔘', label: '객관식' },
  fill_in_blank: { icon: '✏️', label: '빈칸' },
  short_answer: { icon: '📝', label: '단답형' },
  true_false: { icon: '⭕', label: 'O/X' },
}

function TypeStatCard({ typeKey, stats: ts }: { typeKey: string; stats: TrackStats }) {
  const meta = TYPE_LABELS[typeKey] || { icon: '📋', label: typeKey }
  const color = ts.accuracy_rate >= 80 ? 'text-green-600' : ts.accuracy_rate >= 60 ? 'text-blue-600' : 'text-red-600'
  const barColor = ts.accuracy_rate >= 80 ? 'from-green-400 to-green-600' : ts.accuracy_rate >= 60 ? 'from-blue-400 to-blue-600' : 'from-red-400 to-red-600'

  return (
    <div className="rounded-xl bg-white p-3 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-1.5 mb-1">
        <span className="text-base">{meta.icon}</span>
        <span className="text-xs font-semibold text-gray-700">{meta.label}</span>
      </div>
      <p className={`font-math text-xl font-black ${color}`}>{ts.accuracy_rate}%</p>
      <p className="text-[10px] text-gray-400 mt-0.5">{ts.correct_answers}/{ts.total_questions}문제</p>
      <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-gray-100">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${ts.accuracy_rate}%` }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full bg-gradient-to-r ${barColor}`}
        />
      </div>
    </div>
  )
}

// 최근 시험 이력 행
function RecentTestRow({ test }: { test: RecentTestItem }) {
  const date = new Date(test.completed_at)
  const dateStr = `${date.getMonth() + 1}/${date.getDate()}`
  const color = test.accuracy_rate >= 80 ? 'text-green-600' : test.accuracy_rate >= 60 ? 'text-blue-600' : 'text-red-600'

  return (
    <div className="flex items-center justify-between rounded-lg bg-white px-3 py-2.5 shadow-sm">
      <div className="flex items-center gap-2 min-w-0">
        <span className="text-xs text-gray-400 shrink-0">{dateStr}</span>
        <span className="text-sm font-medium text-gray-900 truncate">{test.test_title}</span>
      </div>
      <div className="flex items-center gap-2 shrink-0">
        <span className="text-xs text-gray-500">{test.score}/{test.max_score}</span>
        <span className={`font-math text-sm font-bold ${color}`}>{test.accuracy_rate}%</span>
      </div>
    </div>
  )
}
