#!/usr/bin/env pip-run
"""Generate milestones for the next 60 years."""

from contextlib import suppress
from datetime import date, timedelta
from string import capwords
from subprocess import SubprocessError, getoutput, run

from monthdelta import monthdelta  # type: ignore[import-untyped]

__requires__ = ["monthdelta"]

TODAY = date.today()

YEAR = TODAY.year
MONTH = TODAY.month
LIST = getoutput("gh milestone list --repo=bswck/oss")

# ruff: noqa: DTZ011,EXE003,PLR2004,T201

# Create milestones for the next 60 years
# Hopefully I'll live that long :)
for year in range(YEAR, YEAR + 60):
    months = range(MONTH if year == YEAR else 1, 13)

    for month in months:
        due_date = (
            date(
                year=year,
                month=month,
                day=1,
            )
            + monthdelta(1)
            - timedelta(days=1)
        )

        title = capwords(due_date.strftime("%B %Y"))
        if title not in LIST:  # Note: this will only work for first 100 milestones
            print(f"Creating milestone {title}...")
            with suppress(SubprocessError):
                run(
                    [  # noqa: S603,S607
                        "gh",
                        "milestone",
                        "create",
                        "--repo=bswck/oss",
                        f"--title={title}",
                        f"--description=Things to do in {title}",
                        f"--due-date={due_date}",
                    ],
                    check=True,
                )
