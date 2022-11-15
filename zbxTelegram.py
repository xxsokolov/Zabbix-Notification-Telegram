#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
# https://github.com/xxsokolov/Zabbix-Notification-Telegram
__author__ = "Sokolov Dmitry"
__maintainer__ = "Sokolov Dmitry"
__license__ = "MIT"
import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from zbxTelegram_files.classes.argparser import ArgParsing
import xmltodict
from zbxTelegram_config import *
import requests
import urllib3
import re
import sys
import os
import io
from PIL import Image, ImageDraw, ImageFont
import json
from errno import ENOENT
import logging
import html


class System:
    def __init__(self, debug=False):
        # configuring log
        if debug:
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO

        log_format = logging.Formatter(
            '[%(asctime)s] - PID:%(process)s - %(funcName)s() - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')
        self.log = logging.getLogger()
        self.log.setLevel(self.log_level)

        # writing to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        # stdout_handler = logging.StreamHandler(codecs.getwriter("utf-8")(sys.stdout.detach()))
        stdout_handler.setLevel(self.log_level)
        stdout_handler.setFormatter(log_format)
        # writing to file
        file_handler = logging.FileHandler(filename=config_log_file, mode='a')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(log_format)

        self.log.addHandler(stdout_handler)
        self.log.addHandler(file_handler)


class FailSafeDict(dict):
    def __missing__(self, key):
        return '{{key not found: {}}}'.format(key)


args = ArgParsing().create_parser().parse_args(sys.argv[1:])
loggings = System(config_debug_mode if not args.debug else True).log
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot = telebot.TeleBot(tg_token)
if tg_proxy:
    apihelper.proxy = tg_proxy_server


def xml_parsing(data):
    try:
        data = dict(xmltodict.parse(data, process_namespaces=True)['root'])

        message = data['body']['messages']

        settings_graphs_bool = data['settings']['graphs']
        settings_graphlinks_bool = data['settings']['graphlinks']
        settings_triggerlinks_bool = data['settings']['triggerlinks']
        settings_hostlinks_bool = data['settings']['hostlinks']
        settings_acklinks_bool = data['settings']['acklinks']
        settings_eventlinks_bool = data['settings']['eventlinks']

        settings_eventtag_bool = data['settings']['eventtag']
        settings_eventidtag_bool = data['settings']['eventidtag']
        settings_itemidtag_bool = data['settings']['itemidtag']
        settings_triggeridtag_bool = data['settings']['triggeridtag']
        settings_actionidtag_bool = data['settings']['actionidtag']
        settings_hostidtag_bool = data['settings']['hostidtag']
        settings_zntsettingstag_bool = data['settings']['zntsettingstag']

        settings_mentions_bool = data['settings']['zntmentions']

        settings_keyboard = data['settings']['keyboard']

        settings_graphs_period = data['settings']['graphs_period']
        settings_host = data['settings']['host']
        settings_itemid = data['settings']['itemid']
        settings_triggerid = data['settings']['triggerid']
        settings_eventid = data['settings']['eventid']
        settings_actionid = data['settings']['actionid']
        settings_hostid = data['settings']['hostid']
        settings_title = data['settings']['title']
        settings_trigger_url = data['settings']['triggerurl']

        settings_eventtags = data['settings']['eventtags']

        return dict(title=settings_title, message=message, eventtags=settings_eventtags,
                    settings_graphs_bool=eval(settings_graphs_bool.capitalize()),
                    settings_graphlinks_bool=eval(settings_graphlinks_bool.capitalize()),
                    settings_triggerlinks_bool=eval(settings_triggerlinks_bool.capitalize()),
                    settings_hostlinks_bool=eval(settings_hostlinks_bool.capitalize()),
                    settings_acklinks_bool=eval(settings_acklinks_bool.capitalize()),
                    settings_eventlinks_bool=eval(settings_eventlinks_bool.capitalize()),
                    settings_eventtag_bool=eval(settings_eventtag_bool.capitalize()),
                    settings_eventidtag_bool=eval(settings_eventidtag_bool.capitalize()),
                    settings_itemidtag_bool=eval(settings_itemidtag_bool.capitalize()),
                    settings_triggeridtag_bool=eval(settings_triggeridtag_bool.capitalize()),
                    settings_actionidtag_bool=eval(settings_actionidtag_bool.capitalize()),
                    settings_hostidtag_bool=eval(settings_hostidtag_bool.capitalize()),
                    settings_zntsettingstag_bool=eval(settings_zntsettingstag_bool.capitalize()),
                    settings_zntmentions_bool=eval(settings_mentions_bool.capitalize()),
                    settings_keyboard_bool=eval(settings_keyboard.capitalize()),
                    graphs_period=settings_graphs_period, host=settings_host, itemid=settings_itemid,
                    triggerid=settings_triggerid, triggerurl=settings_trigger_url, eventid=settings_eventid,
                    actionid=settings_actionid, hostid=settings_hostid)

    except Exception as err:
        loggings.error("Exception occurred: No XML in zabbix actions or it's not valid (xml parsing error). XML: {} ".format(
            err), exc_info=config_exc_info), exit(1)


