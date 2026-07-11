"""
FastAPI entrypoint.

Run from the project root (one level above this file) with:
    uvicorn backend.main:app --reload --port 8000

Endpoints:
    POST /api/hunt          -> runs a full hunt session, returns findings + trace
    GET  /api/logs          -> raw sample log events (for the log viewer panel)
    GET  /api/mitre         -> full local MITRE ATT&CK reference list
    WS   /ws/hunt           -> runs a hunt and streams trace events live as they happen
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .agents import coordinator
from .tools.log_loader import load_logs
from .tools.mitre_db import all_techniques

app = FastAPI(title="Agentic Threat Hunting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this for production use
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/hunt")
def run_hunt():
    """Runs the full pipeline synchronously and returns the complete result."""
    result = coordinator.run_hunt()
    return result


@app.get("/api/logs")
def get_logs():
    return load_logs()


@app.get("/api/mitre")
def get_mitre():
    return all_techniques()


@app.websocket("/ws/hunt")
async def ws_hunt(websocket: WebSocket):
    """
    Streams trace events to the client as the pipeline produces them, giving
    the dashboard's live 'Agent Activity Feed' its real-time feel. The
    coordinator itself runs synchronously (LLM calls are blocking), so we
    run it in a thread and poll the shared trace list for new entries.
    """
    await websocket.accept()
    trace = []
    result_holder = {}

    def worker():
        result_holder["result"] = coordinator.run_hunt_with_trace(trace)

    try:
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, worker)

        sent = 0
        while not task.done() or sent < len(trace):
            if sent < len(trace):
                await websocket.send_json({"type": "trace", "event": trace[sent]})
                sent += 1
            else:
                await asyncio.sleep(0.15)

        await websocket.send_json({"type": "final", "result": result_holder["result"]})
    except WebSocketDisconnect:
        pass
