#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import telebot
from telebot import apihelper
import xmltodict
from zbxTelegram_config import *
import requests
import re, sys, os, time
import io
from PIL import Image, ImageDraw, ImageFont
import json


def error_processing(err):
    print(json.dumps(err)), exit(err['num'])


def xml_parsing(data):
    try:
        data = dict(xmltodict.parse(data, process_namespaces=True)['root'])

        message = data['body']['messages']
        settings_tags = data['settings']['tags']
        # settings_graphs = data['settings']['graphs']
        settings_graphs_period = data['settings']['graphs_period']
        settings_itemid = data['settings']['itemid']
        settings_triggerid = data['settings']['triggerid']
        settings_eventid = data['settings']['eventid']
        settings_title = data['settings']['title']
        settings_trigger_url = data['settings']['triggerurl']

        return {'title': settings_title,
                'message': message,
                'tags': settings_tags,
                'graphs_period': settings_graphs_period,
                'itemid': settings_itemid,
                'triggerid': settings_triggerid,
                'triggerurl': settings_trigger_url,
                'eventid': settings_eventid
                }

    except Exception as err:
        error_processing({"num": 1, "class": str(type(err)), "disc": "Error XML format", "msg": str([err])})


def watermark_text(img):
    img = io.BytesIO(img.read())
    img = Image.open(img)
    font = ImageFont.truetype(os.path.dirname(sys.argv[0])+watermark_font, 14)

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
    data_api = {"name": zabbix_api_login, "password": zabbix_api_pass, "enter": "Sign in"}

    req_cookie = requests.post(zabbix_api_url + "/", data=data_api, verify=True)
    cookie = req_cookie.cookies
    response = requests.get(zabbix_graff_chart.format(name=graff_name,
                                                      itemid=itemid,
                                                      zabbix_server=zabbix_api_url,
                                                      range_time= graphs_period_default if not period else period),
                            cookies=cookie,
                            verify=True)

    attachment = io.BytesIO
    response.raw.decode_content = True
    data = attachment(response.content)
    data = watermark_text(data)  # Накладываем ватермарку
    return dict(img=data, url=response.url)  # возвращаем словарь с картинко и урл


def create_tags_list(settings_tags, settings_eventid, settings_itemid, settings_triggerid):
    tags_list = []
    try:
        if settings_tags and (re.search(r'\w', settings_tags)):
            for tags in settings_tags.split(', '):
                if tags:
                    if tags.find(':') != -1:
                        tag, value = tags.split(':')
                        tags_list.append('#{tag}_{value}'.format(tag=re.sub('[^a-zA-Z0-9 \n\.]', '', tag),
                                                                 value=re.sub('[^a-zA-Z0-9 \n\.]', '', value)))
                    else:
                        tags_list.append('#{tag}'.format(tag=re.sub('[^a-zA-Z0-9 \n\.]', '', tags)))
                else:
                    tags_list.append(body_messages_no_tags)
        else:
            tags_list.append(body_messages_no_tags)
    except ValueError:
        tags_list.append(body_messages_no_tags)

    tags_list.append('#eid_' + settings_eventid)
    tags_list.append('#iid_' + settings_itemid)
    tags_list.append('#tid_' + settings_triggerid)

    return tags_list


def create_links_list(settings_triggerurl):
    url_list = []
    try:
        if settings_triggerurl and (re.search(r'\w', settings_triggerurl)):
            url_list.append(body_messages_url.format(settings_triggerurl))
        else:
            url_list.append(body_messages_no_url)
    except ValueError:
        url_list.append(body_messages_no_url)

    return url_list


def send_messages(sent_to, message, graphs_png):
    try:
        bot = telebot.TeleBot(tg_token)
        apihelper.proxy = tg_proxy

        if not graphs_png:
            bot.send_message(chat_id=tg_groupid,text=message)

        if message and graphs_png and graphs_png:
            bot.send_photo(sent_to, graphs_png.get('img'), caption=message, parse_mode="HTML")
        exit(0)

    except Exception as err:
        error_processing({"num": 1, "class": str(type(err)), "disc": "Error send messages", "msg": str([err])})


def main(args):
    try:
        if args[0] and args[1] and args[2]:
            print(args)
    except Exception as err:
        error_processing({"num": 1, "class": str(type(err)), "disc": "Error! Arguments is empty!", "msg": str([err])})

    sent_to = args[0]
    subject = args[1]
    data_zabbix = xml_parsing(args[2])

    tags_list = create_tags_list(data_zabbix['tags'],
                                 data_zabbix['eventid'],
                                 data_zabbix['itemid'],
                                 data_zabbix['triggerid'])

    url_list = create_links_list(data_zabbix['triggerurl'])

    graphs_name = body_messages_title.format(
        title=data_zabbix['title'],
        period_hour=time.strftime("%H", time.gmtime(graphs_period_default if not data_zabbix['graphs_period'] else int(data_zabbix['graphs_period']))).lstrip("0").replace(" 0", " "))

    graphs_png = get_chart_png(itemid=data_zabbix['itemid'],
                        graff_name=graphs_name,
                        period=data_zabbix['graphs_period'])

    message = body_messages.format(
        subject = subject.format_map(zabbix_status_emoji_map),
        messages = data_zabbix['message'],
        links = ' '.join(url_list),
        tags = ', '.join(tags_list))


    send_messages(sent_to, message, graphs_png)

    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
