import datetime, re, csv, operator, math, urllib.request, statistics
def exp_range(): return [date for date in [datetime.datetime.now() + datetime.timedelta(days = 24) + datetime.timedelta(days = i) for i in range(14)] if date.weekday() == 4]
def volatility(file, dpy = 365):
	def expiration(symbol):
		m = re.search('[A-Z]{1,5}(\d{2})(\d{2})([A-L])', symbol)
		return datetime.datetime(int(m.group(1)) + 2000, ord(m.group(3)) - 64, int(m.group(2)))
	def strike(symbol): return float(re.search('[A-Z]{1,5}\d{4}[A-L](.+)', symbol).group(1))
	def q(x, last, bid, ask):
		if x[bid] and x[ask]: mid = (x[bid] + x[ask])/2
		elif x[ask]: mid = None
		else: mid = x[last]
		return [mid]
	option_chain = list(csv.reader(open(file)))[1:]
	symbol = list(zip(*option_chain))[0]
	exp, prefix = set([expiration(s) for s in symbol]), set([re.match('([A-Z]{1,5}\d{4}[A-L])', s).group(0) for s in symbol])
	exp, prefix = [min(exp), max(exp)], [s[0] for s in sorted([(p, expiration(p)) for p in prefix], key = operator.itemgetter(1))]
	term, t, variance, N30 = {i: [x for x in option_chain if x[0][:len(prefix[i])] == prefix[i]] for i in range(2)}, [], [], 30/dpy
	for i in range(2):
		for x in term[i]:
			for j in [1, 2, 3, 4, 8, 9, 10, 11]: x[j] = float(x[j]) if x[j] else None
		n, K, delta, abs_diff = len(term[i]) - 1, [strike(x[0]) for x in term[i]], exp[i] - datetime.datetime.now(), [abs(x[3] + x[4] - x[10] - x[11])/2 for x in term[i] if all([x[3], x[4], x[10], x[11]])]
		t += [(delta.days + delta.seconds/86400)/dpy]
		delta_K, growth, minimum = [K[1] - K[0]] + [(K[j + 1] - K[j - 1])/2 for j in range(1, n)] + [K[n] - K[n - 1]], math.exp(float(re.findall('<td class=\"text_view_data\">(.+?)</td>', ''.join([x.decode('utf-8').strip() for x in urllib.request.urlopen('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield')]))[-10])/100*t[i]), min(abs_diff)
		m, Q = abs_diff.index(minimum), []
		F = K[m] + growth*minimum
		K0 = max([x for x in K if x < F])
		for j in range(n + 1):
			if K[j] > K0: Q += q(term[i][j], 3, 4, 1)
			elif K[j] < K0: Q += q(term[i][j], 8, 10, 11)
			else: Q += [statistics.mean([term[i][j][k] for k in [3, 4, 10, 11]])]
		for j in range(m, 1, -1):
			if not Q[j - 1] and not Q[j]:
				for k in range(j - 1): Q[k] = None
				break
		for j in range(m, n):
			if not Q[j] and not Q[j + 1]:
				for k in range(j + 2, len(Q)): Q[k] = None
				break
		exp[i] = exp[i].replace(hour = 8, minute = 30) if exp[i].day in range(15, 22) else exp[i].replace(hour = 15)
		variance += [(2*sum([delta_K[j]/K[j]**2*growth*Q[j] for j in range(n + 1) if Q[j]]) - (F/K0 - 1)**2)/t[i]]
	return math.sqrt((t[0]*variance[0]*(t[1] - N30) + t[1]*variance[1]*(N30 - t[0]))/(t[1] - t[0])/N30)