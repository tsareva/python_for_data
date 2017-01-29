#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

column_rage = [6, 7, 8, 9, 12] #column range of keywords for creating keyword dictionary and preparing file for analysis

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
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved in ", filename
	result_file.close()
	
def create_list_of_unique_items(data, column_number):
	list_of_unique_items = [u"Города из исходного файла"]
	print "Creating list from column numbered", column_number + 1
	for row in data:
		item = row[column_number]
		if (item in list_of_unique_items or
				item is None or item == ""):
			continue
		else:
			list_of_unique_items.append(item)
	return list_of_unique_items

def recode_city_for_tableau(fieldnames, data):
	(names, city_data) = read_csv_file("city_for_tableau.csv")
	city_dictionary = dict()
	country_dictionary = dict()
	for city in city_data:
		city_dictionary[city[0]] = city[1]
	for country in city_data:
		country_dictionary[country[0]] = country[2]
	for row in data:
		city = "UNKNOWN"
		country = "UNKNOWN"
		for rus_city, tableau_city in city_dictionary.iteritems():
			if row[4] == rus_city:
				city = tableau_city
		row.append(city)
		for city, country_name in country_dictionary.iteritems():
			if row[4] == city:
				country = country_name
		row.append(country)
	fieldnames.extend(["Cities for Tableau", "Country"])
	print "Data about cities and countries are recoded for Tableau format"
	return fieldnames, data

def create_keywords_list(data):
	keywords_list = []
	for row in data:
		for number in column_rage:
			item = row[number].strip()
			if (item in keywords_list or
					item is None or item == ""
					or item == "0"):
				continue
			else:
				keywords_list.append(item)
	print "Keyworld list was created based on columns #", column_rage
	keywords_list = sorted(keywords_list)
	return keywords_list

def create_wordcloud(data, filename):	
	with codecs.open(filename, "w+", "utf-8-sig") as file:
		file.write('\n'.join(keywords_list))
			
def create_keywords_columns(fieldnames, data, keywords_list):
	n_of_newcolumns = len(keywords_list)
	print "Found %s keywords" % n_of_newcolumns
	n_of_columns_to_add = n_of_newcolumns
	while n_of_columns_to_add > 0:
		for row in data:
			row.append("")
		n_of_columns_to_add = n_of_columns_to_add - 1
	for item in keywords_list:
		fieldnames.append(item)
	n_of_allcolumns = len(fieldnames)
	print "There are %s fieldnames" % n_of_allcolumns
	for row in data: 
		x = n_of_allcolumns - n_of_newcolumns 
		keywords_in_row = []
		for n in column_rage: 
			if (row[n] in keywords_in_row or row[n] ==""):
				continue
			else:
				keyword = row[n].strip()
				keywords_in_row.append(keyword)
		while x < n_of_allcolumns:
			for word in keywords_in_row:
				if word == fieldnames[x]:
					row[x] = "да"
				else:
					row[x] = 0
			x = x + 1		
			
def sum_column(fieldnames, data, keywords_list):
	count_list = []
	for word in keywords_list:
		n = fieldnames.index(word)
		word_count = [fieldnames[n]]
		sum = 0
		for row in data:
			if (row[n] is None or row[n] == 0):
				continue
			else:
				sum += 1
		word_count.append(sum)
		count_list.append(word_count)
	return count_list

def resharp_date(data):
	for row in data:
		row[5] = "01.01." + row[5].replace(unichr(160),"")



fieldnames, data = read_csv_file('law_thesis.csv')
fieldnames, data = recode_city_for_tableau(fieldnames, data)
keywords_list = create_keywords_list(data)
create_keywords_columns(fieldnames, data, keywords_list)

keyworld_cloud = sum_column(fieldnames, data, keywords_list)
cloud_fieldnames = ["Word", "Count"]
write_to_result("word_cloud.csv", keyworld_cloud, cloud_fieldnames)

resharp_date(data)

write_to_result('law_thesis_tableau.csv', data, fieldnames)