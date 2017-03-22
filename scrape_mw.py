#!/usr/bin/python

import sys, getopt, string
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

   csv = open('./all_mfund_tickers.csv', 'w+')
   csv.write('"{0}", "{1}"\n'.format("ticker", "name"))

   for first_letter in string.lowercase:
      print "Getting funds starting with {}".format(first_letter)
      browser.get('http://www.marketwatch.com/tools/mutual-fund/list/{}'.format(first_letter))
      soup = BeautifulSoup(browser.page_source, "html.parser")

      # Write the pertinent bits to a csv
      for row in soup.find(class_='quotelist').find_all('tr')[1:]:
         cells = row.find_all('td')
         csv.write('"{0}", "{1}"\n'.format(cells[0].a.text.strip().replace(',', ''), cells[1].a.text.strip().replace(',', '')))
   
   csv.close()

if __name__ == "__main__":
   main(sys.argv[1:])
