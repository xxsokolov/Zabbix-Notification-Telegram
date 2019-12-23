#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import xmltodict
from zbxTelegram_config import *
import requests
import urllib3
import re, sys, os, time
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
            self.log_level=logging.DEBUG
        else:
            self.log_level=logging.INFO

        log_format = logging.Formatter('[%(asctime)s] - PID:%(process)s - %(funcName)s() - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')
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

loggings = System(config_debug_mode).log
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
        settings_tag_bool = data['settings']['tag']
        settings_keyboard = data['settings']['keyboard']

        settings_graphs_period = data['settings']['graphs_period']
        settings_hostid = data['settings']['hostid']
        settings_itemid = data['settings']['itemid']
        settings_triggerid = data['settings']['triggerid']
        settings_eventid = data['settings']['eventid']
        settings_actionid = data['settings']['actionid']
        settings_title = data['settings']['title']
        settings_trigger_url = data['settings']['triggerurl']

        settings_tags = data['settings']['tags']


        return dict(title=settings_title, message=message, tags=settings_tags,
                    settings_graphs_bool=eval(settings_graphs_bool.capitalize()),
                    settings_graphlinks_bool=eval(settings_graphlinks_bool.capitalize()),
                    settings_triggerlinks_bool=eval(settings_triggerlinks_bool.capitalize()),
                    settings_hostlinks_bool=eval(settings_hostlinks_bool.capitalize()),
                    settings_tag_bool=eval(settings_tag_bool.capitalize()),
                    settings_keyboard_bool=eval(settings_keyboard.capitalize()),
                    graphs_period=settings_graphs_period, hostid=settings_hostid,itemid=settings_itemid, triggerid=settings_triggerid,
                    triggerurl=settings_trigger_url, eventid=settings_eventid, actionid=settings_actionid)

    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def watermark_text(img):
    img = io.BytesIO(img)
    img = Image.open(img)
    if img.height < 20:
        return False
    font = ImageFont.truetype(watermark_font, 14)

    line_height = sum(font.getmetrics())

    fontimage = Image.new('L', (font.getsize(watermark_label)[0], line_height))
    ImageDraw.Draw(fontimage).text((0, 0), watermark_label, fill=watermark_fill, font=font)
    fontimage = fontimage.rotate(watermark_rotate,  resample=Image.BICUBIC, expand=True)

    img_size = img.crop().size
    size = (img_size[0]-fontimage.size[0]-5,img_size[1]-fontimage.size[1]-10)

    img.paste(watermark_text_color, box=size, mask=fontimage)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr


def get_chart_png(itemid, graff_name, period=None):
    try:
        data_api = {"name": zabbix_api_login, "password": zabbix_api_pass, "enter": "Sign in"}

        req_cookie = requests.post(zabbix_api_url, data=data_api, verify=False)
        cookie = req_cookie.cookies
        response = requests.get(zabbix_graff_chart.format(name=graff_name,
                                                          itemid=itemid,
                                                          zabbix_server=zabbix_api_url,
                                                          range_time= graphs_period_default if not period else period),
                                cookies=cookie,
                                verify=False)

        if watermark:
            wmt = watermark_text(response.content)
            if wmt:
                return dict(img=wmt, url=response.url)
            else:
                return dict(img=response.content, url=response.url)
        else:
            return dict(img=response.content, url=response.url)
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def create_tags_list(settings_tags, settings_eventid, settings_itemid, settings_triggerid, settings_actionid):
    tags_list = []
    try:
        if settings_tags and (re.search(r'\w', settings_tags)):
            for tags in settings_tags.split(', '):
                if tags:
                    if tags.find(':') != -1:
                        tag, value = tags.split(':')
                        tags_list.append('#{tag}_{value}'.format(tag=re.sub("\W+", "_",tag),
                                                                 value=re.sub("\W+", "_",value)))
                    else:
                        tags_list.append('#{tag}'.format(tag=re.sub("\W+", "_",tags)))
                else:
                    tags_list.append(body_messages_no_tags)
        else:
            tags_list.append(body_messages_no_tags)
    except ValueError:
        tags_list.append(body_messages_no_tags)

    if body_messages_add_tags_event:
        tags_list.append(body_messages_tag_eventid + settings_eventid)

    if body_messages_add_tags_item:
        for item_id in list(set([x for x in settings_itemid.split()])):
            if re.findall("\d+",item_id):
                tags_list.append(body_messages_tag_itemid + item_id)

    if body_messages_add_tags_trigger:
        tags_list.append(body_messages_tag_triggerid + settings_triggerid)

    if body_messages_add_tags_action:
        tags_list.append(body_messages_tag_actionid + settings_actionid)

    return body_messages_tags_delimiter.join(tags_list)


