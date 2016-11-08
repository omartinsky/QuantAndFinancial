# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from math import fabs

# f - function with 1 float returning float
# x0 - initial value
# y	- desired value
# maxIter - max iterations
# minError - minimum error abs(f(x)-y)
def newton(f, fArg, x0, y, maxIter, minError):
	def func(f, fArg, x, y):
		return f(x, fArg) - y
	def slope(f, fArg, x, y):
		xp = x * 1.05
		return (func(f, fArg, xp, y)-func(f, fArg, x, y)) / (xp-x)		
	counter = 0
	while 1:
		sl = slope(f, fArg, x0, y)
		x0 = x0 - func(f, fArg, x0, y) / sl
		if (counter > maxIter): break
		if (abs(f(x0, fArg)-y) < minError): break
		counter += 1
	return x0
