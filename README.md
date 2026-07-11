# SENTINEL — Agentic AI for Automated Threat Hunting

A multi-agent AI system that autonomously hunts for threats in security logs:
it parses raw events, matches them against Sigma-style detection rules,
enriches hits with threat intel (IOC lookups), maps confirmed activity to
MITRE ATT&CK techniques, correlates everything into a small number of
high-confidence findings, and writes a shift-handover executive summary —
all visible live in a dashboard as the agents work.

Built with **FastAPI + Groq (Llama 3.3 70B)** on the backend and
**React + Tailwind + Recharts** on the frontend.

---

## 1. Architecture

```
Raw Logs (synthetic dataset, 4 injected attack scenarios)
        │
        ▼
┌─────────────────────┐
│  Log Parser Agent    │  Sigma-style rule engine + LLM analyst notes
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  IOC Enrichment Agent │  Threat intel lookups (IP/domain/hash) + LLM context
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  MITRE Mapping Agent  │  Confirms ATT&CK techniques against grounded reference
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Correlation Agent    │  Fuses signals into Findings + severity/confidence
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Report Agent         │  Executive summary for shift handover
└─────────┬────────────┘
          ▼
     Coordinator (orchestrates all of the above, emits a live trace)
```

Each agent is a small Python module with one job. The Coordinator runs them
in sequence and every agent appends structured events to a shared `trace`
list — this is what the dashboard's **Agent Reasoning Trace** console
streams live over a WebSocket, so a viewer can literally watch the agents
think and hand off work to each other.

**Why deterministic tools + LLM reasoning (not just "ask the LLM everything")：**
The Sigma-rule engine and MITRE/IOC lookups are plain Python — deterministic,
auditable, no hallucination risk. The LLM is used specifically for what it's
good at: explaining *why* a pattern is suspicious, judging whether evidence
actually supports a MITRE technique, and writing natural-language summaries.
This split is also the answer to "how do you reduce false positives" in an
interview — confidence scores are grounded in how many independent
deterministic signals corroborate each other, not just LLM vibes.

---

## 2. Project structure

```
threat-hunter-ai/
├── backend/
│   ├── main.py                  # FastAPI app (REST + WebSocket)
│   ├── groq_client.py           # Groq API wrapper
│   ├── models.py                # Pydantic schemas
│   ├── agents/
│   │   ├── coordinator.py
│   │   ├── log_parser_agent.py
│   │   ├── ioc_enrichment_agent.py
│   │   ├── mitre_mapping_agent.py
│   │   ├── correlation_agent.py
│   │   └── report_agent.py
│   ├── tools/
│   │   ├── log_loader.py
│   │   ├── ioc_checker.py
│   │   ├── mitre_db.py
│   │   └── sigma_rules.py
│   ├── data/
│   │   ├── generate_logs.py     # regenerates sample_logs.json
│   │   ├── sample_logs.json     # 168 synthetic events, 4 attack scenarios
│   │   ├── known_iocs.json
│   │   └── mitre_attack.json
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   └── components/          # Header, StatCards, SeverityChart,
    │                             # AgentTraceConsole, MitreHeatmap,
    │                             # FindingsList, ExecutiveSummary, LogExplorer
    ├── package.json
    └── vite.config.js
```

---

## 3. Setup & run

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and paste your Groq API key (https://console.groq.com/keys)

cd ..                              # run from project root so package imports resolve
uvicorn backend.main:app --reload --port 8000
```

Verify it's up: open `http://localhost:8000/api/health` → `{"status":"ok"}`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`, click **Run Hunt Session**, and watch the
Agent Reasoning Trace populate live as each agent completes its step,
followed by correlated findings, a MITRE ATT&CK coverage heatmap, and an
executive summary.

### Regenerating the log dataset (optional)

```bash
cd backend/data
python3 generate_logs.py
```

This reseeds the synthetic dataset — 4 attack chains (brute force →
credential access, C2 beaconing, lateral movement, DNS exfiltration) mixed
into ~140 benign background events.

---

## 4. What each attack scenario in the dataset represents

| Scenario | MITRE Techniques | What the pipeline should catch |
|---|---|---|
| 9 failed logins → 1 success, same source IP | T1110, T1078 | `SIGMA-BF-001` rule fires, correlated as credential access |
| Repeated outbound connections to a flagged external IP/domain | T1071, T1105 | `SIGMA-C2-002` fires, IOC match on the C2 IP/domain |
| ADMIN$ share access → new remote service created | T1021, T1570, T1543 | `SIGMA-LM-003` fires, lateral movement chain |
| Repeated long/random-looking DNS subdomain queries | T1048 | `SIGMA-EX-004` fires, exfiltration-over-DNS pattern |

The Correlation Agent is expected to fuse the brute-force → beacon →
lateral-movement events (they share a host/user) into **one** high-severity
finding rather than three separate low-confidence ones — that's the "false
positive reduction" story to walk through in interviews.

---