def create_links_list(_bool=None, url=None, _type=None, url_list=None):
    try:
        if _bool:
            if url and (re.search(r'\w', url)):
                return body_messages_url_template.format(url=url, icon=_type)
            else:
                return body_messages_no_url
        elif url_list:
            return url_list
        else:
            return False
    except ValueError:
        return body_messages_no_url


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
    f.write(json.dumps(cache,sort_keys=True, indent=4))
    f.close()
    if update:
        loggings.info("Updated id for {} ({}): old '{}' -> new '{}' in cache file".format(title, sent_type,update, send_id ))
    else:
        loggings.info("Add new id {} for {} ({}) in cache file".format(send_id,title,sent_type))
    return True


def migrate_group_id(sent_to, sent_id, err):
    for key, value in json.loads(err.result.text).items():
        if key == 'parameters' and value['migrate_to_chat_id']:
            loggings.error("Group chat was upgraded to a supergroup chat ({})".format(value['migrate_to_chat_id']), exc_info=config_exc_info)
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

        for line in bot.get_updates(timeout=5,offset=0):
            if line.message:
                chat = line.message.chat
            elif line.edited_message:
                chat = line.edited_message.chat

            if chat.type in ["group", "supergroup"] and chat.title and chat.title == send_to:
                if not send_id:
                    set_cache(send_to, chat.id, chat.type)
                return chat.id

            if chat.type in ["private"] and chat.username == send_to.replace("@", ""):
                if not send_id:
                    set_cache(send_to, chat.id, chat.type)
                return chat.id

        raise ValueError('Username or groupname not found in the cache file. No access occurred or bot is not added to '
                         'group "{sendto}" (Add bot group and/or send message to {bot})'.format(bot=bot.get_me().username,
                                                                                                sendto=send_to))
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def gen_markup(eventid):
    markup = InlineKeyboardMarkup()
    markup.row_width = zabbix_keyboard_row_width
    markup.add(
        InlineKeyboardButton(zabbix_keyboard_button_message,
                             callback_data='{}'.format(json.dumps(dict(action="messages",eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_acknowledge,
                             callback_data='{}'.format(json.dumps(dict(action="acknowledge",eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="history",eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="last value",eventid=eventid)))),
        InlineKeyboardButton(zabbix_keyboard_button_history,
                             callback_data='{}'.format(json.dumps(dict(action="graphs",eventid=eventid)))))
    return markup


def send_messages(sent_to, message, graphs_png, eventid = None, settings_keyboard = None):
    try:
        sent_id = get_send_id(sent_to)
        if message and sent_to:
            if  graphs_png and type(graphs_png) is list:
                try:
                    print('Send group')
                    graphs_png[0].caption = message
                    graphs_png[0].parse_mode = "HTML"
                    bot.send_media_group(chat_id=sent_id, media=graphs_png)
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
                                   reply_markup=gen_markup(eventid) if zabbix_keyboard and settings_keyboard else None)
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
                    loggings.info('Bot @{busername}({bid}) send photo to "{sent_to}" ({sent_id}).'.format(
                        sent_to=sent_to, sent_id=sent_id, busername=bot.get_me().username, bid=bot.get_me().id))
                    exit(0)
            else:
                try:
                    bot.send_message(chat_id=sent_id, text=message, parse_mode="HTML", disable_web_page_preview=True,
                                     reply_markup=gen_markup(eventid) if zabbix_keyboard and settings_keyboard  else None)
                except apihelper.ApiException as err:
                    if 'migrate_to_chat_id' in json.loads(err.result.text).get('parameters'):
                        migrate_group_id(sent_to, sent_id, err)
                        send_messages(sent_to, message, graphs_png, settings_keyboard)
                    else:
                        loggings.error("Exception occurred in Api Telegram: {}".format(err), exc_info=config_exc_info)
                        exit(1)
                except Exception as err:
                    loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info),exit(1)
                else:
                    loggings.info('Bot @{busername}({bid}) send message to "{sent_to}" ({sent_id}).'.format(
                        sent_to=sent_to, sent_id=sent_id, busername=bot.get_me().username, bid=bot.get_me().id))
                    exit(0)

    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)


