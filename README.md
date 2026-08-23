# Football Trackers 2026-27 — Dashboard

A single landing page linking out to all six season trackers:
- [Premier League](https://paradox-a.github.io/premier-league-tracker/)
- [Championship](https://paradox-a.github.io/championship-tracker/)
- [LaLiga](https://paradox-a.github.io/laliga-tracker/)
- [Bundesliga](https://paradox-a.github.io/bundesliga-tracker/)
- [Serie A](https://paradox-a.github.io/serie-a-tracker/)
- [Ligue 1](https://paradox-a.github.io/ligue1-tracker/)

Each card shows a top-5 standings snapshot and current matchday, pulled independently from football-data.org — this page doesn't depend on the other six repos being fetched or up to date, it fetches its own lightweight standings-only snapshot.

## Data source
[football-data.org](https://www.football-data.org/) free API — standings only (no matches/scorers needed for a snapshot view).

## Regenerating

```bash
export FOOTBALL_DATA_API_TOKEN=your_token_here
./fetch_data.sh
git add index.html
git commit -m "Refresh snapshot"
git push
```

Not live-updating — rebuild whenever you want a fresher snapshot. Since this only shows top-5 rows per league, it doesn't need refreshing as often as the full trackers.
