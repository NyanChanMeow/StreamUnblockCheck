# -*- coding: utf-8 -*-

import requests
import logging
from dns.resolver import Resolver
from abc import ABC, abstractmethod
from urllib3.util import connection
from urllib3.exceptions import ConnectionError

_orig_create_connection = connection.create_connection


class MediaBase(ABC):
    def __init__(self, config: dict = {}):
        self._user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
        self._timeout = 10
        self._url = ""

        self._dns = config.get("dns", "8.8.8.8")

        def _dns_create_connection(address: tuple, *args, **kwargs):
            host, port = address
            resolver = Resolver(configure=False)
            resolver.nameservers = [self._dns]
            logging.info("Resolving {} via {}".format(host, self._dns))
            resp = resolver.resolve(host, "a")
            if len(resp) == 0:
                raise ConnectionError("Cannot resolve {}".format(host))

            return _orig_create_connection((str(resp[0]), port), *args, **kwargs)

        self._dns_create_connection = _dns_create_connection

    def _post(self, url_override: str = "", data: dict = {}, headers: dict = {}, json: dict = {}) -> requests.Response:
        if not self._url and not url_override:
            raise ValueError("URL unspecified")

        h = {"User-Agent": self._user_agent}
        h.update(headers)
        try:
            connection.create_connection = self._dns_create_connection
            resp = requests.post(
                url=self._url if not url_override else url_override,
                timeout=self._timeout,
                headers=h,
                data=data,
                json=json
            )
        finally:
            connection.create_connection = _orig_create_connection

        logging.debug(resp.text)

        return resp

    def _get(self, url_override: str = "", headers: dict = {}) -> requests.Response:
        if not self._url and not url_override:
            raise ValueError("URL unspecified")

        h = {"User-Agent": self._user_agent}
        h.update(headers)

        try:
            connection.create_connection = self._dns_create_connection
            resp = requests.get(
                url=self._url if not url_override else url_override,
                timeout=self._timeout,
                headers=h
            )
        finally:
            connection.create_connection = _orig_create_connection

        logging.debug(resp.text)

        return resp

    @abstractmethod
    def run(self) -> bool:
        pass


class MediaBaseSelenium(ABC):
    def __init__(self, config: dict = {}):
        self._webdri = None
        self._ff_profile = None

    @abstractmethod
    def run(self) -> bool:
        pass

    def _set_string_preferce(self, key: str, value: str):
        self._webdri.get("about:config")
        self._webdri.execute_script("""
var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
prefs.setStringPref(arguments[0], arguments[1]);
        """, key, value)
