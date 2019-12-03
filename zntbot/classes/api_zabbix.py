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
        print("Connected to Zabbix API Version %s" % self.zapi.api_version())

    def getHGroup(self, name):
        return self.zapi.hostgroup.get(
            search={"name": name},
            # excludeSearch={"name": "!Proda*"},
            searchWildcardsEnabled='true',
            output='groupid')

    def getProblem(self, groupid):
        return self.zapi.trigger.get(
            groupids=groupid,
            selectLastEvent='extend',
            selectDependencies='extend',
            # selectTags='extend',
            selectHosts='extend',
            selectItems='extend',
            # selectInterfaces='extend',
            min_severity=2,
            filter=[{"value": 1}],
            sortfield="lastchange",
            sortorder="DESC",
            only_true='true',
            monitored='true',
            active='true',
            expandDescription='true',
            expandComment='true',
            expandExpression='true'
            # recent='false',
            # selectAcknowledges=['acknowledgeid','userid','message'],
            # output=['']

        )

    def getAcknowledges(self, eventids):
        return self.zapi.event.get(
            eventids=eventids,
            select_acknowledges='extend'
        )

    # https://www.zabbix.com/documentation/4.0/ru/manual/api/reference/event/acknowledge
    def setAcknowledge(self, eventids, message):
        self.zapi.event.acknowledge(
            eventids=eventids,
            action=4,
            message=message
        )

    def get_user(self, userid):
        return self.zapi.user.get(
            userids=userid,
            output=['alias',
                    'name',
                    'surname']
        )

    def getHostinterface(self, hostid):
        return self.zapi.hostinterface.get(
            hostids=hostid,
            filter={'type': 1},
            output=['ip']
        )

    def getInventory(self, hostid):
        return self.zapi.host.get(
            hostids=hostid,
            selectInventory='extend',
            output=['inventory']
        )
