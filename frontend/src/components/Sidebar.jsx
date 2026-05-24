import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { RatingBadge } from './UI'

const NAV_ITEMS = [
  { to: '/',           icon: '◈', label: 'Dashboard'     },
  { to: '/analysis',   icon: '◎', label: 'Analysis'      },
  { to: '/progress',   icon: '▲', label: 'Progress'      },
  { to: '/recommend',  icon: '⬡', label: 'Recommend'     },
  { to: '/stats',      icon: '▬', label: 'My Stats'      },
  { to: '/profile', icon: '◉', label: 'Profile' },
]

export default function Sidebar() {
  const { username, logout } = useAuth()

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-56 glass border-r border-void-600 flex flex-col z-50">

      {/* Logo */}
      <div className="p-5 border-b border-void-600">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-sm bg-brand-500 flex items-center justify-center
                          text-void-900 font-display font-black text-xs">
            CP
          </div>
          <span className="font-display font-semibold text-sm">Analytics AI</span>
        </div>
      </div>

      {/* User pill */}
      <div className="px-5 py-4 border-b border-void-600">
        <div className="text-void-400 font-mono text-xs mb-0.5">Signed in as</div>
        <div className="font-mono text-sm text-void-100 truncate">{username}</div>
        <div className="mt-1">
          <RatingBadge rating={1200} />
        </div>
      </div>

      {/* Nav links */}
      <nav className="flex-1 py-4 flex flex-col gap-1 px-3">
        {NAV_ITEMS.map(({ to, icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-all w-full
               ${isActive
                 ? 'bg-brand-500/10 text-brand-400 font-semibold'
                 : 'text-void-300 hover:text-void-100 hover:bg-void-700/50'}`
            }
          >
            <span className="text-base leading-none">{icon}</span>
            <span className="font-display">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-void-600">
        <button onClick={logout} className="btn-ghost px-4 py-2 rounded-md text-xs w-full">
          ← Logout
        </button>
      </div>

    </aside>
  )
}
