from auto_web_learn import auto_learn
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def main():
    # Run auto-learning
    logs = auto_learn(log_enabled=True)

    # Print summary
    print(f"[MoonAI] Total entries added: {len(logs)}")
    for log in logs:
        print(log)

    # Save logs to a file with timestamp
    if logs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(LOGS_DIR, f"moonai_log_{timestamp}.txt")
        with open(log_file, "w", encoding="utf-8") as f:
            for log in logs:
                f.write(log + "\n")
        print(f"[MoonAI] Logs saved to {log_file}")

if __name__ == "__main__":
    main()
