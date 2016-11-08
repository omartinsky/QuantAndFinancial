# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from datetime import datetime
import urllib.request
import io
import zipfile
import sys
from xml.dom import minidom

def get_indicator(indicator):
	print("Downloading %s" % indicator)
	url = "http://api.worldbank.org/datafiles/%s_Indicator_MetaData_en_xml.zip" % indicator
	print("Unzipping %s" % indicator)
	zipdata = io.BytesIO(urllib.request.urlopen(url).read())
	archive = zipfile.ZipFile(zipdata)
	xmldata = io.BytesIO(archive.open("%s_Indicator_en.xml" % indicator).read())
	print("Parsing %s" % indicator)
	doc = minidom.parse(xmldata)
	print("Populating %s" % indicator)
	unpivoted = []
	for d in doc.getElementsByTagName('data'):
		records = d.getElementsByTagName('record')
		for r in records:
			fields = r.getElementsByTagName('field')
			countryKey = fields[0].attributes['key'].value
			countryName = fields[0].firstChild.nodeValue
			indicatorKey = fields[1].attributes['key'].value
			indicatorName = fields[1].firstChild.nodeValue
			year = fields[2].firstChild.nodeValue
			value = fields[3].firstChild
			if value!=None: 
				value = value.nodeValue
				countryName = countryName.replace(',', ' ')
				indicatorName = indicatorName.replace(',', ' ')
				unpivoted.append((countryKey, countryName, indicatorKey, indicatorName, year, value))
	return unpivoted
	
def get_indicators(indicators):
	unpivoted = []
	for indicator in indicators:
		u = get_indicator(indicator)
		unpivoted.extend(u)
	return unpivoted