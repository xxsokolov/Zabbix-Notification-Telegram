#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################

config_debug_mode = False
config_exc_info = False
config_cache_file = '/usr/lib/zabbix/alertscripts/zbxTelegram_files/id.cache'
config_log_file = '/usr/lib/zabbix/alertscripts/zbxTelegram_files/znt.log'

tg_proxy = True
tg_proxy_server = {'https': 'socks5://username:password@domen:port'}
tg_token = '123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'

watermark = True
watermark_label = 'Dmitry Sokolov (https://github.com/xxsokolov)'
watermark_font = '/usr/lib/zabbix/alertscripts/zbxTelegram_files/ArialMT.ttf'
watermark_fill = 255
watermark_rotate = 0
watermark_expand = True
watermark_text_color = (60, 60, 60)

body_messages = '<b>{subject}</b>\n\n{messages}'
body_messages_title = '{title} ({period_hour}h)'
body_messages_url = True
body_messages_url_template = '<a href="{url}">{icon}</a>'
body_messages_no_url = '➖'
body_messages_url_notes = 'ℹ️'
body_messages_url_ld_graphs = '📊'

body_messages_tags = True
body_messages_no_tags = '#no_tags'
body_messages_add_tags_event = True
body_messages_add_tags_item = True
body_messages_add_tags_trigger = True
body_messages_add_tags_action= True

zabbix_api_url = 'http://zbx.local/'
zabbix_api_login = 'Admin'
zabbix_api_pass = 'zabbix'
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
    "Update": "🚧",
    "Information": "💙",
    "Warning":"💛",
    "Average":"🧡",
    "High":"❤️",
    "Disaster": "💔",
    "Test": "🚽💩"}
