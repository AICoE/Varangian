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

VARANGIAN_BUG_BODY = """
# Automated issue created by Varangian
## Description:
id: {trace_id}
Infer bug type: {bug_type}
Location: {location}
Description: {description}
Rank: {rank}
Confidence: {confidence}
## Bug trace:
{trace_preview}
<details>
  <summary><b>Show more</b></summary>
  {full_trace}
</details>
"""
