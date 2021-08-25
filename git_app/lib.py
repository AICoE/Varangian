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
import logging
import os

from ogr.services.base import BaseGitService, BaseGitProject
from ogr.abstract import IssueStatus
from ogr.services.github import GithubService, GithubProject
from ogr.services.gitlab import GitlabService, GitlabProject
from ogr.services.pagure import PagureService, PagureProject

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
    infer_info = re.split(": ", lines[1])
    description = lines[2]
    return {
        "bug_type": infer_info[2],
        "description": description,
    }


def _get_link_from_location(ogr_project: BaseGitProject, location: str, git_ref: Optional[str] = None):
    if git_ref is None:
        git_ref = ogr_project.default_branch
    if isinstance(ogr_project, GithubProject):
        return f"../blob/{git_ref}/{location}"
    elif isinstance(ogr_project, GitlabProject):
        return f"../../blob/{git_ref}/{location}"
    elif isinstance(ogr_project, PagureProject):
        return f"blob/{git_ref}/f/{location}"
    else:
        raise ValueError("Project is not from known services.")


def _find_issue_and_update(ogr_project: BaseGitProject, bug_id: str, title: str, body: str) -> Optional[bool]:
    to_find = re.compile(rf"<!-- {bug_id} -->")
    issues = ogr_project.get_issue_list(status=IssueStatus.all, labels=["bug"])
    for issue in issues:
        if to_find.search(issue.description):
            try:
                if issue.status == IssueStatus.open:
                    issue.title = title
                    issue.description = body
                    logging.debug("Editing already existing issue.")
                    return True  # already open issues count towards max
                else:  # No point in wasting API quota on a closed issue
                    return False
            except Exception:
                logging.error("Failed to update issue.")
    else:
        return None


def _generate_issue_title_and_body(
    ogr_project: BaseGitProject,
    bug_id: str,
    trace_contents: str,
    confidence: str,
    rank: int,
    location: str,
    trace_preview_length: int = 5,
    commit_hash: Optional[str] = None,
) -> tuple:
    infer_info = _parse_trace(trace_contents)
    bug_type_link = f"https://fbinfer.com/docs/all-issue-types#{infer_info['bug_type'].lower().replace(' ', '_')}"
    title = f"{infer_info['bug_type']}-{location} Rank-{rank} "
    full_trace = trace_contents.replace("\t", " ").splitlines(keepends=False)
    bug_link = _get_link_from_location(
        ogr_project=ogr_project, location=location.replace(":", "#L"), git_ref=commit_hash or ogr_project.default_branch
    )
    body = VARANGIAN_BUG_BODY.format(
        bug_id=bug_id,
        bug_type=infer_info["bug_type"],
        bug_type_link=bug_type_link,
        location=location,
        bug_link=bug_link,
        description=infer_info["description"],
        confidence=confidence,
        rank=rank,
        trace_preview="\n".join(full_trace[:trace_preview_length]),
        full_trace="\n".join(full_trace[trace_preview_length:]),
    )
    return title, body


def _update_issue(
    ogr_project: BaseGitProject,
    bug_id: str,
    trace_contents: str,
    confidence: str,
    rank: int,
    location: str,
    trace_preview_length: int = 5,
    commit_hash: Optional[str] = None,
) -> None:
    title, body = _generate_issue_title_and_body(
        ogr_project=ogr_project,
        bug_id=bug_id,
        trace_contents=trace_contents,
        confidence=confidence,
        rank=rank,
        location=location,
        trace_preview_length=trace_preview_length,
        commit_hash=commit_hash,
    )
    if _find_issue_and_update(ogr_project=ogr_project, bug_id=bug_id, title=title, body=body) is None:
        logging.warning(f"Issue with bug_id={bug_id} not found when explicitly asked to update.")


def _find_closed_issue(ogr_project: BaseGitProject, bug_id: str) -> bool:
    for issue in ogr_project.get_issue_list(status=IssueStatus.closed, author=ogr_project.service.user.get_username()):
        to_find = re.compile(rf"<!-- {bug_id} -->")
        match = re.search(to_find, issue.description)
        if match is not None:
            return True
    else:
        return False


