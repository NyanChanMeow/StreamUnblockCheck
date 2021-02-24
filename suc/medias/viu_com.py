# -*- coding: utf-8 -*-

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class ViuCom(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://www.viu.com/ott/geo/check.php"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            j = resp.headers.get("location", None)
            if j is not None and j == "https://www.viu.com/ott/no-service/":
                return False
            else:
                return True
        else:
            raise StatusCodeInvalid(resp.status_code)
