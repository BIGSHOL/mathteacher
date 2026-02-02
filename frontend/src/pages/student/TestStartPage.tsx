// 테스트 시작 페이지

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../../lib/api'
import type { TestWithQuestions } from '../../types'

export function TestStartPage() {
  const { testId } = useParams<{ testId: string }>()
  const navigate = useNavigate()
  const [test, setTest] = useState<TestWithQuestions | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isStarting, setIsStarting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (testId) {
      fetchTestDetail()
    }
  }, [testId])

  const fetchTestDetail = async () => {
    try {
      setIsLoading(true)
      const response = await api.get<{ success: boolean; data: TestWithQuestions }>(
        `/api/v1/tests/${testId}`
      )
      setTest(response.data.data)
    } catch {
      setError('테스트 정보를 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleStartTest = async () => {
    if (!testId) return

    try {
      setIsStarting(true)
      const response = await api.post<{
        success: boolean
        data: { attempt_id: string }
      }>(`/api/v1/tests/${testId}/start`)

      const attemptId = response.data.data.attempt_id
      navigate(`/test/play/${attemptId}`)
    } catch {
      setError('테스트 시작에 실패했습니다.')
      setIsStarting(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-primary-50 to-white">
        <div className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div>
          <p className="text-gray-600">테스트 정보를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error || !test) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-primary-50 to-white">
        <div className="text-center">
          <p className="mb-4 text-red-500">{error || '테스트를 찾을 수 없습니다.'}</p>
          <button onClick={() => navigate('/tests')} className="btn-primary px-4 py-2">
            목록으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-primary-50 to-white px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md"
      >
        <div className="card overflow-hidden">
          {/* 헤더 */}
          <div className="bg-primary-500 p-6 text-white">
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-2xl font-bold">{test.title}</h1>
              {test.category && (
                <span className="rounded-full bg-white/20 px-2 py-1 text-xs font-medium text-white">
                  {test.category === 'computation' ? '연산' : '개념'}
                </span>
              )}
              {test.is_adaptive && (
                <span className="rounded-full bg-white/20 px-2 py-1 text-xs font-medium text-white">
                  적응형
                </span>
              )}
            </div>
            <p className="mt-2 text-primary-100">{test.description}</p>
          </div>

          {/* 테스트 정보 */}
          <div className="p-6">
            <div className="mb-6 grid grid-cols-2 gap-4">
              <InfoItem icon="📝" label="문제 수" value={`${test.question_count}문제`} />
              <InfoItem
                icon="⏱️"
                label="제한 시간"
                value={test.time_limit_minutes ? `${test.time_limit_minutes}분` : '없음'}
              />
            </div>

            {/* 안내 사항 */}
            <div className="mb-6 rounded-xl bg-gray-50 p-4">
              <h3 className="mb-2 font-semibold text-gray-900">안내 사항</h3>
              <ul className="space-y-1 text-sm text-gray-600">
                <li>• 문제를 풀면 바로 정답을 확인할 수 있어요</li>
                <li>• 연속으로 맞추면 콤보 보너스를 받아요</li>
                <li>• 중간에 나가면 진행 상황이 저장되지 않아요</li>
              </ul>
            </div>

            {/* 적응형 안내 */}
            {test.is_adaptive && (
              <div className="mb-6 rounded-xl bg-indigo-50 p-4">
                <h3 className="mb-2 font-semibold text-indigo-900">적응형 테스트</h3>
                <ul className="space-y-1 text-sm text-indigo-700">
                  <li>• 내 실력에 맞게 난이도가 자동 조절돼요</li>
                  <li>• 정답을 맞추면 더 어려운 문제가 나와요</li>
                  <li>• 틀리면 조금 쉬운 문제로 넘어가요</li>
                </ul>
              </div>
            )}

            {/* 시작 버튼 */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleStartTest}
              disabled={isStarting}
              className="btn-primary w-full py-4 text-lg"
            >
              {isStarting ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  시작하는 중...
                </span>
              ) : (
                '테스트 시작하기'
              )}
            </motion.button>

            {/* 뒤로 가기 */}
            <button
              onClick={() => navigate('/tests')}
              className="mt-4 w-full py-2 text-sm text-gray-500 hover:text-gray-700"
            >
              목록으로 돌아가기
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

interface InfoItemProps {
  icon: string
  label: string
  value: string
}

function InfoItem({ icon, label, value }: InfoItemProps) {
  return (
    <div className="rounded-xl bg-gray-50 p-4 text-center">
      <div className="mb-1 text-2xl">{icon}</div>
      <div className="text-xs text-gray-500">{label}</div>
      <div className="font-semibold text-gray-900">{value}</div>
    </div>
  )
}
