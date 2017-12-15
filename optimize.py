import numpy, urllib.request, re, statistics, math
from scipy import optimize
def variance(w, sigma, R):
	product = numpy.multiply(w, sigma)
	return numpy.matmul(numpy.matmul(numpy.transpose(product), R), product)
def eff_front(target, mu, sigma, R):
	def con_mu(w, mu, target): return sum(numpy.multiply(w, mu))/sum(w) - target
	n = len(mu)
	assert n == len(sigma) == len(R)
	weight = optimize.minimize(variance, len(mu)*[1/n], args = (sigma, R), bounds = n*[(0, 1)], constraints = ({'type': 'eq', 'fun': con_mu, 'args': (mu, target)}, {'type': 'eq', 'fun': lambda x: 1 - sum(x)}))
	if weight.success: return weight.x, variance(weight.x, sigma, R)
def kelly(target, mu, sigma, R, ef = None):
	if not ef: ef = eff_front(target, mu, sigma, R)
	return (sum(numpy.multiply(ef[0], mu)) - float(re.findall('<td class=\"text_view_data\">(.+?)</td>', ''.join([x.decode('utf-8').strip() for x in urllib.request.urlopen('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield')]))[-10])/100)/ef[1]
def kelly_opt(target, mu, sigma, R): return (kelly(target, mu, sigma, R) - 1)**2
def evaluate(mu, sigma, R):
	portfolio_mu = optimize.minimize(kelly_opt, statistics.median(mu), args = (mu, sigma, R), bounds = [(min(mu), max(mu))]).x
	ef = eff_front(portfolio_mu, mu, sigma, R)
	return {'weight': min(1, kelly(portfolio_mu, mu, sigma, R, ef))*(ef[0]), 'portfolio expected return': portfolio_mu[0], 'portfolio volatility': math.sqrt(ef[1])}