import urllib.request, datetime, pandas, csv, statistics
ie_data = pandas.read_excel(urllib.request.urlopen('http://www.econ.yale.edu/~shiller/data/ie_data.xls'))
ie, dpy = [list(ie_data[col]) for col in ie_data], 365.2425
def read_csv(url): return [(datetime.datetime.strptime(y[0], '%Y-%m-%d %H:%M:%S'), float(y[1])) for y in [x.split(',') for x in urllib.request.urlopen(url).read().decode('utf-8').split('\n')][:-1]]
def write_csv(file):
	market_cap, volume = read_csv('https://api.blockchain.info/charts/market-cap?timespan=all&format=csv'), read_csv('https://api.blockchain.info/charts/estimated-transaction-volume-usd?timespan=all&format=csv')
	cpi, n, w = {}, len(market_cap), csv.writer(open(file, 'w', newline = ''))
	for i in range(6, len(ie[0]) - 1):
		year = int(ie[0][i])
		cpi[datetime.datetime(year, int(100*(ie[0][i] - year) + 0.5), 1)] = ie[4][i]
	assert n == len(volume)
	iat = {market_cap[i][0]: volume[i][1]/cpi[market_cap[i][0].replace(month = (market_cap[i][0].replace(day = 1) - datetime.timedelta(days = 1)).month, day = 1) if market_cap[i][0].month == datetime.datetime.now().month and market_cap[i][0].year == datetime.datetime.now().year else market_cap[i][0].replace(day = 1)] for i in range(n)}
	for i in range(n):
		try: start = market_cap[i][0].replace(year = market_cap[i][0].year - 6)
		except ValueError: start = market_cap[i][0].replace(year = market_cap[i][0].year - 6, day = market_cap[i][0].day - 1)
		if market_cap[i][0] >= market_cap[0][0].replace(year = market_cap[0][0].year + 6): w.writerow([market_cap[i][0], market_cap[i][1]/statistics.mean([iat[date] for date in iat if start <= date < market_cap[i][0]])])