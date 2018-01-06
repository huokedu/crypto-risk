import urllib.request, json
def read_json(url): return json.loads(urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8'))
miner_fee, price, miner_fee_usd = {r['pair'].split('_')[1]: r['minerFee'] for r in read_json('https://shapeshift.io/rate')}, {cmc['symbol']: float(cmc['price_usd']) for cmc in read_json('https://api.coinmarketcap.com/v1/ticker/')}, {}
i = 0
for mf in miner_fee:
	try: miner_fee_usd[mf] = miner_fee[mf]*price[mf]
	except KeyError: continue