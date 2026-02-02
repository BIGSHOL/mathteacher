import { motion } from 'framer-motion'
import { useAuthStore } from '../store/authStore'
import { useNavigate } from 'react-router-dom'

export function DashboardPage() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary-500">수학 테스트</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">
              {user?.name || '학생'}님
            </span>
            <button
              onClick={handleLogout}
              className="btn-outline px-4 py-2 text-sm"
            >
              로그아웃
            </button>
          </div>
        </div>
      </header>

      {/* 메인 콘텐츠 */}
      <main className="container mx-auto px-4 py-8">
        {/* 통계 카드 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
        >
          <StatCard label="오늘 학습" value="0문제" icon="📝" />
          <StatCard label="연속 정답" value="0회" icon="🔥" color="streak" />
          <StatCard label="현재 레벨" value="Lv.1" icon="⭐" color="level" />
          <StatCard label="총 콤보" value="0" icon="💫" color="combo" />
        </motion.div>

        {/* 학습 메뉴 */}
        <h2 className="text-xl font-semibold text-gray-900 mb-4">학습하기</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <LearningCard
            title="개념 테스트"
            description="수학 개념을 테스트하고 이해도를 확인해보세요"
            icon="📚"
            href="/test/concept"
          />
          <LearningCard
            title="연산 연습"
            description="빠른 연산 능력을 키워보세요"
            icon="🧮"
            href="/test/operation"
          />
          <LearningCard
            title="복습하기"
            description="틀렸던 문제를 다시 풀어보세요"
            icon="🔄"
            href="/review"
          />
        </div>
      </main>
    </div>
  )
}

interface StatCardProps {
  label: string
  value: string
  icon: string
  color?: 'combo' | 'streak' | 'level'
}

function StatCard({ label, value, icon, color }: StatCardProps) {
  const colorClasses = {
    combo: 'bg-amber-50 border-amber-200',
    streak: 'bg-red-50 border-red-200',
    level: 'bg-purple-50 border-purple-200',
  }

  return (
    <div className={`card p-4 border ${color ? colorClasses[color] : 'border-gray-100'}`}>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{icon}</span>
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}

interface LearningCardProps {
  title: string
  description: string
  icon: string
  href: string
}

function LearningCard({ title, description, icon, href }: LearningCardProps) {
  return (
    <motion.a
      href={href}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className="card p-6 block cursor-pointer hover:border-primary-200"
    >
      <div className="text-3xl mb-3">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </motion.a>
  )
}
