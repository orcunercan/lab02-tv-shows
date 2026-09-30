import json
import sys
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


def count_unrated(records):
    """Return how many shows have no average rating."""
    return sum(1 for show in records
               if (show.get("rating") or {}).get("average") is None)


def build_summary(records):
    """Combine the aggregations into one dict ready to write."""
    totals = rating_totals_by_language(records)
    return {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
        "shows_per_genre": shows_per_genre(records),
        "shows_without_genre": shows_without_genre(records),
        "average_rating_by_language": average_rating_by_language(totals),
        "unrated_shows": count_unrated(records),
    }


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main():
    try:
        records = fetch_records(SOURCE_URL)
    except requests.RequestException as error:
        sys.exit(f"Could not download data from {SOURCE_URL}: {error}")

    summary = build_summary(records)
    write_summary(summary, OUTPUT)
    print(f"Processed {summary['records_processed']} shows.")
    print(f"Summary written to {OUTPUT}")


if __name__ == "__main__":
    main()