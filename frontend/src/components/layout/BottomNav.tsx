// 모바일 하단 네비게이션 컴포넌트

import { NavLink, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuthStore } from '../../store/authStore'

interface NavItemProps {
  to: string
  icon: string
  label: string
}

function NavItem({ to, icon, label }: NavItemProps) {
  const location = useLocation()
  const isActive = location.pathname === to || location.pathname.startsWith(to + '/')

  return (
    <NavLink
      to={to}
      className="flex flex-1 flex-col items-center justify-center py-2"
    >
      <motion.div
        whileTap={{ scale: 0.9 }}
        className="flex flex-col items-center"
      >
        <div
          className={`mb-1 flex h-8 w-8 items-center justify-center rounded-xl transition-colors ${
            isActive ? 'bg-primary-100' : ''
          }`}
        >
          <span className={`text-xl ${isActive ? '' : 'grayscale opacity-60'}`}>
            {icon}
          </span>
        </div>
        <span
          className={`text-xs font-medium transition-colors ${
            isActive ? 'text-primary-600' : 'text-gray-500'
          }`}
        >
          {label}
        </span>
        {isActive && (
          <motion.div
            layoutId="bottomNavIndicator"
            className="absolute bottom-1 h-1 w-8 rounded-full bg-primary-500"
            transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          />
        )}
      </motion.div>
    </NavLink>
  )
}

export function BottomNav() {
  const { user } = useAuthStore()
  const isStaff = user?.role === 'teacher' || user?.role === 'admin' || user?.role === 'master'
  const isAdmin = user?.role === 'admin' || user?.role === 'master'

  // 로그인하지 않은 경우 표시하지 않음
  if (!user) return null

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-gray-200 bg-white/95 backdrop-blur md:hidden">
      <div className="mx-auto flex h-16 max-w-lg items-center justify-around">
        {isStaff ? (
          // 강사/관리자용 네비게이션
          <>
            <NavItem to="/teacher/dashboard" icon="📊" label="대시보드" />
            <NavItem to="/teacher/students" icon="👥" label="학생관리" />
            {isAdmin && <NavItem to="/admin/users" icon="🔑" label="계정관리" />}
            <NavItem to="/profile" icon="👤" label="내 정보" />
          </>
        ) : (
          // 학생용 네비게이션
          <>
            <NavItem to="/tests" icon="📝" label="테스트" />
            <NavItem to="/my-stats" icon="📊" label="내 통계" />
            <NavItem to="/help" icon="📖" label="도움말" />
            <NavItem to="/profile" icon="👤" label="내 정보" />
          </>
        )}
      </div>
      {/* 하단 안전 영역 (노치 대응) */}
      <div className="h-safe-area-inset-bottom bg-white" />
    </nav>
  )
}
