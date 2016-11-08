# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from structures.bond import Bond
import io
from datetime import datetime
import quant
	
def readfromfile(filename):
	f = io.open(filename, 'r')
	data = f.read()
	bonds = []
	i = 0
	for line in data.split('\n'):
		i += 1
		if (i==1): continue
		entries = line.split(',')
		if (len(entries) != 9): continue
		b = Bond()
		b.freq = 2
		b.epic = entries[0]
		b.desc = entries[1]
		b.couponRate = float(entries[2]) / 100.0
		b.maturity = datetime.strptime(entries[3], '%d-%b-%y')
		b.bid = float(entries[4]) / 100
		b.ask = float(entries[5]) / 100
		bonds.append(b)
	f.close()
	return bonds
	
