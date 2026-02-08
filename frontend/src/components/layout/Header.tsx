// 헤더 컴포넌트

import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuthStore } from '../../store/authStore'
import { XpBadge } from '../gamification/XpBar'
import { StreakBadge } from '../gamification/StreakDisplay'

export function Header() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isStaff = user?.role === 'teacher' || user?.role === 'admin' || user?.role === 'master'
  const isAdmin = user?.role === 'admin' || user?.role === 'master'

  const getRoleLabel = (role: string) => {
    switch (role) {
      case 'master': return '마스터'
      case 'admin': return '관리자'
      case 'teacher': return '강사'
      default: return '학생'
    }
  }

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/95 backdrop-blur">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* 로고 */}
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl">📐</span>
            <span className="text-xl font-bold text-primary-600">개념 연산 수학</span>
          </Link>

          {/* 네비게이션 */}
          {user && (
            <nav className="hidden items-center gap-6 md:flex">
              {isStaff ? (
                <>
                  <NavLink to="/teacher/dashboard">대시보드</NavLink>
                  <NavLink to="/teacher/students">학생 관리</NavLink>
                  {isAdmin && <NavLink to="/admin/questions">문제 은행</NavLink>}
                  {user?.role === 'master' && <NavLink to="/admin/generate">문제 생성</NavLink>}
                  {isAdmin && <NavLink to="/admin/users">계정 관리</NavLink>}
                </>
              ) : (
                <>
                  <NavLink to="/daily-lab">이달의 수학</NavLink>
                  <NavLink to="/tests">테스트</NavLink>
                  <NavLink to="/leaderboard">랭킹</NavLink>
                  <NavLink to="/my-stats">내 통계</NavLink>
                  {/* <NavLink to="/shop">상점</NavLink> */}
                </>
              )}
            </nav>
          )}

          {/* 사용자 정보 */}
          <div className="flex items-center gap-4">
            {user && !isStaff && (
              <div className="hidden items-center gap-2 md:flex">
                <XpBadge level={user.level} totalXp={user.total_xp} />
                <StreakBadge streak={user.current_streak} />
              </div>
            )}

            {user ? (
              <div className="flex items-center gap-3">
                <div className="hidden text-right md:block">
                  <p className="text-sm font-medium text-gray-900">{user.name}</p>
                  <p className="text-xs text-gray-500">
                    {getRoleLabel(user.role)}
                  </p>
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLogout}
                  className="rounded-lg bg-gray-100 px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-200"
                >
                  로그아웃
                </motion.button>
              </div>
            ) : (
              <Link
                to="/login"
                className="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600"
              >
                로그인
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const location = useLocation()
  const isActive = location.pathname === to || location.pathname.startsWith(to + '/')

  return (
    <Link
      to={to}
      className={`relative text-sm font-medium transition-colors ${isActive
        ? 'text-primary-600'
        : 'text-gray-600 hover:text-primary-600'
        }`}
    >
      {children}
      {isActive && (
        <span className="absolute -bottom-[19px] left-0 right-0 h-[2px] rounded-full bg-primary-500" />
      )}
    </Link>
  )
}
