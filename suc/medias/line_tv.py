# -*- coding: utf-8 -*-

import re

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class LineTV(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://tv.line.me/"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            if "NOT AVAILABLE" in resp.text:
                return False
            return True
        else:
            raise StatusCodeInvalid(resp.status_code)