def watermark_text(img):
    img = io.BytesIO(img)
    img = Image.open(img)
    if img.height < watermark_minimal_height:
        loggings.info("Cannot set watermark text, img height {} (min. {})".format(img.height, watermark_minimal_height))
        return False
    font = ImageFont.truetype(watermark_font, 14)

    line_height = sum(font.getmetrics())

    fontimage = Image.new('L', (font.getsize(watermark_label)[0], line_height))
    ImageDraw.Draw(fontimage).text((0, 0), watermark_label, fill=watermark_fill, font=font)
    fontimage = fontimage.rotate(watermark_rotate,  resample=Image.BICUBIC, expand=True)

    img_size = img.crop().size
    size = (img_size[0]-fontimage.size[0]-5, img_size[1]-fontimage.size[1]-10)

    img.paste(watermark_text_color, box=size, mask=fontimage)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr


def get_cookie():
    data_api = {"name": zabbix_api_login,"password": zabbix_api_pass,"enter": "Sign in"}
    req_cookie = requests.post(zabbix_api_url, data=data_api, verify=False)
    cookie = req_cookie.cookies
    req_cookie.close()
    if not any(_ in cookie for _ in ['zbx_session', 'zbx_sessionid']):
        loggings.error(
            'User authorization failed: {} ({})'.format('Login name or password is incorrect.', zabbix_api_url))
        return False
    return cookie


def get_chart_png(itemid, graff_name, period=None):
    try:
        cookies = get_cookie()
        if cookies:
            response = requests.get(zabbix_graph_chart.format(
                name=graff_name,
                itemid=itemid,
                zabbix_server=zabbix_api_url,
                range_time=period),
                cookies=cookies,
                verify=False)

            if watermark:
                wmt = watermark_text(response.content)
                if wmt:
                    return dict(img=wmt, url=response.url)
                else:
                    return dict(img=response.content, url=response.url)
            else:
                return dict(img=response.content, url=response.url)
        else:
            return dict(img=None, url=None)
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def create_tags_list(_bool=False, tag=None, _type=None, zntsettingstag=False):
    tags_list = []
    settings_list = []
    try:
        if _bool:
            if tag and (re.search(r'\w', tag)):
                for tags in tag.split(', '):
                    if tags:
                        if not zntsettingstag:
                            if tags.find(':') != -1:
                                tag, value = re.split(r':+',tags, maxsplit=1)
                                if tag != trigger_settings_tag and tag != trigger_info_mentions_tag:
                                    tags_list.append('#{tag}_{value}'.format(
                                        tag=_type + re.sub(r"\W+", "_", tag) if _type else re.sub(r"\W+", "_", tag),
                                        value=re.sub(r"\W+", "_", value)))
                                else:
                                    continue
                            else:
                                if len(tags.split()) > 0:
                                    for tg_s in tags.split():
                                        tags_list.append('#{tag}'.format(
                                            tag=_type + re.sub(r"\W+", "_", tg_s) if _type else re.sub(r"\W+", "_", tg_s)))
                                else:
                                    tags_list.append('#{tag}'.format(
                                        tag=_type + re.sub(r"\W+", "_", tags) if _type else re.sub(r"\W+", "_", tags)))
                        else:
                            if tags.find(':') != -1:
                                tag, value = re.split(r':+',tags, maxsplit=1)
                                if tag == trigger_settings_tag:
                                    tags_list.append('#{tag}_{value}'.format(
                                        tag=_type + re.sub(r"\W+", "_", tag) if _type else re.sub(r"\W+", "_", tag),
                                        value=re.sub(r"\W+", "_", value)))
                                    settings_list.append(value)
                                else:
                                    continue
                            else:
                                continue
                    else:
                        tags_list.append(body_messages_tags_no)
            else:
                tags_list.append(body_messages_tags_no)
        else:
            return False

    except ValueError:
        tags_list.append(body_messages_tags_no)
    else:
        return body_messages_tags_delimiter.join(tags_list) if not zntsettingstag else {
            'tags': body_messages_tags_delimiter.join(tags_list),
            trigger_settings_tag: settings_list}


