from pathlib import Path
import argparse
import requests

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

FIRST_YEAR = 1990
LAST_YEAR = 2025


def rsssf_url(year: int) -> str:
    if year <= 2009:
        return f"https://rsssf.org/tablesi/ijs{year % 100:02d}.html"
    return f"https://rsssf.org/tablesi/ijs{year}.html"


def download(year: int):
    url = rsssf_url(year)
    outfile = RAW_DIR / f"{year}.html"

    if outfile.exists():
        print(f"✓ {year} already downloaded")
        return

    print(f"Downloading {year}...")

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    r.raise_for_status()

    outfile.write_text(r.text, encoding="utf-8")

    print(f"Saved {outfile}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int)
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    if args.year:
        download(args.year)

    elif args.all:
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            try:
                download(year)
            except Exception as e:
                print(f"{year}: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()