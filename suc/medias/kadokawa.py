# -*- coding: utf-8 -*-


from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


# 艦隊これくしょん -艦これ-
class KanColle(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = ""
        self._domain_override = config.get("domain_override", "203.104.209.7")
        self._headers = {
            "Host": config.get("headers", {}).get("Host", "203.104.209.7")
        }

    def run(self) -> bool:
        self._url = "http://{}/gadget_html5/script/rollover.js".format(
            self._domain_override)
        resp = self._get(headers=self._headers)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 403:
            return False
        else:
            raise StatusCodeInvalid(resp.status_code)
