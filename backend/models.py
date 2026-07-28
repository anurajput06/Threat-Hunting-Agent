"""
Pydantic models shared across the agent pipeline.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class LogEvent(BaseModel):
    id: str
    timestamp: str
    source: str            # e.g. "auth", "network", "endpoint", "dns"
    host: str
    user: Optional[str] = None
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    event_type: str
    raw: str                # raw log line, what the LLM actually reads
class IOC(BaseModel):
    value: str
    type: str               # ip, domain, hash
    threat: str
    severity: str


class MitreTechnique(BaseModel):
    technique_id: str
    name: str
    tactic: str
    description: str


class AgentTraceEvent(BaseModel):
    agent: str
    step: str
    detail: str
    timestamp: str


class Finding(BaseModel):
    id: str
    title: str
    severity: str            # low, medium, high, critical
    confidence: int           # 0-100
    related_events: List[str]
    mitre_techniques: List[str]
    iocs_matched: List[str]
    summary: str
    recommended_action: str


class HuntResult(BaseModel):
    session_id: str
    findings: List[Finding]
    stats: Dict[str, Any]
    trace: List[AgentTraceEvent]
