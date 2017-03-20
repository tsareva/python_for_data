#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time, pprint

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)


#vk.board.getTopics(group_id=group_id, count=40, preview_length=0)
#board.getComments(group_id=group_id, topic_id=topic_id,need_likes=1)

#unix_time = wall[2][u'date']

#datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S') #перевод времени в человекопонятный формат


def get_wall_messages(group_id):
	if type(group_id) is int:
		group_id = str(group_id)
	wall = []
	while len(wall) is 0:
		try:
			wall = vk.wall.get(owner_id=("-"+group_id), count=90)
			count = wall[0]
			time.sleep(0.2)
		except (socket.gaierror, socket.timeout, ssl.SSLError):
			print "Can't get info. Trying again..." 
			time.sleep(0.2)
			continue	
	print "There are %s posts at group wall" % count
	offset = 0
	posts = []
	while (count > len(posts)):
		try:
			wall = vk.wall.get(owner_id=("-"+group_id), count=90, offset=offset)
			offset += 90
			posts+=wall[1:]
			print "Getting posts: %s of %s done" % (len(posts), count)
			time.sleep(0.2)
		except (socket.gaierror, socket.timeout, ssl.SSLError):
			print "Can't get info. Trying again..." 
			time.sleep(0.2)
			continue
	return posts

def get_message_info(post):
	print type(post)
	if post.get(u'post_type', None) is None:
		get_original(post)


def get_original(post):
	post_dict = dict()
	post_dict[u'id'] = post.get(u'id', "")
	post_dict[u'from_id'] = post.get(u'from_id', "")
	post_dict[u'signer_id'] = post.get(u'signer_id', "")
	post_dict[u'to_id'] = post.get(u'to_id', "")
	post_dict[u'date'] = post.get(u'date', "")	
	post_dict[u'text'] = post.get(u'text', "").decode('utf-8')
	post_dict[u'reposts_count'] = post[u'reposts'].get(u'count', 0)
	post_dict[u'likes_count'] = post[u'likes'].get(u'count', 0)
	post_dict[u'comments'] = post[u'comments'].get(u'count', 0)
	post_dict[u'marked_as_ads'] = post.get(u'marked_as_ads')
	post_dict[u'is_pinned'] = post.get(u'is_pinned', 0)
	return post_dict

def get_comments(group_id, post_id):
	comments = vk.wall.getComments(owner_id=group_id, post_id=post_id,need_likes=1)
	return comments