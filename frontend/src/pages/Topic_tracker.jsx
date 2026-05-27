import { useEffect, useState } from 'react'
import { topicApi } from '../api/endpoints'
import { Spinner, ErrorBanner } from '../components/UI'

function topicStatus(impSolved, impTotal, totalSolved) {
  if (impSolved === impTotal && impTotal > 0)
    return { icon: '✅', color: '#22c55e', label: 'Mastered' }

  if (totalSolved >= 3)
    return { icon: '⚠️', color: '#eab308', label: 'In Progress' }

  return { icon: '❌', color: '#ef4444', label: 'Not Started' }
}

function ratingColor(r) {
  if (r >= 2400) return '#ff4444'
  if (r >= 2100) return '#ff8c00'
  if (r >= 1900) return '#aa00ff'
  if (r >= 1700) return '#4488ff'
  if (r >= 1500) return '#22c55e'
  return '#aaaaaa'
}

function ProblemRow({ problem }) {
  return (
    <div
      className={`
        flex items-center gap-3 px-4 py-2.5 rounded-lg border transition-all
        ${
          problem.solved
            ? 'bg-brand-500/5 border-brand-500/20'
            : 'bg-void-800/30 border-void-700/30'
        }
      `}
    >
      <span className="text-sm flex-shrink-0">
        {problem.solved ? '✅' : '❌'}
      </span>

      <span
        className={`flex-1 font-mono text-xs
          ${
            problem.solved
              ? 'line-through text-void-500'
              : 'text-void-200'
          }`}
      >
        {problem.name}
      </span>

      <a
        href={`https://codeforces.com/problemset/problem/${problem.pid.slice(
          0,
          -1
        )}/${problem.pid.slice(-1)}`}
        target="_blank"
        rel="noreferrer"
        className="font-mono text-[10px] text-void-500 hover:text-brand-400 transition-colors"
      >
        {problem.pid} ↗
      </a>

      <span
        className="font-mono text-[10px] px-2 py-0.5 rounded-full"
        style={{
          color: ratingColor(problem.rating),
          background: ratingColor(problem.rating) + '20',
        }}
      >
        {problem.rating}
      </span>
    </div>
  )
}

function TopicSection({ topic }) {
  const [open, setOpen] = useState(false)

  const status = topicStatus(
    topic.imp_solved,
    topic.imp_total,
    topic.total_solved
  )

  const percent = topic.imp_total
    ? Math.round((topic.imp_solved / topic.imp_total) * 100)
    : 0

  return (
    <div className="card overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-4 px-5 py-4
                   hover:bg-void-700/20 transition-colors text-left"
      >
        <span className="text-lg flex-shrink-0">{status.icon}</span>

        <span className="font-display font-semibold text-sm flex-1">
          {topic.label}
        </span>

        <span className="font-mono text-xs text-void-400">
          {topic.total_solved} solved overall
        </span>

        <span
          className="font-mono text-xs px-2 py-1 rounded"
          style={{
            color: status.color,
            background: status.color + '15',
          }}
        >
          {topic.imp_solved}/{topic.imp_total} key problems
        </span>

        <span
          className={`text-void-500 text-xs transition-transform duration-200
            ${open ? 'rotate-90' : ''}`}
        >
          ▶
        </span>
      </button>

      {open && (
        <div className="px-4 pb-4 flex flex-col gap-2">
          <div className="flex items-center gap-3 mb-2 px-1">
            <div className="flex-1 h-1.5 bg-void-700 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${percent}%`,
                  background: status.color,
                }}
              />
            </div>

            <span className="font-mono text-[10px] text-void-400">
              {percent}%
            </span>
          </div>

          {topic.problems.map(p => (
            <ProblemRow key={p.pid} problem={p} />
          ))}

          <a
            href={`https://codeforces.com/problemset?tags=${encodeURIComponent(
              topic.tag
            )}`}
            target="_blank"
            rel="noreferrer"
            className="font-mono text-[10px] text-void-500 hover:text-brand-400
                       transition-colors mt-1 px-1"
          >
            + More {topic.label} problems on Codeforces ↗
          </a>
        </div>
      )}
    </div>
  )
}

export default function TopicTracker() {
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    topicApi
      .getTracker()
      .then(setTopics)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const mastered = topics.filter(
    t => t.imp_solved === t.imp_total && t.imp_total > 0
  ).length

  const inProgress = topics.filter(
    t => t.total_solved >= 3 && t.imp_solved < t.imp_total
  ).length

  const notStarted = topics.filter(
    t => t.total_solved < 3
  ).length

  const filtered = topics.filter(t => {
    if (filter === 'mastered')
      return t.imp_solved === t.imp_total && t.imp_total > 0

    if (filter === 'in_progress')
      return t.total_solved >= 3 && t.imp_solved < t.imp_total

    if (filter === 'not_started')
      return t.total_solved < 3

    return true
  })

  if (loading) return <Spinner />
  if (error) return <ErrorBanner msg={error} />

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="font-display text-2xl font-bold">
          Topic Tracker
        </h1>

        <p className="text-void-300 font-mono text-xs mt-1">
          Important DSA topics + key problems — solved status
          tumhare CF submissions se
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="card p-4 text-center">
          <p className="text-2xl font-black font-display text-brand-400">
            {mastered}
          </p>

          <p className="font-mono text-xs text-void-400 mt-1">
            ✅ Mastered
          </p>
        </div>

        <div className="card p-4 text-center">
          <p className="text-2xl font-black font-display text-yellow-400">
            {inProgress}
          </p>

          <p className="font-mono text-xs text-void-400 mt-1">
            ⚠️ In Progress
          </p>
        </div>

        <div className="card p-4 text-center">
          <p className="text-2xl font-black font-display text-red-400">
            {notStarted}
          </p>

          <p className="font-mono text-xs text-void-400 mt-1">
            ❌ Not Started
          </p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {[
          { key: 'all', label: 'All' },
          { key: 'mastered', label: '✅ Mastered' },
          { key: 'in_progress', label: '⚠️ In Progress' },
          { key: 'not_started', label: '❌ Not Started' },
        ].map(f => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            className={`font-mono text-xs px-3 py-2 rounded-md transition-all
              ${
                filter === f.key
                  ? 'bg-brand-500 text-void-900 font-bold'
                  : 'bg-void-800 text-void-400 hover:text-void-200'
              }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-3">
        {filtered.length > 0 ? (
          filtered.map(topic => (
            <TopicSection key={topic.tag} topic={topic} />
          ))
        ) : (
          <div className="card p-8 text-center">
            <p className="font-mono text-sm text-void-400">
              {topics.length === 0
                ? 'Koi data nahi — pehle Dashboard pe CF handle search karo'
                : 'Is filter mein koi topic nahi'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}