import json
from pathlib import Path

import requests

SOURCE_URL = "https://api.tvmaze.com/shows?page=0"
OUTPUT = Path("summary.json")


def fetch_records(url):
    """Download the TV show records and return them as a list of dicts."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    records = fetch_records(SOURCE_URL)
    print(f"Downloaded {len(records)} shows.")
    print(records[0]["name"], records[0]["genres"], records[0]["rating"])


if __name__ == "__main__":
    main()