#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)


vk.board.getTopics(group_id=group_id, preview_length=0)
board.getComments(group_id=group_id, topic_id=topic_id,need_likes=1)
