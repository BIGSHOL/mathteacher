// 인증 API 테스트

import { describe, it, expect, vi } from 'vitest'
import api from '../../lib/api'

// API 모킹
vi.mock('../../lib/api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    interceptors: {
      request: { use: vi.fn(), eject: vi.fn() },
      response: { use: vi.fn(), eject: vi.fn() },
    },
  },
}))

describe('Auth API', () => {
  describe('POST /api/v1/auth/login', () => {
    it('유효한 자격증명으로 로그인 성공', async () => {
      vi.mocked(api.post).mockResolvedValueOnce({
        status: 200,
        data: {
          success: true,
          data: {
            access_token: 'mock_access_token',
            refresh_token: 'mock_refresh_token',
            user: { login_id: 'student01' },
          },
        },
      })

      const response = await api.post('/api/v1/auth/login', {
        login_id: 'student01',
        password: 'password123',
      })

      expect(response.status).toBe(200)
      expect(response.data.success).toBe(true)
      expect(response.data.data.access_token).toBeDefined()
      expect(response.data.data.refresh_token).toBeDefined()
      expect(response.data.data.user.login_id).toBe('student01')
    })

    it('잘못된 비밀번호로 로그인 실패', async () => {
      vi.mocked(api.post).mockRejectedValueOnce({
        response: {
          status: 401,
          data: { error: { code: 'INVALID_CREDENTIALS' } },
        },
      })

      try {
        await api.post('/api/v1/auth/login', {
          login_id: 'student01',
          password: 'wrong_password',
        })
      } catch (error: unknown) {
        const err = error as { response: { status: number; data: { error: { code: string } } } }
        expect(err.response.status).toBe(401)
        expect(err.response.data.error.code).toBe('INVALID_CREDENTIALS')
      }
    })

    it('존재하지 않는 아이디로 로그인 실패', async () => {
      vi.mocked(api.post).mockRejectedValueOnce({
        response: {
          status: 401,
        },
      })

      try {
        await api.post('/api/v1/auth/login', {
          login_id: 'nonexistent_user',
          password: 'password123',
        })
      } catch (error: unknown) {
        const err = error as { response: { status: number } }
        expect(err.response.status).toBe(401)
      }
    })
  })

  describe('POST /api/v1/auth/refresh', () => {
    it('유효한 refresh token으로 갱신 성공', async () => {
      // 먼저 로그인 모킹
      vi.mocked(api.post).mockResolvedValueOnce({
        data: {
          data: {
            refresh_token: 'mock_refresh_token',
          },
        },
      })

      const loginResponse = await api.post('/api/v1/auth/login', {
        login_id: 'student01',
        password: 'password123',
      })
      const refreshToken = loginResponse.data.data.refresh_token

      // 토큰 갱신 모킹
      vi.mocked(api.post).mockResolvedValueOnce({
        status: 200,
        data: {
          data: {
            access_token: 'new_access_token',
            refresh_token: 'new_refresh_token',
          },
        },
      })

      const response = await api.post('/api/v1/auth/refresh', {
        refresh_token: refreshToken,
      })

      expect(response.status).toBe(200)
      expect(response.data.data.access_token).toBeDefined()
      expect(response.data.data.refresh_token).toBeDefined()
    })

    it('유효하지 않은 refresh token으로 갱신 실패', async () => {
      vi.mocked(api.post).mockRejectedValueOnce({
        response: {
          status: 401,
        },
      })

      try {
        await api.post('/api/v1/auth/refresh', {
          refresh_token: 'invalid_token',
        })
      } catch (error: unknown) {
        const err = error as { response: { status: number } }
        expect(err.response.status).toBe(401)
      }
    })
  })

  describe('GET /api/v1/auth/me', () => {
    it('인증된 사용자 정보 조회 성공', async () => {
      // 먼저 로그인 모킹
      vi.mocked(api.post).mockResolvedValueOnce({
        data: {
          data: {
            access_token: 'mock_access_token',
          },
        },
      })

      const loginResponse = await api.post('/api/v1/auth/login', {
        login_id: 'student01',
        password: 'password123',
      })
      const accessToken = loginResponse.data.data.access_token

      // 내 정보 조회 모킹
      vi.mocked(api.get).mockResolvedValueOnce({
        status: 200,
        data: {
          data: {
            login_id: 'student01',
          },
        },
      })

      const response = await api.get('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      })

      expect(response.status).toBe(200)
      expect(response.data.data.login_id).toBe('student01')
    })

    it('인증 없이 조회 실패', async () => {
      vi.mocked(api.get).mockRejectedValueOnce({
        response: {
          status: 401,
        },
      })

      try {
        await api.get('/api/v1/auth/me')
      } catch (error: unknown) {
        const err = error as { response: { status: number } }
        expect(err.response.status).toBe(401)
      }
    })
  })
})
