#!/usr/bin/envquit() python
# -*- coding: utf-8 -*-
import sys, socket, ssl
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv, sqlite3, urllib, vkontakte, time
from create_token import create_token


token = open("files/token.txt").read()
vk = vkontakte.API(token=token)

def get_friends(user_id):
	
	
