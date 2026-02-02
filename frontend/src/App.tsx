import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { TestListPage, TestStartPage, TestPlayPage, TestResultPage, MyStatsPage } from './pages/student'
import { TeacherDashboardPage, TeacherStudentsListPage } from './pages/teacher'
import { MainLayout } from './components/layout'
import { ProtectedRoute, PublicRoute } from './components/auth'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 공개 페이지 */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />

        {/* 테스트 플레이 (전체화면, 레이아웃 없음) */}
        <Route
          path="/test/play/:attemptId"
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <TestPlayPage />
            </ProtectedRoute>
          }
        />

        {/* 레이아웃 적용 페이지 */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />

          {/* 학생용 라우트 */}
          <Route
            path="/tests"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <TestListPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/test/:testId"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <TestStartPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/test/result/:attemptId"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <TestResultPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/my-stats"
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <MyStatsPage />
              </ProtectedRoute>
            }
          />

          {/* 강사용 라우트 */}
          <Route
            path="/teacher/dashboard"
            element={
              <ProtectedRoute allowedRoles={['teacher', 'admin']}>
                <TeacherDashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teacher/students"
            element={
              <ProtectedRoute allowedRoles={['teacher', 'admin']}>
                <TeacherStudentsListPage />
              </ProtectedRoute>
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
