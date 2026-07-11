"""
Report Agent
-------------
Job: write a short executive summary across all correlated findings -
the kind of 3-4 sentence brief a SOC lead could paste into a Slack
channel or incident ticket at the start of a shift.
"""
from datetime import datetime
from ..groq_client import ask_llm

SYSTEM_PROMPT = """You are a SOC reporting agent. Given a list of correlated
security findings, write a concise executive summary (4-6 sentences,
plain English, no bullet points) suitable for a shift-handover brief.
Mention the overall risk level, the most severe finding, and whether
immediate action is recommended. Respond ONLY in JSON:
{"executive_summary": "..."}
"""


def run(trace: list, findings: list):
    if not findings:
        summary = ("No suspicious activity was correlated in this hunting window. "
                   "The environment appears within normal operating baseline.")
        trace.append({
            "agent": "ReportAgent", "step": "result",
            "detail": "Generated clean-bill-of-health summary.",
            "timestamp": datetime.utcnow().isoformat(),
        })
        return summary

    result = ask_llm(SYSTEM_PROMPT, str(findings), json_mode=True)

    trace.append({
        "agent": "ReportAgent", "step": "executive_summary",
        "detail": "Generated executive summary for shift handover.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    return result["executive_summary"]
