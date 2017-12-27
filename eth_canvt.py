import urllib.request, datetime, statistics
def read_url(url): return [(datetime.datetime.strptime(z[0], '%m/%d/%Y'), int(z[1]), *[float(a) for a in z[2:]]) for z in [[y[1:-1] for y in x.decode('ascii').split(',')] for x in urllib.request.urlopen(urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0'})).read().splitlines()[1:]]]
nv, tx_fee, price  = read_url('https://etherscan.io/chart/marketcap?output=csv'), read_url('https://etherscan.io/chart/transactionfee?output=csv'), read_url('https://etherscan.io/chart/etherprice?output=csv')
n = len(nv)
assert n == len(tx_fee) == len(price)
for i in range(366, n):
	x = []
	for j in range(i - 365):
		if price[j][2]: x += [tx_fee[j][2]/price[j][2]]
	if x: print(nv[i][0], nv[i][1]/statistics.mean(x)*10**12)