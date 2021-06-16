# -*- coding: utf-8 -*-

import json

from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid

# TODO: Retrieve token
class DisneyPlus(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://global.edge.bamgrid.com/token"
        self._authorization = config.get("authorization", "")
        self._raw_data = config.get("raw_data", "")

    def run(self) -> bool:
        headers = {
            "Accept": "application/json",
            "authorization": self._authorization,
            "Content-Type": "application/x-www-form-urlencoded",
            "x-bamsdk-platform": "windows",
            "x-bamsdk-version": "4.10",
            "Origin": "https://www.disneyplus.com",
            "Referer": "https://www.disneyplus.com/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "Trailers"
        }

        resp = self._post(data=self._raw_data, headers=headers)
        if resp.status_code == 400:
            try:
                res = resp.json()
                if res.get("error", "") == "unauthorized_client" and res.get("error_description", "") == "forbidden-location":
                    return False
                else:
                    raise ResponseInvalid(
                        "Response invalid: {}".format(resp.text))
            except json.decoder.JSONDecodeError:
                raise ResponseInvalid("Response invalid: {}".format(resp.text))
        elif resp.status_code == 403:
            return False
        elif resp.status_code == 200 or resp.status_code == 204:
            return True
        else:
            raise StatusCodeInvalid(resp.status_code)
