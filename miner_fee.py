import urllib.request, json
def read_json(url): return json.loads(urllib.request.urlopen(urllib.request.Request(url)).read().decode('utf-8'))
data = read_json('https://shapeshift.io/rate')
miner_fee = {x['pair'].split('_')[1]: x['minerFee'] for x in data}
rate = {x['pair']: float(x['rate']) for x in data}
mf_btc = {x: miner_fee[x]*rate[x + '_BTC'] for x in miner_fee if x != 'BTC'}
mf_btc['BTC'] = miner_fee['BTC']