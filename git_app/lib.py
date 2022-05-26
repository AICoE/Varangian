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

from typing import Dict, Optional, List, NamedTuple, Tuple, Set
import re
import logging
import os
import urllib.parse

from ogr.abstract import IssueStatus, Issue, GitService, GitProject
from ogr.services.github import GithubService, GithubProject
from ogr.services.gitlab import GitlabService, GitlabProject
from ogr.services.pagure import PagureService, PagureProject

from config import _Config
from templates import VARANGIAN_BUG_BODY, SINGLE_TRACE_CONTENTS, ISSUE_FOOTER, ISSUE_BODY, CREATE_ISSUE_SECTION


RE_BUG_ID_HEADER = r"<!-- ([\w]{40})((,[\w]{40})*) -->"


class AugSaBug(NamedTuple):
    """Represents a bug from the csv outputted by the augmented static analyzer."""

    bug_id: str
    bug_location: str
    report_name: str
    bug_type: str
    score: float
    priority: str
    rank: int

    @classmethod
    def from_csv(cls, row, rank=0):
        """Create bug from a 'row' of a csv with rank passed separately."""
        return cls(row[0], row[1], row[2], row[3], float(row[4]), row[5], rank)


def _get_all_ids_from_issue(issue: Issue) -> Optional[List[str]]:
    match = re.search(RE_BUG_ID_HEADER, issue.description)
    if match is None:
        return None
    ids = [match.group(1)]
    if match.group(2):
        ids = ids + match.group(2)[1:].split(",")
    return ids


def _ogr_service_from_dict(service_dict: Dict[str, str]) -> GitService:
    if service_dict["service_name"] == "GITHUB":
        return GithubService(
            token=service_dict.get("auth_token"),
            github_app_id=service_dict.get("github_app_id"),
            github_app_private_key_path=service_dict.get("github_app_private_key_path"),
        )
    elif service_dict["service_name"] == "GITLAB":
        return GitlabService(token=service_dict.get("auth_token"), instance_url=service_dict.get("service_url"))
    elif service_dict["service_name"] == "PAGURE":
        return PagureService(
            token=service_dict.get("auth_token"),
            instance_url=service_dict.get("service_url", "https://pagure.io"),
        )
    else:
        raise NotImplementedError(f"Varangian cannot run on {service_dict['service_name']} git services.")


def _get_link_from_location(ogr_project: GitProject, location: str, git_ref: Optional[str] = None):
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


def _get_trace_contents(
    bug: AugSaBug,
    trace_directory: str,
):
    with open(os.path.join(trace_directory, bug.report_name), "r") as f:
        return f.read()


def _get_trace_desc_and_root(
    bug: AugSaBug,
    trace_directory: str,
):
    trace_contents = _get_trace_contents(bug=bug, trace_directory=trace_directory)
    final_step = trace_contents.rsplit("\n\n", 1)[-1]
    description = final_step.split("\n", 1)[0]
    return description, final_step


def _generate_issue_title_and_body(
    ogr_project: GitProject,
    agg_list: List[AugSaBug],
    trace_directory: str,
    commit_hash: Optional[str] = None,
) -> tuple:
    confidence = _get_confidence(agg_list[0].priority)
    bug_type_link = f"https://fbinfer.com/docs/all-issue-types#{agg_list[0].bug_type.lower().replace(' ', '_')}"
    title = f"{agg_list[0].bug_type}-{agg_list[0].bug_location}-{confidence}"
    description, bug_trace_root = _get_trace_desc_and_root(agg_list[0], trace_directory)
    bug_link = _get_link_from_location(
        ogr_project=ogr_project,
        location=agg_list[0].bug_location.replace(":", "#L"),
        git_ref=commit_hash or ogr_project.default_branch,
    )
    bug_ids = [bug.bug_id for bug in agg_list]
    body = VARANGIAN_BUG_BODY.format(
        bug_ids=",".join(bug_ids),
        bug_type=agg_list[0].bug_type,
        bug_type_link=bug_type_link,
        location=agg_list[0].bug_location,
        bug_link=bug_link,
        description=description,
        confidence=confidence,
        bug_trace_root=bug_trace_root,
    )
    for bug in agg_list:
        trace_contents = _get_trace_contents(bug=bug, trace_directory=trace_directory)
        body += SINGLE_TRACE_CONTENTS.format(rank=bug.rank, trace_contents=trace_contents)

    body += ISSUE_FOOTER
    return title, body


