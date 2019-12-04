#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
from pyzabbix import ZabbixAPI
import urllib3
from zntbot.zntBot_config import *


class MBZabbix:

    def __init__(self):
        # Отключаем предупреждение об ssl
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.zapi = ZabbixAPI(zabbix_api_url)
        self.zapi.session.verify = False
        self.zapi.login(zabbix_api_login, zabbix_api_pass, )
        # print("Connected to Zabbix API Version %s" % self.zapi.api_version())

    # https://www.zabbix.com/documentation/4.4/ru/manual/api/reference/event/acknowledge
    def set_message(self, eventids, message):
        self.zapi.event.acknowledge(
            eventids=eventids,
            action=4,
            message=message
        )
