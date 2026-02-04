// 인증 API 테스트

import { describe, it, expect } from 'vitest'
import api from '../../lib/api'

describe('Auth API', () => {
  describe('POST /api/v1/auth/login', () => {
    it('유효한 자격증명으로 로그인 성공', async () => {
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
      // 먼저 로그인
      const loginResponse = await api.post('/api/v1/auth/login', {
        login_id: 'student01',
        password: 'password123',
      })
      const refreshToken = loginResponse.data.data.refresh_token

      // 토큰 갱신
      const response = await api.post('/api/v1/auth/refresh', {
        refresh_token: refreshToken,
      })

      expect(response.status).toBe(200)
      expect(response.data.data.access_token).toBeDefined()
      expect(response.data.data.refresh_token).toBeDefined()
    })

    it('유효하지 않은 refresh token으로 갱신 실패', async () => {
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
      // 먼저 로그인
      const loginResponse = await api.post('/api/v1/auth/login', {
        login_id: 'student01',
        password: 'password123',
      })
      const accessToken = loginResponse.data.data.access_token

      // 내 정보 조회
      const response = await api.get('/api/v1/auth/me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      })

      expect(response.status).toBe(200)
      expect(response.data.data.login_id).toBe('student01')
    })

    it('인증 없이 조회 실패', async () => {
      try {
        await api.get('/api/v1/auth/me')
      } catch (error: unknown) {
        const err = error as { response: { status: number } }
        expect(err.response.status).toBe(401)
      }
    })
  })
})