def create_mentions_list(_bool=False, mentions=None):
    mentions_list = []
    try:
        if _bool and mentions:
            for tags in mentions.split(', '):
                if tags.find(':') != -1:
                    tag, value = re.split(r':+',tags, maxsplit=1)
                    if tag == trigger_info_mentions_tag:
                        for username in value.split():
                            mentions_list.append(username)
            return mentions_list
        else:
            return False
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def create_links_list(_bool=None, url=None, _type=None, url_list=None):
    try:
        if _bool:
            if url and (re.search(r'\w', url)):
                return body_messages_url_template.format(url=url, icon=_type)
            else:
                return body_messages_url_emoji_no_url
        elif url_list:
            return url_list
        else:
            return False
    except ValueError:
        return body_messages_url_emoji_no_url


def get_cache(title):
    read_cache = None
    try:
        if not os.path.exists(config_cache_file):
            raise IOError(ENOENT, 'No such file or directory', config_cache_file)
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info)
        open(config_cache_file, 'a').close()
        loggings.info("Cache file created in {}".format(config_cache_file))
    else:
        read_cache = open(config_cache_file, 'r').read()

    if read_cache:
        cache = json.loads(read_cache)

        for name, value in cache.items():
            if title == name:
                return value['id']
    else:
        return False


def set_cache(title, send_id, sent_type, cache=None, update=None):
    f = open(config_cache_file, 'r+')
    r = f.read()
    if r:
        cache = json.loads(r)
    if not cache:
        cache = {title: dict(type=str(sent_type), id=str(send_id))}
    else:
        if not update:
            cache[title] = dict(type=str(sent_type), id=str(send_id))
        else:
            cache[title] = dict(type=str(sent_type), id=str(send_id), old=str(update))
    f.seek(0)
    f.write(json.dumps(cache,sort_keys=True, ensure_ascii=False, indent=4))
    f.close()
    if update:
        loggings.info("Updated id for {} ({}): old '{}' -> new '{}' in cache file".format(
            title, sent_type, update, send_id))
    else:
        loggings.info("Add new id {} for {} ({}) in cache file".format(send_id, title, sent_type))
    return True


def migrate_group_id(sent_to, sent_id, err):
    for key, value in json.loads(err.result.text).items():
        if key == 'parameters' and value['migrate_to_chat_id']:
            loggings.warning("Group chat was upgraded to a supergroup chat ({})".format(value['migrate_to_chat_id']),
                             exc_info=config_exc_info)
            set_cache(sent_to, value['migrate_to_chat_id'], 'supergroup', update=sent_id)


