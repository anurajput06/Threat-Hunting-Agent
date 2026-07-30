import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_logs():
    with open(os.path.join(DATA_DIR, "sample_logs.json")) as f:
        return json.load(f)
def filter_by_source(logs, source):
    return [e for e in logs if e["source"] == source]
def group_by_host(logs):
    hosts = {}
    for e in logs:
        hosts.setdefault(e["host"], []).append(e)
    return hosts


def count_login_failures(logs):
    """Deterministic heuristic: hosts/users with >=5 failed logins in the window."""
    counts = {}
    for e in logs:
        if e["event_type"] == "login_failure":
            key = (e["host"], e.get("user"), e.get("src_ip"))
            counts[key] = counts.get(key, 0) + 1
    return {k: v for k, v in counts.items() if v >= 5}
