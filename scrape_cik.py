import sys, getopt, requests, re

def main(argv):
   ticker = ''
   try:
      opts, args = getopt.getopt(argv,"ht:",["ticker=",])
   except getopt.GetoptError:
      print 'Usage: test.py -t <ticker>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Usage: test.py -t <ticker>'
         sys.exit()
      elif opt in ("-t", "--ticker"):
         ticker = arg
   if ticker:
      scrape(ticker)
   else:
      print 'Usage: test.py -t <ticker>'

def scrape(ticker):
	# Set utf-8 encoding
	reload(sys)
 	sys.setdefaultencoding('utf-8')
	
	csv = open('./csv/{}_mfund_holders.csv'.format(ticker), 'r')
	tickers=[line.split(",")[-1].strip().replace('"', '') for line in csv if line.split(",")[-1].strip().replace('"', '') != "NULL"][1:]
	csv.close()

	URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
	CIK_RE = re.compile(r'.*CIK=(\d{10}).*')

	csv = open('./csv/{}_mfund_ciks.csv'.format(ticker), 'w+')
	csv.write('"mfund_ticker", "cik"\n')
	for mfund_ticker in tickers:
	    results = CIK_RE.findall(requests.get(URL.format(mfund_ticker)).content)
	    if len(results):
	        csv.write('"{}", "{}"\n'.format(str(mfund_ticker).upper(), str(results[0])))
	csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])