// 로그인 페이지 테스트 (RED 상태)

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { LoginPage } from '../../pages/LoginPage'

const mockNavigate = vi.fn()

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

describe('LoginPage', () => {
  const renderLogin = () => {
    return render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )
  }

  beforeEach(() => {
    mockNavigate.mockClear()
  })

  describe('렌더링', () => {
    it('아이디 입력 필드가 표시된다', () => {
      renderLogin()
      expect(screen.getByLabelText(/아이디/i)).toBeInTheDocument()
    })

    it('비밀번호 입력 필드가 표시된다', () => {
      renderLogin()
      expect(screen.getByLabelText(/비밀번호/i)).toBeInTheDocument()
    })

    it('로그인 버튼이 표시된다', () => {
      renderLogin()
      expect(screen.getByRole('button', { name: /로그인/i })).toBeInTheDocument()
    })
  })

  describe('폼 제출', () => {
    it('유효한 자격증명으로 로그인 성공 시 대시보드로 이동한다', async () => {
      // fetch 모킹: 성공 응답
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          success: true,
          data: {
            user: { id: 'u1', login_id: 'student01', name: 'S1', role: 'student' },
            access_token: 'at',
            refresh_token: 'rt'
          }
        })
      } as Response)

      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/아이디/i), 'student01')
      await user.type(screen.getByLabelText(/비밀번호/i), 'password123')
      await user.click(screen.getByRole('button', { name: /로그인/i }))

      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalled()
      })
    })

    it('잘못된 자격증명으로 로그인 실패 시 에러 메시지가 표시된다', async () => {
      // fetch 모킹: 실패 응답
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        json: async () => ({
          error: { message: '로그인에 실패했습니다.' }
        })
      } as Response)

      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/아이디/i), 'student01')
      await user.type(screen.getByLabelText(/비밀번호/i), 'wrong_password')
      await user.click(screen.getByRole('button', { name: /로그인/i }))

      await waitFor(() => {
        expect(screen.getByText(/로그인에 실패했습니다/i)).toBeInTheDocument()
      })
    })

    it('아이디 필드가 비어있으면 제출되지 않는다', async () => {
      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/비밀번호/i), 'password123')
      await user.click(screen.getByRole('button', { name: /로그인/i }))

      expect(mockNavigate).not.toHaveBeenCalled()
    })

    it('비밀번호 필드가 비어있으면 제출되지 않는다', async () => {
      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/아이디/i), 'student01')
      await user.click(screen.getByRole('button', { name: /로그인/i }))

      expect(mockNavigate).not.toHaveBeenCalled()
    })
  })

  describe('로딩 상태', () => {
    it('로그인 요청 중에는 버튼이 비활성화된다', async () => {
      // 딜레이가 있는 fetch 모킹
      let resolveFetch: (value: Response) => void
      const fetchPromise = new Promise<Response>((resolve) => {
        resolveFetch = resolve
      })
      vi.mocked(fetch).mockReturnValueOnce(fetchPromise)

      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/아이디/i), 'student01')
      await user.type(screen.getByLabelText(/비밀번호/i), 'password123')

      const button = screen.getByRole('button', { name: /로그인/i })
      await user.click(button)

      // 로딩 중 상태 확인
      expect(button).toBeDisabled()

      // 마무리
      resolveFetch!({
        ok: true,
        json: async () => ({ success: true, data: { user: { role: 'student' }, access_token: 'at' } })
      } as Response)
    })

    it('로그인 요청 중에는 로딩 텍스트가 표시된다', async () => {
      // 딜레이가 있는 fetch 모킹
      let resolveFetch: (value: Response) => void
      const fetchPromise = new Promise<Response>((resolve) => {
        resolveFetch = resolve
      })
      vi.mocked(fetch).mockReturnValueOnce(fetchPromise)

      const user = userEvent.setup()
      renderLogin()

      await user.type(screen.getByLabelText(/아이디/i), 'student01')
      await user.type(screen.getByLabelText(/비밀번호/i), 'password123')
      await user.click(screen.getByRole('button', { name: /로그인/i }))

      expect(screen.getByText(/로그인 중/i)).toBeInTheDocument()

      // 마무리
      resolveFetch!({
        ok: true,
        json: async () => ({ success: true, data: { user: { role: 'student' }, access_token: 'at' } })
      } as Response)
    })
  })
})
