export const SEVERITY_STYLES = {
  low:      { text: "text-emerald",  bg: "bg-emerald/10",  border: "border-emerald/30",  dot: "bg-emerald"  },
  medium:   { text: "text-amber",    bg: "bg-amber/10",    border: "border-amber/30",    dot: "bg-amber"    },
  high:     { text: "text-orange",   bg: "bg-orange/10",   border: "border-orange/30",   dot: "bg-orange"   },
  critical: { text: "text-crimson",  bg: "bg-crimson/10",  border: "border-crimson/30",  dot: "bg-crimson"  },
}

export const SEVERITY_ORDER = ["critical", "high", "medium", "low"]

export function severityStyle(sev) {
  return SEVERITY_STYLES[sev] || SEVERITY_STYLES.low
}
