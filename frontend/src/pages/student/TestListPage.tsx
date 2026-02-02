// 테스트 목록 페이지

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import type { AvailableTest, PaginatedResponse } from '../../types'

export function TestListPage() {
  const navigate = useNavigate()
  const [tests, setTests] = useState<AvailableTest[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchTests()
  }, [])

  const fetchTests = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<{ success: boolean; data: PaginatedResponse<AvailableTest> }>(
        '/api/v1/tests/available'
      )
      setTests(response.data.data.items)
    } catch {
      setError('테스트 목록을 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleStartTest = (testId: string) => {
    navigate(`/test/${testId}`)
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">테스트 목록을 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error}</p>
          <button onClick={fetchTests} className="btn-primary px-4 py-2">
            다시 시도
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-2xl font-bold text-gray-900">오늘의 테스트</h1>
          <p className="text-gray-600">풀 수 있는 테스트를 선택하세요</p>
        </motion.div>

        {tests.length === 0 ? (
          <div className="rounded-2xl bg-white p-8 text-center shadow-sm">
            <div className="mb-4 text-4xl">📚</div>
            <p className="text-gray-600">현재 풀 수 있는 테스트가 없습니다.</p>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tests.map((test, index) => (
              <TestCard
                key={test.id}
                test={test}
                index={index}
                onStart={() => handleStartTest(test.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

interface TestCardProps {
  test: AvailableTest
  index: number
  onStart: () => void
}

function TestCard({ test, index, onStart }: TestCardProps) {
  const getDifficultyColor = () => {
    if (test.question_count <= 5) return 'bg-green-100 text-green-700'
    if (test.question_count <= 10) return 'bg-yellow-100 text-yellow-700'
    return 'bg-red-100 text-red-700'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="card overflow-hidden"
    >
      <div className="p-6">
        <div className="mb-4 flex items-start justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{test.title}</h3>
            <p className="mt-1 text-sm text-gray-600">{test.description}</p>
          </div>
          {test.is_completed && (
            <span className="rounded-full bg-primary-100 px-2 py-1 text-xs font-medium text-primary-700">
              완료
            </span>
          )}
        </div>

        <div className="mb-4 flex flex-wrap gap-2">
          <span className={`rounded-full px-2 py-1 text-xs font-medium ${getDifficultyColor()}`}>
            {test.question_count}문제
          </span>
          {test.time_limit_minutes && (
            <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700">
              {test.time_limit_minutes}분
            </span>
          )}
          {test.best_score !== undefined && test.best_score !== null && (
            <span className="rounded-full bg-purple-100 px-2 py-1 text-xs font-medium text-purple-700">
              최고 {test.best_score}점
            </span>
          )}
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-500">
            {test.attempt_count > 0 ? `${test.attempt_count}회 도전` : '첫 도전!'}
          </span>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onStart}
            className="btn-primary px-4 py-2 text-sm"
          >
            {test.is_completed ? '다시 풀기' : '시작하기'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}
