"""
Generates a synthetic but realistic security log dataset with a mix of
benign noise and 4 injected attack scenarios:

  1. Brute-force login followed by a successful auth (credential access)
  2. Beaconing to a known-bad C2 domain/IP (command & control)
  3. Lateral movement via admin share + remote service creation
  4. Data staging + exfil over DNS (rare but classic evasion technique)

Run this file directly to regenerate backend/data/sample_logs.json.
"""
import json
import random
import uuid
from datetime import datetime, timedelta
random.seed(42)
USERS = ["jsmith", "areyes", "kpatel", "mgarcia", "tlee", "svc_backup", "admin"]
HOSTS = [f"WKS-{n:03d}" for n in range(1, 12)] + ["DC-01", "FILESRV-01"]
BENIGN_IPS = ["10.0.1." + str(n) for n in range(10, 60)]

BAD_IP = "185.220.101.47"          # fake known-bad C2 IP
BAD_DOMAIN = "cdn-update-check.net"  # fake known-bad C2 domain
ATTACKER_IP = "192.168.77.13"        # internal-looking but attacker-controlled

events = []
start = datetime(2026, 7, 8, 2, 0, 0)


def add(minutes_offset, source, host, event_type, raw, user=None, src_ip=None, dst_ip=None):
    ts = start + timedelta(minutes=minutes_offset)
    events.append({
        "id": str(uuid.uuid4())[:8],
        "timestamp": ts.isoformat(),
        "source": source,
        "host": host,
        "user": user,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "event_type": event_type,
        "raw": raw,
    })


# ---- Benign background noise (normal working hours logins, file access, DNS) ----
t = 0
for _ in range(140):
    t += random.randint(1, 6)
    user = random.choice(USERS)
    host = random.choice(HOSTS)
    ip = random.choice(BENIGN_IPS)
    kind = random.choice(["login_success", "file_access", "dns_query", "process_start"])
    if kind == "login_success":
        add(t, "auth", host, "login_success",
            f"User {user} authenticated successfully from {ip}", user=user, src_ip=ip)
    elif kind == "file_access":
        add(t, "endpoint", host, "file_access",
            f"User {user} opened \\\\FILESRV-01\\shared\\report_q3.xlsx", user=user, src_ip=ip)
    elif kind == "dns_query":
        add(t, "dns", host, "dns_query",
            f"Host {host} resolved outlook.office365.com", src_ip=ip)
    else:
        add(t, "endpoint", host, "process_start",
            f"Process chrome.exe started by {user}", user=user, src_ip=ip)

# ---- Scenario 1: brute force -> successful login (credential access, T1110/T1078) ----
victim_host = "WKS-004"
victim_user = "areyes"
base = 400
for i in range(9):
    add(base + i, "auth", victim_host, "login_failure",
        f"Failed login attempt for user {victim_user} from {ATTACKER_IP}",
        user=victim_user, src_ip=ATTACKER_IP)
add(base + 10, "auth", victim_host, "login_success",
    f"User {victim_user} authenticated successfully from {ATTACKER_IP}",
    user=victim_user, src_ip=ATTACKER_IP)

# ---- Scenario 2: C2 beaconing (T1071/T1105) ----
beacon_host = "WKS-004"
for i in range(6):
    add(base + 12 + i * 5, "network", beacon_host, "outbound_connection",
        f"Outbound TCP connection from {beacon_host} to {BAD_IP}:443",
        src_ip="10.0.1.14", dst_ip=BAD_IP)
    add(base + 13 + i * 5, "dns", beacon_host, "dns_query",
        f"Host {beacon_host} resolved {BAD_DOMAIN}", src_ip="10.0.1.14")

# ---- Scenario 3: lateral movement (T1021/T1570) ----
add(base + 55, "endpoint", beacon_host, "admin_share_access",
    f"User {victim_user} accessed \\\\DC-01\\ADMIN$ from {beacon_host}",
    user=victim_user, src_ip="10.0.1.14", dst_ip="10.0.1.5")
add(base + 57, "endpoint", "DC-01", "remote_service_create",
    f"New remote service 'WinUpdateHelper' created on DC-01 by {victim_user}",
    user=victim_user, src_ip="10.0.1.14")

# ---- Scenario 4: DNS exfil (T1048) ----
for i in range(4):
    add(base + 65 + i, "dns", beacon_host, "dns_query",
        f"Host {beacon_host} queried suspicious subdomain "
        f"{uuid.uuid4().hex[:16]}.{BAD_DOMAIN}", src_ip="10.0.1.14")

events.sort(key=lambda e: e["timestamp"])

with open("sample_logs.json", "w") as f:
    json.dump(events, f, indent=2)

print(f"Generated {len(events)} events -> sample_logs.json")
