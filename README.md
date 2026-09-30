# TV Shows Summary

Downloads TV show records from the TVmaze API, counts shows per genre, calculates the average rating by language, and writes the results to a JSON file. Useful for a quick overview of which genres dominate a TV catalogue and how different languages compare on ratings.

## Data source

https://api.tvmaze.com/shows?page=0

Each record is one TV show, with fields such as name, language, genres, premiere date, rating and network. The first page returns 240 shows.

## Setup

    python -m venv .venv
    source .venv/bin/activate    # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run

    python records.py

## Example output

```json
{
  "source_url": "https://api.tvmaze.com/shows?page=0",
  "records_processed": 240,
  "shows_per_genre": {
    "Drama": 154,
    "Comedy": 66,
    "Crime": 57,
    "Action": 55
  },
  "average_rating_by_language": {
    "English": 7.58,
    "Japanese": 7.88
  },
  "unrated_shows": 4
}
```

(Excerpt.) Drama is by far the most common genre. Japanese shows rate slightly higher on average than English ones, although there are far fewer of them.

## Data quirks

- **Multiple genres per show:** a show can belong to several genres. It is counted once in each genre, so the genre totals add up to more than 240.
- **Shows with no genre:** 5 shows (mostly reality programmes such as The Biggest Loser) have an empty genre list. They are not counted in any genre and are listed separately under `shows_without_genre`.
- **Missing ratings:** 4 shows have no average rating. They are left out of the language averages instead of being counted as 0, which would unfairly lower the average. Their number is reported as `unrated_shows`.
- **Nested or null rating field:** the rating is stored as a nested object (`{"average": 6.5}`), and the average inside it can be null. The program checks both levels safely with `get`.
- **Missing language:** shows with no language are skipped in the language averages.

## Design choices

- **list:** the records returned by the API, and the names of shows without a genre. Both are ordered sequences.
- **dict:** genre counts and language averages, because the results need to be looked up by a key (genre or language name).
- **tuple:** a (rating_sum, count) pair per language. The two values belong together and are only used as a unit, so a tuple is clearer than two separate dictionaries.
- Each aggregation is its own function that takes records in and returns a result, without downloading, printing or writing, so it can be tested on its own.

## Known limitations

- Only the first page of the API (240 shows) is downloaded. As a result, only two languages appear in the averages.
- Averages are not weighted by how many ratings each show has on TVmaze.
- Premiere decade and network are not analysed yet.