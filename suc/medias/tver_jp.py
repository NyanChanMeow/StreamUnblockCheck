# -*- coding: utf-8 -*-

import re

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class TVerJP(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = config["url"]
        self._url_js = config["url_js"]

    def run(self) -> bool:
        resp_js = self._get(url_override = self._url_js)
        policy_key = ""
        if resp_js.status_code == 200:
            res = re.findall(r'policyKey\:\".*?(?=")', resp_js.text)
            if not res:
                raise ResponseInvalid("PolicyKey not found")
            policy_key = res[0][11:]
        else:
            raise StatusCodeInvalid(resp_js.status_code)
        
        headers = {
            "Accept": "application/json;pk={}".format(policy_key),
            "Origin": "https://tver.jp",
            "Referer": "https://tver.jp/",
            "Pargma": "no-cache",
            "Cache-Control": "no-cache"
        }
        resp = self._get(headers=headers)

        # 401: Policy Key Invalid
        if resp.status_code == 200:
            return True
        elif resp.status_code == 403:
            rj = resp.json()
            if rj.get("error_subcode", "") == "CLIENT_GEO":
                return False
            raise ResponseInvalid("Invalid error message {}".format(resp.text))
        elif resp.status_code == 401:
            raise ResponseInvalid("Invalid status code {}, {}".format(resp.status_code, resp.text))
        else:
            raise StatusCodeInvalid(resp.status_code)
