import json
from datetime import datetime, timezone

LEAGUES = [
    {
        "key": "pl",
        "name": "Premier League",
        "country": "England",
        "file": "pl_standings.json",
        "url": "https://paradox-a.github.io/premier-league-tracker/",
        "accent": "#37003c",
    },
    {
        "key": "elc",
        "name": "Championship",
        "country": "England",
        "file": "elc_standings.json",
        "url": "https://paradox-a.github.io/championship-tracker/",
        "accent": "#1a4a8a",
    },
    {
        "key": "pd",
        "name": "LaLiga",
        "country": "Spain",
        "file": "pd_standings.json",
        "url": "https://paradox-a.github.io/laliga-tracker/",
        "accent": "#ee8a09",
    },
    {
        "key": "bl1",
        "name": "Bundesliga",
        "country": "Germany",
        "file": "bl1_standings.json",
        "url": "https://paradox-a.github.io/bundesliga-tracker/",
        "accent": "#d3010c",
    },
]

TOP_N = 5

def load_table(path):
    data = json.load(open(path))
    table = data["standings"][0]["table"]
    table = sorted(table, key=lambda t: (t["position"], -t["points"], -t["goalDifference"]))
    for i, t in enumerate(table, start=1):
        t["displayPos"] = i
    matchday = data["season"]["currentMatchday"]
    season_started = any(t["playedGames"] > 0 for t in table)
    return table, matchday, season_started

def card_html(league):
    table, matchday, started = load_table(league["file"])
    rows = []
    for t in table[:TOP_N]:
        rows.append(f"""
        <tr>
          <td class="pos">{t['displayPos']}</td>
          <td class="team"><img src="{t['team']['crest']}" alt="" class="crest"> {t['team']['shortName']}</td>
          <td>{t['playedGames']}</td>
          <td class="pts">{t['points']}</td>
        </tr>""")
    status_note = "" if started else '<div class="note">Season hasn\'t started yet</div>'
    return f"""
    <a class="card" href="{league['url']}" style="--accent: {league['accent']};">
      <div class="card-head">
        <div>
          <h2>{league['name']}</h2>
          <div class="sub">{league['country']} · Matchday {matchday}</div>
        </div>
        <span class="arrow">→</span>
      </div>
      <table>
        <thead><tr><th>#</th><th class="team">Team</th><th>P</th><th>Pts</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
      {status_note}
      <div class="view-link">View full tracker →</div>
    </a>"""

cards_html = "".join(card_html(league) for league in LEAGUES)

updated = datetime.now(timezone.utc).strftime("%B %d, %Y %H:%M UTC")

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Football Trackers 2026-27</title>
<style>
  :root {{
    --bg: #f6f1e7; --card: #ffffff; --text: #1a1a1a; --muted: #6b6b6b; --border: #e2ddd0;
    --page-accent: #2c2c2c;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #16131a; --card: #211d29; --text: #f0ede4; --muted: #a39d8f; --border: #3a3444;
      --page-accent: #f0ede4;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #16131a; --card: #211d29; --text: #f0ede4; --muted: #a39d8f; --border: #3a3444;
    --page-accent: #f0ede4;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 28px 16px 60px; }}
  .wrap {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.7rem; margin-bottom: 4px; color: var(--page-accent); }}
  .updated {{ color: var(--muted); font-size: 0.85rem; margin-bottom: 24px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
  @media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  .card {{
    display: block; background: var(--card); border: 1px solid var(--border); border-radius: 14px;
    padding: 18px; text-decoration: none; color: var(--text);
    border-top: 4px solid var(--accent);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }}
  .card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
  .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }}
  .card-head h2 {{ font-size: 1.15rem; margin: 0 0 2px; color: var(--accent); }}
  .card-head .sub {{ font-size: 0.78rem; color: var(--muted); }}
  .arrow {{ font-size: 1.3rem; color: var(--accent); }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.82rem; }}
  th, td {{ padding: 5px 6px; text-align: center; border-bottom: 1px solid var(--border); }}
  th {{ color: var(--muted); font-weight: 600; font-size: 0.68rem; text-transform: uppercase; }}
  td.team, th.team {{ text-align: left; }}
  .crest {{ width: 15px; height: 15px; vertical-align: middle; margin-right: 6px; }}
  .pos {{ font-weight: 700; }} .pts {{ font-weight: 700; }}
  .note {{ color: var(--muted); font-size: 0.75rem; margin-top: 8px; font-style: italic; }}
  .view-link {{ margin-top: 12px; font-size: 0.82rem; font-weight: 600; color: var(--accent); }}
  footer {{ text-align: center; color: var(--muted); font-size: 0.75rem; margin-top: 32px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Football Trackers 2026-27</h1>
  <div class="updated">Last updated {updated}</div>
  <div class="grid">
    {cards_html}
  </div>
  <footer>Data: football-data.org · Each card links to its full tracker (table, club stats, player stats)</footer>
</div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
print("wrote index.html", len(html), "bytes")
