#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

import urllib, vkontakte

def find_out_token(url):
	token_start = url.index("token=") + 6
	token_end = url.index("&expires_in")
	token = url[token_start:token_end]
	return token
	
def create_fieldnames(dictionary):
	dict = user_info[0]
	fieldnames = []
	for key, value in dict.iteritems():
		fieldnames.append(key)
	return fieldnames
	
def write_to_result(filename, data, fieldnames):
	print "Saving results..."
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved in ", filename
	result_file.close()
	
url_1 = 'https://oauth.vk.com/authorize?client_id='
client_id = '5866966' #application id from settings
url_2 = '&display=page&redirect_uri=https://oauth.vk.com/blank.html&'
scope = 'scope=stats' 
url_3 = '&response_type=token&v=5.62&state=123456'
url = url_1 + client_id + url_2 + scope + url_3
print "Copy to browser:\n%s\n", url

access_link = raw_input("Enter access link: ")
token = find_out_token(access_link)
vk = vkontakte.API(token=token)

profiles = vk.groups.getMembers(group_id='122564943', count = 2)

#get all user ids for group
user_ids = ''
group_list = []
for user in profiles[u'users']:
	user_ids += (str(user) + ", ")
	groups = vk.users.getSubscriptions(user_id=user, extended=1)
	group_list.append(groups)

user_info = vk.users.get(user_ids=user_ids, fields="home_town")

fieldnames = create_fieldnames(user_info)
data = []

for item in user_info:
	row = []
	for key, value in item.iteritems():
		row.append(value)
	data.append(row)

print group_list
	
#write_to_result('results.csv', data, fieldnames)	