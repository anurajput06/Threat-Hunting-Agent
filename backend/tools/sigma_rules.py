"""
Simplified Sigma-style rules. Real Sigma rules are YAML with field/condition
matching against SIEM schemas; this mirrors that structure with plain Python
so the project can demo the concept without a full Sigma engine dependency.
"""

RULES = [
    {
        "id": "SIGMA-BF-001",
        "name": "Multiple failed logins followed by success",
        "logsource": "auth",
        "description": "Detects >=5 failed logins from the same source followed by a success, "
                        "a classic brute-force -> credential access pattern.",
        "mitre": ["T1110", "T1078"],
    },
    {
        "id": "SIGMA-C2-002",
        "name": "Repeated beaconing to a single external host",
        "logsource": "network",
        "description": "Detects periodic outbound connections to the same external IP/domain, "
                        "suggestive of C2 beaconing.",
        "mitre": ["T1071", "T1105"],
    },
    {
        "id": "SIGMA-LM-003",
        "name": "Admin share access followed by remote service creation",
        "logsource": "endpoint",
        "description": "Detects ADMIN$ share access followed by a new remote service, "
                        "a common lateral movement + persistence chain.",
        "mitre": ["T1021", "T1570", "T1543"],
    },
    {
        "id": "SIGMA-EX-004",
        "name": "High-entropy DNS subdomain queries",
        "logsource": "dns",
        "description": "Detects repeated queries to random-looking subdomains of the same "
                        "parent domain, indicative of DNS tunneling / exfiltration.",
        "mitre": ["T1048"],
    },
]


def match_bruteforce(logs):
    from .log_loader import count_login_failures
    hits = count_login_failures(logs)
    results = []
    for (host, user, ip), count in hits.items():
        success = any(
            e for e in logs
            if e["event_type"] == "login_success" and e["host"] == host
            and e.get("user") == user and e.get("src_ip") == ip
        )
        if success:
            results.append({"rule": "SIGMA-BF-001", "host": host, "user": user,
                             "src_ip": ip, "failed_attempts": count})
    return results


def match_beaconing(logs):
    from collections import Counter
    conns = [e for e in logs if e["event_type"] == "outbound_connection"]
    counts = Counter((e["host"], e["dst_ip"]) for e in conns)
    return [{"rule": "SIGMA-C2-002", "host": h, "dst_ip": ip, "connections": c}
            for (h, ip), c in counts.items() if c >= 4]


def match_lateral_movement(logs):
    admin_access = [e for e in logs if e["event_type"] == "admin_share_access"]
    svc_create = [e for e in logs if e["event_type"] == "remote_service_create"]
    results = []
    for a in admin_access:
        for s in svc_create:
            if a.get("user") == s.get("user"):
                results.append({"rule": "SIGMA-LM-003",
                                 "user": a["user"],
                                 "from_host": a["host"],
                                 "to_host": s["host"]})
    return results


def match_dns_exfil(logs):
    dns_events = [e for e in logs if e["event_type"] == "dns_query"]
    from collections import defaultdict
    by_host = defaultdict(list)
    for e in dns_events:
        by_host[e["host"]].append(e)
    results = []
    for host, events in by_host.items():
        long_subdomains = [e for e in events if len(e["raw"]) > 90]
        if len(long_subdomains) >= 3:
            results.append({"rule": "SIGMA-EX-004", "host": host,
                             "suspicious_queries": len(long_subdomains)})
    return results


def run_all_rules(logs):
    return {
        "SIGMA-BF-001": match_bruteforce(logs),
        "SIGMA-C2-002": match_beaconing(logs),
        "SIGMA-LM-003": match_lateral_movement(logs),
        "SIGMA-EX-004": match_dns_exfil(logs),
    }
