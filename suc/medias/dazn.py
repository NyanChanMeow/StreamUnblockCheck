# -*- coding: utf-8 -*-

import re

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class Dazn(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://startup-prod.dazn.com/misl/v5/Startup"

    def run(self) -> bool:
        resp = self._post(
            json={"LandingPageKey": "generic", "Languages": "zh-TW,zh,en-US,en",
                  "Platform": "web", "Version": "2"},
            headers={"Content-Type": "application/json"})

        res = re.findall(r'(?<=isAllowed":)[0-9A-Za-z]+', resp.text)
        if not res:
            raise ResponseInvalid("Data not found")

        if res[0] == "false":
            return False
        elif res[0] == "true":
            return True
        else:
            raise ResponseInvalid("Invalid Response: {}".format(res[0]))
