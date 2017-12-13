import urllib.request, pandas, csv, math, statistics
from scipy import stats
def write_pearsonr(file):
	ie_data = pandas.read_excel(urllib.request.urlopen('http://www.econ.yale.edu/~shiller/data/ie_data.xls'))
	ie_data = [list(ie_data[col]) for col in ie_data]
	n, w = len(ie_data[0][6:-1])//12, csv.writer(open(file, 'w', newline = ''))
	for t1 in range(1, n):
		for t2 in range(1, n - t1):
			t1_months, t2_months, log_cape, mu = 12*t1, 12*t2, [], []
			for i in range(6 + t1_months, len(ie_data[0]) - t2_months - 1):
				log_cape += [math.log(ie_data[7][i]/statistics.mean([x for x in ie_data[9][i - t1_months:i] if not math.isnan(x)]))]
				mu += [(ie_data[1][i + t2_months]/ie_data[1][i])**(1/t2) - 1]
			w.writerow([t1, t2, stats.pearsonr(log_cape, mu)[0]])