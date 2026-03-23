import json

log_file = "logs.txt"
data_file = "data.json"

usernames = {}
total_attempts = 0

try:
    with open(log_file, "r") as file:
        for line in file:
            total_attempts += 1

            parts = line.split("|")
            username_part = parts[0]

            username = username_part.split(":")[1].strip()

            if username in usernames:
                usernames[username] += 1
            else:
                usernames[username] = 1

except FileNotFoundError:
    print("logs.txt not found")
    exit()

data = {
    "total_attempts": total_attempts,
    "usernames": usernames
}

with open(data_file, "w") as file:
    json.dump(data, file, indent=4)

print("Analysis complete. data.json created.") 