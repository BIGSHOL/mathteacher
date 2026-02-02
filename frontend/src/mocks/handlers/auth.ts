// 인증 API Mock 핸들러

import { http, HttpResponse } from 'msw'
import { findUserByEmail, verifyPassword, findUserById } from '../data/users'

// 간단한 토큰 생성 (실제로는 JWT 사용)
function generateToken(userId: string, type: 'access' | 'refresh'): string {
  return `mock_${type}_token_${userId}_${Date.now()}`
}

function parseToken(token: string): { userId: string } | null {
  const match = token.match(/mock_(access|refresh)_token_([^_]+)_/)
  if (match) {
    return { userId: match[2] as string }
  }
  return null
}

// 저장된 refresh 토큰 (실제로는 DB에 저장)
const validRefreshTokens = new Set<string>()

export const authHandlers = [
  // POST /api/v1/auth/login
  http.post('/api/v1/auth/login', async ({ request }) => {
    const body = (await request.json()) as { email: string; password: string }
    const { email, password } = body

    const user = findUserByEmail(email)
    if (!user || !verifyPassword(email, password)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_CREDENTIALS',
            message: '이메일 또는 비밀번호가 올바르지 않습니다.',
          },
        },
        { status: 401 }
      )
    }

    const accessToken = generateToken(user.id, 'access')
    const refreshToken = generateToken(user.id, 'refresh')
    validRefreshTokens.add(refreshToken)

    return HttpResponse.json({
      success: true,
      data: {
        user,
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: 'bearer',
        expires_in: 1800, // 30분
      },
    })
  }),

  // POST /api/v1/auth/refresh
  http.post('/api/v1/auth/refresh', async ({ request }) => {
    const body = (await request.json()) as { refresh_token: string }
    const { refresh_token: refreshToken } = body

    if (!validRefreshTokens.has(refreshToken)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '유효하지 않은 토큰입니다.',
          },
        },
        { status: 401 }
      )
    }

    const parsed = parseToken(refreshToken)
    if (!parsed) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '유효하지 않은 토큰입니다.',
          },
        },
        { status: 401 }
      )
    }

    // 기존 토큰 무효화 후 새 토큰 발급
    validRefreshTokens.delete(refreshToken)
    const newAccessToken = generateToken(parsed.userId, 'access')
    const newRefreshToken = generateToken(parsed.userId, 'refresh')
    validRefreshTokens.add(newRefreshToken)

    return HttpResponse.json({
      success: true,
      data: {
        access_token: newAccessToken,
        refresh_token: newRefreshToken,
        token_type: 'bearer',
        expires_in: 1800,
      },
    })
  }),

  // POST /api/v1/auth/logout
  http.post('/api/v1/auth/logout', async ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '인증이 필요합니다.',
          },
        },
        { status: 401 }
      )
    }

    const body = (await request.json()) as { refresh_token: string }
    validRefreshTokens.delete(body.refresh_token)

    return HttpResponse.json({
      success: true,
      data: {
        message: '로그아웃 성공',
      },
    })
  }),

  // GET /api/v1/auth/me
  http.get('/api/v1/auth/me', ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '인증이 필요합니다.',
          },
        },
        { status: 401 }
      )
    }

    const token = authHeader.replace('Bearer ', '')
    const parsed = parseToken(token)
    if (!parsed) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '유효하지 않은 토큰입니다.',
          },
        },
        { status: 401 }
      )
    }

    const user = findUserById(parsed.userId)
    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'USER_NOT_FOUND',
            message: '사용자를 찾을 수 없습니다.',
          },
        },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      success: true,
      data: user,
    })
  }),

  // POST /api/v1/auth/register
  http.post('/api/v1/auth/register', async ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '인증이 필요합니다.',
          },
        },
        { status: 401 }
      )
    }

    const token = authHeader.replace('Bearer ', '')
    const parsed = parseToken(token)
    if (!parsed) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '유효하지 않은 토큰입니다.',
          },
        },
        { status: 401 }
      )
    }

    const currentUser = findUserById(parsed.userId)
    if (!currentUser || currentUser.role === 'student') {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: '권한이 없습니다.',
          },
        },
        { status: 403 }
      )
    }

    const body = (await request.json()) as {
      email: string
      password: string
      name: string
      role: string
      grade?: string
      class_id?: string
    }

    // 이메일 중복 체크
    if (findUserByEmail(body.email)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'EMAIL_ALREADY_EXISTS',
            message: '이미 사용 중인 이메일입니다.',
          },
        },
        { status: 400 }
      )
    }

    const newUser = {
      id: `user-${Date.now()}`,
      email: body.email,
      name: body.name,
      role: body.role as 'student' | 'teacher' | 'admin',
      grade: body.grade,
      class_id: body.class_id,
      level: 1,
      total_xp: 0,
      current_streak: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }

    return HttpResponse.json(
      {
        success: true,
        data: {
          user: newUser,
          message: '사용자가 등록되었습니다.',
        },
      },
      { status: 201 }
    )
  }),
]
