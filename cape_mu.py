import urllib.request, pandas, datetime, math, numpy, statistics, csv
from scipy import stats
def download_excel(url):
	file = pandas.read_excel(urllib.request.urlopen(url))
	return [list(file[col]) for col in file]
ie, eps_est = download_excel('http://www.econ.yale.edu/~shiller/data/ie_data.xls'), download_excel('http://us.spindices.com/documents/additional-material/sp-500-eps-est.xlsx')
monthly, quarterly, switch = [(ie[0][i], ie[3][i]) for i in range(6, len(ie[0]) - 1)], {}, False
for i in range(eps_est[0].index('ESTIMATES'), len(eps_est[0])):
	if eps_est[0][i] == 'ACTUAL': switch = True
	try: quarterly[datetime.datetime.strptime(eps_est[0][i].split(' ')[0], '%m/%d/%Y').replace(day = 1)] = eps_est[3][i]
	except: pass
	if switch == True and not eps_est[0][i]: break
for i in range(len(monthly)):
	now = datetime.datetime.now()
	try:
		if math.isnan(monthly[i][1]) and not monthly[i][0].month%3 and monthly[i][0] < datetime.datetime(now.year, now.month, 1): ie[3][i + 6] = sum([quarterly[key] for key in quarterly if key <= monthly[i][0] < key.replace(year = key.year + 1)])
	except AttributeError: pass
j = max([y[0] for y in [(x[0], type(x[1]) == float and not math.isnan(x[1])) for x in enumerate(ie[3])] if y[1]]) - 1
n = [j]
while ie[3][j] == numpy.nan:
	n += [j]
	j -= 1
n += [j - 1]
for j in n: ie[3][j] = ie[3][j + 1] - (ie[3][n[0] + 1] - ie[3][n[-1] - 1])/(len(n) + 1)
for i in range(6, len(ie[0]) - 1):
	year = int(ie[0][i])
	ie[0][i] = datetime.datetime(year, int(100*(ie[0][i] - year) + 1/2), 1)
def get_cape(i, t1_months): return ie[7][i]/statistics.mean([x for x in ie[9][i - t1_months:i] if not math.isnan(x)])
def get_mu(i, t2, t2_months): return (ie[1][i + t2_months]/ie[1][i])**(1/t2) - 1
def write_pearsonr(file):
	n, w = len(ie[0][6:-1])//12, csv.writer(open(file, 'w', newline = ''))
	for t1 in range(1, n):
		for t2 in range(1, n - t1):
			t1_months, t2_months, log_cape, mu = 12*t1, 12*t2, [], []
			for i in range(6 + t1_months, len(ie[0]) - t2_months - 1):
				log_cape += [math.log(get_cape(i, t1_months))]
				mu += [get_mu(i, t2, t2_months)]
			w.writerow([t1, t2, stats.pearsonr(log_cape, mu)[0]])
def log_reg(t1, t2, file = None):
	if file: w = csv.writer(open(file, 'w', newline = ''))
	t1_months, t2_months, cape_list, mu_list = 12*t1, 12*t2, [], []
	for i in range(6 + t1_months, len(ie[0]) - t2_months - 1):
		cape, mu = math.log(get_cape(i, t1_months)), get_mu(i, t2, t2_months)
		cape_list += [cape]
		mu_list += [mu]
		if file: w.writerow([ie[0][i], cape, mu])
	return numpy.polyfit(cape_list, mu_list, 1)
def mu(t1, t2):
	m, b = log_reg(t1, t2)
	cape0 = get_cape(-2, 12*t1)
	return m*math.log(get_cape(-2, 12*t1)) + b