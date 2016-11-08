# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from datasources.bondscape import readfromfile
from quant.tvm import TVM
from datetime import datetime
import scipy.interpolate
from math import floor, ceil
from quant.optimization import newton
import io

#local time
localtime = datetime(2012,9,19)

#load bonds
bonds = readfromfile('data/gilts_2012_09_19.csv')

#calculate yield curve
# Calculated YTMs doesn't necessarily correspond to those quoted in data file (source: Bondscape.net), due to accrued interest
# and a fact that coupon payment are bound to some specific calendar date, not necessarily, one semiannually
tr, yr = [], []
for b in bonds:
	ttm = (b.maturity - localtime).days / 360
	price = (b.bid+b.ask)/2
	ytm = TVM(n=ttm*b.freq, pv=-price, pmt=b.couponRate/b.freq, fv=1).calc_r() * b.freq
	tr.append(ttm)
	yr.append(ytm)

print('Raw yield curve')
for i in range(0, len(tr)):
	print("%.2f\t%.2f%%" % (tr[i], 100*yr[i]))
 
# interpolation
t = list(i for i in range(1,41))
y = []
interp = scipy.interpolate.interp1d(tr, yr, bounds_error=False, fill_value=scipy.nan)
for i in t:
	value = float(interp(i))
	if not scipy.isnan(value):
		y.append(value)

print('Interpolated yield curve')
for i in range(0, len(t)):
	print("%.2f\t%.2f%%" % (t[i], 100*y[i]))

# bootstrapping
s = [] # output array for spot rates
for i in range(0, len(t)): #calculate i-th spot rate 
	sum = 0
	for j in range(0, i): #by iterating through 0..i
		sum += y[i] / (1 + s[j])**t[j]
	value = ((1+y[i]) / (1-sum))**(1/t[i]) - 1
	s.append(value)
  
print('Spot rates')
for i in range(0, len(t)):
	print("%.2f\t%.2f%%" % (t[i], 100*s[i]))

# reverse check
#for i in range(0, len(t)):
#	sum = 0
#	ytm = y[i]
#	for j in range(0, i):
#		sum += ytm / (1+s[j])**t[j]
#	sum += (1+ytm) / (1+s[i])**t[i]
#	if (sum < 1-1e-5 or sum > 1+1e+5): raise Exception('Reverse-check for bootstrapping failed, sum=%f' % sum)
 
from pylab import *

#subplot(311)
#plot(tr, array(yr)*100, marker='^'), title('Original Yield Curve'), xlabel('Time to maturity'), ylabel('Yield to maturity'), grid(True)
#subplot(312)
#plot(t, array(y)*100, marker='^'), title('Interpolated Yield Curve'), xlabel('Time to maturity'), ylabel('Yield to maturity'), grid(True)
#subplot(313)
#plot(t, array(s)*100, marker='^'), title('Spot Rate Curve'), xlabel('Time'), ylabel('Spot Rate'), grid(True)
#show()   

p1 = plot(tr, array(yr)*100, marker='^'), xlabel('Time to maturity'), grid(True)
p2 = plot(t, array(y)*100, marker='^'), xlabel('Time to maturity'), grid(True)
p3 = plot(t, array(s)*100, marker='o') , xlabel('Time to maturity'), grid(True)
legend([p1[0][0],p2[0][0],p3[0][0]], ['Original Yield Curve', 'Interpolated Yield Curve', 'Spot Rate Curve'], 4)
show()   

