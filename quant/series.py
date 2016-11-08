# Copyright (c) 2012 Quantitative & Financial
# www.quantandfinancial.com

import math

def avg(x):
	sum = 0
	for i in x: sum+=i
	return sum/len(x)
	
def beta(x,m):
	return covar(x,m) / var(m)
	
def correl(x1,x2):
	return covar(x1,x2)/math.sqrt(var(x1)*var(x2))
	
def var(x, issample=True):
	return covar(x,x,issample)

def covar(v1, v2, issample=True):
	n = len(v1)
	if len(v1) != len(v2) or n<2:
		return None
	avg1, avg2 = avg(v1), avg(v2)
	sum = 0
	for i in range(0,n):
		sum += (v1[i]-avg1)*(v2[i]-avg2)
	if issample:
		return sum / (n-1)
	else:
		return sum / n
		
def cv(x): # coefficient of variation
	return math.sqrt(var(x)) / avg(x)
	
	