<div align="center">

# 🦅 Agentic Threat Hunting Pipeline

**A multi-agent AI system that autonomously hunts threats in security logs — parsing, enriching, mapping to MITRE ATT&CK, correlating, and reporting, all visible live in a real-time dashboard.**

Built with **FastAPI + Groq (Llama 3.3 70B)** on the backend and **React + Tailwind + Recharts** on the frontend.

</div>

---

## 📌 Overview

HawkEye AI automates the first-pass work of a SOC (Security Operations Center) analyst. Instead of a human manually scanning thousands of log lines, five specialized AI agents work in sequence — each with one clear job — to detect, enrich, map, correlate, and summarize threats, with every step streamed live to a dashboard so you can literally watch the agents reason.

## 🧠 How It Works

```
Raw Logs → Log Parser Agent → IOC Enrichment Agent → MITRE Mapping Agent
         → Correlation Agent → Report Agent → Dashboard
```

| Agent | Job (in short) |
|---|---|
| **Log Parser** | Runs Sigma-style rules on raw logs, flags suspicious patterns |
| **IOC Enrichment** | Checks flagged events against known threat intel (IPs/domains/hashes) |
| **MITRE Mapping** | Confirms which ATT&CK techniques the evidence actually supports |
| **Correlation** | Fuses signals into a small number of findings with severity + confidence scores |
| **Report** | Writes a plain-English executive summary for shift handover |

**Why this design:** rule matching and lookups are deterministic Python (no hallucination risk); the LLM is only used where it's actually useful — explaining *why* something is suspicious, judging evidence, and writing summaries. This also directly answers the classic "how do you reduce false positives" interview question.

## ✨ Features

- 5-agent orchestration pipeline with a live "Agent Reasoning Trace" console (WebSocket streaming)
- Sigma-style rule engine + local MITRE ATT&CK reference + IOC threat-intel lookup
- Synthetic log dataset with 4 realistic attack chains (brute force, C2 beaconing, lateral movement, DNS exfiltration)
- Full dashboard: severity chart, MITRE coverage heatmap, correlated findings with confidence scores, raw log explorer

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, Groq API (Llama 3.3 70B), Pydantic, WebSockets
**Frontend:** React, Vite, Tailwind CSS, Recharts

## 📁 Project Structure

```
threat-hunter-ai/
├── backend/
│   ├── main.py              # FastAPI app (REST + WebSocket)
│   ├── agents/               # 5 agents + coordinator
│   ├── tools/                 # Sigma rules, IOC checker, MITRE DB, log loader
│   └── data/                   # synthetic logs, IOC list, MITRE reference
└── frontend/
    └── src/components/        # dashboard UI components
```

## 🚀 Setup & Run

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # then paste your Groq API key inside
cd ..
uvicorn backend.main:app --reload --port 8000
```
Get a free Groq API key: https://console.groq.com/keys

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` → click **Run Hunt Session**.

## 🎯 Sample Detection Scenarios

| Scenario | MITRE Techniques |
|---|---|
| Brute-force login → success | T1110, T1078 |
| C2 beaconing to flagged IP/domain | T1071, T1105 |
| Lateral movement via admin share | T1021, T1570, T1543 |
| DNS tunneling / exfiltration | T1048 |


## 👤 Author

**Anu**
GitHub: [@anurajput06](https://github.com/anurajput06)

## 📄 Note

The log dataset and threat intel used in this project are synthetic/fictional, built for demonstration purposes only.
