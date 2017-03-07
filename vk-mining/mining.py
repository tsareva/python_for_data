#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('files/')
import get_group_info

group_id = '38532412' #vk.com/privivkanet
current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())

connection = sqlite3.connect('vk_vaccination.db')
cur = connection.cursor()

print "Connected to database\n * * * \n"

token = open("token.txt").read()
vk = vkontakte.API(token=token)

raw_input(": ")