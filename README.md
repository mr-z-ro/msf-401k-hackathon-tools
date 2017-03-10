# MSF 401k Hackathon Tools!

Included in this repository is a set of tools and specifications for use at [MSF's 401K Investor Resource Hackathon](https://twitter.com/MSF_USA/status/837702440636067840).

Please note that these scripts have been run on 10 March 2017, and the resulting data is included in csv, json, and mysql formats in respective directories within the repository as well.

## Feedback Welcome!

For requests, tech questions, general comments, happy feedback, etc, feel free to use the wonderful Github tools provided here, or reach out via twitter to [@mr_z_ro](https://twitter.com/mr_z_ro)!

## Data!

### MySQL Data

The data that's presented granularly below has also been collated into a MySQL data dump, which is included in the repository's mysql directory. 

The data is also be hosted live in a location that can be accessed with credentials that will be announced at the hackathon.

### Sources

The following sources were referenced in aggregating this data

- MorningStar: Aggregated list of top 20 funds holding [PFE](http://investors.morningstar.com/ownership/shareholders-major.html?t=PFE&region=usa&culture=en-US&ownerCountry=USA) and [GSK](http://investors.morningstar.com/ownership/shareholders-major.html?t=GSK&region=usa&culture=en-US&ownerCountry=USA)
- HoldingsChannel: Aggregated Lists of all Institutions (mislabeled on their site as “funds”) holding [PFE](https://www.holdingschannel.com/funds/holding-pfe/) and [GSK](https://www.holdingschannel.com/funds/holding-gsk/), pulled from [SEC’s EDGAR database](https://www.sec.gov/edgar/searchedgar/webusers.htm)
- ETFdb: List of ETFs holding [PFE](etfdb.com/stock/PFE/) and [GSK](etfdb.com/stock/GSK/)
- [MutualFunds.com](http://mutualfunds.com/funds/): List of all funds with corresponding abbreviations

### Granular Data

All data provided are for the PFE and GSK stocks, and their respective data are in files prefixed with their ticker.

## #Prerequisites for Gathering Fresh Data

For use cases requiring fresh data beyond the hackathon, the scripts can be run on demand, after installing the following prerequisites.

The scripts require [BeautifulSoup](https://pypi.python.org/pypi/bs4) and [Selenium](https://pypi.python.org/pypi/selenium) libraries, which can be installed using [pip](https://pip.pypa.io/en/stable/installing/) as follows:

```
pip install bs4
pip install selenium
```

Next, in order to actually walk through the data, browser emulators are needed. PhantomJS is a great one that can be installed as follows:

```
Download phantomjs (for silent scraping):
http://phantomjs.org/download.html
[extract]
mv ~/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs /usr/local/bin
```

Firefox (geckodriver) can also be helpful for debugging, and can be installed as follows:

```
Download geckodriver (for debugging):
https://github.com/mozilla/geckodriver/releases
[extract]
mv ~/Downloads/geckodriver /usr/local/bin
```

Note: please ensure PATH is updated to include `/usr/local/bin` directory. An example of how to do this for a linux-based system (e.g. Mac, Ubuntu, or Windows with [cygwin](https://www.cygwin.com/)) can be found [here](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux)

###Using the Tools

####scrape_ms.py
This script pulls data about the top mutual fund holders of a given stock (parameterized by TICKER) and dumps to a file called `TICKER_mfund_holder.csv`. For instance, for Google (GOOG), this script can be run by calling:

```
python scrape_ms.py -t GOOG
```

Sample files for [PFE](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/PFE_mfund_holders.csv) and [GSK](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/GSK_mfund_holders.csv) have been provided as part of this repository.

####scrape_edb.py
This script pulls data about the top exchange-traded funds (ETFs) that hold a given stock (parameterized by TICKER) and dumps to a file called `TICKER_etf_holder.csv`. For instance, for Yahoo (YHOO), this script can be run by calling:

```
python scrape_edb.py -t YHOO
```

Sample files for [PFE](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/PFE_etf_holders.csv) and [GSK](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/GSK_etf_holders.csv) have been provided as part of this repository.

####scrape_hc.py
This script pulls data about the top Institutions that hold a given stock (parameterized by TICKER) and dumps to a file called `TICKER_inst_holder.csv`. For instance, for Yahoo (YHOO), this script can be run by calling:

```
python scrape_hc.py -t YHOO
```

Sample files for [PFE](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/PFE_inst_holders.csv) and [GSK](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/csv/GSK_inst_holders.csv) have been provided as part of this repository.

####scrape_mf.py
This script pulls data about the ticker symbols of the top mutual funds, and dumps to a file called `mfund_tickers.csv`. It can be run by calling:

```
python scrape_mf.py
```

####cleanup.sh
This script cleans up logs and csvs produced by running the scrape files. It can be executed by running:

```
./cleanup.sh
```


