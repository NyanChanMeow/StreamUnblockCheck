# -*- coding: utf-8 -*-

import time
import os
import logging
import requests

from suc import medias
from suc.config import Configs

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    handlers=[
        logging.FileHandler(
            filename="./logs/" +
            time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info("Starting test")
    for k, v in Configs["tasks"].items():
        if not v.get("enabled", True):
            continue

        logging.info("Starting task {}".format(k))
        for kk, vv in v["medias"].items():
            if not vv.get("enabled", True):
                continue

            logging.info("Running {} in task {}".format(kk, k))
            hw = medias.Medias.get(kk, None)
            if hw is None:
                logging.error("{} not found, task {}".format(kk, k))
            wcnm = hw(vv)
            logging.info("{}: {}".format(kk, wcnm.run()))