def get_send_id(send_to):
    try:
        chat = None
        if re.search('^[0-9]+$', send_to) or re.search('^-[0-9]+$', send_to):
            return send_to
        elif re.search('^@+[a-zA-Z0-9_]{5,}$', send_to):
            send_to = send_to.replace("@", "")
        elif not send_to:
            raise ValueError('Username or groupname is not specified. You can use for username '
                             '@[a-z,A-Z,0-9 and underscores] and for groupname any characters. ')

        send_id = get_cache(send_to)

        if send_id:
            return send_id

        loggings.info("Telegram API: method getUpdate: started")
        get_updates_list = bot.get_updates(timeout=10)
        sum_del_update_id = 0
        while len([value.update_id for value in get_updates_list]) >= 100:
            sum_del_update_id += len([value.update_id for value in get_updates_list])
            get_updates_list = bot.get_updates(timeout=10, offset=max([value.update_id for value in get_updates_list]))

        if sum_del_update_id > 0:
            loggings.info("In getUpdate list was cleared {} messages. Submitted for processing {}.".format(
                sum_del_update_id, len([value.update_id for value in get_updates_list])))

        for line in get_updates_list:
            if line.message:
                chat = line.message.chat
            elif line.edited_message:
                chat = line.edited_message.chat
            elif line.channel_post:
                chat = line.channel_post.chat

            if chat.type in ["group", "supergroup"] and chat.title and chat.title == send_to:
                if not send_id:
                    set_cache(send_to, chat.id, chat.type)
                bot.get_updates(timeout=10, offset=-1)
                return chat.id

            if chat.type in ["channel"] and chat.title and chat.title == send_to:
                if not send_id:
                    set_cache(send_to, chat.id, chat.type)
                bot.get_updates(timeout=10, offset=-1)
                return chat.id

            if chat.type in ["private"] and chat.username == send_to.replace("@", ""):
                if not send_id:
                    set_cache(send_to, chat.id, chat.type)
                bot.get_updates(timeout=10, offset=-1)
                return chat.id

        raise ValueError('Username or groupname not found in the cache file. No access occurred or bot is not added to '
                         'group "{sendto}" (Add bot group and/or send message to {bot})'.format(
            bot=bot.get_me().username,
            sendto=send_to))
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def gen_markup(eventid):
    markup = InlineKeyboardMarkup()
    markup.row_width = zabbix_keyboard_row_width
    markup.add(
        InlineKeyboardButton(zabbix_keyboard_button_message,
                             callback_data='{}'.format(json.dumps(dict(action="messages", eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_acknowledge,
                             callback_data='{}'.format(json.dumps(dict(action="acknowledge", eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="history", eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="last value", eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="graphs", eventid=eventid)))))
    return markup


def send_messages(sent_to, message, graphs_png, eventid=None, settings_keyboard=None, disable_notification=False):
    try:
        sent_id = get_send_id(sent_to)
        if message and sent_to:
            if graphs_png and isinstance(graphs_png, list):
                try:
                    graphs_png[0].caption = message
                    graphs_png[0].parse_mode = "HTML"
                    bot.send_media_group(chat_id=sent_id, media=graphs_png, disable_notification=disable_notification)
                except apihelper.ApiException as err:
                    if 'migrate_to_chat_id' in err.result.text:
                        migrate_group_id(sent_to, sent_id, err)
                        send_messages(sent_to, message, graphs_png, settings_keyboard)
                    else:
                        loggings.error("Exception occurred in Api Telegram: {}".format(err), exc_info=config_exc_info),
                        exit(1)
                except Exception as err:
                    loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info),exit(1)
                else:
                    loggings.info('Bot @{busername}({bid}) send media group to "{sent_to}" ({sent_id}).'.format(
                        sent_to=sent_to, sent_id=sent_id, busername=bot.get_me().username, bid=bot.get_me().id))
                    exit(0)
            elif graphs_png and graphs_png.get('img'):
                try:
                    bot.send_photo(chat_id=sent_id, photo=graphs_png.get('img'), caption=message, parse_mode="HTML",
                                   reply_markup=gen_markup(eventid) if zabbix_keyboard and settings_keyboard else None,
                                   disable_notification=disable_notification)
                except apihelper.ApiException as err:
                    if 'migrate_to_chat_id' in err.result.text:
                        migrate_group_id(sent_to, sent_id, err)
                        send_messages(sent_to, message, graphs_png, settings_keyboard, disable_notification)
                    elif 'IMAGE_PROCESS_FAILED' in err.result.text:
                        bot.send_photo(chat_id=sent_id, photo=open(
                              file='{0}/zbxTelegram_files/error_send_photo.png'.format(
                                  os.path.dirname(os.path.realpath(__file__))),
                              mode='rb').read(), caption=message, parse_mode="HTML",
                                       reply_markup=gen_markup(
                                           eventid) if zabbix_keyboard and settings_keyboard else None,
                                       disable_notification=disable_notification)
                    else:
                        loggings.error("Exception occurred in Api Telegram: {}".format(err), exc_info=config_exc_info),
                        exit(1)
                except Exception as err:
                    loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info),exit(1)
                else:
                    loggings.info('Bot @{busername}({bid}) send photo to "{sent_to}" ({sent_id}).'.format(
                        sent_to=sent_to, sent_id=sent_id, busername=bot.get_me().username, bid=bot.get_me().id))
            else:
                try:
                    bot.send_message(chat_id=sent_id, text=message, parse_mode="HTML", disable_web_page_preview=True,
                                     reply_markup=gen_markup(eventid) if zabbix_keyboard and settings_keyboard
                                     else None,
                                     disable_notification=disable_notification)
                except apihelper.ApiException as err:
                    if 'migrate_to_chat_id' in json.loads(err.result.text).get('parameters'):
                        migrate_group_id(sent_to, sent_id, err)
                        send_messages(sent_to, message, graphs_png, settings_keyboard, disable_notification)
                    else:
                        loggings.error("Exception occurred in Api Telegram: {}".format(err), exc_info=config_exc_info)
                        exit(1)
                except Exception as err:
                    loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)
                else:
                    loggings.info('Bot @{busername}({bid}) send message to "{sent_to}" ({sent_id}).'.format(
                        sent_to=sent_to, sent_id=sent_id, busername=bot.get_me().username, bid=bot.get_me().id))
                    exit(0)
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def set_period_day_hour(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '{}d {}h'.format(days, hours) if hours > 0 else '{}d'.format(days)
    elif hours > 0:
        return '{}h {}m'.format(hours, minutes) if minutes > 0 else '{}h'.format(hours)
    elif minutes > 0:
        return '{}m'.format(minutes)


def main():
    graph_period = None
    graph_period_raw = None
    loggings.info("Send to {} action: {}".format(args.username, args.subject))
    loggings.debug("sys.argv: {}".format(sys.argv[1:]))
    loggings.debug("Send to {}\naction: {}\nxml: {}".format(args.username, args.subject, args.messages))

    if args.subject in ['Test subject', 'test', 'Тестовая тема'] or args.messages in \
            ['This is the test message from Zabbix', 'test', 'Это тестовое сообщение от Zabbix']:
        if get_cookie():
            loggings.info('Connection check passed ({})'.format(zabbix_api_url))
            test_graph_file = '{0}/zbxTelegram_files/test.png'
            error_code = 0
        else:
            test_graph_file = '{0}/zbxTelegram_files/error_send_photo.png'
            error_code = 1

        send_messages(sent_to=args.username, message='🚨 Test 🚽💩: Test message\n'
                                                     'Host: testhost [192.168.0.0]\n'
                                                     'Last value: test (10:00:00)\n'
                                                     'Duration: 1m\n'
                                                     'Description: This message is generated with test data. '
                                                     'specify as the topic and / or zabbix\n\n'
                                                     '#Test, #eid_130144443, #iid_60605, #tid_39303, #aid_22',
                      graphs_png=dict(
                          img=open(
                              file=test_graph_file.format(os.path.dirname(os.path.realpath(__file__))),
                              mode='rb').read()))
        exit(error_code)

    data_zabbix = xml_parsing(args.messages)

    event_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_eventtag_bool') and body_messages_tags_event else False,
        tag=data_zabbix['eventtags'], _type=None)
    eventid_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_eventidtag_bool') and body_messages_tags_eventid else False,
        tag=data_zabbix['eventid'], _type=body_messages_tags_prefix_eventid)
    itemid_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_itemidtag_bool') and body_messages_tags_itemid else False,
        tag=' '.join([item_id for item_id in data_zabbix['itemid'].split() if re.findall(r"\d+", item_id)]),
        _type=body_messages_tags_prefix_itemid)
    triggerid_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_triggeridtag_bool') and body_messages_tags_triggerid else False,
        tag=data_zabbix['triggerid'], _type=body_messages_tags_prefix_triggerid)
    actionid_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_actionidtag_bool') and body_messages_tags_actionid else False,
        tag=data_zabbix['actionid'], _type=body_messages_tags_prefix_actionid)
    hostid_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_hostidtag_bool') and body_messages_tags_hostid else False,
        tag=data_zabbix['hostid'], _type=body_messages_tags_prefix_hostid)
    zntsettings_tags = create_tags_list(
        _bool=True if data_zabbix.get('settings_zntsettingstag_bool') and body_messages_tags_trigger_settings
        else False,
        tag=data_zabbix['eventtags'], _type=None, zntsettingstag=True)

    mentions = create_mentions_list(
        _bool=True if data_zabbix.get('settings_zntmentions_bool') and body_messages_mentions_settings else False,
        mentions=data_zabbix['eventtags'])

    tags_list = []
    if isinstance(zntsettings_tags, dict) and len(zntsettings_tags[trigger_settings_tag]) > 0:
        loggings.info("Found settings tag: {}: {}".format(trigger_settings_tag,
                                                          ', '.join(zntsettings_tags[trigger_settings_tag])))
        tags_list.append(zntsettings_tags['tags']) if zntsettings_tags['tags'] else None
        if trigger_settings_tag_no_alert in zntsettings_tags[trigger_settings_tag]:
            loggings.info("Message sending canceled: {}:{}".format(trigger_settings_tag, trigger_settings_tag_no_alert))
            exit(1)

    tags_list.append(event_tags) if event_tags else None
    tags_list.append(eventid_tags) if eventid_tags else None
    tags_list.append(itemid_tags) if itemid_tags else None
    tags_list.append(triggerid_tags) if triggerid_tags else None
    tags_list.append(actionid_tags) if actionid_tags else None
    tags_list.append(hostid_tags) if hostid_tags else None


    trigger_url = create_links_list(
        _bool=True if data_zabbix.get('settings_triggerlinks_bool') and body_messages_url_notes else False,
        url=data_zabbix.get('triggerurl'),
        _type=body_messages_url_emoji_notes)

    host_url = create_links_list(
        _bool=True if data_zabbix.get('settings_hostlinks_bool') and body_messages_url_host else False,
        url=zabbix_host_link.format(zabbix_server=zabbix_api_url, host=data_zabbix.get('host')),
        _type=body_messages_url_emoji_host)

    ack_url = create_links_list(
        _bool=True if data_zabbix.get('settings_acklinks_bool') and body_messages_url_ack else False,
        url=zabbix_ack_link.format(zabbix_server=zabbix_api_url, eventid=data_zabbix.get('eventid')),
        _type=body_messages_url_emoji_ack)

    event_url = create_links_list(
        _bool=True if data_zabbix.get('settings_eventlinks_bool') and body_messages_url_event else False,
        url=zabbix_event_link.format(zabbix_server=zabbix_api_url, eventid=data_zabbix.get('eventid'),
                                     triggerid=data_zabbix.get('triggerid')), _type=body_messages_url_emoji_event)

    if isinstance(zntsettings_tags, dict) and not all(settings.find(trigger_settings_tag_graph_period) and len(settings) > 0 for settings in zntsettings_tags[trigger_settings_tag]):
        try:
            graph_period_raw = [settings if settings.find(trigger_settings_tag_graph_period) == 0 else False for
                                settings in zntsettings_tags['ZNTSettings']][0]
            graph_period = int(graph_period_raw.split('=')[1])
        except Exception as err:
            loggings.error("Exception occurred: {}:{}, {}".format(
                trigger_settings_tag, graph_period_raw, err), exc_info=config_exc_info), exit(1)
    elif data_zabbix['graphs_period'] != 'default':
        graph_period = data_zabbix['graphs_period']
    else:
        graph_period = zabbix_graph_period_default
    
    url_list = []
    url_list.append(trigger_url) if trigger_url else None
    for item_id in list(set([x for x in data_zabbix.get('itemid').split()])):
        if re.findall(r"\d+", item_id):
            items_link = create_links_list(
                _bool=True if data_zabbix.get('settings_graphlinks_bool') and body_messages_url_graphs else False,
                url=zabbix_graph_link.format(zabbix_server=zabbix_api_url, itemid=item_id,
                                             range_time=data_zabbix['graphs_period']),
                _type=body_messages_url_emoji_graphs
                                           )
            url_list.append(items_link) if items_link else None
    url_list.append(event_url) if event_url else None
    url_list.append(ack_url) if ack_url else None
    url_list.append(host_url) if host_url else None
    
    graphs_name = body_messages_title.format(
        title=data_zabbix['title'],
        period_time=set_period_day_hour(graph_period))

    if (data_zabbix.get('settings_graphs_bool') and zabbix_graph) and trigger_settings_tag_no_graph not in zntsettings_tags[trigger_settings_tag]:
        num_items_id = [item_id for item_id in data_zabbix['itemid'].split() if re.findall(r"\d+", item_id)]
        if len(num_items_id) == 1:
            graphs_png = get_chart_png(itemid=num_items_id[0],
                                       graff_name=graphs_name,
                                       period=graph_period)
        else:
            graphs_png_group = []
            #  get the unique itemid
            for item_id in list(set([x for x in data_zabbix.get('itemid').split()])):
                if re.findall(r"\d+", item_id):
                    graphs_png_group.append(InputMediaPhoto(get_chart_png(
                        itemid=item_id,
                        graff_name=graphs_name,
                        period=graph_period).get('img')))
            graphs_png = graphs_png_group
    else:
        graphs_png = False

    subject = html.escape(args.subject.format_map(FailSafeDict(zabbix_status_emoji_map)))

    if body_messages_cut_symbol and len(data_zabbix['message']) > body_messages_max_symbol:
        truncated = True
        loggings.info("Message truncated to {} characters".format(body_messages_max_symbol))
    else:
        truncated = False

    body = '{} <a href="{}">...</a>'.format(
        html.escape(data_zabbix['message'])[:body_messages_max_symbol],
        zabbix_event_link.format(
            zabbix_server=zabbix_api_url, eventid=data_zabbix.get('eventid'),
            triggerid=data_zabbix.get('triggerid'))) if truncated else html.escape(data_zabbix['message'])

    links = body_messages_url_delimiter.join(url_list) if body_messages_url and len(url_list) != 0 else ''

    tags = body_messages_tags_delimiter.join(tags_list) if body_messages_tags and len(tags_list) != 0 else ''

    mentions = ' '.join(mentions) if not isinstance(mentions, bool) and body_messages_mentions_settings and len(mentions) != 0 else ''

    message = body_messages.format(subject=subject, body='\n\n'+body if body else '',
                                   links='\n'+links if links else '', tags='\n\n'+tags if tags else '',
                                   mentions='\n\n'+mentions if mentions else '')

    send_messages(args.username, message, graphs_png, data_zabbix['eventid'], data_zabbix.get('settings_keyboard_bool'),
                  disable_notification=True if isinstance(zntsettings_tags, dict) and trigger_settings_tag_not_notify in zntsettings_tags[trigger_settings_tag]
                  else False)
    exit(0)


if __name__ == "__main__":
    main()
