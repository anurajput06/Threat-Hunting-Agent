"""
IOC Enrichment Agent
--------------------
Job: take the events flagged by the Log Parser Agent, scan them against
known threat intel (IPs, domains, hashes), and ask the LLM to explain the
significance of any matches in the context of the rule hits already found.
"""
from datetime import datetime
from ..tools.ioc_checker import scan_events_for_iocs
from ..groq_client import ask_llm

SYSTEM_PROMPT = """You are a threat intelligence enrichment agent. You are given
raw IOC (Indicator of Compromise) matches found in log events, plus the
Sigma rule context that flagged those events. Explain, in 2-3 sentences per
match, why this specific IOC match raises confidence that the activity is
malicious rather than coincidental. Respond ONLY in JSON:
{"enrichment": [{"event_id": "<id>", "ioc_value": "<value>", "explanation": "<text>"}]}
"""


def run(trace: list, parsed: dict):
    logs = parsed["logs"]
    matches = scan_events_for_iocs(logs)

    trace.append({
        "agent": "IOCEnrichmentAgent", "step": "ioc_scan",
        "detail": f"Checked {len(logs)} events against known threat intel; "
                  f"found {len(matches)} IOC match(es).",
        "timestamp": datetime.utcnow().isoformat(),
    })

    if not matches:
        return {"matches": [], "enrichment": []}

    compact = [{"event_id": m["event_id"], "field": m["field"],
                "ioc_value": m["ioc"]["value"], "threat": m["ioc"]["threat"],
                "severity": m["ioc"]["severity"]} for m in matches]

    enrichment = ask_llm(
        SYSTEM_PROMPT,
        f"IOC matches: {compact}\nRule hits so far: {parsed.get('rule_hits')}",
        json_mode=True,
    )["enrichment"]

    trace.append({
        "agent": "IOCEnrichmentAgent", "step": "llm_enrichment",
        "detail": f"LLM generated enrichment context for {len(enrichment)} IOC match(es).",
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {"matches": compact, "enrichment": enrichment}