def _update_issue(
    ogr_project: GitProject,
    trace_directory: str,
    issue: Issue,
    agg_list: List[AugSaBug],
    commit_hash: Optional[str] = None,
) -> None:
    title, body = _generate_issue_title_and_body(
        ogr_project=ogr_project,
        trace_directory=trace_directory,
        agg_list=agg_list,
        commit_hash=commit_hash,
    )
    if issue.title != title:
        issue.title = title  # type: ignore
    if issue.description != body:
        issue.description = body  # type: ignore


def _update_all(
    ogr_project: GitProject,
    trace_directory: str,
    to_update: List[Tuple[List[AugSaBug], Issue]],
    commit_hash: Optional[str] = None,
):
    for agg_list, issue in to_update:
        _update_issue(
            ogr_project=ogr_project,
            trace_directory=trace_directory,
            issue=issue,
            agg_list=agg_list,
            commit_hash=commit_hash,
        )


def _get_all_closed_bug_ids(ogr_project: GitProject):
    to_ret = set()
    for issue in ogr_project.get_issue_list(status=IssueStatus.closed, author=ogr_project.service.user.get_username()):
        to_ret.update(_get_all_ids_from_issue(issue) or [])  # handles the case where the function returns None
    return to_ret


def _create_issue(
    ogr_project: GitProject,
    agg_list: List[AugSaBug],
    trace_directory: str,
    commit_hash: Optional[str] = None,
) -> bool:
    if _get_confidence(agg_list[0].priority) is None:
        logging.debug("Bug falls below confidence threshold.")
        return False
    title, body = _generate_issue_title_and_body(
        ogr_project=ogr_project,
        trace_directory=trace_directory,
        agg_list=agg_list,
        commit_hash=commit_hash,
    )
    try:
        ogr_project.create_issue(title=title, body=body, labels=["bug", "bot"])
        return True
    except Exception as exc:
        logging.exception(f"Failed to create issue. With exception: {str(exc)}")
        return False


def _get_confidence(priority: str) -> Optional[str]:
    if priority == "H":
        return "HIGH"
    elif priority == "M":
        return "MEDIUM"
    elif priority == "L":
        return "LOW"
    else:
        return None


def _ingest_results_and_create_issues(
    ogr_project: GitProject,
    trace_directory: str,
    max_count: int,
    commit_hash: Optional[str],
    aggregated_bug_list: List[List[AugSaBug]],
    to_update: List[Tuple[List[AugSaBug], Issue]],
) -> int:
    count = len(to_update)
    _update_all(ogr_project=ogr_project, trace_directory=trace_directory, to_update=to_update, commit_hash=commit_hash)
    for agg_list in aggregated_bug_list:
        if count >= max_count:
            break
        count = count + _create_issue(
            ogr_project=ogr_project, agg_list=agg_list, trace_directory=trace_directory, commit_hash=commit_hash
        )
    return count


def _which_aggregate_list_has_id(aggregated_bug_list: List[List[AugSaBug]], bug_id: str) -> Optional[int]:
    for idx, aggregate in enumerate(aggregated_bug_list):
        agg_ids = [bug.bug_id for bug in aggregate]
        if bug_id in agg_ids:
            return idx
    else:
        return None


def _close_issues4bugs_not_in_results(
    ogr_project: GitProject, predictions_file_name: str, aggregated_bug_list: List[List[AugSaBug]]
) -> List[Tuple[List[AugSaBug], Issue]]:
    # returns a list of tuples with aggregated_bug_list and the issue they are associated with
    issue_list = ogr_project.get_issue_list(author=ogr_project.service.user.get_username())
    to_update = []
    for issue in issue_list:
        issue_bug_ids = _get_all_ids_from_issue(issue)
        if issue_bug_ids is None:
            continue
        for issue_bug_id in issue_bug_ids:
            idx = _which_aggregate_list_has_id(aggregated_bug_list, issue_bug_id)
            if idx is not None and idx not in to_update:
                to_update.append((aggregated_bug_list.pop(idx), issue))
                break
        else:
            issue.comment("Bug no longer found in Varangian's results. May have been fixed.")
            issue.close()
    return to_update


