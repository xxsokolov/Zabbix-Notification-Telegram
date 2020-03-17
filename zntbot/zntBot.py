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
from errno import ENOENT
import telebot
import json
from telebot import apihelper, TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib3
from zntbot.classes.bot_threads import BOThread
from zntbot.classes.api_zabbix import MBZabbix
from zntbot.classes.logger import Log
from zntbot.zntBot_config import *


loggings = Log(config_debug_mode).log
zbx = MBZabbix()
thr = BOThread()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot: TeleBot = telebot.TeleBot(tg_token, threaded=False, num_threads=3)
if tg_proxy:
    apihelper.proxy = tg_proxy_server

arrays_call_data = {}

def set_call_history(chat_id,call_id,message_id,buttons=None,delete=None):
    cache = None
    f = open(config_cache_file, 'r')
    r = f.read()
    f.close()

    f = open(config_cache_file,'w')
    if len(r) > 1:
        cache = json.loads(r)
    if not cache:
        if not delete:
            # cache = {str(chat_id): dict( message_id=str(message_id), call_id=call_id,buttons=buttons)}
            cache = {str(call_id): dict(chat_id=str(chat_id), message_id=str(message_id),buttons=buttons)}
        else:
            del cache[str(call_id)]
    else:
        if not delete:
            cache[str(call_id)] = dict(chat_id=str(chat_id), message_id=str(message_id),buttons=buttons)
        else:
            del cache[str(call_id)]
    # f.seek(0)
    f.write(json.dumps(cache,sort_keys=True, indent=4))
    f.close()
    # if cache:
    #     loggings.info("Updated id for {} ({}): old '{}' -> new '{}' in cache file".format(title, sent_type,update, send_id ))
    # else:
    #     loggings.info("Add new id {} for {} ({}) in cache file".format(send_id,title,sent_type))
    return True


def gen_reverse_dialog_markup(keyboards):
    buttons = []
    markup = InlineKeyboardMarkup()

    for dialog in keyboards:
        buttons.append(InlineKeyboardButton(text=dialog['text'], callback_data=dialog['callback_data']))
    markup.add(*buttons)
    return markup


def gen_dialog_markup(cid,message=None,mid=None):
    buttons = []
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=message,callback_data='{"action": "No action"}'))
    markup.row_width = 2

    for dialog in answer_dialog_keyboard:
        callback_data = '{{"action":"{action}", "cid": "{cid}"}}'.format(action=dialog.get('action'),cid=cid)
        buttons.append(InlineKeyboardButton(text=dialog.get('name'), callback_data=callback_data))
    markup.add(*buttons)
    return markup


def gen_markup(actions,url=None):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(''.join([x.get('name') for x in answer_keyboard if x.get('action') == actions]),
                                    callback_data='{{"action": "{action}"}}'.format(
                                        action=''.join(
                                            [x.get('action') for x in answer_keyboard if x.get('action') == actions])),
                                        url=url))
    return markup


def timeout_dialog(chat_id, message_id):
    bot.clear_step_handler_by_chat_id(chat_id)
    bot.edit_message_reply_markup(chat_id=chat_id,message_id=message_id,
                                  reply_markup=gen_reverse_dialog_markup(keyboards=[dict(text='Timeout',callback_data='{"action": "No action"}')]))


def create_request_data(message,call,waiting_dialog):
    try:
        thr.cancel_timer1()
        bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        bot.edit_message_text(chat_id=waiting_dialog.chat.id,message_id=waiting_dialog.message_id,
                              text='{replay} {message}'.format(replay=waiting_dialog.text, message=message.text.lower(),
                                                               parse_mode='html'))
        bot.edit_message_reply_markup(chat_id=waiting_dialog.chat.id,message_id=waiting_dialog.message_id,
                                      reply_markup=gen_markup(actions='sending'))

        bot.send_message(chat_id=arrays_call_data['call_group_id'],
                         text=bot_message_complete.format(username=message.from_user.username,
                                                          lastname=message.from_user.last_name,
                                                          firstname=message.from_user.first_name,
                                                          action=arrays_call_data['call_data']['action'],
                                                          message=message.text.lower()),
                         reply_to_message_id=arrays_call_data['call_message_id'], disable_notification=True)

    except Exception as err:
        loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)
    else:
        zbx.set_message(eventids=arrays_call_data['call_data_eventid'], message=message.text.capitalize())
        bot.edit_message_reply_markup(chat_id=waiting_dialog.chat.id,message_id=waiting_dialog.message_id,
                                      reply_markup=gen_markup(actions='sent',url='{url}'.format(
                                          url=bot.export_chat_invite_link(call.message.chat.id))))
        loggings.info('{id} Done. Message: "{message}" sending.'.format(id=arrays_call_data['call_id'], message=message.text.lower()))



