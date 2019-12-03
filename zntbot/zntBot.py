#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import time
import os
import sys
import telebot
import json
from telebot import apihelper, TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from zntbot.zntBot_config import *


class System:

    def __init__(self, debug=False):

        # configuring log
        if debug:
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO

        log_format = logging.Formatter('[%(asctime)s] - PID:%(process)s - %(funcName)s() - %(filename)s:%(lineno)d - %(levelname)s: %(message)s')
        self.log = logging.getLogger()
        self.log.setLevel(self.log_level)

        # writing to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self.log_level)
        stdout_handler.setFormatter(log_format)
        # writing to file
        file_handler = logging.FileHandler(filename=os.path.dirname(sys.argv[0]) + log_file, mode='a')
        # file_handler = logging.handlers.SysLogHandler(address='/dev/log')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(log_format)

        self.log.addHandler(stdout_handler)
        self.log.addHandler(file_handler)


bot: TeleBot = telebot.TeleBot(tg_token, threaded=False, num_threads=3)
apihelper.proxy = tg_proxy
loggings = System(debug=True).log


def make_keyboard(name):
    buttons = []
    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    buttons.append(types.KeyboardButton(name))
    markup.add(*buttons)
    return markup

def gen_markup(actions):
    var = [x['name'] for x in answer_keyboard if x['action'] == actions]


    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(''.join([x.get('name') for x in answer_keyboard if x.get('action') == actions]),
                                    callback_data=''.join([x.get('action') for x in answer_keyboard if x.get('action') == actions])))
    return markup

def email_create_request_data(message,call,call_data,replay_msg):
    bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    call_data['message'] = message.text.lower()
    # bot.send_message(chat_id=message.chat.id, text=str(call_data), disable_notification=True)
    ggg = bot.export_chat_invite_link(call.message.chat.id)
    bot.edit_message_text(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id, text='{} {}.\n<a href="{}">Go back to chat</a>'.format(
        replay_msg.text,
        call_data.get('message'),
        ggg),parse_mode='html')
    bot.edit_message_reply_markup(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id,
                                  reply_markup=gen_markup(actions='sending'))
    time.sleep(3)
    bot.edit_message_reply_markup(chat_id=replay_msg.chat.id,message_id=replay_msg.message_id,reply_markup=gen_markup(actions='sent'))
    # bot.forward_message(chat_id=call.message.chat.id,from_chat_id=message.chat.id,
    # message_id=replay_msg.message_id,disable_notification=True)
    bot.send_message(chat_id=call.message.chat.id,
                     text='User @{username} ({lastname} {firstname}) completed an action "{action}: {message}"'.format(
                         username=message.from_user.username,
                         lastname=message.from_user.last_name,
                         firstname=message.from_user.first_name,
                         action=call_data.get('action'),
                         message=call_data.get('message')),reply_to_message_id=call.message.message_id)

    # bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)



@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_query(call):
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
        if action == "ikb_messages":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid),show_alert=False,cache_time=3)
            forward = bot.forward_message(chat_id=call.from_user.id,from_chat_id=call.message.chat.id,
                                message_id=call.message.message_id,disable_notification=True)
            send = bot.send_message(call.from_user.id,'Enter a message:',reply_to_message_id=forward.message_id,reply_markup=gen_markup(actions='cancel'),disable_notification=False)
            # bot.register_next_step_handler(call.message, email_create_request_data)
            ggg=bot.export_chat_invite_link(call.message.chat.id)
            bot.register_next_step_handler(send,lambda m: email_create_request_data(m,call,json_data_call,
                                                                                            replay_msg=send))
        elif action == "ikb_acknowledge":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid),show_alert=False,cache_time=3)
            send = bot.send_message(call.message.chat.id,'Enter a message to acknowledge (or leave blank):',reply_to_message_id=call.message.message_id)
            bot.register_next_step_handler(call.message,lambda m: email_create_request_data(m,call,json_data_call,
                                                                                            replay_msg=send))
        elif action == "ikb_severity":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_history":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_more":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))






if __name__ == '__main__':

    var = ''.join([x.get('name') for x in answer_keyboard if x.get('action') == 'cancel'])


    start_completed = time.time()
    # xxx = bot.send_message(59552110, '✅ Я я на связи!')
    loggings.info("Bot starting...")

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=300)
        except Exception as err:
            loggings.error(
                "Exception occurred: {}".format(err)), bot.send_message(59552110, text="⚠️ Exception occurred: {}. Time execute: {}".format(err, round(float(time.time() - start_completed), 3))), exit(1)
            # bot.send_message(59552110, '❗ Неееет! Я хочу жить!')
            time.sleep(15)
    # send_screens_prob/lem2('rrrrrr')
