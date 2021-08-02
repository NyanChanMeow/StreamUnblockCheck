from .media_base import MediaBase
from ..types.errors.requests import StatusCodeInvalid


class Niconico(MediaBase):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._url = "https://www.nicovideo.jp/watch/so23017073"

    def run(self) -> bool:
        resp = self._get()
        if resp.status_code == 200:
            return not "同じ地域" in resp.text
        else:
            raise StatusCodeInvalid(resp.status_code)