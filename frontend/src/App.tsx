import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import { MainLayout } from './components/layout'
import { ProtectedRoute, PublicRoute } from './components/auth'

// 공통 페이지 (즉시 로드)
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

// 학생 페이지 (lazy load)
const DailyLabPage = lazy(() => import('./pages/student/DailyLabPage').then(m => ({ default: m.DailyLabPage })))
const TestListPage = lazy(() => import('./pages/student/TestListPage').then(m => ({ default: m.TestListPage })))
const TestStartPage = lazy(() => import('./pages/student/TestStartPage').then(m => ({ default: m.TestStartPage })))
const TestPlayPage = lazy(() => import('./pages/student/TestPlayPage').then(m => ({ default: m.TestPlayPage })))
const TestResultPage = lazy(() => import('./pages/student/TestResultPage').then(m => ({ default: m.TestResultPage })))
const MyStatsPage = lazy(() => import('./pages/student/MyStatsPage').then(m => ({ default: m.MyStatsPage })))
const ReviewPage = lazy(() => import('./pages/student/ReviewPage').then(m => ({ default: m.ReviewPage })))
const QuickPracticeSetupPage = lazy(() => import('./pages/student/QuickPracticeSetupPage').then(m => ({ default: m.QuickPracticeSetupPage })))
const HelpPage = lazy(() => import('./pages/student/HelpPage').then(m => ({ default: m.HelpPage })))
const ProfilePage = lazy(() => import('./pages/student/ProfilePage').then(m => ({ default: m.ProfilePage })))
const FocusCheckPage = lazy(() => import('./pages/student/FocusCheckPage').then(m => ({ default: m.FocusCheckPage })))
const LeaderboardPage = lazy(() => import('./pages/student/LeaderboardPage').then(m => ({ default: m.LeaderboardPage })))
const ShopPage = lazy(() => import('./pages/student/ShopPage').then(m => ({ default: m.ShopPage })))
const InventoryPage = lazy(() => import('./pages/student/InventoryPage').then(m => ({ default: m.InventoryPage })))

// 강사 페이지 (lazy load)
const TeacherDashboardPage = lazy(() => import('./pages/teacher').then(m => ({ default: m.TeacherDashboardPage })))
const TeacherStudentsListPage = lazy(() => import('./pages/teacher').then(m => ({ default: m.TeacherStudentsListPage })))
const TeacherStudentDetailPage = lazy(() => import('./pages/teacher').then(m => ({ default: m.TeacherStudentDetailPage })))

// 관리자 페이지 (lazy load)
const QuestionBankPage = lazy(() => import('./pages/admin/QuestionBankPage').then(m => ({ default: m.QuestionBankPage })))
const UserManagementPage = lazy(() => import('./pages/admin/UserManagementPage').then(m => ({ default: m.UserManagementPage })))
const QuestionGenerationPage = lazy(() => import('./pages/admin/QuestionGenerationPage').then(m => ({ default: m.QuestionGenerationPage })))

function PageLoader() {
  return (
    <div className="flex min-h-[50vh] items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent" />
    </div>
  )
}

function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Suspense fallback={<PageLoader />}>
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
              path="/daily-lab"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <DailyLabPage />
                </ProtectedRoute>
              }
            />
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
            <Route
              path="/review"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <ReviewPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/practice"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <QuickPracticeSetupPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/help"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <HelpPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/focus-check"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <FocusCheckPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/leaderboard"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <LeaderboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/shop"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <ShopPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/inventory"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <InventoryPage />
                </ProtectedRoute>
              }
            />

            {/* 강사용 라우트 */}
            <Route
              path="/teacher/dashboard"
              element={
                <ProtectedRoute allowedRoles={['teacher', 'admin', 'master']}>
                  <TeacherDashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/students"
              element={
                <ProtectedRoute allowedRoles={['teacher', 'admin', 'master']}>
                  <TeacherStudentsListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/teacher/students/:studentId"
              element={
                <ProtectedRoute allowedRoles={['teacher', 'admin', 'master']}>
                  <TeacherStudentDetailPage />
                </ProtectedRoute>
              }
            />

            {/* 관리자용 라우트 */}
            <Route
              path="/admin/questions"
              element={
                <ProtectedRoute allowedRoles={['admin', 'master']}>
                  <QuestionBankPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/users"
              element={
                <ProtectedRoute allowedRoles={['admin', 'master']}>
                  <UserManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/generate"
              element={
                <ProtectedRoute allowedRoles={['master']}>
                  <QuestionGenerationPage />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
