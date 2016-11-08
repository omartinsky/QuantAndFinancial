# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

import io
import time
from quant.tvm import TVM

class Bond:
	epic = None
	desc = None
	couponRate = None	# quoted annually
	maturity = None		# payment frequency
	freq = None
	bid = None
	ask = None
	def __str__(self):
		return "epic=%s ttm=%f ytm=%f" % (self.epic, self.ttm(), self.calc_ytm())
	def ttm(self, localtime, daysInYear = 360): # in years
		delta = self.maturity - localtime
		return delta.days / daysInYear
	def mid(self):
		return (self.bid + self.ask) / 2
	def calc_ytm(self):
		tvm = TVM(self.ttm()*self.freq, 0, -self.mid(), self.couponRate/self.freq, 1) #semiannual payment
		try:
			return tvm.calc_r() * self.freq
		except Exception:
			return None
	def calc_duration(self):
		price = (self.bid+self.ask)/2
		tvm = TVM(n=ttm*self.freq, pv=-price, pmt=self.couponRate/self.freq, fv=1)
		ytm = tvm.calc_r() * self.freq
		ytmDelta = .001
		tvm.r = (ytm-ytmDelta)/b.freq
		priceHigh = -tvm.calc_pv()
		tvm.r = (ytm+ytmDelta)/b.freq
		priceLow =  -tvm.calc_pv()
		duration = ((priceHigh-priceLow)*2 / (priceHigh+priceLow)) / (ytmDelta*2)
		return duration