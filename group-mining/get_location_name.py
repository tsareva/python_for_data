#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

import urllib, vkontakte, pprint
import time

token = open("token.txt").read()
vk = vkontakte.API(token=token)

def read_csv_file(filename):
	with codecs.open(filename, 'r', 'utf-8-sig') as file:
		print "Getting data from... ", filename
		opened_file = csv.reader(file, delimiter=';')
		fieldnames = next(opened_file)
		data = []
		for row in opened_file:
			data.append(row)
	return fieldnames, data
	
def write_to_result(filename, data, fieldnames):
	if len(data) > 0:
		print "Saving results..."
		result_file = codecs.open(filename, "wb", "utf-8-sig")
		writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow(fieldnames)
		for row in data:
			writer.writerow(row)
		print "Results were saved in ", filename
		result_file.close()
	else:
		print "No data to be saved"

def create_list_city_ids(fieldnames, data):
	city_id = fieldnames.index("city")
	list_city_ids = []
	for row in data:
		if row[city_id] not in list_city_ids:
			list_city_ids.append(row[city_id])
		else:
			continue
	return list_city_ids

def create_city_dict(list_city_ids):
	city_dict = dict()
	print len(list_city_ids), " cities were found"
	x = 1
	for city_id in list_city_ids:
		print "Defining city ", x, " of ", len(list_city_ids)
		city = vk.database.getCitiesById(city_ids=city_id)
		city_dict[city_id] = city
		x+=1
		time.sleep(0.2)
	return city_dict

def append_city(fieldnames, data, city_dict):
	city_id = fieldnames.index("city")
	for row in data:
		for id, city in city_dict.iteritems():
			if row[city_id] == id:
				row.append(city)
	fieldnames.append(fieldnames[city_id]+" from database")
	return fieldnames, data

	
fieldnames, data = read_csv_file('users_info_38532412.csv')

city_dict = create_city_dict(create_list_city_ids(fieldnames, data))
fieldnames, data = append_city(fieldnames, data, city_dict)

write_to_result("recode_file.csv", data, fieldnames)
