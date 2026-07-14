"""
Correlation Agent
------------------
Job: fuse rule hits + IOC enrichment + confirmed MITRE mappings into a
small number of coherent "Findings" - the same way a human analyst would
group scattered signals into one incident narrative. Also assigns
severity and a confidence score, explicitly reasoning about false-positive
risk (this is the "false positive reduction" story piece).
"""
from datetime import datetime
import uuid
from ..groq_client import ask_llm
SYSTEM_PROMPT = """You are a SOC correlation agent responsible for fusing
signals from three upstream agents (log parsing, IOC enrichment, MITRE
mapping) into a small number of coherent security findings. Group related
rule hits into a single finding when they plausibly represent one attack
chain (e.g. brute force -> beaconing -> lateral movement on the same host
is ONE finding, not three). For each finding, assign:
 - severity: low | medium | high | critical
 - confidence: an integer 0-100, reflecting how much corroborating evidence
   exists (multiple independent signals = higher confidence; a single
   weak signal = lower confidence, explicitly to reduce false positives)
 - a short title and 2-3 sentence summary of the attack narrative
 - recommended_action: one concrete next step for a human analyst

Respond ONLY in JSON:
{"findings": [{"title": "...", "severity": "...", "confidence": 0,
  "mitre_techniques": ["T####"], "summary": "...", "recommended_action": "..."}]}
"""


def run(trace: list, parsed: dict, enriched: dict, mapped: dict):
    if not parsed.get("rule_hits"):
        trace.append({
            "agent": "CorrelationAgent", "step": "result",
            "detail": "No findings to correlate - environment appears clean for this window.",
            "timestamp": datetime.utcnow().isoformat(),
        })
        return []

    context = {
        "rule_hits": parsed.get("rule_hits"),
        "parser_notes": parsed.get("notes"),
        "ioc_matches": enriched.get("matches"),
        "ioc_enrichment": enriched.get("enrichment"),
        "mitre_mappings": mapped.get("mappings"),
    }

    trace.append({
        "agent": "CorrelationAgent", "step": "fusing_signals",
        "detail": "Fusing rule hits, IOC enrichment, and confirmed MITRE "
                  "techniques into coherent findings.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    result = ask_llm(SYSTEM_PROMPT, str(context), json_mode=True)
    findings = result["findings"]

    for f in findings:
        f["id"] = str(uuid.uuid4())[:8]
        f.setdefault("related_events", [])
        f.setdefault("iocs_matched", [m["ioc_value"] for m in enriched.get("matches", [])])

    trace.append({
        "agent": "CorrelationAgent", "step": "result",
        "detail": f"Produced {len(findings)} correlated finding(s).",
        "timestamp": datetime.utcnow().isoformat(),
    })

    return findings
