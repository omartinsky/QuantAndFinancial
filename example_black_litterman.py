from numpy import matrix, array, zeros, empty, sqrt, ones, dot, append, mean, cov, transpose, linspace
from numpy.linalg import inv, pinv
from pylab import *
from structures.quote import QuoteSeries
import scipy.optimize
import random

####################################
# Helper Functions
####################################

def load_data_net():
	symbols = ['XOM', 'AAPL', 'MSFT', 'JNJ', 'GE', 'GOOG', 'CVX', 'PG', 'WFC']
	cap = {'^GSPC':14.90e12, 'XOM':403.02e9, 'AAPL':392.90e9, 'MSFT':283.60e9, 'JNJ':243.17e9, 'GE':236.79e9, 'GOOG':292.72e9, 'CVX':231.03e9, 'PG':214.99e9, 'WFC':218.79e9}
	n = len(symbols)
	from datasources import yahoo
	prices_out, caps_out = [], []	
	for s in symbols:
		print("Reading symbol %s" % s)
		q = yahoo.getquotesfromweb(s)
		prices = q.getprices()[-500:]		
		prices_out.append(prices)
		caps_out.append(cap[s])
	return symbols, prices_out, caps_out
	
# Function loads historical stock prices of nine major S&P companies and returns them together
# with their market capitalizations, as of 2013-07-01
def load_data():
	symbols = ['XOM', 'AAPL', 'MSFT', 'JNJ', 'GE', 'GOOG', 'CVX', 'PG', 'WFC']
	cap = {'^GSPC':14.90e12, 'XOM':403.02e9, 'AAPL':392.90e9, 'MSFT':283.60e9, 'JNJ':243.17e9, 'GE':236.79e9, 'GOOG':292.72e9, 'CVX':231.03e9, 'PG':214.99e9, 'WFC':218.79e9}
	n = len(symbols)
	prices_out, caps_out = [], []	
	for s in symbols:
		print("Reading symbol %s" % s)
		q = QuoteSeries.loadfromfile(s, 'data/black_litterman/%s.csv' % s)
		prices = q.getprices()[-500:]		
		prices_out.append(prices)
		caps_out.append(cap[s])
	return symbols, prices_out, caps_out
	
# Function takes historical stock prices together with market capitalizations and calculates
# names       - array of assets' names
# prices      - array of historical (daily) prices
# caps	      - array of assets' market capitalizations
# returns:
# names       - array of assets' names
# weights     - array of assets' weights (derived from mkt caps)
# expreturns  - expected returns based on historical data
# covars	  - covariance matrix between assets based on historical data
def assets_meanvar(names, prices, caps):
	prices = matrix(prices)				# create numpy matrix from prices
	weights = array(caps) / sum(caps)	# create weights
	
	# create matrix of historical returns
	rows, cols = prices.shape
	returns = empty([rows, cols-1])
	for r in range(rows):
		for c in range(cols-1):
			p0, p1 = prices[r,c], prices[r,c+1]
			returns[r,c] = (p1/p0)-1
			
	# calculate expected returns
	expreturns = array([])
	for r in range(rows):
		expreturns = append(expreturns, mean(returns[r]))
	# calculate covariances
	covars = cov(returns)				
	
	expreturns = (1+expreturns)**250-1	# Annualize expected returns
	covars = covars * 250				# Annualize covariances

	return names, weights, expreturns, covars
	
# 	rf		risk free rate
#	lmb		lambda - risk aversion coefficient
#	C 		assets covariance matrix
# 	V		assets variances (diagonal in covariance matrix)
#	W 		assets weights
#	R		assets returns
#	mean	portfolio historical return
#	var		portfolio historical variance
#	Pi		portfolio equilibrium excess returns
# 	tau 	scaling factor for Black-litterman
	
# Calculates portfolio mean return
def port_mean(W, R):
	return sum(R*W)

# Calculates portfolio variance of returns
def port_var(W, C):
	return dot(dot(W, C), W)
	
# Combination of the two functions above - mean and variance of returns calculation
def port_mean_var(W, R, C):
	return port_mean(W, R), port_var(W, C)
	
# Given risk-free rate, assets returns and covariances, this function calculates
# mean-variance frontier and returns its [x,y] points in two arrays
def solve_frontier(R, C, rf):
	def fitness(W, R, C, r):
		# For given level of return r, find weights which minimizes
		# portfolio variance.
		mean, var = port_mean_var(W, R, C)
		# Big penalty for not meeting stated portfolio return effectively serves as optimization constraint
		penalty = 50*abs(mean-r)
		return var + penalty
	frontier_mean, frontier_var, frontier_weights = [], [], []
	n = len(R)	# Number of assets in the portfolio
	for r in linspace(min(R), max(R), num=20): # Iterate through the range of returns on Y axis
		W = ones([n])/n		# start optimization with equal weights
		b_ = [(0,1) for i in range(n)]
		c_ = ({'type':'eq', 'fun': lambda W: sum(W)-1. })
		optimized = scipy.optimize.minimize(fitness, W, (R, C, r), method='SLSQP', constraints=c_, bounds=b_)	
		if not optimized.success: 
			raise BaseException(optimized.message)
		# add point to the min-var frontier [x,y] = [optimized.x, r]
		frontier_mean.append(r)							# return
		frontier_var.append(port_var(optimized.x, C))	# min-variance based on optimized weights
		frontier_weights.append(optimized.x)
	return array(frontier_mean), array(frontier_var), frontier_weights
	
