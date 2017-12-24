import datetime, re, urllib.request, pandas, math, statistics, numpy, csv
def risk_free(): return {datetime.datetime.strptime(row[0], '%m/%d/%y'): float(row[1])/100 for row in re.findall('<td scope=\"row\" class=\"text_view_data\">(\d{2}/\d{2}/\d{2})</td>' + 11*'<td class=\"text_view_data\">(\d+\.\d{2})</td>', ''.join([x.decode('utf-8').strip() for x in urllib.request.urlopen('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll')]))}
def volatility():
	spreadsheet = pandas.read_excel(urllib.request.urlopen('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixarchive.xls'))
	col = list(spreadsheet)
	date = spreadsheet[col[0]]
	vix = {date[i]: float(spreadsheet[col[4]][i])/100 for i in range(1, len(date))}
	for row in [line.split(',') for line in urllib.request.urlopen('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv').read().decode('utf-8').splitlines()[2:-1]]: vix[datetime.datetime.strptime(row[0], '%m/%d/%Y')] = float(row[4])/100
	return vix
def log_reg(t1, t2):
	t1_months, t2_months, cape_list, mu_list = 12*t1, 12*t2, [], []
	for i in range(6 + t1_months, len(ie[0]) - t2_months - 1):
		year = int(ie[0][i])
		cape_list += [math.log(ie[7][i]/statistics.mean([x for x in ie[9][i - t1_months:i] if not math.isnan(x)]))]
		mu_list += [(ie[1][i + t2_months]/ie[1][i])**(1/t2) - 1]
	return numpy.polyfit(cape_list, mu_list, 1)
def nearest(d, target): return d.get(target d[min(d.keys(), key = lambda x: abs(x - target))])
def write_file(t1, t2, file):
	ie_data, r, sigma = pandas.read_excel(urllib.request.urlopen('http://www.econ.yale.edu/~shiller/data/ie_data.xls')), risk_free(), volatility()
	t1_months, t2_months, ie, w = 12*t1, 12*t2, [list(ie_data[col]) for col in ie_data], csv.writer(open(file, 'w', newline = ''))
	m, b = log_reg(t1, t2)
	for i in range(6 + t1_months, len(ie[0])):
		date_str = float(ie[0][i])
		year = int(date_str)
		date = datetime.datetime(year, int(100*(date_str - year) + 1/2), 1)
		w.writerow([date, statistics.median([0, (m*math.log(ie[7][i]/statistics.mean([x for x in ie[9][i - t1_months:i]])) + b - nearest(r, date))/nearest(sigma, date)**2, 1]), nearest(r, date), ie[7][i]])