def change_keyboard_from_history(call_id, timer=None):
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

    if len(read_cache) > 1:
        cache = json.loads(read_cache)

        for _id, values in cache.items():
            if call_id == _id or not call_id:
                chat_id = values['chat_id']
                message_id = values['message_id']
                buttons = values['buttons']

                bot.edit_message_reply_markup(chat_id=chat_id,message_id=message_id,
                                          reply_markup=gen_reverse_dialog_markup(buttons))
                set_call_history(chat_id=chat_id,call_id=call_id,message_id=message_id,buttons=buttons,delete=True)
                loggings.debug("{id} keyboard has been changed to a timeout. ({sleep})".format(id=call_id, sleep=0))


    # threading.enumerate()

@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == "yes")
def callback_query(call):
    try:
        # thr.cancel_timer1()
        # thr.start_timer1(interval=10,function=change_keyboard_from_history,kwargs=dict(call_id=arrays_call_data['call_id'],timer=True))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                  reply_markup = gen_markup(
                                      actions='goto',
                                      url='https://t.me/{}'.format(call.message.from_user.username)))


        # bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,
        #                               reply_markup=gen_reverse_dialog_markup(arrays_call_data['buttons']))

        forward = bot.forward_message(chat_id=call.from_user.id,from_chat_id=call.message.chat.id,
                                      message_id=arrays_call_data.get('call_message_id'),disable_notification=True,)

        waiting_dialog = bot.send_message(chat_id=call.from_user.id, text='Enter a message:', reply_to_message_id=forward.message_id,
                                 reply_markup=gen_markup(actions='cancel'),disable_notification=False)


    except Exception as err:
        loggings.error("Exception occurred: {}".format(err),exc_info=config_exc_info)


    else:
        # set_call_history(chat_id=call.message.chat.id,call_id=call.id,message_id=call.message.message_id,
        #                  buttons=call.message.json['reply_markup']['inline_keyboard'][0])
        bot.register_next_step_handler(waiting_dialog,lambda m: create_request_data(m,call=call,waiting_dialog=waiting_dialog))
        loggings.info('{id} {firstname} {lastname} (@{username}) requested action {action}'.format(
            id=arrays_call_data['call_id'],
            action=json.loads(call.data).get('action').capitalize(),
            username=call.from_user.username,
            lastname=call.from_user.last_name,
            firstname=call.from_user.first_name))

        thr.start_timer1(interval=120,function=timeout_dialog,
                         kwargs=dict(chat_id=waiting_dialog.chat.id, message_id=waiting_dialog.message_id))

        # thr.start_timer1(interval=10,function=change_keyboard_from_history,kwargs=dict(call_id=arrays_call_data['call_id'],timer=True))


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == "no")
def callback_query(call):
    # set_call_history(chat_id=call.message.chat.id,call_id=call.id,message_id=call.message.message_id,
    #                  buttons=call.message.json['reply_markup']['inline_keyboard'][0])
    try:
        thr.cancel_timer1()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                  reply_markup=gen_reverse_dialog_markup(arrays_call_data['buttons']))
    except Exception as err:
        loggings.error("Exception occurred: {}".format(err),exc_info=config_exc_info)

    else:
        set_call_history(chat_id=call.message.chat.id,call_id=arrays_call_data['call_id'],message_id=call.message.message_id,delete=True)
        loggings.info('{id} {firstname} {lastname} (@{username}) requested action {action}'.format(
        id=arrays_call_data['call_id'],
        action=json.loads(call.data).get('action').capitalize(),
        username=call.from_user.username,
        lastname=call.from_user.last_name,
        firstname=call.from_user.first_name))


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == "cancel")
def callback_query(call):
    loggings.info('{id} {firstname} {lastname} (@{username}) requested action {action}'.format(
        id=arrays_call_data['call_id'],
        action=json.loads(call.data).get('action').capitalize(),
        username=call.from_user.username,
        lastname=call.from_user.last_name,
        firstname=call.from_user.first_name))

    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

