# -*- coding: utf-8 -*-

import requests
from abc import ABC, abstractmethod


class MediaBase(ABC):
    def __init__(self):
        self._user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
        self._timeout = 10
        self._url = ""
        self.name = ""

    def _send(self) -> requests.Response:
        if not self._url:
            raise ValueError("URL unspecified")

        return requests.get(
            url=self._url,
            timeout=self._timeout,
            headers={"User-Agent": self._user_agent}
        )

    @abstractmethod
    def run(self) -> bool:
        pass
