import { severityStyle } from "../severity"

function ConfidenceBar({ value }) {
  return (
    <div className="w-24 h-1.5 rounded-full bg-border overflow-hidden">
      <div
        className="h-full bg-cyan rounded-full"
        style={{ width: `${value}%` }}
      />
    </div>
  )
}

export default function FindingsList({ findings }) {
  if (!findings || findings.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-panel p-6 text-center text-textMuted text-sm">
        No correlated findings yet. Run a hunt session to populate this panel.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {findings.map((f) => {
        const style = severityStyle(f.severity)
        return (
          <div key={f.id} className={`rounded-lg border ${style.border} bg-panel p-4`}>
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${style.dot}`} />
                <h3 className="font-display font-semibold text-textPrimary">{f.title}</h3>
              </div>
              <span className={`text-[11px] uppercase font-mono px-2 py-0.5 rounded ${style.bg} ${style.text} border ${style.border}`}>
                {f.severity}
              </span>
            </div>

            <p className="text-sm text-textMuted mt-2 leading-relaxed">{f.summary}</p>

            <div className="flex flex-wrap items-center gap-4 mt-3">
              <div className="flex items-center gap-2">
                <span className="text-[11px] text-textMuted font-mono">confidence</span>
                <ConfidenceBar value={f.confidence} />
                <span className="text-[11px] text-textPrimary font-mono">{f.confidence}%</span>
              </div>
              <div className="flex gap-1.5">
                {(f.mitre_techniques || []).map((t) => (
                  <span key={t} className="text-[11px] font-mono px-1.5 py-0.5 rounded bg-panelAlt border border-border text-textMuted">
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-border/60">
              <p className="text-[11px] uppercase tracking-wide text-textMuted font-mono mb-1">
                Recommended Action
              </p>
              <p className="text-sm text-textPrimary">{f.recommended_action}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}
