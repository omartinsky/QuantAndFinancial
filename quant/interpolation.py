# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

def interpolate(xy, x):
	def find_left(xy, x):
		for xy in reversed(xy):
			if xy[0] <= x: 
				return xy
	def find_right(xy, x):
		for xy in xy:
			if xy[0] >= x: 
				return xy
	if x <= xy[0][0]: # x is lower than xy[0].x
		l, r = xy[0], xy[1]
	elif x >= xy[-1][0]:
		l, r = xy[-2], xy[-1]
	else:
		l,r = find_left(xy, x), find_right(xy,x)
	return (x-l[0])/(r[0]-l[0]) * (r[1]-l[1]) + l[1]