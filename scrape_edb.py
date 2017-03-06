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
   while True:
      print "Parsing Page..."
      soup = BeautifulSoup(browser.page_source, "html.parser")

      # Close the popup
#      if soup.find(id='interstitial-modal'):
#         button = soup.find_element_by_css_selector('#interstitial-modal div.modal-footer button')
#         button.click()

      # Write the pertinent bits to a csv
      for row in soup.find(id='etfs').find_all('tr')[1:]:
         cells = row.find_all('td')
         csv.write('"{0}", "{1}", "{2}", {3}\n'.format(cells[0].text.strip().replace(',', ''), cells[1].text.strip().replace(',', ''), cells[2].text.strip().replace(',', ''), cells[3].text.strip().replace(',', '').replace('%', '')))

      print "Page Parsed, Checking for Next Link"

      # Check for a link to the next results
      try:
         with wait_for_page_load(browser):
            next_link = browser.find_element_by_css_selector('li.page-next:not(.disabled) a')
            if next_link:
               print "Clicking Next Link"
               next_link.click()
            else:
               break
      except NoSuchElementException:
         break

   # Close the csv
   print "Closing CSV"
   csv.close()

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 8:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

if __name__ == "__main__":
   main(sys.argv[1:])
