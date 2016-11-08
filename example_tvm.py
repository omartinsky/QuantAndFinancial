# Copyright (c) 2012 Quantitative & Financial, All rights reserved
# www.quantandfinancial.com

from quant.tvm import TVM

pmt = TVM(n=25*12, r=.04/12, pv=500000, fv=0).calc_pmt()
print("Payment = %f" % pmt)

i = TVM(n=10*2, pmt=6/2, pv=-80, fv=100).calc_r()
print("r = %f" % i)
