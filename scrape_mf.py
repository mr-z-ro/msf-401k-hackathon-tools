#!/usr/bin/python

import sys, getopt
from bs4 import BeautifulSoup
from selenium import webdriver

def main(argv):
   scrape()

def scrape():
   # Set utf-8 encoding
   reload(sys)
   sys.setdefaultencoding('utf-8')

   # Use beautifulsoup phantom browser to scrape and parse
   #browser = webdriver.PhantomJS()
   browser = webdriver.Firefox() # for debugging
   browser.get('http://mutualfunds.com/funds/')
   soup = BeautifulSoup(browser.page_source, "html.parser")

   # Write the pertinent bits to a csv
   csv = open('./mfund_tickers.csv', 'w+')
   csv.write('"{0}", "{1}", "{2}", "{3}", "{4}"\n'.format("position", "ticker", "name", "family", "num_searches"))
   for row in soup.find(class_='article__content').table.find_all('tr')[1:]:
      cells = row.find_all('td')
      csv.write('{0}, "{1}", "{2}", "{3}", {4}\n'.format(cells[0].p.text.strip().replace(',', ''), cells[1].a.text.strip().replace(',', ''), cells[2].a.text.strip().replace(',', ''), cells[3].p.text.strip().replace(',', ''), cells[4].p.text.strip().replace(',', '')))
   csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])
