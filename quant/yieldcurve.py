# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

# Given raw yields (yr), raw times to maturity (tr) and desired times to maturity (t),
# this method will calculate and return the interpolated yield curve (t,y)

import scipy.interpolate

def interpolate(tr, yr, t):
	y = []
	interp = scipy.interpolate.interp1d(tr, yr, bounds_error=False, fill_value=scipy.nan)
	for i in t:
		value = float(interp(i))
		if not scipy.isnan(value):
			y.append(value)
	return t, y
	
# This function bootstraps yield curve given as (t, y) and returns the corresponding
# spot rate curve (t, s)
def bootstrapping(t, oy):
	s = [] # output array for spot rates
	for i in range(0, len(t)): #calculate i-th spot rate 
		sum = 0
		for j in range(0, i): #by iterating through 0..i
			sum += y[i] / (1 + s[j])**t[j]
		value = ((1+y[i]) / (1-sum))**(1/t[i]) - 1
		s.append(value)
	return t, s