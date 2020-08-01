# -*- coding: utf-8 -*-

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


# Thanks for LemonBench
class HBONow(MediaBase):
    def __init__(self):
        super().__init__()
        self._url = "https://play.hbonow.com"
        self.name = "HBO Now"

    def run(self) -> bool:
        resp = self._send()
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
