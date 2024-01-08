#!/usr/bin/env pip-run
"""Generate milestones for the next 60 years."""

from datetime import datetime, timedelta
from string import capwords
from subprocess import getoutput, run

from monthdelta import monthdelta  # type: ignore[import-untyped]
from zoneinfo import ZoneInfo

__requires__ = ["monthdelta"]

ZONE = ZoneInfo("Europe/Warsaw")
TODAY = datetime.today().astimezone(ZONE)

YEAR = TODAY.year
MONTH = TODAY.month

# ruff: noqa: EXE003,PLR2004,T201

# Create milestones for the next 60 years
# Hopefully I'll live that long :)
for year in range(YEAR, YEAR + 60):
    months = range(MONTH, 13) if year == YEAR else range(1, 13)

    for month in months:
        due_date = (
            datetime(
                year=year,
                month=month,
                day=1,
                tzinfo=ZONE,
            )
            + monthdelta(1)
            - timedelta(days=1)
        )

        title = capwords(due_date.strftime("%B %Y"))
        if title not in getoutput("gh milestone list --repo=bswck/oss"):
            print(f"Creating milestone {title}...")
            run(
                [  # noqa: S603,S607
                    "gh",
                    "milestone",
                    "create",
                    "--repo=bswck/oss",
                    f"--title={title}",
                    f"--description=Things to do in {title}",
                    f"--due-date={due_date.strftime('%Y-%m-%d')}",
                ],
                check=True,
            )
