import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
  role: 'student' | 'teacher' | 'admin'
  level: number
  total_xp: number
  current_streak: number
}

interface AuthState {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  setAccessToken: (token: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        const response = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail?.message || 'Login failed')
        }

        const result = await response.json()
        const data = result.data

        set({
          user: {
            id: data.user.id,
            email: data.user.email,
            name: data.user.name,
            role: data.user.role,
            level: data.user.level || 1,
            total_xp: data.user.total_xp || 0,
            current_streak: data.user.current_streak || 0,
          },
          accessToken: data.access_token,
          isAuthenticated: true,
        })
      },

      logout: () => {
        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
        })
      },

      setUser: (user) => set({ user, isAuthenticated: true }),
      setAccessToken: (token) => set({ accessToken: token }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
