#!/usr/bin/env python3
# Varangian
# Copyright(C) 2020 Kevin Postlethwait
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""CLI for Varangian git application."""

import click
import json

import lib


def _json_callback(ctx, param, value):
    if value is None:
        return value
    try:
        return json.loads(value)
    except ValueError:
        raise click.BadParameter("argument must be valid json")


@click.command()
@click.option(
    "-n", "--namespace", envvar="VARANGIAN_NAMESPACE", type=str, required=True, help="Namespace of project to act on."
)
@click.option("-r", "--repo", envvar="VARANGIAN_REPO", type=str, required=True, help="Name of repository to act on.")
@click.option(
    "-p",
    "--predictions-file",
    envvar="VARANGIAN_PREDICTIONS_FILE",
    type=click.Path(exists=True),
    required=True,
    help="Location of predictions file containing confidence and trace id information.",
)
@click.option(
    "-t",
    "--trace-file",
    envvar="VARANGIAN_TRACE_FILE",
    type=click.Path(exists=True),
    required=True,
    help="Location of bug traces which can be indexed by the trace id.",
)
@click.option(
    "-c",
    "--confidence-threshold",
    envvar="VARANGIAN_CONFIDENCE_THRESHOLD",
    type=click.FloatRange(0, 1),
    default=0.6,
    help="Cut off for which bug traces should result in issues in the repository.",
)
@click.option(
    "-C",
    "--max-count",
    envvar="VARANGIAN_MAX_COUNT",
    type=click.IntRange(1),
    default=10,
    help="Maximum number of issues which can be opened in a single run.",
)
@click.option(
    "-l",
    "--trace-length",
    envvar="VARANGIAN_TRACE_LENGTH",
    type=click.IntRange(0),
    default=None,
    help="Number of lines of the bug trace to include in the issue body, None indicates inclusion of the full trace.",
)
@click.option(
    "-s",
    "--service-dict",
    envvar="VARANGIAN_SERVICE_DICT",
    type=str,
    callback=_json_callback,
    help="Json dictionary containing service related information for authentication.",
)
def cli(namespace, repo, predictions_file, trace_file, confidence_threshold, max_count, trace_length, service_dict):
    """Run base command for varangian git forge application."""
    lib.run(
        repo=repo,
        predictions_file=predictions_file,
        trace_file=trace_file,
        namespace=namespace,
        confidence_threshold=confidence_threshold,
        max_count=max_count,
        trace_length=trace_length,
        service_dict=service_dict,
    )


if __name__ == "__main__":
    cli()
