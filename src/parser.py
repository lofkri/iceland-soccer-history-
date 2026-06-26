from pathlib import Path
import re

RAW_FILE = Path("data/raw/1990.html")

# Match lines like:
# IBV             0-4     Fram
MATCH_RE = re.compile(r"^\s*(.+?)\s+(\d+)-(\d+)\s+(.+?)\s*$")


def main():
    # Read the HTML
    html = RAW_FILE.read_text(encoding="utf-8")

    # Strip HTML tags (RSSSF puts everything inside <pre>)
    text = re.sub(r"<[^>]+>", "", html)

    # Ignore the league table and everything before Round 1
    if "Round 1" not in text:
        raise RuntimeError("Couldn't find 'Round 1' in the file.")

    text = text.split("Round 1", 1)[1]

    matches = []

    for line in text.splitlines():
        m = MATCH_RE.match(line)
        if not m:
            continue

        home = m.group(1).strip()
        hg = int(m.group(2))
        ag = int(m.group(3))
        away = m.group(4).strip()

        matches.append((home, hg, ag, away))

    print(f"Found {len(matches)} possible matches")

    for match in matches[:20]:
        print(match)


if __name__ == "__main__":
    main()