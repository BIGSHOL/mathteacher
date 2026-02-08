// Vitest 설정

import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

// Global Fetch Mock
const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

// window.location Mock (for auth redirects)
const mockLocation = {
  pathname: '/',
  href: '',
}
vi.stubGlobal('location', mockLocation)

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})
