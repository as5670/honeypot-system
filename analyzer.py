import json
import sys
from collections import defaultdict

log_file = "logs.txt"
data_file = "data.json"

ip_count = defaultdict(int)
username_count = defaultdict(int)
total_attempts = 0
skipped_lines = 0

try:
    with open(log_file, "r") as file:
        for line_num, line in enumerate(file, start=1):
            parts = line.strip().split("|")

            # FIX: Warn about skipped invalid lines instead of silently ignoring
            if len(parts) < 4:
                print(f"[!] Skipping malformed line {line_num}: {line.strip()!r}")
                skipped_lines += 1
                continue

            total_attempts += 1

            timestamp = parts[0].strip()
            ip = parts[1].strip()
            username = parts[2].strip()
            password_hash = parts[3].strip()

            ip_count[ip] += 1
            username_count[username] += 1

except FileNotFoundError:
    print(f"[!] {log_file} not found")
    # FIX: Use sys.exit() with proper import instead of bare exit()
    sys.exit(1)

if skipped_lines:
    print(f"[!] {skipped_lines} malformed line(s) were skipped.")

data = {
    "total_attempts": total_attempts,
    "unique_ips": len(ip_count),
    "ip_data": dict(ip_count),
    "username_data": dict(username_count)
}

with open(data_file, "w") as file:
    json.dump(data, file, indent=4)

print(f"✅ Analysis complete. {data_file} created.")
print(f"   Total attempts: {total_attempts} | Unique IPs: {len(ip_count)}")