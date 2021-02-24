# -*- coding: utf-8 -*-

import json

Configs = {}


with open("config.json", "r+") as f:
    Configs = json.load(f)
