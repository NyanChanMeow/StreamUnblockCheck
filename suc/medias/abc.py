# -*- coding: utf-8 -*-

import re
import json

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class ABCCom(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://prod.gatekeeper.us-abc.symphony.edgedatg.go.com/vp2/ws/utils/2020/geo/video/geolocation.json"

    def run(self) -> bool:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://abc.com",
            "Referer": "https://abc.com/shows/the-bachelor-the-greatest-seasons-ever/episode-guide/season-01/07-ali-fedotowsky",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        resp = self._post(headers=headers, data="type=gt&brand=001&device=001")
        if resp.status_code == 200:
            res = re.findall(
                r'(?<=allowed\"\:).*?(?=,)', resp.text)
            if not res:
                raise ResponseInvalid("Data not found")

            if res[0] == "true":
                return True
            elif res[0] == "false":
                return False
            else:
                raise ResponseInvalid("{}".format(resp.text))
        else:
            raise StatusCodeInvalid(resp.status_code)
