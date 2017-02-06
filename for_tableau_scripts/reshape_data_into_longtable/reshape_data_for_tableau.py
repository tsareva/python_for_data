#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs, csv

data_file = 'labeled_data.csv'
status = 4 # number for column with interview status
passport_range = [0, 21, 22, 23, 29, 62, 68] 
# numbers for columns with passport information
# id, district, sex, age, education, faith, how long live in SPb	


print "This script reshape data set from CATI to Tableau format."

def read_csv_file(filename):
	with codecs.open(filename, 'r', 'utf-8-sig') as file:
		print "Getting data from... ", filename
		opened_file = csv.reader(file, delimiter=';')
#		fieldnames = next(opened_file) for tableau shaping script fieldnames creared separately
		data = []
		for row in opened_file:
			data.append(row)
	return data

def write_to_result(filename, data, fieldnames):
	print "Saving results..."
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved in ", filename
	result_file.close()
	
def create_fieldnames(filename):
	with codecs.open(filename, 'r', 'utf-8-sig') as file:
		print "Getting Tableau-style fieldnames from... ", filename
		fieldnames = []
		for item in file:
			fieldnames.append(item.strip())
	return fieldnames

def create_q_dictionary(filename):
	quiestions = read_csv_file(filename)
	questionaire = dict()
	for row in quiestions:
		questionaire[row[0]] = row[1]
	return questionaire

def find_n_of_multq_columns(data):
	list_of_col = []
	for item in data[0]:
		if item.find("M") is not -1:
			i = item.index("_")
			n = int(item[1:i])
			if n not in list_of_col:
				list_of_col.append(n)
	return list_of_col

def define_range_of_multi_columns(list_of_col):
	range_of_multvar_q = []
	for n in list_of_col:
		a_name = "M"+str(n)
		c_name = "S"+str(n)
		mult_set = []
		for item in data[0]:
			if (item.find(a_name) is not -1
					and item.find("Op") is -1):
				col_n = data[0].index(item)
				mult_set.append(col_n)
		range_of_multvar_q.append(c_name)
		range_of_multvar_q.append(mult_set)
	return range_of_multvar_q 
	#range_of_multvar_q[n][0] = id of question in questionaire
	#range_of_multvar_q[n][1] = list of columns in data set with answers to multi-question

def define_range_of_single_columns(data):
	range_of_onevar_q = []
	for item in data[0]:
		if (item.find("S") is not -1 and 
				(item.find("Op") and item.find("Sample")) 
				is -1 and len(item) < 5 and (item == "S1") is False):
			col_n = data[0].index(item)
			if (col_n not in passport_range
					and col_n not in range_of_multvar_q[1]):
				range_of_onevar_q.append(col_n)
	return range_of_onevar_q

def reshape_data(data):
	data_without_header = data[1:]
	data_for_tableau = []
	for i in range_of_onevar_q:
		for row in data_without_header:
			if int(row[status]) < 0: #check if interview was finished
				continue
			else:
				new_row = []
				for n in passport_range:
					new_row.append(row[n])
				new_row.append(questionaire[data[0][i]])
				new_row.append(row[i])
				for TextAnswer, NumericAnswer in coding_dict.iteritems():
					if row[i].find(TextAnswer) is -1:
						continue
					else:
						new_row.append(NumericAnswer)
				data_for_tableau.append(new_row)
	print "Data were reshaped for Tableau presentation"
	return data_for_tableau
		

fieldnames = create_fieldnames('fieldnames.txt')
data = read_csv_file(data_file)
questionaire = create_q_dictionary('quiestions.csv')

print "For adding numeric answers:"
coding_dict = create_q_dictionary('code_for_numerics.csv')

range_of_multvar_q = define_range_of_multi_columns(find_n_of_multq_columns(data))
range_of_onevar_q = define_range_of_single_columns(data)

data_for_tableau = reshape_data(data)
		
write_to_result('data_for_tableau.csv', data_for_tableau, fieldnames)
#нет функции для добавления мультивопросов