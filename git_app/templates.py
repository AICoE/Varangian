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

"""Templates for issues and PRs opened by Varangian git application."""

# the first line of the body is to ensure we don't duplicate issuess
VARANGIAN_BUG_BODY = """
## Description:
Infer bug type: [{bug_type}]({bug_type_link})\n
Location: [{location}]({bug_link})\n
Description: {description}\n
[Likelihood](https://github.com/AICoE/Varangian/blob/main/docs/metrics/README.md#varangian-issue): {confidence}\n
## Mark here for accuracy
- [ ] True positive
- [ ] False positive
## Possible bug location:
{location}
```
{bug_trace_root}
```

## All traces:
"""

CREATE_ISSUE_SECTION = """\n\n## Create Issue from comment

[click here]({project_url}/issues/new?{params})
"""

ISSUE_FOOTER = """
## Feedback

Please open issues [here](https://github.com/AICoE/Varangian/issues/new/choose) if you have any feedback you would like
to give us.
"""

ISSUE_BODY = (
    """
## Varangian Defect Detector Bot:
Varangian is a bot which uses Augmented Static Analysis to automatically create issues for bugs in git ref: {ref}.
More information: https://github.com/AICoE/Varangian
\n
"""
    + ISSUE_FOOTER
)

SINGLE_TRACE_CONTENTS = """
\n<details><summary><b>Show trace for bug with rank {rank}</summary>
[Bug Rank](https://github.com/AICoE/Varangian/blob/main/docs/metrics/README.md#varangian-issue): {rank}\n

```
{trace_contents}
```
</details>
"""
