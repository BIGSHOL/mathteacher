// Mock 사용자 데이터

import type { User } from '../../types'

export const mockUsers: User[] = [
  {
    id: 'student-1',
    login_id: 'student01',
    name: '김철수',
    role: 'student',
    grade: 'middle_1',
    class_id: 'class-1',
    level: 3,
    total_xp: 450,
    current_streak: 5,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'student-2',
    login_id: 'student02',
    name: '이영희',
    role: 'student',
    grade: 'middle_1',
    class_id: 'class-1',
    level: 5,
    total_xp: 820,
    current_streak: 12,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'teacher-1',
    login_id: 'teacher01',
    name: '박선생',
    role: 'teacher',
    level: 1,
    total_xp: 0,
    current_streak: 0,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'admin-1',
    login_id: 'admin01',
    name: '최관리',
    role: 'admin',
    level: 1,
    total_xp: 0,
    current_streak: 0,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
  {
    id: 'master-1',
    login_id: 'master01',
    name: '정마스터',
    role: 'master',
    level: 1,
    total_xp: 0,
    current_streak: 0,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
]

export const mockPasswords: Record<string, string> = {
  'student01': 'password123',
  'student02': 'password123',
  'teacher01': 'password123',
  'admin01': 'password123',
  'master01': 'password123',
}

export function findUserByLoginId(login_id: string): User | undefined {
  return mockUsers.find((user) => user.login_id === login_id)
}

export function findUserById(id: string): User | undefined {
  return mockUsers.find((user) => user.id === id)
}

export function verifyPassword(login_id: string, password: string): boolean {
  return mockPasswords[login_id] === password
}
