import { useState, useMemo } from "react"

const SOURCE_COLORS = {
  auth: "text-cyan",
  network: "text-amber",
  endpoint: "text-orange",
  dns: "text-emerald",
}

export default function LogExplorer({ logs }) {
  const [filter, setFilter] = useState("all")
  const [search, setSearch] = useState("")

  const sources = useMemo(() => ["all", ...new Set(logs.map((l) => l.source))], [logs])

  const filtered = useMemo(() => {
    return logs.filter((l) => {
      const matchesSource = filter === "all" || l.source === filter
      const matchesSearch = search === "" ||
        l.raw.toLowerCase().includes(search.toLowerCase()) ||
        (l.host || "").toLowerCase().includes(search.toLowerCase())
      return matchesSource && matchesSearch
    })
  }, [logs, filter, search])

  return (
    <div className="rounded-lg border border-border bg-panel flex flex-col h-full overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-border bg-panel/50">
        <p className="text-xs uppercase tracking-wide text-textMuted font-mono mr-auto">
          Raw Log Explorer ({filtered.length})
        </p>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-panelAlt border border-border rounded text-xs px-2 py-1 text-textPrimary font-mono"
        >
          {sources.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <input
          placeholder="search host / raw..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-panelAlt border border-border rounded text-xs px-2 py-1 text-textPrimary font-mono w-44 placeholder:text-textMuted/50"
        />
      </div>

      <div className="flex-1 overflow-y-auto font-mono text-[11.5px]">
        <table className="w-full">
          <tbody>
            {filtered.slice(0, 300).map((l) => (
              <tr key={l.id} className="border-b border-border/40 hover:bg-panelAlt/60">
                <td className="px-3 py-1.5 text-textMuted/60 whitespace-nowrap">
                  {new Date(l.timestamp).toLocaleTimeString([], { hour12: false })}
                </td>
                <td className={`px-2 py-1.5 whitespace-nowrap ${SOURCE_COLORS[l.source] || "text-textMuted"}`}>
                  {l.source}
                </td>
                <td className="px-2 py-1.5 whitespace-nowrap text-textMuted">{l.host}</td>
                <td className="px-3 py-1.5 text-textPrimary">{l.raw}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