def _aggregate_bugs(predictions_file_name: str, closed_issue_bug_ids: set) -> List[List[AugSaBug]]:
    to_ret: List[List[AugSaBug]] = list()
    with open(predictions_file_name, "r") as f:
        f.readline()
        rank = 1
        for line in f.readlines():
            line = line.strip()
            new_bug = AugSaBug.from_csv(line.split(","), rank)
            rank += 1
            if new_bug.bug_id in closed_issue_bug_ids:
                continue  # this effectively removes bugs in closed issues from the results
            for agg in to_ret:
                if agg[0].bug_location == new_bug.bug_location and agg[0].bug_type == new_bug.bug_type:
                    agg.append(new_bug)
                    break
            else:
                to_ret.append([new_bug])
    return to_ret


def create_individual_issues(  # original implementation, one issue per aggregated bug
    repo: str,
    predictions_file: str,
    trace_directory: str,
    namespace: str,
    max_count: int = 7,
    service_dict: Optional[Dict[str, str]] = None,
    commit_hash: Optional[str] = None,
) -> None:
    """Take output from Varangian application and apply it to issues on git forges."""
    if service_dict is not None:
        service = _ogr_service_from_dict(service_dict)
    else:
        service = _Config.ogr_service()

    project = service.get_project(namespace=namespace, repo=repo)

    closed_issue_bug_ids = _get_all_closed_bug_ids(project)
    aggregated_bug_list = _aggregate_bugs(predictions_file, closed_issue_bug_ids)
    to_update = _close_issues4bugs_not_in_results(project, predictions_file, aggregated_bug_list)
    _ingest_results_and_create_issues(
        ogr_project=project,
        trace_directory=trace_directory,
        max_count=max_count,
        commit_hash=commit_hash,
        aggregated_bug_list=aggregated_bug_list,
        to_update=to_update,
    )


def create_issue_with_comments(  # new implementation, one issue for each run, each comment is a single aggregated bug
    repo: str,
    predictions_file: str,
    trace_directory: str,
    namespace: str,
    service_dict: Optional[Dict[str, str]] = None,
    ref: Optional[str] = None,
):
    """Take output from Varangian application and create single issue on git forge."""
    if service_dict is not None:
        service = _ogr_service_from_dict(service_dict)
    else:
        service = _Config.ogr_service()
    project = service.get_project(namespace=namespace, repo=repo)
    if ref is None:
        ref = project.default_branch

    # TODO: false_positives = _get_false_positives(service_url, project_id)
    false_positives = _get_false_positives(project.get_web_url())

    aggregated_bug_list = _aggregate_bugs(predictions_file, false_positives)
    issue = _open_base_issue(ogr_project=project, ref=ref)
    _ingest_results_and_create_comments(
        ogr_project=project,
        issue=issue,
        trace_directory=trace_directory,
        ref=ref,
        aggregated_bug_list=aggregated_bug_list,
    )


def _open_base_issue(ogr_project: GitProject, ref: str):
    title = "Varangian: Prioritized Defects"
    body = ISSUE_BODY.format(ref=ref)
    issue = ogr_project.create_issue(title=title, body=body)
    return issue


def _get_false_positives(project_url: str) -> Set[str]:
    return set()  # TODO: replace with DB call


def _ingest_results_and_create_comments(
    ogr_project: GitProject, issue: Issue, trace_directory: str, ref: str, aggregated_bug_list: List[List[AugSaBug]]
):
    for agg_list in aggregated_bug_list:
        title, body = _generate_issue_title_and_body(
            ogr_project, agg_list=agg_list, trace_directory=trace_directory, commit_hash=ref
        )
        if isinstance(ogr_project, GithubProject):
            params = {"title": title, "body": body}
            create_issue = CREATE_ISSUE_SECTION.format(
                project_url=ogr_project.get_web_url().rstrip("/"), params=urllib.parse.urlencode(params)
            )
        elif isinstance(ogr_project, GitlabProject):
            params = {"issue[title]": title, "issue[description]": body}
            create_issue = CREATE_ISSUE_SECTION.format(
                project_url=ogr_project.get_web_url().rstrip("/"), params=urllib.parse.urlencode(params)
            )
        else:
            create_issue = ""
        issue.comment(body=f"## {title}\n\n{body}{create_issue}")


# TODO: get all false positives for this project
# TODO: aggregate bug ids

# TODO: add checkbox to mark bug as false positive or true positive

# OUTSIDE TODO: create a controller which catches edits to issue comments
