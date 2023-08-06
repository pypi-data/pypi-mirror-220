import csv
import datetime
import sys
from dataclasses import asdict, fields
from typing import Annotated, Union

import pkg_resources
import typer

from iscwatch.advisory import Advisory
from iscwatch.scrape import iter_advisories


def cli():
    """CLI entry point executes typer-wrapped main function"""
    typer.run(main)

def main(
    since: Annotated[
        Union[datetime.datetime, None],
        typer.Option(
            help="Output only those summaries released or updated since specified date."
        ),
    ] = None,
    version: Annotated[
        bool,
        typer.Option(help="Output product version and exit.")
    ] = False,
    headers: Annotated[
        bool,
        typer.Option(help="Include column headers in CSV output.")
    ] = True
):
    """Retrieve Security Advisory summaries from Intel website and output as CSV."""
    if version:
        output_version()
    else:
        output_advisories(since, headers)

def output_advisories(since: datetime.datetime | None, headers: bool):
    fieldnames = [field.name for field in fields(Advisory)]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    if headers:
        writer.writeheader()
    select_advisories = [
        asdict(advisory)
        for advisory in iter_advisories()
        if not since or advisory.updated >= since.date()
    ]
    writer.writerows(select_advisories)

def output_version():
    distribution = pkg_resources.get_distribution("iscwatch")
    print(f"{distribution.project_name} {distribution.version}")
