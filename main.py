# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
import logging
import requests
from prometheus_client import start_http_server

from suc import medias
from suc.config import Configs
from suc.data_of_prome import (
    UnblockStatus, DATA_UNBLOCK_ERROR, DATA_UNBLOCK_EXCEPTION,
    DATA_UNBLOCK_OK
)

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

scheduler = BackgroundScheduler()

def run():
    for k, v in Configs["tasks"].items():
        if not v.get("enabled", True):
            continue

        logging.info("Starting task {}".format(k))
        for kk, vv in v["medias"].items():
            vv.update(Configs["public_configs"].get(
                vv.get("public_config", ""), {}))

            if not vv.get("enabled", True):
                continue

            # logging.info("Running {} in task {}".format(kk, k))
            hw = medias.Medias.get(kk, None)
            if hw is None:
                logging.error("{} not found, task {}".format(kk, k))
                continue

            def func(hw, k, kk, vv):
                try:
                    wcnm = hw(vv)
                    result = wcnm.run()
                    if result:
                        UnblockStatus.labels(k, kk).set(DATA_UNBLOCK_OK)
                    else:
                        UnblockStatus.labels(k, kk).set(DATA_UNBLOCK_ERROR)
                    logging.info("{}: {}".format(kk, result))
                except Exception:
                    logging.exception("\n")
                    UnblockStatus.labels(k, kk).set(DATA_UNBLOCK_EXCEPTION)
            logging.info("Running {} in task {} for first time".format(kk, k))
            func(hw, k, kk, vv)

            interval = vv.get("interval", Configs["interval"])
            job = scheduler.add_job(func, "interval", args=(hw, k, kk, vv), seconds=interval)
            logging.info("Added job {} in task {}, interval {}s, id {}".format(kk, k, interval, job.id))


if __name__ == "__main__":
    try:
        logging.info("Starting prometheus exporter at {}:{}".format(
            Configs["prometheus_host"], Configs["prometheus_port"]))
        start_http_server(addr=Configs["prometheus_host"], port=Configs["prometheus_port"])
        run()
        scheduler.start()
        logging.info("Started scheduler")
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Closing scheduler")
        scheduler.shutdown()
        exit(0)
