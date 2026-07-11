import { useState, useRef, useCallback, useEffect } from "react"
import Header from "./components/Header"
import StatCards from "./components/StatCards"
import SeverityChart from "./components/SeverityChart"
import AgentTraceConsole from "./components/AgentTraceConsole"
import MitreHeatmap from "./components/MitreHeatmap"
import FindingsList from "./components/FindingsList"
import ExecutiveSummary from "./components/ExecutiveSummary"
import LogExplorer from "./components/LogExplorer"

const WS_URL = (location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws/hunt"

export default function App() {
  const [status, setStatus] = useState("idle") // idle | running | done
  const [trace, setTrace] = useState([])
  const [findings, setFindings] = useState([])
  const [stats, setStats] = useState(null)
  const [summary, setSummary] = useState("")
  const [sessionId, setSessionId] = useState(null)
  const [logs, setLogs] = useState([])
  const [mitreList, setMitreList] = useState([])
  const wsRef = useRef(null)

  useEffect(() => {
    fetch("/api/logs").then((r) => r.json()).then(setLogs).catch(() => {})
    fetch("/api/mitre").then((r) => r.json()).then(setMitreList).catch(() => {})
  }, [])

  const runHunt = useCallback(() => {
    setStatus("running")
    setTrace([])
    setFindings([])
    setSummary("")
    setStats(null)

    const ws = new WebSocket(WS_URL)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      if (msg.type === "trace") {
        setTrace((prev) => [...prev, msg.event])
      } else if (msg.type === "final") {
        const result = msg.result
        setFindings(result.findings || [])
        setStats(result.stats || null)
        setSummary(result.executive_summary || "")
        setSessionId(result.session_id)
        setStatus("done")
      }
    }

    ws.onerror = () => setStatus("done")
  }, [])

  const isRunning = status === "running"

  return (
    <div className="min-h-screen bg-base flex flex-col">
      <Header status={status} onRun={runHunt} sessionId={sessionId} />

      <main className="flex-1 grid grid-cols-12 gap-4 p-6">
        <div className="col-span-12">
          <ExecutiveSummary summary={summary} isRunning={isRunning} />
        </div>

        <div className="col-span-12">
          <StatCards stats={stats} />
        </div>

        <div className="col-span-4 h-[380px]">
          <AgentTraceConsole trace={trace} isRunning={isRunning} />
        </div>

        <div className="col-span-4 h-[380px]">
          <MitreHeatmap
            techniques={mitreList}
            covered={stats?.mitre_coverage?.covered || []}
          />
        </div>

        <div className="col-span-4 h-[380px] flex flex-col gap-4">
          <SeverityChart stats={stats} />
        </div>

        <div className="col-span-7">
          <p className="text-xs uppercase tracking-wide text-textMuted font-mono mb-2 mt-2">
            Correlated Findings
          </p>
          <FindingsList findings={findings} />
        </div>

        <div className="col-span-5 h-[460px] mt-2">
          <LogExplorer logs={logs} />
        </div>
      </main>

      <footer className="px-6 py-3 border-t border-border text-[11px] text-textMuted font-mono">
        SENTINEL · Agentic AI Threat Hunting Demo · Groq (Llama 3.3 70B) · FastAPI + React
      </footer>
    </div>
  )
}
