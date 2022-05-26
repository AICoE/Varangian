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
    "--trace-directory",
    envvar="VARANGIAN_TRACE_DIRECTORY",
    type=click.Path(exists=True),
    required=True,
    help="Location of bug traces which can be indexed by the trace id.",
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
    "--trace-preview-length",
    envvar="VARANGIAN_TRACE_PREVIEW_LENGTH",
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
@click.option(
    "--ref",
    envvar="VARANGIAN_COMMIT_HASH",
    type=str,
    help="Specific ref for which the augmented static analyzer was run.",
)
def cli(
    namespace,
    repo,
    predictions_file,
    trace_directory,
    max_count,
    trace_preview_length,
    service_dict,
    ref,
):
    """Run base command for varangian git forge application."""
    lib.run2(
        repo=repo,
        predictions_file=predictions_file,
        trace_directory=trace_directory,
        namespace=namespace,
        # max_count=max_count,
        trace_preview_length=trace_preview_length,
        service_dict=service_dict,
        ref=ref,
    )


if __name__ == "__main__":
    cli()
