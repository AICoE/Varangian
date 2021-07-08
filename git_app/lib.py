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

from typing import Dict, Optional
import re
import csv

from ogr.services.base import BaseGitService, BaseGitProject
from ogr.abstract import IssueStatus
from ogr.services.github import GithubService
from ogr.services.gitlab import GitlabService
from ogr.services.pagure import PagureService

from config import _Config
from templates import VARANGIAN_BUG_BODY


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
    trace_length: Optional[int] = None,
) -> None:
    infer_info = _parse_trace(trace_contents)
    if trace_length is not None:
        "\n".join(trace_contents.splitlines(keepends=False)[:trace_length])
    body = VARANGIAN_BUG_BODY.format(
        bug_type=infer_info["bug_type"],
        location=infer_info["location"],
        description=infer_info["description"],
        confidence=confidence,
        bug_trace=trace_contents,
    )
    title = f"{infer_info['bug_type']}-{trace_id}"
    for issue in ogr_project.get_issue_list(status=IssueStatus.all):
        if issue.title == title:
            break
    else:
        ogr_project.create_issue(title=title, body=body, labels=["bug"])


def run(
    repo: str,
    predictions_file: str,
    trace_file: str,
    namespace: str,
    confidence_threshold: float = 0.6,
    max_count: int = 7,
    trace_length: Optional[int] = None,
    service_dict: Optional[Dict[str, str]] = None,
) -> None:
    """Take output from Varangian application and apply it to issues on git forges."""
    if service_dict is not None:
        service = _ogr_service_from_dict(service_dict)
    else:
        service = _Config.ogr_service()

    project = service.get_project(namespace=namespace, repo=repo)

    to_create = []

    with open(predictions_file, "r") as f:
        f.readline()  # skip line with column headers
        for _ in range(max_count):
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            contents = line.split(",")
            if float(contents[2]) >= confidence_threshold:
                to_create.append((contents[1], float(contents[2])))

    ids = [i[0] for i in to_create]
    confidences = [i[1] for i in to_create]

    project.create_issue(title="foo", body="bar")

    with open(trace_file, "r", newline="") as f:
        reader = csv.reader(f, delimiter=",", doublequote=True)
        for row in reader:
            try:
                index = ids.index(row[0])
                _create_issue(
                    ogr_project=project,
                    trace_id=ids[index],
                    trace_contents=row[1],
                    confidence=confidences[index],
                )

                ids.pop(index)
                confidences.pop(index)
            except ValueError:
                pass
