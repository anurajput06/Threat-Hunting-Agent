"""
Coordinator Agent
------------------
The orchestrator. Runs the pipeline in sequence:

  LogParserAgent -> IOCEnrichmentAgent -> MitreMappingAgent
      -> CorrelationAgent -> ReportAgent

Every step appends structured entries to a shared `trace` list, which is
what powers the live "Agent Activity Feed" in the dashboard. In the API
layer this trace is streamed over a WebSocket as it's produced.
"""
import uuid
from datetime import datetime
from . import log_parser_agent, ioc_enrichment_agent, mitre_mapping_agent
from . import correlation_agent, report_agent
from ..tools.mitre_db import all_techniques
def run_hunt():
    """Runs a hunt with its own internal trace list (used by the plain REST endpoint)."""
    trace = []
    return _run_pipeline(trace)
def run_hunt_with_trace(trace: list):
    """Runs a hunt appending to an externally-owned trace list (used by the
    WebSocket endpoint so the caller can poll `trace` for live updates while
    this function is still executing on a worker thread)."""
    return _run_pipeline(trace)
def _run_pipeline(trace: list):
    session_id = str(uuid.uuid4())[:8]

    trace.append({
        "agent": "Coordinator", "step": "session_start",
        "detail": f"Starting autonomous threat hunt session {session_id}.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    parsed = log_parser_agent.run(trace)
    enriched = ioc_enrichment_agent.run(trace, parsed)
    mapped = mitre_mapping_agent.run(trace, parsed, enriched)
    findings = correlation_agent.run(trace, parsed, enriched, mapped)
    summary = report_agent.run(trace, findings)

    trace.append({
        "agent": "Coordinator", "step": "session_complete",
        "detail": f"Hunt session {session_id} complete. "
                  f"{len(findings)} finding(s) produced.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for f in findings:
        sev = f.get("severity", "low")
        if sev in severity_counts:
            severity_counts[sev] += 1

    covered_techniques = sorted({t for f in findings for t in f.get("mitre_techniques", [])})

    stats = {
        "total_events_scanned": len(parsed["logs"]),
        "rule_hits": len(parsed.get("rule_hits", {})),
        "ioc_matches": len(enriched.get("matches", [])),
        "findings": len(findings),
        "severity_counts": severity_counts,
        "mitre_coverage": {
            "total_techniques": len(all_techniques()),
            "covered": covered_techniques,
        },
    }

    return {
        "session_id": session_id,
        "findings": findings,
        "executive_summary": summary,
        "stats": stats,
        "trace": trace,
    }
