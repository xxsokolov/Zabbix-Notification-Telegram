#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################

project_dir = '/zbxTelegram_files'
project_cache_file = 'id.cache'
log_file = '/zbxTelegram_files/znt.log'

tg_proxy = True
tg_proxy_server = {'https': 'socks5://username:password@domen:port'}
tg_token = '123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'

watermark = True
watermark_label = 'Dmitry Sokolov (@xxsokolov)'
watermark_font = '/zbxTelegram_files/ArialMT.ttf'
watermark_fill = 255
watermark_rotate = 0
watermark_expand = True
watermark_text_color = (60, 60, 60)

body_messages = '<b>{subject}</b>\n\n{messages}\nLinks: {links}\n\n{tags}'
body_messages_title = '{title} ({period_hour}h)'
body_messages_url = '<a href="{url}">{icon}</a>'
body_messages_no_url = '➖'
body_messages_url_notes = 'ℹ️'
body_messages_url_ld_graphs = '📊'

body_messages_no_tags = '#no_tags'
body_messages_add_tags_event = True
body_messages_add_tags_item = True
body_messages_add_tags_trigger = True
body_messages_add_tags_action= True

zabbix_api_url = 'http://zbx.brc.local/'
zabbix_api_login = 'zabbix_autocreator'
zabbix_api_pass = '6BJsxQB6G6WPsgLM'
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

zabbix_graff_link = "{zabbix_server}history.php?action=showgraph&itemids[]={itemid}&from=now-{range_time}"

zabbix_status_emoji_map = {
    "Problem": "🚨",
    "Resolved":"✅",
    "Information": "💙",
    "Warning":"💛",
    "Average":"🧡",
    "High":"❤️",
    "Disaster": "💔",
    "Test": "🚽💩"}
