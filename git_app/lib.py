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

"""Library functions for Varangian git application."""

from typing import Dict, Optional, TextIO
import re
import csv
import logging

from ogr.services.base import BaseGitService, BaseGitProject
from ogr.abstract import IssueStatus
from ogr.services.github import GithubService
from ogr.services.gitlab import GitlabService
from ogr.services.pagure import PagureService

from config import _Config
from templates import VARANGIAN_BUG_BODY


def _get_row_from_csv(csv_file: TextIO, index: int, **csv_reader_args):
    reader = csv.reader(csv_file, **csv_reader_args)
    for _ in range(index):
        next(reader)
    return next(reader)


def _ogr_service_from_dict(service_dict: Dict[str, str]) -> BaseGitService:
    if service_dict["service_name"] == "GITHUB":
        return GithubService(
            token=service_dict.get("auth_token"),
            github_app_id=service_dict.get("github_app_id"),
            github_app_private_key_path=service_dict.get("github_app_private_key_path"),
        )
    elif service_dict["service_name"] == "GITLAB":
        return GitlabService(token=service_dict.get("auth_token"), instance_url=service_dict.get("service_url"))
    elif service_dict["service_name"] == "PAGURE":
        return PagureService(token=service_dict.get("auth_token"), instance_url=service_dict.get("service_url"))
    else:
        raise NotImplementedError(f"Varangian cannot run on {service_dict['service_name']} git services.")


def _parse_trace(trace: str) -> Dict[str, str]:
    lines = trace.split("\n")
    infer_info = re.split(": ", lines[0])
    description = lines[1]
    return {
        "bug_type": infer_info[2],
        "location": infer_info[0],
        "description": description,
    }


def _create_issue(
    ogr_project: BaseGitProject,
    trace_id: str,
    trace_contents: str,
    confidence: float,
    rank: int,
    trace_preview_length: int = 5,
) -> bool:
    infer_info = _parse_trace(trace_contents)
    title = f"priority-{rank} {infer_info['bug_type']}-{infer_info['location']}"
    full_trace = trace_contents.splitlines(keepends=False)
    body = VARANGIAN_BUG_BODY.format(
        trace_id=trace_id,
        bug_type=infer_info["bug_type"],
        location=infer_info["location"],
        description=infer_info["description"],
        confidence=confidence,
        rank=rank,
        trace_preview="\n".join(full_trace[:trace_preview_length]),
        full_trace="\n".join(full_trace[trace_preview_length:]),
    )
    to_find = re.compile(rf"## Description:\nid: {trace_id}\n")
    issues = ogr_project.get_issue_list(status=IssueStatus.all)
    for issue in issues:
        if to_find.search(issue.description):
            issue.title = title
            issue.description = body
            logging.debug("Editing already existing issue.")
            return False
    else:
        try:
            ogr_project.create_issue(title=title, body=body, labels=["bug"])
            return True
        except Exception as exc:
            logging.exception(f"Failed to create issue. With exception: {str(exc)}")
            return False


def run(
    repo: str,
    predictions_file: str,
    trace_file: str,
    namespace: str,
    confidence_threshold: float = 0.6,
    max_count: int = 7,
    trace_preview_length: int = 5,
    service_dict: Optional[Dict[str, str]] = None,
) -> None:
    """Take output from Varangian application and apply it to issues on git forges."""
    if service_dict is not None:
        service = _ogr_service_from_dict(service_dict)
    else:
        service = _Config.ogr_service()

    project = service.get_project(namespace=namespace, repo=repo)

    acceptable = []
    trace_ids = []

    with open(predictions_file, "r") as f:
        f.readline()  # skip line with column headers
        for _ in range(max_count):
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            rank, trace_id, confidence, _ = line.split(",")
            if float(confidence) >= confidence_threshold:
                acceptable.append(
                    {
                        "rank": int(rank),
                        "trace_id": trace_id,
                        "confidence": float(confidence),
                        "trace_index": None,
                    }
                )
                trace_ids.append(trace_id)

    with open(trace_file, "r", newline="") as f:
        reader = csv.reader(f, delimiter=",", doublequote=True)

        i = 0
        for row in reader:
            try:
                index = trace_ids.index(row[0])
                acceptable[index]["trace_index"] = i
            except ValueError:
                logging.warning("No prediction entry associated with this trace.")
            finally:
                i = i + 1

        count = 0

        while count <= max_count and acceptable != []:
            to_create = acceptable.pop(0)
            if to_create["trace_index"] is not None:
                f.seek(0)
                count = count + _create_issue(
                    ogr_project=project,
                    trace_id=str(to_create["trace_id"]),
                    trace_contents=_get_row_from_csv(
                        f, int(to_create["trace_index"]), delimiter=",", doublequote=True  # type: ignore
                    )[1],
                    confidence=float(to_create["confidence"]),  # type: ignore
                    rank=int(to_create["rank"]),  # type: ignore
                    trace_preview_length=trace_preview_length,
                )
