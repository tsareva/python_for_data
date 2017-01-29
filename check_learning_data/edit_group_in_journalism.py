#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs, csv

with codecs.open("no replace journalism.csv", "r+", "utf-8-sig") as file:
	russian_group_list = csv.reader(file, delimiter = ";")
	with codecs.open("journalism.csv", "wb",  "utf-8-sig") as outfile:
		writer = csv.writer(outfile, delimiter = ";", quotechar='"', quoting=csv.QUOTE_ALL)
		for row in russian_group_list:
			if row[5] == "Международная журналистика":
				row[4] = row[4].replace("группа", "(международная журналистика)")
			elif row[5] == "Журналистика":
				row[4] = row[4].replace("группа", "(журналистика)")
			elif row[5] == "Реклама и связи с общественностью":
				row[4] = row[4].replace("группа", "(прикладные коммуникации)")
			writer.writerow(row)