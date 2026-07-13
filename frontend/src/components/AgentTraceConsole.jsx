import { useEffect, useRef } from "react"

const AGENT_COLORS = {
  Coordinator: "text-[#E8EAED]",
  LogParserAgent: "text-[#4CC9F0]",
  IOCEnrichmentAgent: "text-[#F2A65A]",
  MitreMappingAgent: "text-[#FF8F5E]",
  CorrelationAgent: "text-[#F0656B]",
  ReportAgent: "text-[#3DDC97]",
}

export default function AgentTraceConsole({ trace, isRunning }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [trace])

  return (
    <div className="rounded-lg border border-border bg-[#0B0D10] flex flex-col h-full overflow-hidden shadow-glow">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-[#232833] bg-[#101317]">
        <p className="text-xs uppercase tracking-wide text-[#8B93A1] font-mono">
          Agent Reasoning Trace
        </p>
        <span className={`w-2 h-2 rounded-full ${isRunning ? "bg-cyan pulse-dot" : "bg-[#3A414D]"}`} />
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 font-mono text-[12.5px] leading-relaxed space-y-1.5">
        {trace.length === 0 && (
          <p className="text-[#8B93A1]/60 italic">
            &gt; awaiting hunt session... click "Run Hunt Session" to activate agents
          </p>
        )}
        {trace.map((t, i) => (
          <div key={i} className="trace-line flex gap-2">
            <span className="text-[#8B93A1]/60 shrink-0">
              {new Date(t.timestamp).toLocaleTimeString([], { hour12: false })}
            </span>
            <span className={`shrink-0 font-medium ${AGENT_COLORS[t.agent] || "text-[#E8EAED]"}`}>
              [{t.agent}]
            </span>
            <span className="text-[#8B93A1] shrink-0">{t.step}:</span>
            <span className="text-[#E8EAED]">{t.detail}</span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
