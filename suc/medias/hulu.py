# -*- coding: utf-8 -*-


from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid, ResponseInvalid


class HuluJP(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://papi.prod.hjholdings.tv/api/v1/playback/auth"

    def run(self) -> bool:
        resp = self._post(
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={"meta_id": "asset:100060582",
                  "vuid": "4b60a7fda1de1fefe701a45f7e9fbf1c",
                  "device_code": 1,
                  "app_id": 1,
                  "with_resume_point": True}
        )
        if resp.status_code == 201:
            return True
        elif resp.status_code == 403:
            return False
        else:
            raise StatusCodeInvalid(resp.status_code)
