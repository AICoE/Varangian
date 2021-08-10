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
<!-- {trace_id} -->
## Description:
Infer bug type: [{bug_type}]({bug_type_link})\n Location: [{location}]({link_location})\n Description: {description}\n
Rank: {rank}\n Confidence: {confidence}\n
## Bug trace:
```
{trace_preview}
```
<details><summary><b>Show more</b></summary>
<p>

```
{full_trace}
```

</p>
</details>

## Feedback

Please open issues [here](https://github.com/AICoE/Varangian/issues/new/choose) if you have any feedback you would like
to give us.

"""
