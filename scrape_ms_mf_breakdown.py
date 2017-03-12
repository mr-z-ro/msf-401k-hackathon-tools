#!/usr/bin/python

import sys, getopt
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

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

   # Get mutual fund tickers
   csv = open('./csv/{}_mfund_holders.csv'.format(ticker), 'r')
   tickers=[line.split(",")[-1].strip().replace('"', '') for line in csv if line.split(",")[-1].strip().replace('"', '') != "NULL"][1:]
   csv.close()

   # Use beautifulsoup phantom browser to scrape and parse
   #browser = webdriver.PhantomJS()
   browser = webdriver.Firefox() # for debugging

   csv = open('./{}_mfund_alternative_stocks.csv'.format(ticker), 'w+')
   csv.write('"{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}"\n'.format("mfund_ticker", "ticker", "perc_portfolio_wt", "shares_owned", "shares_change", "sector", "first_bought", "latest_analyst_report", "country", "ytd_return", "p_e_ratio"))
   for mfund_ticker in tickers:
      
      browser.get('http://portfolios.morningstar.com/fund/holdings?t={}&region=usa&culture=en-US'.format(mfund_ticker))
      soup = BeautifulSoup(browser.page_source, "html.parser")

      if soup.find(id='holding_epage0'):
         # Write the pertinent bits to a csv
         for row in soup.find(id='holding_epage0').find_all('tr', class_=lambda x: x != 'hr')[1:]:
            # Get row cells
            cells = row.find_all('td')

            # Get stock ticker from th tag
            stock_ticker = ""
            if row.find_all('th')[0].a:
               stock_ticker = row.find_all('th')[0].a.get('href').split('/')[-1].split('?')[-1].split('t=')[1].split('&')[0].split(':')[1]
            
            sector = ""
            if cells[6].span:
               sector = cells[6].span.get('title')

            # Get latest analyst report
            latest_analyst_report = ""
            if cells[10].a:
               latest_analyst_report = cells[10].a.text.strip().replace(',', '')

            # Write data
            csv.write('"{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}"\n'.format(mfund_ticker, stock_ticker, cells[3].text.strip().replace(',', ''), cells[4].text.strip().replace(',', ''), cells[5].text.strip().replace(',', ''), sector, cells[9].text.strip().replace(',', ''), latest_analyst_report, cells[11].text.strip().replace(',', ''), cells[12].text.strip(), cells[13].text.strip()))
   
   csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])
