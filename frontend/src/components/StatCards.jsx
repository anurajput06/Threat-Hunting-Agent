function Card({ label, value, accent }) {
  return (
    <div className="flex-1 min-w-[140px] rounded-lg border border-border bg-panel px-4 py-3">
      <p className="text-[11px] uppercase tracking-wide text-textMuted font-mono">{label}</p>
      <p className={`text-2xl font-display font-semibold mt-1 ${accent || "text-textPrimary"}`}>{value}</p>
    </div>
  )
}

export default function StatCards({ stats }) {
  const s = stats || {}
  const sev = s.severity_counts || {}

  return (
    <div className="flex flex-wrap gap-3">
      <Card label="Events Scanned" value={s.total_events_scanned ?? "—"} />
      <Card label="Rule Hits" value={s.rule_hits ?? "—"} accent="text-cyan" />
      <Card label="IOC Matches" value={s.ioc_matches ?? "—"} accent="text-amber" />
      <Card label="Findings" value={s.findings ?? "—"} accent="text-orange" />
      <Card label="Critical" value={sev.critical ?? 0} accent="text-crimson" />
    </div>
  )
}
