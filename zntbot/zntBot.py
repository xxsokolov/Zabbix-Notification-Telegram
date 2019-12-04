#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import time
import telebot
import json
from telebot import apihelper, TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib3
from zntbot.classes.api_zabbix import MBZabbix
from zntbot.classes.logger import Log
from zntbot.zntBot_config import *


loggings = Log(config_debug_mode).log
zbx = MBZabbix()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot: TeleBot = telebot.TeleBot(tg_token, threaded=False, num_threads=3)
if tg_proxy:
    apihelper.proxy = tg_proxy_server


def gen_markup(_id,actions,url=None):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(''.join([x.get('name') for x in answer_keyboard if x.get('action') == actions]),
                                    callback_data='{{"id": "{id}", "action": "{action}"}}'.format(
                                        id=_id,
                                        action=''.join(
                                            [x.get('action') for x in answer_keyboard if x.get('action') == actions]
                                        )),url=url))
    return markup

def create_request_data(message,call,step1,call_data,replay_msg):
    bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    call_data['message'] = message.text.lower()
    # bot.send_message(chat_id=message.chat.id, text=str(call_data), disable_notification=True)
    bot.edit_message_text(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id,
                          text='{replay} {message}'.format(replay=replay_msg.text, message=call_data.get('message'),
                                                           parse_mode='html'))
    bot.edit_message_reply_markup(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id,
                                  reply_markup=gen_markup(_id=call.id,actions='sending'))
    time.sleep(3)
    bot.edit_message_reply_markup(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id,reply_markup=gen_markup(
        _id=call.id,actions='sent',url='{url}'.format(url=bot.export_chat_invite_link(call.message.chat.id))))

    zbx.set_message(eventids=call_data['eventid'], message=call_data['message'])
    # bot.forward_message(chat_id=call.message.chat.id,from_chat_id=message.chat.id,
    # message_id=replay_msg.message_id,disable_notification=True)
    bot.send_message(chat_id=call.message.chat.id,
                     text=bot_message_complete.format(username=message.from_user.username,
                                                      lastname=message.from_user.last_name,
                                                      firstname=message.from_user.first_name,
                                                      action=call_data.get('action'),
                                                      message=call_data.get('message')),
                     reply_to_message_id=call.message.message_id, disable_notification=True)
    bot.delete_message(chat_id=step1.chat.id,message_id=step1.message_id)
    loggings.info('{id} Done. Message: {message}'.format(id=call.id, message=call_data.get('message')))
    # bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == "cancel")
def callback_query(call):
    loggings.info('{id} action was canceled by user'.format(id=json.loads(call.data).get('id')))
    bot.clear_step_handler(call.message)
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        json_data_call = json.loads(call.data)
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err))
        bot.answer_callback_query(call.id,"Error")
    else:
        action = json_data_call.get('action')
        eventid = json_data_call.get('eventid')
        if action == "Messages":
            loggings.info("{id} {firstname} {lastname} (@{username}) requested action {action}".format(id=call.id,
                username=call.from_user.username, lastname=call.from_user.last_name,firstname=call.from_user.first_name,
                action=action))
            bot.answer_callback_query(call.id, 'Received action "{}"'.format(action),show_alert=False,cache_time=5)
            forward = bot.forward_message(chat_id=call.from_user.id,from_chat_id=call.message.chat.id,
                                message_id=call.message.message_id,disable_notification=True)

            step1 = bot.send_message(chat_id=call.message.chat.id,
                                    text='Bot is waiting for you',
                                    reply_to_message_id=call.message.message_id,
                                    reply_markup=gen_markup(_id=call.id, actions='sent',
                                                            url='https://t.me/{}'.format(call.message.from_user.username)),
                                    disable_notification=False)

            step2 = bot.send_message(call.from_user.id,'Enter a message:',reply_to_message_id=forward.message_id,
                                    reply_markup=gen_markup(_id=call.id, actions='cancel'),disable_notification=False)
            bot.register_next_step_handler(step2,lambda m: create_request_data(m,call,step1,json_data_call,
                                                                              replay_msg=step2))
        elif action == "Acknowledge":
            bot.answer_callback_query(call.id, "Received: {}".format(call.data))
        elif action == "History":
            bot.answer_callback_query(call.id, "Received: {}".format(call.data))


if __name__ == '__main__':
    start_completed = time.time()
    # xxx = bot.send_message(59552110, '✅ Я я на связи!')
    loggings.info("Bot is run")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=300)
        except Exception as err:
            loggings.error("Exception occurred: {}".format(err)), \
            bot.send_message(59552110, text="⚠️ Exception occurred: {}. Time execute: {}".format(
                err, round(float(time.time() - start_completed), 3))), exit(1)
            # bot.send_message(59552110, '❗ Неееет! Я хочу жить!')
            time.sleep(15)

    # send_screens_prob/lem2('rrrrrr')
