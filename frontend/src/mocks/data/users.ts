// Mock 사용자 데이터

import type { User } from '../../types'

export const mockUsers: User[] = [
  {
    id: 'student-1',
    email: 'student@test.com',
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
    email: 'student2@test.com',
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
    email: 'teacher@test.com',
    name: '박선생',
    role: 'teacher',
    level: 1,
    total_xp: 0,
    current_streak: 0,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-15T00:00:00Z',
  },
]

export const mockPasswords: Record<string, string> = {
  'student@test.com': 'password123',
  'student2@test.com': 'password123',
  'teacher@test.com': 'password123',
}

export function findUserByEmail(email: string): User | undefined {
  return mockUsers.find((user) => user.email === email)
}

export function findUserById(id: string): User | undefined {
  return mockUsers.find((user) => user.id === id)
}

export function verifyPassword(email: string, password: string): boolean {
  return mockPasswords[email] === password
}
