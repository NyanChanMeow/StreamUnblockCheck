# -*- coding: utf-8 -*-
# Thanks for LemonBench

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class HBONow(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://play.hbonow.com"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            if resp.url == "https://play.hbonow.com" or resp.url == "https://play.hbonow.com/":
                return True
            elif resp.url == "http://hbogeo.cust.footprint.net/hbonow/geo.html" or resp.url == "http://geocust.hbonow.com/hbonow/geo.html":
                return False
            else:
                raise ResponseInvalid(
                    "Invalid response url: {}".format(resp.url))
        else:
            raise StatusCodeInvalid(resp.status_code)
