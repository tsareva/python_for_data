#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time, pprint
import datetime

token = open("files/token.txt").read()
vk = vkontakte.API(token=token)

def get_wall_messages(group_id):
	if type(group_id) is int:
		group_id = str(group_id)
	wall = []
	while len(wall) is 0:
		try:
			wall = vk.wall.get(owner_id=("-"+group_id), count=150)
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

def get_reposts(id, m_id, offset):
	while True:
		try:
			if type(id) is int:
				id = str(id)
			reposts = vk.wall.getReposts(owner_id=id, post_id=m_id, count=150, offset=offset)
			time.sleep(0.2)
			return reposts
		except (socket.gaierror, socket.timeout, ssl.SSLError):
			print "Can't get info. Trying again..." 
			time.sleep(1)
			continue

def get_n_repost(group_id, mid):
	start_m = vk.wall.get(owner_id=group_id, count=1)
	time.sleep(0.2)
	if start_m[1][u'id'] <> int(mid):
		print "Check post id!"
		print start_m[1][u'id']
		quit()
	n_repost = start_m[1][u'reposts'][u'count']
	return n_repost
			
def get_repost_data(reposts):
	data = []
	for post in reposts[u'items']:
		line = get_post_data(post)
		if int(post[u'from_id']) < 0:
			line.append("group")
		elif int(post[u'from_id']) > 0:
			line.append("user")
		data.append(line)
	return data
	
def get_post_data(post):
	try:
		line = []
		line.append(post[u'date'])
		line.append(datetime.datetime.fromtimestamp(int(post[u'date'])).strftime('%Y-%m-%d %H:%M:%S'))
		line.append(post[u'id'])
		line.append(post[u'from_id'])
		line.append(post[u'copy_owner_id'])
		if post.get(u'likes', None) is not None:
			line.append(post[u'likes'][u'count'])
		else:
			line.append("denied")
		if post.get(u'reposts', None) is not None:
			line.append(post[u'reposts'][u'count'])
		else:
			line.append("denied")
		line.append(post.get(u'copy_text', ""))
		return line
	except KeyError as error:
		"Key error: %s for:" % error
		print "User id ", post[u'from_id']
		print "Post id", post[u'id']
		print post[u'likes'][u'count']