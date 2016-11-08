# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from structures.quote import Quote, QuoteSeries
from datetime import datetime
import urllib.request

def getquotesfromstring(symbol, string):
	linecount = 0
	data = []
	for line in string.split("\\n"):
		linecount += 1
		entries = line.split(",")
		if len(entries) != 6 or linecount==1: continue
		quote = Quote(
			datetime.strptime(entries[0], '%d-%b-%y'),
			float(entries[1]),
			float(entries[2]),
			float(entries[3]),
			float(entries[4]),	
			int(entries[5]))
		data.append(quote)
	reversedIterator = reversed(data)
	return QuoteSeries(symbol, list(reversedIterator))

def getquotesfromweb(symbol):
	url = "http://www.google.com/finance/historical?q=" + symbol + "&output=csv"
	page = str(urllib.request.urlopen(url).read())
	return getquotesfromstring(symbol, page)