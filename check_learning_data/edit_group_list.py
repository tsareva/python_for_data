#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

with codecs.open("group_list_russian.csv", "r", "utf-8-sig") as file:
	russian_group_list = csv.reader(file, delimiter = ";")
	with codecs.open("group_list.csv", "wb", "utf-8-sig") as file:
		writer = csv.writer(file, delimiter = ";", quotechar='"', quoting=csv.QUOTE_ALL)
		for row in russian_group_list:
			row[0] = row[0].replace("биологии", "biology")
			row[0] = row[0].replace("востоковедения", "easternstudies")
			row[0] = row[0].replace("журналистики","journalism")
			row[0] = row[0].replace("земли","earth")
			row[0] = row[0].replace("искусств","arts")
			row[0] = row[0].replace("истории","history")
			row[0] = row[0].replace("математики","mathematics")
			row[0] = row[0].replace("мед","medicine")
			row[0] = row[0].replace("международные отношения","ir")
			row[0] = row[0].replace("менеджмента","management")
			row[0] = row[0].replace("пмпу","pmpu")
			row[0] = row[0].replace("политологии","political")
			row[0] = row[0].replace("психологии","psychology")
			row[0] = row[0].replace("социологии","sociology")
			row[0] = row[0].replace("стоматологии","dentistry")
			row[0] = row[0].replace("физики","physics")
			row[0] = row[0].replace("филологии","philology")
			row[0] = row[0].replace("философии","philosophy")
			row[0] = row[0].replace("химии","chemistry")
			row[0] = row[0].replace("экономический","economic")
			row[0] = row[0].replace("юриспруденции","law")
			if row[1] == "1":
				row[1] = row[1].replace("1","2015")
			else:
				if row[1] == "2":
					row[1] = row[1].replace("2","2014")
				else:
					if row[1] == "3":
						row[1] = row[1].replace("3","2013")
					else:
						if row[1] == "4":
							row[1] = row[1].replace("4","2012")
						else:
							if row[1] == "5":
								row[1] = row[1].replace("5","2011")
							else:
								row[1] = row[1].replace("6","2010")
			writer.writerow(row)