import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from "recharts"

const COLORS = { low: "#3DDC97", medium: "#F2A65A", high: "#FF7A45", critical: "#E5484D" }

export default function SeverityChart({ stats }) {
  const sev = stats?.severity_counts || { low: 0, medium: 0, high: 0, critical: 0 }
  const data = Object.entries(sev).map(([name, value]) => ({ name, value }))

  return (
    <div className="rounded-lg border border-border bg-panel p-4 h-full">
      <p className="text-xs uppercase tracking-wide text-textMuted font-mono mb-3">
        Findings by Severity
      </p>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={data} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#232833" vertical={false} />
          <XAxis dataKey="name" stroke="#8B93A1" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="#8B93A1" fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
          <Tooltip
            contentStyle={{ background: "#171C27", border: "1px solid #232833", borderRadius: 6, fontSize: 12 }}
            labelStyle={{ color: "#E6E8EB" }}
          />
          <Bar dataKey="value" radius={[4, 4, 0, 0]}>
            {data.map((d) => <Cell key={d.name} fill={COLORS[d.name]} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
