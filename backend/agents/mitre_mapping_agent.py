"""
MITRE Mapping Agent
--------------------
Job: given rule hits + IOC enrichment, confirm and justify which MITRE
ATT&CK techniques are represented, using the local technique reference
as grounding context (prevents the LLM from hallucinating technique IDs).
"""
from datetime import datetime
from ..tools.mitre_db import techniques_as_prompt_context
from ..tools.sigma_rules import RULES
from ..groq_client import ask_llm
SYSTEM_PROMPT = """You are a MITRE ATT&CK mapping agent. You are given a
reference list of valid ATT&CK techniques, plus rule hits and IOC enrichment
notes from earlier pipeline stages. Each Sigma-style rule already suggests
candidate technique IDs - your job is to confirm whether the evidence
actually supports each suggested technique, using ONLY technique IDs that
appear in the reference list. Respond ONLY in JSON:
{"mappings": [{"technique_id": "<id>", "confirmed": true/false, "justification": "<1-2 sentences>"}]}
"""


def run(trace: list, parsed: dict, enriched: dict):
    rule_hits = parsed.get("rule_hits", {})
    if not rule_hits:
        return {"mappings": []}

    candidate_rules = [r for r in RULES if r["id"] in rule_hits]
    candidate_techniques = sorted({t for r in candidate_rules for t in r["mitre"]})

    trace.append({
        "agent": "MitreMappingAgent", "step": "candidate_selection",
        "detail": f"Identified {len(candidate_techniques)} candidate technique(s) "
                  f"from {len(candidate_rules)} triggered rule(s): {', '.join(candidate_techniques)}.",
        "timestamp": datetime.utcnow().isoformat(),
    })

    mappings = ask_llm(
        SYSTEM_PROMPT,
        f"Reference techniques:\n{techniques_as_prompt_context()}\n\n"
        f"Candidate technique IDs to evaluate: {candidate_techniques}\n"
        f"Rule hits: {rule_hits}\nIOC enrichment: {enriched.get('enrichment')}",
        json_mode=True,
    )["mappings"]

    trace.append({
        "agent": "MitreMappingAgent", "step": "llm_confirmation",
        "detail": f"LLM confirmed {sum(1 for m in mappings if m.get('confirmed'))} "
                  f"of {len(mappings)} candidate technique(s).",
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {"mappings": mappings}
