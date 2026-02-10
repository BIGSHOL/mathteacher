// 인증 보호 라우트 컴포넌트

import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import type { UserRole } from '../../types'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles?: UserRole[]
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { user, isAuthenticated, accessToken, refreshToken } = useAuthStore()
  const location = useLocation()
  const [isRestoring, setIsRestoring] = useState(!accessToken && isAuthenticated)

  // 세션 복원: isAuthenticated=true이지만 accessToken이 없는 경우 (페이지 새로고침)
  useEffect(() => {
    if (!accessToken && isAuthenticated) {
      refreshToken().finally(() => setIsRestoring(false))
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // 토큰 복원 중 로딩 표시
  if (isRestoring) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent" />
      </div>
    )
  }

  // 미인증 사용자는 로그인 페이지로
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // 역할 제한이 있고, 현재 사용자가 허용되지 않은 경우
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // 역할에 따라 적절한 페이지로 리다이렉트
    const redirectPath = getDefaultPath(user.role)
    return <Navigate to={redirectPath} replace />
  }

  return <>{children}</>
}

// 역할별 기본 경로
function getDefaultPath(role: UserRole): string {
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

// 로그인 페이지 가드 (이미 로그인한 경우 리다이렉트)
export function PublicRoute({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated } = useAuthStore()

  if (isAuthenticated && user) {
    const redirectPath = getDefaultPath(user.role)
    return <Navigate to={redirectPath} replace />
  }

  return <>{children}</>
}
