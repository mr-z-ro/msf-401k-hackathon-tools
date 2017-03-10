#!/usr/bin/python

import sys, getopt
from bs4 import BeautifulSoup
from selenium import webdriver

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

   # Use beautifulsoup phantom browser to scrape and parse
   browser = webdriver.PhantomJS()
   #browser = webdriver.Firefox() # for debugging
   browser.get('https://www.holdingschannel.com/funds/holding-{}/'.format(ticker.lower()))
   soup = BeautifulSoup(browser.page_source, "html.parser")

   # Write the pertinent bits to a csv
   csv = open('./{}_inst_holders.csv'.format(ticker), 'w+')
   csv.write('"{0}", "{1}", "{2}", "{3}"\n'.format("name", "shares", "value_of_shares_in_thousands_usd", "date_recorded"))
   for row in soup.find(id='hldtable').find_all('tr', class_=lambda x: x == 'mainrow')[1:]:
      cells = row.find_all('td')
      csv.write('"{0}", {1}, {2}, "{3}"\n'.format(cells[0].text.strip().replace(',', ''), cells[1].text.strip().replace(',', ''), cells[2].text.strip().replace(',', '').replace('$', ''), cells[3].text.strip().replace(',', '')))
   csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])