@bot.message_handler(func=lambda message: True)
def add_answer(message):
    print('xxx')


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print('xxx')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global arrays_call_data
    try:
        json_data_call = json.loads(call.data)
    except Exception as err:
        loggings.error("Exception occurred3: {}".format(err))

    else:
        action = json_data_call.get('action')
        eventid = json_data_call.get('eventid')
        if action == "messages":
            bot.answer_callback_query(call.id, 'Received action "{}"'.format(action),show_alert=False,cache_time=10)

            set_call_history(chat_id=call.message.chat.id,call_id=call.id,message_id=call.message.message_id,buttons=call.message.json['reply_markup']['inline_keyboard'][0])


            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,
                                          reply_markup=gen_dialog_markup(
                                              cid=call.message.chat.id,
                                              message='Hi {firstname} {lastname}!. Have you selected {} action, continue?'.format(
                                                  action.lower(),
                                                  lastname=call.from_user.last_name,
                                                  firstname=call.from_user.first_name)))



            arrays_call_data['buttons'] = call.message.json['reply_markup']['inline_keyboard'][0]
            arrays_call_data['call_id'] = call.id
            arrays_call_data['call_data_eventid'] = eventid
            arrays_call_data['call_data_action'] = action
            arrays_call_data['call_data'] = json_data_call
            arrays_call_data['call_group_id']=call.message.chat.id
            arrays_call_data['call_message_id'] = call.message.message_id
            arrays_call_data['call_action_from_user_id'] = call.from_user.id


            thr.start_timer1(interval=10,function=change_keyboard_from_history,kwargs=dict(call_id=call.id, timer=True))

            loggings.info("{id} {firstname} {lastname} (@{username}) requested action {action}".format(id=call.id,
                username=call.from_user.username, lastname=call.from_user.last_name,firstname=call.from_user.first_name,
                action=action))
        elif action == "Acknowledge":
            bot.answer_callback_query(call.id, "Received: {}".format(call.data))
        elif action == "History":
            bot.answer_callback_query(call.id, "Received: {}".format(call.data))
        elif action == 'No action':
            bot.answer_callback_query(call.id,'No action',show_alert=False,cache_time=5)
        else:
            bot.answer_callback_query(call.id,"Buttons not found!")



if __name__ == '__main__':
    start_completed = time.time()
    # xxx = bot.send_message(59552110, '✅ Я я на связи!')
    loggings.info("Bot is run")

    logger2 = telebot.logger
    telebot.logger.setLevel('DEBUG')
    try:
        bot.get_updates()
    except apihelper.ApiException.__init__ as err:
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    # while True:
    #     try:
    #         # bot.enable_save_reply_handlers(delay=200,filename="./.handler-saves/reply.save")
    #         # bot.enable_save_next_step_handlers(delay=200,filename="./.handler-saves/next.save")
    #         # sending.start()
    #         # bot.polling(none_stop=False, interval=0, timeout=10)
    #         # thr.start_timer1(interval=0,function=change_keyboard_from_history,kwargs=dict(call_id=False,timer=True))
    #         bot.infinity_polling(False)
    #     except apihelper.ApiException as e:
    #         print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    #     except Exception as err:
    #         loggings.error("Exception occurred: {}".format(err), exc_info=config_exc_info), exit(1)
    #         # bot.send_message(59552110, '❗ Неееет! Я хочу жить!')
    #         time.sleep(15)

    # send_screens_prob/lem2('rrrrrr')
