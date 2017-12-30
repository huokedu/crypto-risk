import csv, urllib.request, json, math, os, statistics, time
def rebalance(file):
	w = csv.writer(open(file, 'w', newline = ''))
	while True:
		crypto, data, value = [c for c in json.loads(urllib.request.urlopen(urllib.request.Request('https://api.coinmarketcap.com/v1/ticker/')).read().decode('utf-8')) if int(c['rank']) <= 38 and c['symbol'] != 'USDT'], {}, 0
		s = sum([math.sqrt(float(c['market_cap_usd'])) for c in crypto])
		t = float(crypto[0]['price_usd'])*s/math.sqrt(float(crypto[0]['market_cap_usd']))
		for c in crypto:
			data[c['symbol']] = dict()
			data[c['symbol']]['weight'] = math.sqrt(float(c['market_cap_usd']))/s
			data[c['symbol']]['price'] = float(c['price_usd'])
			data[c['symbol']]['shares'] = int(data[c['symbol']]['weight']*t/data[c['symbol']]['price'] + 1/2)
			value += data[c['symbol']]['price']*data[c['symbol']]['shares']
		os.system('cls')
		print('1 share = US$' + '{:,.2f}'.format(value))
		print()
		print('{:<16} {:<5} {:>6} {:>7} {:>8}'.format('CRYPTOCURRENCY', 'TICKER', 'SHARES', 'WEIGHT', 'PRICE'))
		for c in crypto:
			price = float(c['price_usd'])
			u = statistics.median([-2, int(math.log(price)), 0])
			a = [c['name'], c['symbol'], data[c['symbol']]['shares'], data[c['symbol']]['shares']*price/value, price]
			print(('{:<16} {:<5} {:>6} {:>7.2%} ' + '{:>' + str(10 - u) + '.' + str(2 - u) + 'f}').format(*a))
			w.writerow(a)
		time.sleep(300)
def portfolio_value(url): return sum([int(x.split(',')[2])*float(x.split(',')[4]) for x in urllib.request.urlopen(urllib.request.Request(url)).read().decode('ascii').splitlines()])
def curr_value(url):
	crypto = [c for c in json.loads(urllib.request.urlopen(urllib.request.Request('https://api.coinmarketcap.com/v1/ticker/')).read().decode('utf-8'))]
	data = {c['symbol']: float(c['price_usd']) for c in crypto}
	return sum([int(x.split(',')[2])*{c['symbol']: float(c['price_usd']) for c in crypto}[x.split(',')[1]] for x in urllib.request.urlopen(urllib.request.Request(url)).read().decode('ascii').splitlines()])