import { useEffect, useState } from 'react'
import { profileApi } from '../api/endpoints'
import { useAuth } from '../context/AuthContext'
import { useFetch } from '../hooks'
import { Spinner, ErrorBanner, StatCard } from '../components/UI'

export default function ProfilePage() {
  // Auth context
  const { username, logout } = useAuth()

  // Local UI state
  const [handle, setHandle] = useState('')
  const [saved, setSaved] = useState(false)

  /**
   * Fetch profile hook
   */
  const {
    data: profile,
    loading,
    error,
    execute: fetchProfile
  } = useFetch(profileApi.getMyProfile)

  /**
   * Update CF handle hook
   */
  const {
    loading: saving,
    error: saveError,
    execute: updateHandle
  } = useFetch(profileApi.updateCfHandle)

  /**
   * Load profile on mount
   */
  useEffect(() => {
    async function loadProfile() {
      const data = await fetchProfile()

      if (data) {
        setHandle(data.cf_handle || '')
      }
    }

    loadProfile()
  }, [fetchProfile])

  /**
   * Save Codeforces handle
   */
  async function saveHandle() {
    setSaved(false)

    const result = await updateHandle(handle)

    if (result) {
      setSaved(true)

      // Hide success after 2 sec
      setTimeout(() => setSaved(false), 2000)
    }
  }

  if (loading) return <Spinner />

  if (error || saveError) {
    return <ErrorBanner msg={error || saveError} />
  }

  return (
    <div className="space-y-6 animate-fade-in">

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-bold">
            Profile
          </h1>

          <p className="text-void-300 font-mono text-xs mt-1">
            Your account & stats overview
          </p>
        </div>

      
      </div>

      {/* User card */}
      <div className="glass rounded-xl p-6 flex items-center gap-5">

        {/* Avatar */}
        <div
          className="
            w-16 h-16 rounded-full
            bg-brand-500
            flex items-center justify-center
            font-display font-black text-2xl
            text-void-900
          "
        >
          {username?.[0]?.toUpperCase() || '?'}
        </div>

        <div>
          <p className="font-display font-bold text-xl">
            {username}
          </p>

          <p className="font-mono text-xs text-void-400 mt-0.5">
            CF Rating:{' '}
            <span className="text-brand-400">
              {profile?.rating ?? 1200}
            </span>
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

        <StatCard
          label="Problems Solved"
          value={profile?.total_solved ?? 0}
          accent
        />

        <StatCard
          label="Total Attempted"
          value={profile?.total_attempted ?? 0}
        />

        <StatCard
          label="Accuracy"
          value={`${profile?.accuracy ?? 0}%`}
        />

        <StatCard
          label="Active Days"
          value={profile?.active_days ?? 0}
          sub="Days practiced"
        />
      </div>

      {/* CF Handle */}
      <div className="card p-5">

        <h3 className="font-display font-semibold mb-3 text-sm">
          Codeforces Handle
        </h3>

        <p className="font-mono text-xs text-void-400 mb-4">
          Set once — Dashboard will autofill automatically
        </p>

        <div className="flex gap-3">

          <input
            className="
              terminal-input flex-1
              px-4 py-2.5 rounded-md text-sm
            "
            value={handle}
            onChange={e => setHandle(e.target.value)}
            placeholder="tourist"
          />

          <button
            onClick={saveHandle}
            disabled={saving}
            className="
              btn-primary px-5 py-2.5
              rounded-md text-sm
            "
          >
            {saving
              ? 'Saving…'
              : saved
                ? '✓ Saved!'
                : 'Save'}
          </button>

        </div>
      </div>
    </div>
  )
}