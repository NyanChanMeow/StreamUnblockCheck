# -*- coding: utf-8 -*-

import time
import os
import logging
import requests

from suc import medias

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
    nf = medias.Medias["Netflix"]()
    nf.run()
