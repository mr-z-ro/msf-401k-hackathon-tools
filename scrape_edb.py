#!/usr/bin/python
# coding=utf-8

import sys, getopt, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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
   
   # Load the first page and initialize vars
   browser.get('http://etfdb.com/stock/{}'.format(ticker))
   
   # Set up the csv file for writing
   csv = open('./{}_etf_holders.csv'.format(ticker), 'w+')
   csv.write('"{0}", "{1}", "{2}", "{3}"\n'.format("ticker", "name", "category", "expense_ratio"))

   # Continue grabbing results until there is no next page
   parse_pages(browser, csv)

   # Close the csv
   print "Closing CSV"
   csv.close()

def parse_pages(browser, csv):
  print "Parsing Page..."
  soup = BeautifulSoup(browser.page_source, "html.parser")

  # Close the popup
  if soup.find(id='interstitial-modal'):
    print "Closing ad"
    button = browser.find_element_by_css_selector('#interstitial-modal div.modal-footer button')
    if button:
      button.click()  
      print "Ad closed"
    else:
      print "No ad found"

  # Write the pertinent bits to a csv
  for row in soup.find(id='etfs').find_all('tr')[1:]:
     cells = row.find_all('td')
     csv.write('"{0}", "{1}", "{2}", {3}\n'.format(cells[0].text.strip().replace(',', ''), cells[1].text.strip().replace(',', ''), cells[2].text.strip().replace(',', ''), cells[3].text.strip().replace(',', '').replace('%', '')))

  print "Page Parsed, Checking for Next Link"

  # Check for a link to the next results
  try:
    next_link = browser.find_element_by_css_selector('li.page-next:not(.disabled) a')
    if next_link:
      print "Clicking Next Link"
      next_link.click()
      time.sleep(3) # hacky, should really do with a "with" block or a wait
      parse_pages(browser, csv)
  except NoSuchElementException:
     pass

if __name__ == "__main__":
   main(sys.argv[1:])
