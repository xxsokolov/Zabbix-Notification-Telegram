#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################

tg_proxy = False
tg_proxy_server = {'https': 'socks5://username:password@domen:port'}
tg_token = '123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'

watermark_label = 'Dmitry Sokolov (@xxsokolov)'
watermark_font = '/font/ArialMT.ttf'
watermark_fill = 255
watermark_rotate = 0
watermark_expand = True
watermark_text_color = (60, 60, 60)

body_messages = '<b>{subject}</b>\n\n{messages}\nLinks: {links}\n\n{tags}'
body_messages_title = '{title} ({period_hour}h)'
body_messages_url = '<a href="{}" title="Info">ℹ️</a>'
body_messages_no_url = '➖'
body_messages_no_tags = '#no_tags'

zabbix_api_url = 'http://zbx.local/'
zabbix_api_login = 'zabbix_user'
zabbix_api_pass = '6Beeee6WPsgLM'
graphs_period_default = 43200  # 24h
zabbix_graff_chart = '{zabbix_server}chart3.php?' \
                     'name={name}&' \
                     'from=now-{range_time}&' \
                     'to=now&' \
                     'width=900&' \
                     'height=200&' \
                     'items[0][itemid]={itemid}&' \
                     'legend=1&' \
                     'showtriggers=1&' \
                     'showworkperiod=1'
zabbix_status_emoji_map = {
    "Problem": "🚨",
    "Resolved":"✅",
    "Information": "💙",
    "Warning":"💛",
    "Average":"🧡",
    "High":"❤️",
    "Disaster": "💔",
    "Test": "🚽💩"}
