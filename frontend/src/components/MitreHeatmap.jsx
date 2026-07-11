export default function MitreHeatmap({ techniques, covered }) {
  const coveredSet = new Set(covered || [])

  const byTactic = {}
  for (const t of techniques) {
    byTactic[t.tactic] = byTactic[t.tactic] || []
    byTactic[t.tactic].push(t)
  }

  return (
    <div className="rounded-lg border border-border bg-panel p-4 h-full overflow-y-auto">
      <p className="text-xs uppercase tracking-wide text-textMuted font-mono mb-3">
        MITRE ATT&amp;CK Coverage
      </p>
      <div className="space-y-3">
        {Object.entries(byTactic).map(([tactic, techs]) => (
          <div key={tactic}>
            <p className="text-[11px] text-textMuted mb-1.5">{tactic}</p>
            <div className="flex flex-wrap gap-1.5">
              {techs.map((t) => {
                const isCovered = coveredSet.has(t.technique_id)
                return (
                  <div
                    key={t.technique_id}
                    title={`${t.name}: ${t.description}`}
                    className={`px-2 py-1 rounded text-[11px] font-mono border transition
                      ${isCovered
                        ? "bg-crimson/15 border-crimson/40 text-crimson"
                        : "bg-panelAlt border-border text-textMuted"}`}
                  >
                    {t.technique_id}
                  </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
