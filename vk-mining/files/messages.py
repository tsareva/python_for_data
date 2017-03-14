#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)


#vk.board.getTopics(group_id=group_id, count=40, preview_length=0)
#board.getComments(group_id=group_id, topic_id=topic_id,need_likes=1)

unix_time = wall[2][u'date']

datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S') #перевод времени в человекопонятный формат


def get_wall_messages(group_id):
	wall = wall.get(owner_id=("-"+group_id), count=90)
	count = wall[0] #число постов на стене всего