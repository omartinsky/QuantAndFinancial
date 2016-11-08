# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from datetime import datetime
import io

class QuoteSeries:
	def __init__(self, name = None, data = None):
		self.name = name
		self.data = data if data != None else []
	def __str__(self):
		assert(type(self.data[0].date)==datetime)
		dateFromStr = self.data[0].date.strftime('%Y-%m-%d')
		dateToStr =   self.data[-1].date.strftime('%Y-%m-%d')
		return self.name + " : " + str(len(self.data)) + " quotes [" + dateFromStr + " - " + dateToStr + "], last "+str(self.data[-1].c)
	def getprices(self):
		array = []
		for quote in self.data:
			array.append(quote.c)
		return array
	@staticmethod
	def intersect(qs1, qs2):
		assert(type(qs1)==QuoteSeries and type(qs2)==QuoteSeries)
		set1, set2 = set(), set()
		for q in qs1.data: set1.add(q.date)
		for q in qs2.data: set2.add(q.date)
		set0 = set1 & set2
		qs1out, qs2out = QuoteSeries(qs1.name), QuoteSeries(qs2.name)
		for q in qs1.data:
			if q.date in set0:
				qs1out.data.append(q)
		for q in qs2.data:
			if q.date in set0:
				qs2out.data.append(q)
		if __debug__:
			assert(len(qs1out.data)==len(qs2out.data))
			for i in range(0, len(qs1out.data)):
				assert(qs1out.data[i].date==qs2out.data[i].date)
		return qs1out, qs2out
	@staticmethod
	def loadfromfile(name, filename):
		linecount = 0
		f = io.open(filename, 'r')
		qs = QuoteSeries()
		qs.name = name
		for line in f.read().splitlines():
			linecount += 1
			entries = line.split(",")
			if len(entries) != 6 or linecount==1: continue
			date = datetime.strptime(entries[0], '%y-%m-%d') if len(entries[0])==10 else datetime.strptime(entries[0], '%Y-%m-%d %H:%M:%S')
			quote = Quote(
				date,
				float(entries[1]),
				float(entries[2]),
				float(entries[3]),
				float(entries[4]),	
				int(entries[5]))
			qs.data.append(quote)
		f.close()
		return qs
	def savetofile(self,filename):
		f = io.open(filename, "w")
		f.write('date, open, high, low, close, volume\n')
		for q in self.data:
			f.write(str(q.date)+","+str(q.o)+","+str(q.h)+","+str(q.l)+","+str(q.c)+","+str(q.v)+"\n")
		f.close()
			
class Quote:
	def __init__(self, date, o, h, l, c, v):
		self.date = date
		self.o = o
		self.h = h
		self.l = l
		self.c = c
		self.v = v
	def __str__(self):
		return "%s c=%f" % (str(self.date), self.c)