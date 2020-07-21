#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
__author__ = "Sokolov Dmitry"
__maintainer__ = "Sokolov Dmitry"
__license__ = "MIT"

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
watermark_minimal_height = 30
watermark_fill = 255
watermark_rotate = 0
watermark_expand = True
watermark_text_color = (60, 60, 60)

body_messages = '<b>{subject}</b>\n\n{messages}'
body_messages_title = '{title} ({period_hour}h)'

body_messages_url = True
body_messages_url_notes = True
body_messages_url_graphs = True
body_messages_url_host = True
body_messages_url_ack = True
body_messages_url_event = True
body_messages_url_template = '<a href="{url}">{icon}</a>'
body_messages_url_template_line = '\nLinks: {links}'
body_messages_url_emoji_no_url = '➖'
body_messages_url_emoji_notes = 'ℹ️'  # URL in trigger
body_messages_url_emoji_graphs = '📊'  # URL history graph item
body_messages_url_emoji_host = '📟'  # URL host
body_messages_url_emoji_akk = '✉️'  # URL update problem
body_messages_url_emoji_event = '📋'  # URL in event

body_messages_tags = True
body_messages_tags_event = True
body_messages_tags_eventid = True
body_messages_tags_itemid = True
body_messages_tags_triggerid = True
body_messages_tags_actionid = True
body_messages_tags_hostid = True
body_messages_tags_template_line = '\n\n{tags}'
body_messages_tags_no = '#no_tags'
body_messages_tags_delimiter = ' '
body_messages_tags_prefix_eventid = 'eid_'
body_messages_tags_prefix_itemid = 'iid_'
body_messages_tags_prefix_triggerid = 'tid_'
body_messages_tags_prefix_actionid = 'aid_'
body_messages_tags_prefix_hostid = 'hid_'

tag_settings_no_graph = 'no_graph'

zabbix_keyboard = False
zabbix_keyboard_button_message = 'Message'
zabbix_keyboard_button_acknowledge = 'Acknowledge'
zabbix_keyboard_button_history = 'History'
zabbix_keyboard_row_width = 3

zabbix_api_url = 'http://127.0.0.1/zabbix/'
zabbix_api_login = 'Admin'
zabbix_api_pass = 'zabbix'

zabbix_graph = True
zabbix_graph_period_default = 43200  # 24h
zabbix_graph_chart = '{zabbix_server}chart3.php?' \
                     'name={name}&' \
                     'from=now-{range_time}&' \
                     'to=now&' \
                     'width=900&' \
                     'height=200&' \
                     'items[0][itemid]={itemid}&' \
                     'legend=1&' \
                     'showtriggers=1&' \
                     'showworkperiod=1'

zabbix_host_link = "{zabbix_server}zabbix.php?action=search&search={host}"
zabbix_graph_link = "{zabbix_server}history.php?action=showgraph&itemids[]={itemid}&from=now-{range_time}"
#zabbix_akk_link = "{zabbix_server}zabbix.php?action=acknowledge.edit&eventids[0]={eventid}"  # Zabbix Server ver > 5
zabbix_akk_link = "{zabbix_server}zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]={eventid}" # Zabbix Server ver <= 5
zabbix_event_link = "{zabbix_server}tr_events.php?triggerid={triggerid}&eventid={eventid}"


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
