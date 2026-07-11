"""
Log Parser Agent
-----------------
Job: read the raw log stream, run deterministic Sigma-style rules to find
candidate events of interest, then ask the LLM to describe in plain
language what pattern each candidate represents and why it's worth
escalating to the enrichment stage.
"""
from datetime import datetime
from ..tools.log_loader import load_logs
from ..tools.sigma_rules import run_all_rules
from ..groq_client import ask_llm

SYSTEM_PROMPT = """You are a SOC log-parsing analyst agent inside an autonomous
threat hunting pipeline. You are given the results of deterministic Sigma-style
rule matches over a log window. For each rule hit, write a short, precise
analyst note (2-3 sentences) explaining what happened and why it's suspicious.
Be concrete: reference hosts, users, IPs and counts you were given.
Respond ONLY in JSON with this shape:
{"notes": [{"rule": "<rule id>", "note": "<analyst note>"}]}
"""


def run(trace: list):
    logs = load_logs()
    rule_hits = run_all_rules(logs)

    trace.append({
        "agent": "LogParserAgent",
        "step": "sigma_rule_scan",
        "detail": f"Scanned {len(logs)} log events across 4 sources against "
                  f"{sum(1 for _ in rule_hits)} Sigma-style rules.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    non_empty_hits = {k: v for k, v in rule_hits.items() if v}

    if not non_empty_hits:
        trace.append({
            "agent": "LogParserAgent", "step": "result",
            "detail": "No rule matches found in this window.",
            "timestamp": datetime.utcnow().isoformat(),
        })
        return {"logs": logs, "rule_hits": {}, "notes": []}

    notes = ask_llm(
        SYSTEM_PROMPT,
        f"Rule hits: {non_empty_hits}",
        json_mode=True,
    )["notes"]

    trace.append({
        "agent": "LogParserAgent", "step": "llm_annotation",
        "detail": f"LLM produced analyst notes for {len(notes)} rule hit group(s).",
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {"logs": logs, "rule_hits": non_empty_hits, "notes": notes}
