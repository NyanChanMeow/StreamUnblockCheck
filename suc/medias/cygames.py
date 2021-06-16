# -*- coding: utf-8 -*-

import re
import json

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


# Thanks for LemonBench
class PCRJP(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://api-priconne-redive.cygames.jp/"
        self._user_agent = "Dalvik/2.1.0 (Linux; U; Android 9; ALP-AL00 Build/HUAWEIALP-AL00)"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 404:
            return True
        elif resp.status_code == 403 or resp.status_code == 0:
            return False
        else:
            raise StatusCodeInvalid(resp.status_code)

class UmaJP(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://api-umamusume.cygames.jp/"
        self._user_agent = "Dalvik/2.1.0 (Linux; U; Android 9; ALP-AL00 Build/HUAWEIALP-AL00)"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 404:
            return True
        elif resp.status_code == 403 or resp.status_code == 0:
            return False
        else:
            raise StatusCodeInvalid(resp.status_code)
