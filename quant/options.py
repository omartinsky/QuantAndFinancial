# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

# Binomial Tree Option Valuation
# Cox, Ross, Rubinstein method

from math import exp

class CRR:
	# Definition of enumerators
	call, put, european, american = 100, 101, 102, 103
	
	def __init__(self):
		# inputs
		self.n = 32
		self.side = None
		self.style = None
		self.price = None
		self.strike = None
		self.riskfree = None
		self.divyield = None
		self.tte = None
		self.volat = None
		# outputs
		self.optionvalue = None
		self.delta = None
		self.gamma = None
		self.theta = None
		
	def calculate(self):
		# check inputs
		if (self.side!=CRR.call and self.side!=CRR.put): raise ValueError("'side' - Option side must be either call or put")
		if (self.style!=CRR.american and self.style!=CRR.european): raise ValueError("'style' - Option style must be either american or european")
		if (self.price==None): raise ValueError("'price' - Instrument's price must be defined")
		if (self.strike==None): raise ValueError("'strike' - Option's strike price must be defined")
		if (self.riskfree==None): raise ValueError("'riskfree' - Riskfree rate must be defined")
		if (self.divyield==None): raise ValueError("'divyield' - Dividend yield must be defined")
		if (self.tte==None): raise ValueError("'tte' - Time to expiration (as fraction of year) must be defined")
		if (self.volat==None): raise ValueError("'volat' - Instrument's volatility must be defined")
		
		tdelta = self.tte / self.n				# Time delta per one step
		u = exp(self.volat * tdelta**.5)		# Up movement per step
		d = 1/u									# Down movement per step
		rf = exp(self.riskfree * tdelta) - 1	# Risk-free rate per step
		dy = exp(self.divyield * tdelta) - 1 	# Dividend yield per step
		pu = (1+rf-dy-d) / (u-d)				# Probability of up movement
		pd = 1 - pu								# Probability of down movement
		n = self.n								# number of steps
		
		# Generate terminal nodes of binomial tree
		level = []
		for i in range(0, n+1): # Iterate through nodes from highest to lowest price
			# Instrument's price at the node
			pr = self.price * d**i * u**(n-i) 	
			# Option value at the node (depending on side)
			ov = max(0.0, pr-self.strike) if self.side==CRR.call else max(0.0, self.strike-pr)
			level.append((pr, ov))
			
		levels = [0,0,0]

		# reduce binomial tree
		for i in range(n-1, -1, -1): # [n-1 to 0]
			levelNext = []
			for j in range(0, i+1):	# Iterate through nodes from highest to lowest price
				node_u, node_d = level[j], level[j+1]
				# Instrument's price at the node
				pr = node_d[0] / d
				# Option value at the node (depending on side)
				ov = (node_d[1] * pd + node_u[1] * pu) / (1 + rf)	
				if style==CRR.american: # American options can be exercised anytime
					ov = max(ov, pr-self.strike if side==CRR.call else self.strike-pr)
				levelNext.append((pr, ov))
			level = levelNext
			if j<=2: levels[j]=level # save level 0,1,2 of the tree

		self.optionvalue = levels[0][0][1]
		self.delta = (levels[1][0][1]-levels[1][1][1]) / (levels[1][0][0]-levels[1][1][0])
		delta1 = (levels[2][0][1]-levels[2][1][1]) / (levels[2][0][0]-levels[2][1][0])
		delta2 = (levels[2][1][1]-levels[2][2][1]) / (levels[2][1][0]-levels[2][2][0])
		self.gamma = (delta1-delta2) / (levels[2][0][0] - levels[2][2][0])
		self.theta = (levels[2][1][1]-self.optionvalue) / (2*tdelta)		