def _create_issue(
    ogr_project: BaseGitProject,
    bug_id: str,
    trace_contents: str,
    confidence: str,
    rank: int,
    location: str,
    trace_preview_length: int = 5,
    commit_hash: Optional[str] = None,
) -> bool:
    title, body = _generate_issue_title_and_body(
        ogr_project=ogr_project,
        bug_id=bug_id,
        trace_contents=trace_contents,
        confidence=confidence,
        rank=rank,
        location=location,
        trace_preview_length=trace_preview_length,
        commit_hash=commit_hash,
    )
    if _find_closed_issue(ogr_project, bug_id):
        return False
    try:
        ogr_project.create_issue(title=title, body=body, labels=["bug", "bot"])
        return True
    except Exception as exc:
        logging.exception(f"Failed to create issue. With exception: {str(exc)}")
        return False


def _get_trace_contents(trace_directory: str, report_name: str) -> str:
    with open(os.path.join(trace_directory, report_name), "r") as f:
        return f.read()


def _get_confidence(priority: str) -> Optional[str]:
    if priority == "H":
        return "HIGH"
    elif priority == "M":
        return "MEDIUM"
    elif priority == "L":
        return "LOW"
    else:
        return None


def _injest_results_and_create_issues(
    ogr_project: BaseGitProject,
    predictions_file: str,
    trace_directory: str,
    namespace: str,
    max_count: int,
    trace_preview_length: int,
    service_dict: Optional[Dict[str, str]],
    commit_hash: Optional[str],
    to_update: list,
) -> int:
    count = len(to_update)
    with open(predictions_file, "r") as f:
        f.readline()  # skip line with column headers
        rank = 0
        for line in f.readlines():
            rank += 1
            line = line.strip()
            bug_id, location, report_name, _, _, priority = line.split(",")
            confidence = _get_confidence(priority)
            trace_contents = _get_trace_contents(trace_directory, report_name)
            if bug_id in to_update:
                _update_issue(
                    ogr_project=ogr_project,
                    bug_id=bug_id,
                    trace_contents=trace_contents,
                    confidence=confidence or "Below threshold",
                    rank=rank,
                    location=location,
                    trace_preview_length=trace_preview_length,
                    commit_hash=commit_hash,
                )
                continue
            if confidence is None:
                continue  # we do not break because issues may need updating
            if count < max_count:
                count = count + _create_issue(
                    ogr_project=ogr_project,
                    bug_id=bug_id,
                    trace_contents=trace_contents,
                    confidence=confidence,
                    rank=rank,
                    location=location,
                    trace_preview_length=trace_preview_length,
                    commit_hash=commit_hash,
                )
    return count


def _get_id_set_from_predictions_file(predictions_file_name: str) -> set:
    to_ret = set()
    with open(predictions_file_name, "r") as f:
        f.readline()
        for line in f.readlines():
            bug_id, _, _, _, _, _ = line.split(",")
            to_ret.add(bug_id)
    return to_ret


def _close_issues4bugs_not_in_results(ogr_project: BaseGitProject, predictions_file_name: str) -> list:
    bug_ids = _get_id_set_from_predictions_file(predictions_file_name)
    issue_list = ogr_project.get_issue_list(author=ogr_project.service.user.get_username(), labels=["bug"])
    to_update = []
    for issue in issue_list:
        pattern = re.compile(r"<!-- (?P<bug_id>\w{40}) -->")
        match = re.search(pattern=pattern, string=issue.description)
        if match is None:
            continue
        if match.group("bug_id") not in bug_ids:
            issue.close()
        else:
            to_update.append(match.group("bug_id"))
    return to_update


def run(
    repo: str,
    predictions_file: str,
    trace_directory: str,
    namespace: str,
    max_count: int = 7,
    trace_preview_length: int = 5,
    service_dict: Optional[Dict[str, str]] = None,
    commit_hash: Optional[str] = None,
) -> None:
    """Take output from Varangian application and apply it to issues on git forges."""
    if service_dict is not None:
        service = _ogr_service_from_dict(service_dict)
    else:
        service = _Config.ogr_service()

    project = service.get_project(namespace=namespace, repo=repo)

    to_update = _close_issues4bugs_not_in_results(project, predictions_file)

    _injest_results_and_create_issues(
        ogr_project=project,
        predictions_file=predictions_file,
        trace_directory=trace_directory,
        namespace=namespace,
        max_count=max_count,
        trace_preview_length=trace_preview_length,
        service_dict=service_dict,
        commit_hash=commit_hash,
        to_update=to_update,
    )
