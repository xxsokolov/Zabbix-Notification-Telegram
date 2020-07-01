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
import argparse
import textwrap
from argparse import RawTextHelpFormatter


class EmptyIsTrue(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) == 0:
            values = True
        setattr(namespace, self.dest, values)


class ArgParsing:

    def __init__(self):
        self.parser = None
        self.parent_group = None
        self.subparsers = None
        self.file_mode_parser = None
        self.discovery_mode_parser = None

    def create_parser(self):
        self.parser = argparse.ArgumentParser(
            prog='znt',
            description='''Скрипт для для отправки Zabbix нотификаций в Telegram''',
            epilog='''(c) Dmitry Sokolov 2019 @ https://github.com/xxsokolov/''',
            add_help=False, formatter_class=RawTextHelpFormatter)

        # self.parent_group = self.parser.add_argument_group(title='Параметры')
        # self.parent_group.add_argument('--help', '-h', action='help', help='Справка')
        # self.subparsers = self.parser.add_subparsers(
        #     dest='command',
        #     title='Возможные команды',
        #     description='Команды, которые должны быть в качестве первого параметра '
        #                 '%(prog)s')
        #
        # self.file_mode_parser = self.subparsers.add_parser('', help='Запуск в режиме file"',
        #                                                    description='''Запуск в режиме File.
        #                                                    В этом режиме программа анализирует лог файл Nginx.''',
        #                                                    formatter_class=RawTextHelpFormatter)
        # self.file_mode_parser.add_argument('-c','--config',default='./zpn_files/config.py',metavar='PATH',
        #                                    help='Путь до файла конфигурации')

        self.parser.add_argument('username', nargs='?', help='Set username Telegram')
        self.parser.add_argument('subject', nargs='?',help='Set subject')
        self.parser.add_argument('messages', nargs='?',help='Set message')
        self.parser.add_argument('--debug', default=False, action=EmptyIsTrue, help='Debug mode')
        # res = parser.parse_args()

        return self.parser
