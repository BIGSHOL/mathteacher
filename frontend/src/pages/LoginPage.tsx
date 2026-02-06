import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuthStore } from '../store/authStore'

export function LoginPage() {
  const [loginId, setLoginId] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const location = useLocation()
  const login = useAuthStore((state) => state.login)

  // 이전 페이지가 있으면 그곳으로, 없으면 역할에 따라 리다이렉트
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname

  const getDefaultPath = (role: string): string => {
    switch (role) {
      case 'master':
      case 'admin':
      case 'teacher':
        return '/teacher/dashboard'
      case 'student':
      default:
        return '/daily-lab'
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      await login(loginId, password)
      // 로그인 후 사용자 정보로 리다이렉트 경로 결정
      const currentUser = useAuthStore.getState().user
      const redirectPath = from || (currentUser ? getDefaultPath(currentUser.role) : '/daily-lab')
      navigate(redirectPath, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card w-full max-w-md p-8"
      >
        <div className="text-center mb-8">
          <Link to="/" className="text-3xl font-bold text-primary-500">
            개념 연산 수학
          </Link>
          <p className="text-gray-600 mt-2">개념부터 연산까지, 로그인하고 수학 테스트를 시작하세요</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6" autoComplete="off">
          {error && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-red-50 text-red-600 p-3 rounded-lg text-sm"
            >
              {error}
            </motion.div>
          )}

          <div>
            <label htmlFor="loginId" className="block text-sm font-medium text-gray-700 mb-1">
              아이디
            </label>
            <input
              id="loginId"
              type="text"
              value={loginId}
              onChange={(e) => setLoginId(e.target.value)}
              className="input"
              placeholder="아이디를 입력하세요"
              required
              minLength={4}
              autoComplete="off"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              비밀번호
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              placeholder="••••••••"
              required
              autoComplete="new-password"
            />
          </div>

          <motion.button
            type="submit"
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-primary w-full py-3"
          >
            {isLoading ? '로그인 중...' : '로그인'}
          </motion.button>
        </form>
      </motion.div>
    </div>
  )
}
