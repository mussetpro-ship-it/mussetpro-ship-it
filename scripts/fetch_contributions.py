#!/usr/bin/env python3
"""Save the profile's contribution calendar (the last 12 months) to data/contributions.json.

    GITHUB_TOKEN=... python3 scripts/fetch_contributions.py    # in GitHub Actions
    python3 scripts/fetch_contributions.py                      # locally, through the gh command line

The calendar is the one shown on the profile page: it counts private contributions
only as numbers, and only when the profile is set to show them.
"""

import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER = "mussetpro-ship-it"
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
            headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={USER}"],
        check=True, capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def main():
    calendar = fetch()["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [day for week in calendar["weeks"] for day in week["contributionDays"]]
    data = {"total": calendar["totalContributions"], "weeks": [
        [[d["date"], d["contributionCount"], d["contributionLevel"]] for d in week["contributionDays"]]
        for week in calendar["weeks"]
    ]}
    path = ROOT / "data" / "contributions.json"
    # The window moves one day at a time: a total that halves overnight means the token sees less, not that
    # the work vanished. Keep the last good calendar rather than draw a wrong one.
    if path.exists():
        previous = json.loads(path.read_text())["total"]
        if data["total"] < previous / 2:
            print(f"Kept the saved calendar: {data['total']} contributions now against {previous} saved.")
            return
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    print(f"{path.relative_to(ROOT)}: {data['total']} contributions over {len(days)} days")


if __name__ == "__main__":
    main()
