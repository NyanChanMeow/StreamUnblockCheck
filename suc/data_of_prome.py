# -*- coding: utf-8 -*-


from prometheus_client import Gauge


DATA_UNBLOCK_OK = 1
DATA_UNBLOCK_ERROR = 0
DATA_UNBLOCK_EXCEPTION = -1

UnblockStatus = Gauge("suc_unblock_status",
                      "Unblock status",
                      labelnames=("task", "media"))
