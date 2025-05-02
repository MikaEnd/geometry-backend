import sys
from pathlib import Path

LOG_FILE = Path("logs/AGENT_INTERACTION_LOG.txt")

def tail_markdown_blocks(n=5):
    if not LOG_FILE.exists():
        print("❌ Лог-файл не найден.")
        return

    with open(LOG_FILE, encoding="utf-8") as f:
        content = f.read().strip().split("---\n")

    last_blocks = content[-n:] if n > 0 else content
    print("\n\n".join(block.strip() for block in last_blocks if block.strip()))

if __name__ == "__main__":
    try:
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except ValueError:
        count = 5

    tail_markdown_blocks(count)
