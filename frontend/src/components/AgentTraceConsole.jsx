import { useEffect, useRef } from "react"

const AGENT_COLORS = {
  Coordinator: "text-textPrimary",
  LogParserAgent: "text-cyan",
  IOCEnrichmentAgent: "text-amber",
  MitreMappingAgent: "text-orange",
  CorrelationAgent: "text-crimson",
  ReportAgent: "text-emerald",
}

export default function AgentTraceConsole({ trace, isRunning }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [trace])

  return (
    <div className="rounded-lg border border-border bg-[#0D1017] flex flex-col h-full overflow-hidden shadow-glow">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-panel/50">
        <p className="text-xs uppercase tracking-wide text-textMuted font-mono">
          Agent Reasoning Trace
        </p>
        <span className={`w-2 h-2 rounded-full ${isRunning ? "bg-cyan pulse-dot" : "bg-border"}`} />
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 font-mono text-[12.5px] leading-relaxed space-y-1.5">
        {trace.length === 0 && (
          <p className="text-textMuted/60 italic">
            &gt; awaiting hunt session... click "Run Hunt Session" to activate agents
          </p>
        )}
        {trace.map((t, i) => (
          <div key={i} className="trace-line flex gap-2">
            <span className="text-textMuted/50 shrink-0">
              {new Date(t.timestamp).toLocaleTimeString([], { hour12: false })}
            </span>
            <span className={`shrink-0 font-medium ${AGENT_COLORS[t.agent] || "text-textPrimary"}`}>
              [{t.agent}]
            </span>
            <span className="text-textMuted shrink-0">{t.step}:</span>
            <span className="text-textPrimary">{t.detail}</span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
