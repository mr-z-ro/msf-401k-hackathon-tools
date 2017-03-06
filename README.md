# MSF 401k Hackathon Tools

A set of tools, data, and specifications for use at [MSF's 401K Investor Resource Hackathon](https://twitter.com/MSF_USA/status/837702440636067840).

## Prerequisites

The scripts require BeautifulSoup and Selenium libraries, which can be installed using [pip](https://pip.pypa.io/en/stable/installing/) as follows:

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

##Using the Tools

###scrape_ms.py
This script pulls data about the top mutual fund holders of a given stock (parameterized by TICKER) and dumps to a file called `TICKER_mfund_holder.csv`. For instance, for Google (GOOG), this script can be run by calling:

```
python scrape_ms.py -t GOOG
```

Sample files for [PFE](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/PFE_mfund_holders.csv) and [GSK](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/GSK_mfund_holders.csv) have been provided as part of this repository.

###scrape_edb.py
This script pulls data about the top exchange-traded funds (ETFs) that hold a given stock (parameterized by TICKER) and dumps to a file called `TICKER_etf_holder.csv`. For instance, for Yahoo (YHOO), this script can be run by calling:

```
python scrape_edb.py -t YHOO
```

Sample files for [PFE](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/PFE_etf_holders.csv) and [GSK](https://github.com/mr-z-ro/msf-401k-hackathon-tools/blob/master/GSK_etf_holders.csv) have been provided as part of this repository.

###cleanup.sh
This script cleans up logs and csvs produced by running the scrape files. It can be executed by running:

```
./cleanup.sh
```

## Feedback

For questions, comments, feedback, etc, feel free to use the wonderful Github tools provided here, or reach out via twitter to [@mr_z_ro](https://twitter.com/mr_z_ro)
