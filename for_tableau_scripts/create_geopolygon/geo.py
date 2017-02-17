#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib, codecs, json, csv

with codecs.open("districts.txt","r","utf-8-sig") as file:
	districts = filter(None, file.read().splitlines())

openstreetmap_search_link =	"http://nominatim.openstreetmap.org/search?format=json&q="
enable_geojson = "&exclude_place_ids=158190293&polygon_geojson=1"

def get_district_coordinates(district):
	print "Download data for " + district
	link = openstreetmap_search_link + district.encode("utf-8")+ enable_geojson
	url = urllib.urlopen(link) 
	geodata = json.load(url)
	if is_polygon(geodata) is False:
		if is_MultiPolygon(geodata) is False:
			print "Check data type for ", district
			exit()
		else:
			district_coords = geodata[0]["geojson"]["coordinates"][0][0]
	else:
		district_coords = geodata[0]["geojson"]["coordinates"][0]
	return district_coords

def is_polygon(geodata):
	if geodata[0]["geojson"]["type"] != "Polygon":
		return False
	else:
		return True

def is_MultiPolygon(geodata):
	if geodata[0]["geojson"]["type"] != "MultiPolygon":
		return False
	else:
		return True
		
def is_administrative_boundary(geodata):
	if (geodata[0]["type"] != "administrative"
			and geodata[0]["class"] != "boundary"):
		return False
	else:
		return True	
	
		
def get_district_name(district):
	if district.find(" ") is not -1:
		i = district.index(" ")
		district_name = district[0:i]
	else:
		district_name = district
	return district_name

def save_district_coordinates(district):
	district_name = get_district_name(district)
	district_coords = get_district_coordinates(district)
	coord_set = []
	path = 1
	for item in district_coords:
		row = []
		row.append(district_name)
		longitude = item[0]
		row.append(longitude)
		latitude = item[1]
		row.append(latitude)
		row.append(path)
		path += 1
		coord_set.append(row)
	return coord_set

def write_to_result(filename, data, fieldnames):
	result_file = codecs.open(filename, "wb", "utf-8-sig")
	writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(fieldnames)
	for row in data:
		writer.writerow(row)
	print "Results were saved in ", filename
	result_file.close()

def create_data(districts):
	data =[]
	for district in districts:
		coord_set = save_district_coordinates(district)
		for row in coord_set:
			data.append(row)
	return data

data = create_data(districts)
			
fieldnames = ["District", "Longitude", "Latitude", "Path"]
write_to_result('karelia_districts.csv', data, fieldnames)	