def main(args):
    try:
        if args[0] and args[1] and args[2]:
            loggings.info("Send to {} action: {}".format(args[0], args[1]))
            loggings.debug("Send to {}\naction: {}\nxml: {}".format(args[0],args[1],args[2]))
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)

    if args[1] == 'test' or args[2] == 'test':
        send_messages(sent_to=args[0], message='🚨 Test 💛: Service is not running\nHost: testhost [192.168.0.77]\n'
                                               'Last value: Stop (10:00:00 )\nDuration: 0m\n\n#Test, '
                                               '#eid_130144443, #iid_60605, #tid_39303, #aid_22',
                      graphs_png=dict(
                          img=open(
                              file='{0}/zbxTelegram_files/test.png'.format(os.path.dirname(os.path.realpath(__file__))),
                              mode='rb').read()))
        exit(0)

    sent_to = args[0]
    subject = args[1]
    data_zabbix = xml_parsing(args[2])

    # if tags_list
    tags_list = create_tags_list(data_zabbix['tags'],
                                 data_zabbix['eventid'],
                                 data_zabbix['itemid'],
                                 data_zabbix['triggerid'],
                                 data_zabbix['actionid'])


    trigger_url = create_links_list(_bool=data_zabbix.get('settings_triggerlinks_bool'),
                                    url=data_zabbix.get('triggerurl'), _type=body_messages_url_notes)

    host_url = create_links_list(_bool=data_zabbix.get('settings_hostlinks_bool'),
                                 url=zabbix_host_link.format(
                                              zabbix_server=zabbix_api_url,
                                              hostid=data_zabbix.get('hostid')),
                                 _type=body_messages_url_host)
    url_list = []
    for item_id in list(set([x for x in data_zabbix.get('itemid').split()])):
        if re.findall("\d+",item_id):
            url_list.append(create_links_list(_bool=data_zabbix.get('settings_graphlinks_bool'),
                                          url=zabbix_graff_link.format(
                                              zabbix_server=zabbix_api_url,
                                              itemid=item_id,
                                              range_time=data_zabbix['graphs_period']),
                                          _type=body_messages_url_ld_graphs
                                          ))
    url_list.append(trigger_url) if trigger_url else None
    url_list.append(host_url) if host_url else None

    graphs_name = body_messages_title.format(
        title=data_zabbix['title'],
        period_hour=time.strftime(
            "%H", time.gmtime(
                graphs_period_default if not data_zabbix['graphs_period']
                else int(data_zabbix['graphs_period']))).lstrip("0").replace(" 0", " "))

    if data_zabbix.get('settings_graphs_bool'):
        if len(data_zabbix['itemid'].split()) == 1:
            graphs_png = get_chart_png(itemid=data_zabbix['itemid'],
                                   graff_name=graphs_name,
                                   period=data_zabbix['graphs_period'])
        else:
            graphs_png_group = []
            #  get the unique itemid
            for item_id in list(set([x for x in data_zabbix.get('itemid').split()])):
                if re.findall("\d+",item_id):
                    graphs_png_group.append(InputMediaPhoto(get_chart_png(itemid=item_id,
                                               graff_name=graphs_name,
                                               period=data_zabbix['graphs_period']).get('img')))
            graphs_png = graphs_png_group
    else:
        graphs_png = False

    message = body_messages.format(
        subject = html.escape(subject.format_map(FailSafeDict(zabbix_status_emoji_map))),
        messages = '{body}{links}{tags}'.format(
            body=html.escape(data_zabbix['message']),
            links = '\nLinks: {}'.format(' '.join(sorted(url_list))) if body_messages_url and len(url_list) != 0 else '',
            tags = '\n\n{}'.format(tags_list) if body_messages_tags and data_zabbix.get('settings_tag_bool') else ''))

    send_messages(sent_to, message, graphs_png, data_zabbix['eventid'], data_zabbix.get('settings_keyboard_bool'))
    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
