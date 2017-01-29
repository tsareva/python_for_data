#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv, datetime

def load_csv_from_file(filename):
	with codecs.open(filename, "r", "utf-8-sig") as file:
		data = csv.reader(file, delimiter=';')
		print "Getting ... ", filename
		reader = csv.reader(file, delimiter=';')
		fieldnames = next(reader)
		data = []
		for row in reader:
			data.append(row)
	return (fieldnames, data)
	
def write_to_result (filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	result_file.close()
	
def delete_not_existed_members(data):
	print "Deleting banned or deleted users ..."
	cleaned_data = []
	deleted_count = 0
	for user in data:
		if user[4] == "banned":
			deleted_count += 1
		elif user[4] == "deleted":
			deleted_count += 1
		else:
			cleaned_data.append(user)
	print "Deleted ", deleted_count, " users"
	return cleaned_data

def recode_city_for_tableau(data):
	(names, city_data) = load_csv_from_file("city_for_tableau.csv")
	city_dictionary = dict()
	for city in city_data:
		city_dictionary[city[0]] = city[1]
	for row in data:
		city = "UNKNOWN"
		for rus_city, tableau_city in city_dictionary.iteritems():
			if row[6] == rus_city:
				city = tableau_city
		row.append(city)
	return data
	
(fieldnames, data) = load_csv_from_file("group516_members.csv")

data = recode_city_for_tableau(delete_not_existed_members(data))
fieldnames.append("City_Tableau")

for row in data:
	date_str = row[5]
	try:
		date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
	except:
		date = None
	if date != None:
		delta = (datetime.datetime.now() - date)
		row.append(delta.days / 365)
	else:
		row.append("N/A")
	
fieldnames.append("age")

write_to_result("edited_larp.csv", data, fieldnames)