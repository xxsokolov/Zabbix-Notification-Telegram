#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
config_debug_mode = False
config_exc_info = False
config_cache_file = './zbxTelegram_files/id.cache'
config_log_file = './zntbot.log'

tg_proxy = True
tg_proxy_server = {'https': 'socks5://username:password@domen:port'}
tg_token = '123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'

zabbix_api_url = 'https://modulmon.ru/admin/zabbix/'
zabbix_api_login = 'zabbix_autocreator'
zabbix_api_pass = '6BJsxQB6G6WPsgLM'

bot_message_complete = 'User @{username} ({lastname} {firstname}) completed an action "{action}: {message}"'
bot_meesage_go_back = 'Go back to chat'
answer_keyboard = [
    dict(name='❌ Cancel',action='cancel'),
    dict(name='✅ Sent',action='sent'),
    dict(name='🚀 Sending',action='sending')

]