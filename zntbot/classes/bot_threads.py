#!/usr/lib/zabbix/alertscripts/venv/bin/python
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import threading


class BOThread:

    def __init__(self):
        self.timer1 = None
        self.timer2 = None


    def init_thread(self,interval, function, kwargs):
        return threading.Timer(interval=interval,function=function,kwargs=kwargs)


    def start_timer1(self,interval, function, kwargs):
        self.timer1 = self.init_thread(interval=interval,function=function,kwargs=kwargs)
        self.timer1.start()
        # print('start thr1')


    def start_timer2(self,interval, function, kwargs):
        self.timer2 = self.init_thread(interval=interval,function=function,kwargs=kwargs)
        self.timer2.start()
        # print('start thr2')


    def cancel_timer1(self):
        self.timer1.cancel()
        # print('cancel thr1')


    def cancel_timer2(self):
        self.timer2.cancel()
        # print('cancel thr2')




# def tests(thr):
#     print (thr+' - Run')
#
#
# if __name__ == "__main__":
#     thr = BOThread()
#     thr.start_thread_1(interval=20,function=tests,kwargs=dict(thr='thread_1'))
#     thr.start_thread_2(interval=3,function=tests,kwargs=dict(thr='thread_2'))
#
#
#     thr.cancel_thread_1()
    # thr.start_thread_2(interval=3,function=tests,kwargs=dict(thr='thread_2'))


    # thr.name1.start()
    # thr.name2.start()

    # thr.name1.cancel()

    # my_thread.cancel()
    # my_thread.
    # name1.start()