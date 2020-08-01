# -*- coding: utf-8 -*-

import time
import os
import logging

from suc.medias import HBONow

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
    hbo_now = HBONow()
    print("{}: {}".format(hbo_now.name, hbo_now.run()))
