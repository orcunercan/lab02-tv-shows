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

def rating_totals_by_language(records):
    """Return a dict mapping each language to a (rating_sum, count) tuple.

    Shows with no rating or no language are skipped.
    """
    totals = {}
    for show in records:
        language = show.get("language")
        rating = (show.get("rating") or {}).get("average")
        if language is None or rating is None:
            continue
        rating_sum, count = totals.get(language, (0, 0))
        totals[language] = (rating_sum + rating, count + 1)
    return totals


def average_rating_by_language(totals):
    """Convert (rating_sum, count) pairs into average ratings."""
    return {language: round(rating_sum / count, 2)
            for language, (rating_sum, count) in totals.items()}


def main():
    records = fetch_records(SOURCE_URL)
    print(f"Downloaded {len(records)} shows.")
    print(shows_per_genre(records))
    print(shows_without_genre(records))
    totals = rating_totals_by_language(records)
    print(average_rating_by_language(totals))
    

if __name__ == "__main__":
    main()