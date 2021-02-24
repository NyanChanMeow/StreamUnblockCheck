# -*- coding: utf-8 -*-
# Thanks for LemonBench

import re
import json

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class AbemaTV(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://abema.tv/now-on-air/abema-news"

    def run(self) -> bool:
        # check ip region
        resp = self._get("http://abematv.akamaized.net/region")
        if resp.status_code == 403 or resp.status_code == 0:
            return False
        elif resp.status_code != 200:
            raise StatusCodeInvalid(resp.status_code)

        resp = self._get()
        if resp.status_code == 200:
            res = re.findall(
                r"(?<=window\.__CLIENT_REGION__\ \=\ ).*?(?=;)", resp.text)
            if not res:
                raise ResponseInvalid("Data not found")

            jc = {}
            try:
                jc = json.loads(res[0])
            except Exception as e:
                raise ResponseInvalid(str(e))

            nmsl = jc.get("isAllowed", None)
            if nmsl is None or not isinstance(nmsl, bool):
                raise ResponseInvalid(
                    "Data not found, raw data: {}".format(res[0]))

            return nmsl
        else:
            raise StatusCodeInvalid(resp.status_code)
