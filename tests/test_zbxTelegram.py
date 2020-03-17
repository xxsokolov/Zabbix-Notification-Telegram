# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
import sys

sys.path.append('../')

import time
import pytest
import os

should_skip = 'TOKEN' and 'CHAT_ID' not in os.environ.values()

if not should_skip:
    TOKEN = os.environ.get('TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    GROUP_ID = os.environ.get('GROUP_ID')


@pytest.mark.skipif(should_skip, reason="No environment variables configured")
class zbxTelegram:
    def test_message_listener(self):
        msg_list = []
        for x in range(100):
            msg_list.append(self.create_text_message('Message ' + str(x)))
