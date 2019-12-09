#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import sys
from zntbot.zntBot_config import *
import logging



class Log:

    def __init__(self, debug=False):
        # configuring log
        if debug:
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO

        log_format = logging.Formatter('[%(asctime)s] - PID:%(process)s - %(funcName)s() - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')
        self.log = logging.getLogger()
        self.log.setLevel(self.log_level)

        # writing to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self.log_level)
        stdout_handler.setFormatter(log_format)
        # writing to file
        file_handler = logging.FileHandler(filename=config_log_file, mode='a')
        # file_handler = logging.handlers.SysLogHandler(address='/dev/log')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(log_format)

        self.log.addHandler(stdout_handler)
        self.log.addHandler(file_handler)