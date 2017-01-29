#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

def create_list_of_unique_items(data, column_number):
	list_of_unique_items = [u"Города из исходного файла"]
	print "Creating list from column numbered", column_number + 1
	for row in data:
		city = row[column_number]
		if (city in list_of_unique_items or
				city is None or city == ""):
			continue
		else:
			list_of_unique_items.append(city)
	return list_of_unique_items
	

city_list = create_list_of_unique_items(data, 4)

with codecs.open('law_cities.txt', "w+", "utf-8-sig") as file:
	file.write('\n'.join(city_list))
	