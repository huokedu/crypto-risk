import math, numpy
from scipy import integrate, stats, optimize
def integrate_mu(a, b, mu, sigma, p): return integrate.quad(lambda x: x*math.exp(-(x - mu)**2/(2*sigma**2))/math.sqrt(2*math.pi*sigma**2), a, b)[0]/p
def g_piece(mu, r, f, sigma): return r + (mu - r)*f - (sigma*f)**2/2
def g(f, mu, r, sigma, tax):
	q = stats.norm.cdf(0, mu, sigma)
	p = 1 - q
	args = [mu, sigma]
	return -g_piece(integrate_mu(0, numpy.inf, mu, sigma, p)*(1 - tax), r, f, sigma)*p - g_piece(integrate_mu(-numpy.inf, 0, mu, sigma, q), r, f, sigma)*q
def kelly(mu, r, sigma, tax):
	f = optimize.minimize(g, (mu - r)/sigma**2, args = (mu, r, sigma, tax))
	if f.success: return f.x