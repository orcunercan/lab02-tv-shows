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

def shows_per_genre(records):
    """Return a dict mapping each genre to the number of shows in it.

    A show with several genres is counted once in each.
    Shows with no genres are not counted here.
    """
    counts = {}
    for show in records:
        for genre in show.get("genres") or []:
            counts[genre] = counts.get(genre, 0) + 1
    return counts


def shows_without_genre(records):
    """Return the names of shows that have no genre listed."""
    return [show["name"] for show in records if not show.get("genres")]

def main():
    records = fetch_records(SOURCE_URL)
    print(f"Downloaded {len(records)} shows.")
    print(shows_per_genre(records))
    print(shows_without_genre(records))


if __name__ == "__main__":
    main()