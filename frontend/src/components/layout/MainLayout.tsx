// 메인 레이아웃 컴포넌트

import { Outlet } from 'react-router-dom'
import { Header } from './Header'

export function MainLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>
        <Outlet />
      </main>
    </div>
  )
}