# Given risk-free rate, assets returns and covariances, this 
# function calculates weights of tangency portfolio with respect to 
# sharpe ratio maximization
def solve_weights(R, C, rf):
	def fitness(W, R, C, rf):
		mean, var = port_mean_var(W, R, C)	# calculate mean/variance of the portfolio
		util = (mean - rf) / sqrt(var)		# utility = Sharpe ratio
		return 1/util						# maximize the utility, minimize its inverse value
	n = len(R)
	W = ones([n])/n						# start optimization with equal weights
	b_ = [(0.,1.) for i in range(n)]	# weights for boundaries between 0%..100%. No leverage, no shorting
	c_ = ({'type':'eq', 'fun': lambda W: sum(W)-1. })	# Sum of weights must be 100%
	optimized = scipy.optimize.minimize(fitness, W, (R, C, rf), method='SLSQP', constraints=c_, bounds=b_)	
	if not optimized.success: 
		raise BaseException(optimized.message)
	return optimized.x	
	
def print_assets(names, W, R, C):
	print("%-10s %6s %6s %6s %s" % ("Name", "Weight", "Return", "Dev", "   Correlations"))
	for i in range(len(names)):
		print("%-10s %5.1f%% %5.1f%% %5.1f%%    " % (names[i], 100*W[i], 100*R[i], 100*C[i,i]**.5), end='')
		for j in range(i+1):
			corr = C[i,j] / (sqrt(C[i,i]) * (sqrt(C[j,j]))) # calculate correlation from covariance
			print("%.3f " % corr, end='')
		print()
		
def optimize_and_display(title, names, R, C, rf, color='black'):
	# optimize
	W = solve_weights(R, C, rf)
	mean, var = port_mean_var(W, R, C)						# calculate tangency portfolio
	f_mean, f_var, f_weights = solve_frontier(R, C, rf)		# calculate min-var frontier
	
	# display min-var frontier
	print(title)
	print_assets(names, W, R, C)
	n = len(names)
	scatter([C[i,i]**.5 for i in range(n)], R, marker='x',color=color)  # draw assets   
	for i in range(n): 										# draw labels
		text(C[i,i]**.5, R[i], '  %s'%names[i], verticalalignment='center', color=color) 
	scatter(var**.5, mean, marker='o', color=color)			# draw tangency portfolio
	plot(f_var**.5, f_mean, color=color)					# draw min-var frontier
	xlabel('$\sigma$'), ylabel('$r$')
	grid(True)
#	show() 
	
	# Display weights
	#m = empty([n, len(f_weights)])
	#for i in range(n):
	#	for j in range(m.shape[1]):
	#		m[i,j] = f_weights[j][i]
	#stackplot(f_mean, m)
	#show()
	
# given the pairs of assets, prepare the views and link matrices. This function is created just for users' convenience
def prepare_views_and_link_matrix(names, views):
	r, c = len(views), len(names)
	Q = [views[i][3] for i in range(r)]	# view matrix
	P = zeros([r, c])					# link matrix
	nameToIndex = dict()
	for i, n in enumerate(names):
		nameToIndex[n] = i
	for i, v in enumerate(views):
		name1, name2 = views[i][0], views[i][2]
		P[i, nameToIndex[name1]] = +1 if views[i][1]=='>' else -1
		P[i, nameToIndex[name2]] = -1 if views[i][1]=='>' else +1
	return array(Q), P
	
####################################
# Main
####################################
	
# Load names, prices, capitalizations from the data source(yahoo finance)
names, prices, caps = load_data()
n = len(names)

# Estimate assets's expected return and covariances
names, W, R, C = assets_meanvar(names, prices, caps)
rf = .015  	# Risk-free rate

print("Historical Weights")
print_assets(names, W, R, C)

# Calculate portfolio historical return and variance
mean, var = port_mean_var(W, R, C)

# Mean-Variance Optimization (based on historical returns)
optimize_and_display('Optimization based on Historical returns', names, R, C, rf, color='red')
show()

# Black-litterman reverse optimization
lmb = (mean - rf) / var				# Calculate return/risk trade-off
Pi = dot(dot(lmb, C), W)			# Calculate equilibrium excess returns

# Mean-variance Optimization (based on equilibrium returns)
optimize_and_display('Optimization based on Equilibrium returns', names, Pi+rf, C, rf, color='green')
show()

# Determine views to the equilibrium returns and prepare views (Q) and link (P) matrices
views = [
	('MSFT', '>', 'GE', 0.02), 
	('AAPL', '<', 'JNJ', 0.02)
	]

Q, P = prepare_views_and_link_matrix(names, views)
print('Views Matrix')
print(Q)
print('Link Matrix')
print(P)

tau = .025 # scaling factor

# Calculate omega - uncertainty matrix about views
omega = dot(dot(dot(tau, P), C), transpose(P)) # 0.025 * P * C * transpose(P)
# Calculate equilibrium excess returns with views incorporated
sub_a = inv(dot(tau, C))
sub_b = dot(dot(transpose(P), inv(omega)), P)
sub_c = dot(inv(dot(tau, C)), Pi)
sub_d = dot(dot(transpose(P), inv(omega)), Q)
Pi = dot(inv(sub_a + sub_b), (sub_c + sub_d))

# Mean-variance Optimization (based on equilibrium returns)
optimize_and_display('Optimization based on Equilibrium returns with adjusted views', names, Pi+rf, C, rf, color='blue')
show()
