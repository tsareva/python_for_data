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

#unix_time = wall[2][u'date']

#datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S') #перевод времени в человекопонятный формат


def get_wall_messages(group_id):
	wall = vk.wall.get(owner_id=("-"+group_id), count=90)
	count = wall[0] #число постов на стене всего
	offset = 90
	posts = []
	posts += wall[1:]
	while (count > len(id_list)):
		try:
			wall = vk.wall.get(owner_id=("-"+group_id), count=90, offset=offset)
			print "Getting posts: %s of %s done" % (len(id_list), count)
			offset += 90
			time.sleep(0.2)
		except:
			time.sleep(0.2)
			continue
	return posts

def get_message_info(post):
	post_dict = dict()
	post_dict[u'id'] = post.get(u'id', "")
	post_dict[u'from_id'] = post.get(u'from_id', "")
	post_dict[u'signer_id'] = post.get(u'signer_id', "")	
	post_dict[u'to_id'] = post.get(u'to_id', "")
	post_dict[u'date'] = post.get(u'date', "")	
	post_dict[u'text'] = post.get(u'text', "")
	post_dict[u'reposts count'] = post[u'reposts'].get(u'count', 0)
	post_dict[u'likes count'] = post[u'likes'].get(u'count', 0)
	post_dict[u'comments'] = post[u'comments'].get(u'count', 0)
	post_dict[u'marked_as_ads'] = post.get(u'marked_as_ads')
	post_dict[u'is_pinned'] = post.get(u'is_pinned')
	return post_dict