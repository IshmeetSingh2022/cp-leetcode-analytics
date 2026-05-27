import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Sidebar       from './components/Sidebar'
import AuthPage      from './pages/AuthPage'
import Dashboard     from './pages/Dashboard'
import AnalysisPage  from './pages/AnalysisPage'
import ProgressPage  from './pages/ProgressPage'
import RecommendPage from './pages/RecommendPage'
import StatsPage     from './pages/StatsPage'
import ProfilePage   from './pages/ProfilePage'
import TopicTracker  from './pages/Topic_tracker'   // ✅ NAYA

function AppLayout() {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />

  return (
    <div className="min-h-screen grid-bg">
      <Sidebar />
      <main className="ml-56 p-8 max-w-5xl">
        <Routes>
          <Route path="/"          element={<Dashboard />}     />
          <Route path="/analysis"  element={<AnalysisPage />}  />
          <Route path="/progress"  element={<ProgressPage />}  />
          <Route path="/recommend" element={<RecommendPage />} />
          <Route path="/stats"     element={<StatsPage />}     />
          <Route path="/profile"   element={<ProfilePage />}   />
          <Route path="/topics"    element={<TopicTracker />}  />  {/* ✅ NAYA */}
          <Route path="*"          element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<AuthGate />} />
        <Route path="/*"     element={<AppLayout />} />
      </Routes>
    </AuthProvider>
  )
}

function AuthGate() {
  const { token } = useAuth()
  return token ? <Navigate to="/" replace /> : <AuthPage />
}