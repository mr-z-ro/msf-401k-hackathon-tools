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
   browser.get('http://investors.morningstar.com/ownership/shareholders-major.html?t={}&region=usa&culture=en-US&ownerCountry=USA'.format(ticker))
   soup = BeautifulSoup(browser.page_source, "html.parser")

   # Write the pertinent bits to a csv
   csv = open('./{}_holders.csv'.format(ticker), 'w+')
   csv.write('"{0}", "{1}", "{2}", "{3}", "{4}", "{5}"\n'.format("name", "shares", "percentage_of_all_shares", "change_num_shares", "change_percentage", "percent_total_assets", "date_of_portfolio"))
   for row in soup.find(id='FundList').table.find_all('tr', class_=lambda x: x != 'hr')[1:]:
      cells = row.find_all('td')
      csv.write('"{0}", {1}, {2}, {3}, {4}, {5}\n'.format(cells[0].text.strip().replace(',', ''), cells[1].text.strip().replace(',', ''), cells[2].text.strip().replace(',', ''), cells[3].text.strip().replace(',', ''), cells[4].text.strip().replace(',', ''), cells[5].text.strip().replace(',', ''), cells[7].text.strip().replace(',', '')))
   csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])