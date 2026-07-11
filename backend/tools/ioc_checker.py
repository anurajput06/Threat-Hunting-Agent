import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA_DIR, "known_iocs.json")) as f:
    _IOCS = json.load(f)

_IOC_INDEX = {i["value"]: i for i in _IOCS}


def check_ioc(value: str):
    """Returns the IOC record if value is a known bad IP/domain/hash, else None."""
    return _IOC_INDEX.get(value)


def scan_events_for_iocs(events):
    """Scan a list of log events for any field matching a known IOC."""
    matches = []
    for e in events:
        for field in ("src_ip", "dst_ip"):
            val = e.get(field)
            if val and val in _IOC_INDEX:
                matches.append({"event_id": e["id"], "field": field, "ioc": _IOC_INDEX[val]})
        if e.get("raw"):
            for domain_ioc in [i for i in _IOCS if i["type"] == "domain"]:
                if domain_ioc["value"] in e["raw"]:
                    matches.append({"event_id": e["id"], "field": "raw", "ioc": domain_ioc})
    return matches
