# -*- coding: utf-8 -*-

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class HBOMax(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://www.hbomax.com"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            return not "Not in service area" in resp.text
        else:
            raise StatusCodeInvalid(resp.status_code)
