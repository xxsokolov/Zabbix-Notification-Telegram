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
import logging
from zbxTelegramBot_config import *


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
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_acknowledge":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_severity":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_history":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))
        elif action == "ikb_more":
            bot.answer_callback_query(call.id, "Received eventid {}".format(eventid))


if __name__ == '__main__':
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
