# -*- coding: utf-8 -*-
# Thanks for LemonBench

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class BahamuteAnime(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://ani.gamer.com.tw/ajax/token.php?adID=89422&sn=14667"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            try:
                j = resp.json()
                jn = j.get("error", None)
                jy = j.get("animeSn", None)
                if isinstance(jn, dict):
                    return False
                elif isinstance(jy, int):
                    return True
                else:
                    raise ResponseInvalid(
                        "Invalid response: {}".format(resp.text))
            except Exception as e:
                raise ResponseInvalid(str(e))
        else:
            raise StatusCodeInvalid(resp.status_code)
