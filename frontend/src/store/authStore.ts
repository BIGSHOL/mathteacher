import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Grade, UserRole } from '../types'

// Production: VITE_API_URL 사용, Development: 프록시 사용
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

interface User {
  id: string
  login_id: string
  name: string
  role: UserRole
  grade?: Grade
  level: number
  total_xp: number
  current_streak: number
}

interface AuthState {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
  isRefreshing: boolean
  login: (login_id: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<boolean>
  setUser: (user: User) => void
  setAccessToken: (token: string) => void
  fetchUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null, // 메모리에만 저장 (persist에서 제외)
      isAuthenticated: false,
      isRefreshing: false,

      fetchUser: async () => {
        const { accessToken } = get()
        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
            headers: {
              'Content-Type': 'application/json',
              ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
            },
            credentials: 'include',
          })
          if (response.ok) {
            const result = await response.json()
            const data = result.data
            // Update user state partially or fully
            set((state) => ({
              user: {
                ...state.user!,
                ...data, // API returns UserResponse which should match User interface mostly
                // Ensure specific fields if needed
                level: data.level || 1,
                total_xp: data.total_xp || 0,
                current_streak: data.current_streak || 0,
              }
            }))
          }
        } catch (error) {
          console.error("Failed to fetch user", error)
        }
      },

      login: async (login_id: string, password: string) => {
        const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include', // HttpOnly 쿠키 수신을 위해 필요
          body: JSON.stringify({ login_id, password }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.error?.message || error.detail?.message || '로그인에 실패했습니다.')
        }

        const result = await response.json()
        const data = result.data

        set({
          user: {
            id: data.user.id,
            login_id: data.user.login_id,
            name: data.user.name,
            role: data.user.role,
            grade: data.user.grade,
            level: data.user.level || 1,
            total_xp: data.user.total_xp || 0,
            current_streak: data.user.current_streak || 0,
          },
          accessToken: data.access_token, // 메모리에만 저장
          isAuthenticated: true,
        })
      },

      logout: async () => {
        const { accessToken } = get()

        try {
          // 서버에 로그아웃 요청 (HttpOnly 쿠키 삭제)
          await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
            },
            credentials: 'include', // HttpOnly 쿠키 전송
          })
        } catch {
          // 로그아웃 요청 실패해도 로컬 상태는 초기화
        }

        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
        })
      },

      refreshToken: async () => {
        const { isRefreshing } = get()

        // 이미 갱신 중이면 중복 요청 방지
        if (isRefreshing) return false

        set({ isRefreshing: true })

        try {
          const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
            method: 'POST',
            credentials: 'include', // HttpOnly 쿠키 전송
          })

          if (!response.ok) {
            // 갱신 실패 시 로그아웃 처리
            set({
              user: null,
              accessToken: null,
              isAuthenticated: false,
              isRefreshing: false,
            })
            return false
          }

          const result = await response.json()
          const data = result.data

          set({
            accessToken: data.access_token,
            isRefreshing: false,
          })

          return true
        } catch {
          set({
            user: null,
            accessToken: null,
            isAuthenticated: false,
            isRefreshing: false,
          })
          return false
        }
      },

      setUser: (user) => set({ user, isAuthenticated: true }),
      setAccessToken: (token) => set({ accessToken: token }),
    }),
    {
      name: 'auth-storage',
      // sessionStorage: 브라우저(탭) 종료 시 자동 로그아웃
      storage: {
        getItem: (name) => {
          const val = sessionStorage.getItem(name)
          return val ? JSON.parse(val) : null
        },
        setItem: (name, value) => sessionStorage.setItem(name, JSON.stringify(value)),
        removeItem: (name) => sessionStorage.removeItem(name),
      },
      // accessToken은 메모리에만 저장 (만료된 토큰이 재사용되는 것 방지)
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        // accessToken 제외 - 페이지 새로고침 시 refresh 엔드포인트로 갱신
      }),
    }
  )
)
