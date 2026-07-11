export default function ExecutiveSummary({ summary, isRunning }) {
  if (!summary && !isRunning) return null

  return (
    <div className="rounded-lg border border-cyan/25 bg-cyan/5 px-4 py-3">
      <p className="text-[11px] uppercase tracking-wide text-cyan font-mono mb-1">
        Shift Handover Brief
      </p>
      <p className="text-sm text-textPrimary leading-relaxed">
        {isRunning ? "Generating executive summary..." : summary}
      </p>
    </div>
  )
}
