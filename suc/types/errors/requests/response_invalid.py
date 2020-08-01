# -*- coding: utf-8 -*-


class ResponseInvalid(Exception):
    def __init__(self, message: str):
        super().__init__(message)
