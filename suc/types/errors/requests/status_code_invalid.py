# -*- coding: utf-8 -*-

from .response_invalid import ResponseInvalid


class StatusCodeInvalid(ResponseInvalid):
    def __init__(self, status_code: int):
        super().__init__("Invalid status code: {}".format(status_code))
