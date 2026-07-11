export default function Header({ status, onRun, sessionId }) {
  const isRunning = status === "running"

  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-panel/60 backdrop-blur">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-cyan/10 border border-cyan/30 flex items-center justify-center">
          <span className="font-display font-bold text-cyan text-sm">S</span>
        </div>
        <div>
          <h1 className="font-display font-bold text-lg tracking-tight text-textPrimary leading-none">
            SENTINEL
          </h1>
          <p className="text-[11px] text-textMuted font-mono tracking-wide leading-none mt-1">
            AGENTIC THREAT HUNTING PIPELINE
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {sessionId && (
          <span className="text-xs font-mono text-textMuted border border-border rounded px-2 py-1">
            session:{sessionId}
          </span>
        )}
        <div className="flex items-center gap-2 text-xs font-mono text-textMuted">
          <span className={`w-2 h-2 rounded-full ${isRunning ? "bg-cyan pulse-dot" : "bg-emerald"}`} />
          {isRunning ? "AGENTS ACTIVE" : "IDLE"}
        </div>
        <button
          onClick={onRun}
          disabled={isRunning}
          className="px-4 py-2 rounded-md bg-cyan/10 border border-cyan/40 text-cyan text-sm font-medium
                     hover:bg-cyan/20 hover:shadow-glow transition disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isRunning ? "Hunting..." : "Run Hunt Session"}
        </button>
      </div>
    </header>
  )
}
