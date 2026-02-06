// 빠른 연습 설정 페이지

import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import { useAuthStore } from '../../store/authStore'
import api from '../../lib/api'
import type { Grade, QuestionCategory } from '../../types'

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

const COUNT_OPTIONS = [10, 15, 20]

export function QuickPracticeSetupPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const user = useAuthStore((state) => state.user)

  const initialCategory = (searchParams.get('category') as QuestionCategory) || null
  const [category, setCategory] = useState<QuestionCategory | null>(initialCategory)
  const [count, setCount] = useState(10)
  const [difficulty, setDifficulty] = useState(user?.level ?? 5)
  const [isStarting, setIsStarting] = useState(false)
  const [error, setError] = useState('')

  const grade = user?.grade ?? 'middle_1'
  const gradeLabel = GRADE_LABELS[grade] ?? grade

  const handleStart = async () => {
    if (!category) return

    try {
      setIsStarting(true)
      setError('')

      const response = await api.post<{
        success: boolean
        data: { attempt_id: string }
      }>('/api/v1/practice/start', {
        grade,
        category,
        count,
        starting_difficulty: difficulty,
      })

      const attemptId = response.data.data.attempt_id
      navigate(`/test/play/${attemptId}`)
    } catch {
      setError('연습을 시작하는데 실패했습니다.')
      setIsStarting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white py-8">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mx-auto max-w-lg"
        >
          {/* 헤더 */}
          <div className="mb-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900">빠른 연습</h1>
            <p className="mt-1 text-gray-600">
              <span className="font-medium text-primary-600">{gradeLabel}</span> 수학 문제를
              풀어보세요
            </p>
          </div>

          <div className="card p-6">
            {/* 카테고리 선택 */}
            <div className="mb-6">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">유형 선택</h3>
              <div className="grid grid-cols-2 gap-3">
                <CategoryCard
                  icon="🧮"
                  label="연산"
                  description="빠른 계산 연습"
                  isSelected={category === 'computation'}
                  onClick={() => setCategory('computation')}
                />
                <CategoryCard
                  icon="📚"
                  label="개념"
                  description="개념 이해도 확인"
                  isSelected={category === 'concept'}
                  onClick={() => setCategory('concept')}
                />
              </div>
            </div>

            {/* 문제 수 선택 */}
            <div className="mb-6">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">문제 수</h3>
              <div className="flex gap-2">
                {COUNT_OPTIONS.map((n) => (
                  <button
                    key={n}
                    onClick={() => setCount(n)}
                    className={clsx(
                      'flex-1 rounded-xl py-3 text-center text-sm font-medium transition-all',
                      count === n
                        ? 'bg-primary-500 text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    )}
                  >
                    {n}문제
                  </button>
                ))}
              </div>
            </div>

            {/* 난이도 선택 */}
            <div className="mb-8">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">
                시작 난이도: <span className="text-primary-600">Lv.{difficulty}</span>
              </h3>
              <div className="grid grid-cols-5 gap-2">
                {Array.from({ length: 10 }, (_, i) => i + 1).map((lv) => (
                  <button
                    key={lv}
                    onClick={() => setDifficulty(lv)}
                    className={clsx(
                      'rounded-lg py-2.5 text-center text-sm font-medium transition-all',
                      difficulty === lv
                        ? 'bg-primary-500 text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    )}
                  >
                    {lv}
                  </button>
                ))}
              </div>
              <div className="mt-1.5 flex justify-between text-xs text-gray-400">
                <span>쉬움</span>
                <span>어려움</span>
              </div>
              <p className="mt-2 text-center text-xs text-gray-500">
                정답을 맞추면 난이도가 올라가고, 틀리면 내려갑니다
              </p>
            </div>

            {/* 에러 */}
            {error && (
              <p className="mb-4 text-center text-sm text-red-500">{error}</p>
            )}

            {/* 시작 버튼 */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleStart}
              disabled={!category || isStarting}
              className="btn-primary w-full py-4 text-lg disabled:opacity-50"
            >
              {isStarting ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  시작하는 중...
                </span>
              ) : (
                '연습 시작하기'
              )}
            </motion.button>

            {/* 뒤로 가기 */}
            <button
              onClick={() => navigate('/dashboard')}
              className="mt-4 w-full py-2 text-sm text-gray-500 hover:text-gray-700"
            >
              대시보드로 돌아가기
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

interface CategoryCardProps {
  icon: string
  label: string
  description: string
  isSelected: boolean
  onClick: () => void
}

function CategoryCard({ icon, label, description, isSelected, onClick }: CategoryCardProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={clsx(
        'rounded-xl border-2 p-4 text-left transition-all',
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      )}
    >
      <div className="mb-2 text-3xl">{icon}</div>
      <div className="text-sm font-semibold text-gray-900">{label}</div>
      <div className="text-xs text-gray-500">{description}</div>
    </motion.button>
  )
}
