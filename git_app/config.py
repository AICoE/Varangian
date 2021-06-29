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

"""Configuration for Varangian git application."""

import os
from ogr.services.github import GithubService
from ogr.services.gitlab import GitlabService
from ogr.services.pagure import PagureService
from ogr.services.base import BaseGitService


class _Config:
    SERVICE_NAME = os.getenv("VARANGIAN_SERVICE_NAME", "")
    SERVICE_URL = os.getenv("VARANGIAN_SERVICE_URL")
    GITHUB_APP_ID = os.getenv("VARANGIAN_APP_ID")
    GITHUB_APP_PRIVATE_KEY_PATH = os.getenv("VARANGIAN_APP_PRIVATE_KEY_PATH")
    AUTH_TOKEN = os.getenv(f"VARANGIAN_{SERVICE_NAME.upper()}_AUTH_TOKEN")

    @classmethod
    def ogr_service(cls) -> BaseGitService:
        if cls.SERVICE_NAME == "GITHUB":
            return GithubService(
                token=cls.AUTH_TOKEN,
                github_app_id=cls.GITHUB_APP_ID,
                github_app_private_key_path=cls.GITHUB_APP_PRIVATE_KEY_PATH,
            )
        elif cls.SERVICE_NAME == "GITLAB":
            return GitlabService(token=cls.AUTH_TOKEN, instance_url=cls.SERVICE_URL)
        elif cls.SERVICE_NAME == "PAGURE":
            return PagureService(token=cls.AUTH_TOKEN, instance_url=cls.SERVICE_URL)
        else:
            raise NotImplementedError(f"Varangian cannot run on {cls.SERVICE_NAME} git services.")
