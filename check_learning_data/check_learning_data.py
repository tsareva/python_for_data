#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

name = "philosophy"
original_file = name+".csv"
edited_file = "edited_"+name+".csv"
print "Creating ... ", edited_file


delete_list = []
group_list = []
group_dont_exist = []
entries = set()
#change this to use load_csv_from_file(...)
with codecs.open("group_list.csv", "r", "utf-8-sig") as file:
	group_file = csv.reader(file, delimiter=';')
	for row in group_file:
		if row[0] == name:
			list = []
			list.append(row[1])
			list.append(row[2])
			list[1] = list[1].replace(" ", "")
			list.append(row[3])
			group_list.append(list)
	
def delete_st(text):
	text = text.replace(" (","(").replace(") ",")")
	while text.find("(") and text.find(")") is not -1: 
		first_sym = text.find("(")
		second_sym = text.find(")") + 1
		text = text.replace(text[first_sym:second_sym],"")
		text = text.replace(";",",")
	return text

def get_group_from_row (row):
	groups = []
	for item in row[4].split(","):
		if item == "":
			continue
		list = []
		list.append(row[2])
		list.append(row[3])
		list[1] = list[1].replace(" ", "")
		list.append(item.strip())
		groups.append(list)
	return groups	
	
def check_group_list(data):
	for row in data:
		groups = get_group_from_row(row)
		for item in groups:
			if item not in group_list:
				if item not in group_dont_exist:
					group_dont_exist.append(item)
				
def remove_duplicates(data):
	for row in data:
		key = (row[0], row[1],row[2],row[3],row[4])
		if key not in entries:
			entries.add(key)
	return entries

def merge_group_rows(data):
	streams_dict = dict()
	for row in data:
		key = (row[0], row[1],row[2],row[3])
		if key not in streams_dict:
			streams_dict[key] = []
		streams_dict[key].append(row[4])
	result = []
	for key,value in streams_dict.iteritems():
		result.append((key[0], key[1], key[2], key[3], ",".join(value)))
	return result
	
def check_data(data):
	for row in data:
		row[0] = delete_st(row[0])
		row[4] = row[4].replace(";",",").strip()
		for item in delete_list:
			row[4] = row[4].replace(item,"")
	return data

def write_to_result (filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	result_file.close()

def load_csv_from_file(filename):
	with codecs.open(filename, "r", "utf-8-sig") as file:
		print "Getting ... ", filename
		reader = csv.reader(file, delimiter=';')
		fieldnames = next(reader)
		data = []
		for row in reader:
			data.append(row)
	return (fieldnames, data)

		
(fieldnames, data) = load_csv_from_file(original_file)
result = merge_group_rows(remove_duplicates(check_data(data)))
write_to_result(edited_file, result, fieldnames)

check_group_list(result)

write_to_result("group_dont_exist.csv", group_dont_exist, ["Year", "Type", "Group"])