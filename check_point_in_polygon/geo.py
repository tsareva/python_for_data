#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib, codecs, json, csv
from shapely.geometry import shape, Point

with codecs.open("districts.txt","r","utf-8-sig") as file:
	districts = filter(None, file.read().splitlines())
openstreetmap_search_link =	"http://nominatim.openstreetmap.org/search?format=json&q="
enable_geojson = "&polygon_geojson=1"
long = []
lat = []

with codecs.open("3.csv","r","utf-8-sig") as csvfile:
	raw_points = csv.reader(csvfile, delimiter=';')
	raw_points.next() #ignore first line as header
	for row in raw_points:
		lat.append(row[0].replace("_","."))
		long.append(row[1].replace("_","."))


		
district_coords = dict()

print "Downloading geodata..."

for district in districts:
	print "Download data for " + district
	link = openstreetmap_search_link + district.encode("utf-8")+ enable_geojson
	url = urllib.urlopen(link) 
	geodata = json.load(url)
	coordinates = geodata[0]["geojson"]
	polygon = shape(coordinates)
	district_coords[district] = polygon
	
def get_district_name(point, district_coords):
	found_district = None
	for district, polygon in district_coords.iteritems():
		if polygon.contains(point):
			if found_district != None:
				manual_process_list.append(point)
				return u"Не найдено"
			found_district = district
			
	if found_district != None:
		return found_district
	manual_process_list.append(point)
	return u"Не найдено"

manual_process_list = []	

district_counts = dict()

for district_name in districts:
	district_counts[district_name] = 0

district_counts[u"Не найдено"] = 0

print "Start processing points"

for lg, lt in zip(long, lat):
	point = Point(float(lg), float(lt)) #format for long/lat as in geojson points
	district_name = get_district_name (point, district_coords)
	district_counts[district_name] += 1

	
for district, count in district_counts.iteritems():
	if count > 0:
		print district + " = " , count

for point in manual_process_list:
	print point