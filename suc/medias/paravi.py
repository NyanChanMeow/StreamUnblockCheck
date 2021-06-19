# -*- coding: utf-8 -*-

import re

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


# Thanks for https://github.com/lmc999/RegionRestrictionCheck
class Paravi(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://api.paravi.jp/api/v1/playback/auth"

    def run(self) -> bool:
        resp = self._post(
            json={"meta_id": 71885,
                  "vuid": "3b64a775a4e38d90cc43ea4c7214702b",
                  "device_code": 1,
                  "app_id": 1},
            headers={"Content-Type": "application/json"})

        if resp.status_code != 201:
            raise StatusCodeInvalid(resp.status_code)

        try:
            if resp.json()["error"]["code"] == 2055:
                return False
        except KeyError:
            pass
        except Exception as e:
            raise ResponseInvalid("Invalid Response: {}".format(str(e)))

        if "playback_validity_end_at" in resp.text:
            return True
        else:
            return False
