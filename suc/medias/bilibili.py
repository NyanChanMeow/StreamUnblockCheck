# -*- coding: utf-8 -*-
# Thanks for LemonBench

import random
import string
import hashlib

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class _BilibiliBase(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._session = self.random_session()

    def random_session(self) -> str:
        a = string.ascii_letters
        b = "".join(random.choice(a) for i in range(32))
        c = hashlib.md5(b.encode("utf-8"))
        return c.hexdigest()

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            try:
                j = resp.json()
                jc = j.get("code", None)
                if isinstance(jc, int):
                    if jc == 0:
                        return True
                    else:
                        return False
                else:
                    raise ResponseInvalid(
                        "Invalid response: {}".format(resp.text))
            except Exception as e:
                raise ResponseInvalid(str(e))
        else:
            raise StatusCodeInvalid(resp.status_code)


class BilibiliHKMOTW(_BilibiliBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://api.bilibili.com/pgc/player/web/playurl?avid=18281381&cid=29892777&qn=0&type=&otype=json&ep_id=183799&fourk=1&fnver=0&fnval=16&session={}&module=bangumi".format(
            self._session)


class BilibiliTWOnly(_BilibiliBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://api.bilibili.com/pgc/player/web/playurl?avid=50762638&cid=100279344&qn=0&type=&otype=json&ep_id=268176&fourk=1&fnver=0&fnval=16&session={}&module=bangumi".format(
            self._session)
