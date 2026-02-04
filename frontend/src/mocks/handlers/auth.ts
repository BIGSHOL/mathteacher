// 인증 API Mock 핸들러

import { http, HttpResponse } from 'msw'
import { mockUsers, mockPasswords, findUserByLoginId, verifyPassword, findUserById } from '../data/users'
import type { UserRole } from '../../types'

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
    const body = (await request.json()) as { login_id: string; password: string }
    const { login_id, password } = body

    const user = findUserByLoginId(login_id)
    if (!user || !verifyPassword(login_id, password)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_CREDENTIALS',
            message: '아이디 또는 비밀번호가 올바르지 않습니다.',
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
    if (!currentUser || currentUser.role === 'student' || currentUser.role === 'teacher') {
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
      login_id: string
      password: string
      name: string
      role: string
      grade?: string
      class_id?: string
    }

    const requestedRole = body.role as UserRole

    // admin은 강사/학생만 생성 가능
    if (currentUser.role === 'admin' && !['teacher', 'student'].includes(requestedRole)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: '관리자는 강사 및 학생 계정만 생성할 수 있습니다.',
          },
        },
        { status: 403 }
      )
    }

    // master는 관리자/강사/학생 생성 가능 (다른 master는 불가)
    if (currentUser.role === 'master' && !['admin', 'teacher', 'student'].includes(requestedRole)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: '마스터는 관리자, 강사, 학생 계정만 생성할 수 있습니다.',
          },
        },
        { status: 403 }
      )
    }

    // 아이디 중복 체크
    if (findUserByLoginId(body.login_id)) {
      return HttpResponse.json(
        {
          success: false,
          error: {
            code: 'LOGIN_ID_ALREADY_EXISTS',
            message: '이미 사용 중인 아이디입니다.',
          },
        },
        { status: 400 }
      )
    }

    const newUser = {
      id: `user-${Date.now()}`,
      login_id: body.login_id,
      name: body.name,
      role: requestedRole,
      grade: body.grade,
      class_id: body.class_id,
      level: 1,
      total_xp: 0,
      current_streak: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }

    // mock 데이터에 추가 (세션 내 로그인 가능하도록)
    mockUsers.push(newUser as typeof mockUsers[number])
    mockPasswords[body.login_id] = body.password

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

  // GET /api/v1/admin/users (관리자/마스터 전용)
  http.get('/api/v1/admin/users', ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'UNAUTHORIZED', message: '인증이 필요합니다.' },
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
          error: { code: 'INVALID_TOKEN', message: '유효하지 않은 토큰입니다.' },
        },
        { status: 401 }
      )
    }

    const currentUser = findUserById(parsed.userId)
    if (!currentUser || !['admin', 'master'].includes(currentUser.role)) {
      return HttpResponse.json(
        {
          success: false,
          error: { code: 'FORBIDDEN', message: '권한이 없습니다.' },
        },
        { status: 403 }
      )
    }

    const url = new URL(request.url)
    const roleFilter = url.searchParams.get('role')
    let filteredUsers = mockUsers
    if (roleFilter) {
      filteredUsers = filteredUsers.filter((u) => u.role === roleFilter)
    }

    return HttpResponse.json({
      success: true,
      data: {
        items: filteredUsers.map(({ id, login_id, name, role, grade, class_id, created_at }) => ({
          id, login_id, name, role, grade, class_id, created_at,
        })),
        total: filteredUsers.length,
        page: 1,
        page_size: 50,
        total_pages: 1,
      },
    })
  }),
]
