import { render, screen } from '@testing-library/react'
import { LoadingSpinner } from '../LoadingSpinner'

describe('LoadingSpinner', () => {
  it('renders with default text', () => {
    render(<LoadingSpinner />)
    expect(screen.getByText('로딩 중...')).toBeTruthy()
  })

  it('renders with custom text', () => {
    render(<LoadingSpinner text="데이터 불러오는 중..." />)
    expect(screen.getByText('데이터 불러오는 중...')).toBeTruthy()
  })

  it('hides text when empty string', () => {
    const { container } = render(<LoadingSpinner text="" />)
    const p = container.querySelector('p')
    expect(p).toBeNull()
  })

  it('renders spinner image', () => {
    render(<LoadingSpinner />)
    const img = screen.getByAltText('로딩 중')
    expect(img).toBeTruthy()
  })

  it('applies size classes', () => {
    const { container: smContainer } = render(<LoadingSpinner size="sm" />)
    expect(smContainer.querySelector('.w-8')).toBeTruthy()

    const { container: lgContainer } = render(<LoadingSpinner size="lg" />)
    expect(lgContainer.querySelector('.w-24')).toBeTruthy()
  })
})
