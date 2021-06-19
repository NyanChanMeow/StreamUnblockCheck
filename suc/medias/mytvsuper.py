# -*- coding: utf-8 -*-

import re

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid


# Thanks for https://github.com/lmc999/RegionRestrictionCheck
class MyTVSuper(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://www.mytvsuper.com/iptest.php"

    def run(self) -> bool:
        resp = self._get()

        if resp.status_code != 200:
            raise StatusCodeInvalid(resp.status_code)

        if "HK" in resp.text:
            return True
        else:
            return False
