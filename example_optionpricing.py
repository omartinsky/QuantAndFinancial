# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

import datasources.google as google
from structures.quote import QuoteSeries
import numpy
from math import log, exp
from datetime import datetime

# Definition of enumerators
call, put, european, american = 100, 101, 102, 103

#google.getquotesfromweb('IVV').savetofile('data/ivv.csv')

prices = QuoteSeries.loadfromfile('IVV', 'data/ivv_2012_11_05.csv').getprices()
prices = prices[-250:]	# We will use last 250 trading days

# Calculation of daily continuous (logaritmic) returns
returns = []
for i in range(0, len(prices)-1):
	r = log(prices[i] / prices[i-1])
	returns.append(r)

# Calculation of daily and annualized volatility from daily returns
volat_d = numpy.std(returns)	# Daily volatility
volat = volat_d * 250**.5		# Annualized volatility

# Calculation inputs
side = call				# Option side
style = american 		# Option style
price = prices[-1]		# Current instrument price (147.31, as of 2012/11/05)
strike = 140			# Strike price
riskfree = .0007		# Risk-free rate, Yield on 3m US Treasury Yields, as of 2012/11/05
divyield = .0199		# Dividend yield on S&P 500 (IVV), as of 2012/11/05
tte = (datetime(2012,12,22) - datetime(2012,11, 6)).days  	# Time to expiration in days

print('Calculation Inputs')
print('%18s : %0.3f' % ('Price', price))
print('%18s : %0.3f' % ('Strike', strike))
print('%18s : %0.3f' % ('Risk-free', riskfree))
print('%18s : %0.3f' % ('Div Yield', divyield))
print('%18s : %0.3f' % ('TTE Days', tte))
print('%18s : %0.3f' % ('Volatility', volat))
print()

# Pre-processing of inputs and calculation of per-step figures
n = 8							# Depth of binomial tree (levels are numbered from 0 to n)
tdelta = tte / (n * 365)		# Time delta per one step (as fraction of year)
u = exp(volat * tdelta**.5)		# Up movement per step
d = 1/u							# Down movement per step
rf = exp(riskfree * tdelta) - 1	# Risk-free rate per step
dy = exp(divyield * tdelta) - 1 # Dividend yield per step
pu = (1+rf-dy-d) / (u-d)		# Probability of up movement
pd = 1 - pu						# Probability of down movement

print('%18s : %0.8f' % ('Node prob U', pu))
print('%18s : %0.8f' % ('Node prob D', pd))
print('%18s : %0.8f' % ('Node tdelta', tdelta))
print('%18s : %0.8f' % ('Node discount f', rf))
print()

assert(side==call or side==put)
assert(style==american or style==european)

print('Binomial Tree')
# Generate terminal nodes of binomial tree
level = []
print('Tree level %i' % n)
for i in range(0, n+1): # Iterate through nodes from highest to lowest price
	# Instrument's price at the node
	pr = price * d**i * u**(n-i) 	
	# Option value at the node (depending on side)
	ov = max(0.0, pr-strike) if side==call else max(0.0, strike-pr)
	level.append((pr, ov))
	print('Node Price %.3f, Option Value %.3f' %(pr, ov))
	
levels = [None,None,None] # Remember levels 0,1,2 for the greeks

# reduce binomial tree
for i in range(n-1, -1, -1): # [n-1 to 0]
	levelNext = []
	print('Tree level %i' % i)
	for j in range(0, i+1):	# Iterate through nodes from highest to lowest price
		node_u, node_d = level[j], level[j+1]
		# Instrument's price at the node
		pr = node_d[0] / d
		# Option value at the node (depending on side)
		ov = (node_d[1] * pd + node_u[1] * pu) / (1 + rf)	
		if style==american: # American options can be exercised anytime
			ov = max(ov, pr-strike if side==call else strike-pr)
		levelNext.append((pr, ov))
		print('Node Price %.3f, Option Value %.3f' %(pr, ov))
	level = levelNext
	if j<=2: levels[j]=level # save level 0,1,2 of the tree

optionvalue = levels[0][0][1]
delta = (levels[1][0][1]-levels[1][1][1]) / (levels[1][0][0]-levels[1][1][0])
delta1 = (levels[2][0][1]-levels[2][1][1]) / (levels[2][0][0]-levels[2][1][0])
delta2 = (levels[2][1][1]-levels[2][2][1]) / (levels[2][1][0]-levels[2][2][0])
gamma = (delta1-delta2) / (levels[2][0][0] - levels[2][2][0])
theta = (levels[2][1][1]-optionvalue) / (2*tdelta)

print()	
print('Results')
print('Option Value %.03f' % optionvalue)
print('Delta %.03f' % delta)
print('Gamma %.03f' % gamma)
print('Theta %.03f' % theta)