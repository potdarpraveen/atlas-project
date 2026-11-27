import random
from datetime import datetime, timedelta
from pathlib import Path

# Define WORKDIR based on the previously set workdir string variable
WORKDIR = Path(r"D:\atlas-project\atlas-project")  # Adjust this path as needed

def make_support_log(path: Path, n: int = 50_000, seed: int = 7) -> Path:
    rng = random.Random(seed)
    codes = ["E1042", "E2001", "E3003", "E4004", "E5005", "E6006",
             "E7007", "E8008", "E9009", "E1100", "E1200", "E1300"]
    weights = [30, 12, 9, 7, 6, 5, 4, 3, 2, 2, 1, 1]
    messages = {
        "E1042": "Disk quota exceeded", "E2001": "Upstream timeout", "E3003": "Auth token expired",
        "E4004": "Ticket not found", "E5005": "Rate limit hit", "E6006": "Index rebuild failed",
        "E7007": "Mailbox unreachable", "E8008": "Bad request payload", "E9009": "Certificate expired",
        "E1100": "VPN tunnel dropped", "E1200": "SSO redirect loop", "E1300": "Queue backlog high",
    }
    infos = ["started", "user login ok", "cache warmed", "sync complete", "heartbeat"]
    warns = ["slow query 2.3s", "retrying request", "memory at 81%", "deprecated endpoint used"]
    start = datetime(2026, 11, 20, 0, 0, 0)
    lines: list[str] = []
    for i in range(n):
        ts = (start + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
        r = rng.random()
        if lines and r < 0.05:                      # exact duplicate of the previous line
            lines.append(lines[-1])
        elif r < 0.07:                              # malformed
            lines.append(rng.choice(["garbage line", "", "#### truncated", f"{ts} ERROR"]))
        elif r < 0.47:
            code = rng.choices(codes, weights)[0]
            lines.append(f"{ts} ERROR {code} {messages[code]}")
        elif r < 0.67:
            lines.append(f"{ts} WARN {rng.choice(warns)}")
        else:
            lines.append(f"{ts} INFO {rng.choice(infos)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path

LOG = make_support_log(WORKDIR / "support.log")
print(f"{LOG.name}: {sum(1 for _ in LOG.open()):,} lines")
print(*LOG.read_text().splitlines()[:6], sep="\n")