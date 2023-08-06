#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import logging.config

from path import Path

from .config import ConfigLoader


def initialize(loglevel=None, conf="logging.yaml", *, mode=os.getenv):
    # 获取日志配置
    cfgl = ConfigLoader()
    cfg = cfgl.get(conf, mode)
    # 创建日志目录
    for handler in cfg["handlers"].values():
        logfile = handler.get("filename")
        if logfile:
            Path(logfile).parent.makedirs_p(mode=755)
    # 初始化日志
    logging.config.dictConfig(config=cfg)
    # 设置日志级别
    if not loglevel:
        loglevel = os.getenv(f"{cfgl.name.upper()}_LOG_LEVEL") or os.getenv(f"PROJECT_LOG_LEVEL")
    if loglevel:
        logging.getLogger().setLevel(loglevel)
    # debug
    logging.getLogger("logs").debug(str(cfgl.get_file(conf)))
