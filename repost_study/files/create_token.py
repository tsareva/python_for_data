#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv
import webbrowser
import urllib, vkontakte, time

def get_server_time():
	token = open("files/token.txt").read()
	vk = vkontakte.API(token=token)
	server_time = vk.getServerTime()
	print "Time now: ", time.ctime(int(server_time))

def find_out_token(url):
	token_start = url.index("token=") + 6
	token_end = url.index("&expires_in")
	token = url[token_start:token_end]
	return token

def create_token():
	url_1 = 'https://oauth.vk.com/authorize?client_id='
	client_id = '5866966' #application id from settings
	url_2 = '&display=page&redirect_uri=https://oauth.vk.com/blank.html&'
	scope = 'scope=stats' 
	url_3 = '&response_type=token&v=5.62&state=123456'
	url = url_1 + client_id + url_2 + scope + url_3
	print "Copy to browser:\n%s\n", url
	webbrowser.open(url)
	access_link = raw_input("Enter access link: ")
	token = find_out_token(access_link)
	with open("files/token.txt", "w") as file:
		file.write(token)
		print "Session token was successfully saved"